import { NextRequest, NextResponse } from "next/server";
import { createServerClient } from "@/src/lib/supabase";

/**
 * POST /api/validate-code
 * 验证访问码并绑定用户（使用 Supabase 数据库）
 * 
 * 请求体：
 * {
 *   accessCode: string,
 *   userEmail?: string,  // 用户邮箱（首次绑定或验证时必需）
 *   userPhone?: string   // 用户手机号（可选，与邮箱二选一）
 * }
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { accessCode, userEmail, userPhone } = body;

    if (!accessCode || typeof accessCode !== "string") {
      return NextResponse.json(
        { success: false, error: "访问码不能为空" },
        { status: 400 }
      );
    }

    // 验证用户身份（邮箱或手机号至少提供一个）
    const userIdentity = userEmail?.trim() || userPhone?.trim();
    if (!userIdentity) {
      return NextResponse.json(
        { 
          success: false, 
          error: "请提供邮箱或手机号",
          requiresUserInfo: true 
        },
        { status: 400 }
      );
    }

    // 创建 Supabase 客户端
    let supabase;
    try {
      supabase = createServerClient();
    } catch (supabaseError: any) {
      console.error("创建 Supabase 客户端失败:", supabaseError);
      return NextResponse.json(
        { 
          success: false, 
          error: "服务器配置错误，请检查环境变量" 
        },
        { status: 500 }
      );
    }

    // 规范化访问码（不区分大小写，去除空格和连字符）
    const normalizedInput = accessCode
      .toUpperCase()
      .replace(/\s+/g, "")
      .replace(/-/g, "");

    // 查询访问码
    const { data: codes, error: queryError } = await supabase
      .from("access_codes")
      .select("*")
      .eq("code", accessCode.toUpperCase().trim());

    if (queryError) {
      console.error("查询访问码失败:", queryError);
      return NextResponse.json(
        { success: false, error: "服务器错误：无法查询访问码" },
        { status: 500 }
      );
    }

    let codeEntry;
    if (!codes || codes.length === 0) {
      // 如果精确匹配失败，尝试规范化匹配
      const { data: allCodes } = await supabase
        .from("access_codes")
        .select("*");

      if (allCodes) {
        const matchedCode = allCodes.find((c) => {
          const normalizedCode = c.code
            .toUpperCase()
            .replace(/\s+/g, "")
            .replace(/-/g, "");
          return normalizedCode === normalizedInput;
        });

        if (!matchedCode) {
          return NextResponse.json(
            { success: false, error: "访问码无效" },
            { status: 401 }
          );
        }
        codeEntry = matchedCode;
      } else {
        return NextResponse.json(
          { success: false, error: "访问码无效" },
          { status: 401 }
        );
      }
    } else {
      codeEntry = codes[0];
    }

    // 检查状态
    if (codeEntry.status === "revoked") {
      return NextResponse.json(
        { success: false, error: "访问码已被撤销" },
        { status: 403 }
      );
    }

    // 检查是否过期
    const now = new Date();
    const expiresAt = new Date(codeEntry.expires_at);

    if (now > expiresAt) {
      // 自动更新状态为 expired
      await supabase
        .from("access_codes")
        .update({ status: "expired" })
        .eq("id", codeEntry.id);

      return NextResponse.json(
        { success: false, error: "访问码已过期" },
        { status: 403 }
      );
    }

    // 检查是否已绑定用户
    const isBound = !!(codeEntry.bound_user_email || codeEntry.bound_user_phone);
    
    if (isBound) {
      // 已绑定：验证用户身份
      const boundEmail = codeEntry.bound_user_email?.toLowerCase().trim();
      const boundPhone = codeEntry.bound_user_phone?.trim();
      const providedEmail = userEmail?.toLowerCase().trim();
      const providedPhone = userPhone?.trim();

      const emailMatch = boundEmail && providedEmail && boundEmail === providedEmail;
      const phoneMatch = boundPhone && providedPhone && boundPhone === providedPhone;

      if (!emailMatch && !phoneMatch) {
        return NextResponse.json(
          { 
            success: false, 
            error: "此访问码已绑定其他用户，请输入绑定的邮箱或手机号",
            isBound: true,
            requiresUserInfo: true
          },
          { status: 403 }
        );
      }
    } else {
      // 未绑定：进行绑定
      const updateData: any = {
        bound_at: now.toISOString(),
      };

      if (userEmail) {
        updateData.bound_user_email = userEmail.toLowerCase().trim();
      }
      if (userPhone) {
        updateData.bound_user_phone = userPhone.trim();
      }

      const { error: bindError } = await supabase
        .from("access_codes")
        .update(updateData)
        .eq("id", codeEntry.id);

      if (bindError) {
        console.error("绑定用户失败:", bindError);
        return NextResponse.json(
          { success: false, error: "绑定用户失败，请重试" },
          { status: 500 }
        );
      }
    }

    // 验证通过，更新使用记录
    const { error: updateError } = await supabase
      .from("access_codes")
      .update({
        usage_count: (codeEntry.usage_count || 0) + 1,
        last_used_at: now.toISOString(),
      })
      .eq("id", codeEntry.id);

    if (updateError) {
      console.error("更新访问码使用记录失败:", updateError);
      // 即使更新失败，也允许用户登录（只记录日志）
    }

    return NextResponse.json({
      success: true,
      message: isBound ? "访问码验证成功" : "访问码验证成功，已绑定您的账户",
      code: codeEntry.code,
      expires_at: codeEntry.expires_at,
      usage_count: (codeEntry.usage_count || 0) + 1,
      isBound: true,
      boundUserEmail: codeEntry.bound_user_email || userEmail?.toLowerCase().trim(),
      boundUserPhone: codeEntry.bound_user_phone || userPhone?.trim(),
    });
  } catch (error) {
    console.error("验证访问码时发生错误:", error);
    return NextResponse.json(
      { success: false, error: "服务器错误" },
      { status: 500 }
    );
  }
}
