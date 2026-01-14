#!/usr/bin/env python3
"""
IELTS Novel Flow - 访问码生成与管理工具（Supabase 版本）
用于生成、管理和导出访问码
"""

import os
import random
import string
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import csv
from dotenv import load_dotenv
from supabase import create_client, Client

# 加载环境变量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ENV_FILE = os.path.join(PROJECT_ROOT, ".env.local")

# 尝试加载 .env.local 文件
if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    # 也尝试从环境变量读取（可能已经在系统中设置）
    load_dotenv()


def get_supabase_client() -> Client:
    """创建 Supabase 客户端"""
    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "缺少 Supabase 环境变量。请设置 NEXT_PUBLIC_SUPABASE_URL 和 SUPABASE_SERVICE_ROLE_KEY\n"
            "可以在 .env.local 文件中设置，或通过环境变量设置。"
        )

    return create_client(supabase_url, supabase_key)


def generate_access_code(length: int = 8) -> str:
    """
    生成随机访问码
    格式：XXXX-XXXX（字母数字混合，大写）
    
    Args:
        length: 总长度（不包括分隔符），默认8，会分成两组
    
    Returns:
        访问码字符串，如 "A3F7-K9M2"
    """
    chars = string.ascii_uppercase + string.digits
    # 排除容易混淆的字符：0, O, I, 1
    chars = chars.replace('0', '').replace('O', '').replace('I', '').replace('1', '')
    
    half = length // 2
    part1 = ''.join(random.choice(chars) for _ in range(half))
    part2 = ''.join(random.choice(chars) for _ in range(half))
    return f"{part1}-{part2}"


def generate_codes(
    supabase: Client,
    count: int,
    validity_days: int = 365,
    expires_at: Optional[str] = None,
    notes: Optional[str] = None
) -> List[Dict]:
    """
    生成指定数量的访问码并保存到 Supabase
    
    Args:
        supabase: Supabase 客户端
        count: 生成数量
        validity_days: 有效期（天数），默认365天（1年）
        expires_at: 直接指定过期时间（ISO 格式字符串），如果提供则忽略 validity_days
        notes: 备注信息（如批次号、客户名称等）
    
    Returns:
        生成的访问码列表
    """
    codes = []
    now = datetime.now()
    
    if expires_at:
        expires_datetime = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        validity_days = (expires_datetime - now).days
    else:
        expires_datetime = now + timedelta(days=validity_days)
    
    for i in range(count):
        code = generate_access_code()
        
        # 检查访问码是否已存在
        existing = supabase.table("access_codes").select("code").eq("code", code).execute()
        if existing.data:
            # 如果已存在，重新生成
            while True:
                code = generate_access_code()
                existing = supabase.table("access_codes").select("code").eq("code", code).execute()
                if not existing.data:
                    break
        
        code_data = {
            "code": code,
            "status": "active",
            "expires_at": expires_datetime.isoformat(),
            "validity_days": validity_days,
            "usage_count": 0,
            "last_used_at": None,
            "notes": notes or f"批量生成-{now.strftime('%Y%m%d')}"
        }
        
        # 插入到 Supabase
        result = supabase.table("access_codes").insert(code_data).execute()
        if result.data:
            codes.append(result.data[0])
            print(f"✅ 已生成访问码: {code}")
        else:
            print(f"⚠️  生成访问码失败: {code}")
    
    return codes


def list_codes(supabase: Client, status_filter: Optional[str] = None, show_stats: bool = True):
    """列出访问码"""
    query = supabase.table("access_codes").select("*")
    
    if status_filter:
        query = query.eq("status", status_filter)
    
    result = query.order("created_at", desc=True).execute()
    codes = result.data if result.data else []
    
    if show_stats:
        # 获取统计信息
        all_result = supabase.table("access_codes").select("status").execute()
        all_codes = all_result.data if all_result.data else []
        
        total = len(all_codes)
        active = len([c for c in all_codes if c.get("status") == "active"])
        expired = len([c for c in all_codes if c.get("status") == "expired"])
        revoked = len([c for c in all_codes if c.get("status") == "revoked"])
        
        print(f"\n📊 访问码统计:")
        print(f"   总计: {total}")
        print(f"   有效: {active}")
        print(f"   已过期: {expired}")
        print(f"   已撤销: {revoked}")
        print()
    
    if not codes:
        print("⚠️  没有符合条件的访问码")
        return
    
    print(f"📋 访问码列表 ({len(codes)} 个):")
    print("-" * 100)
    for code_data in codes:
        expires = datetime.fromisoformat(code_data["expires_at"].replace('Z', '+00:00'))
        expires_str = expires.strftime("%Y-%m-%d")
        usage = code_data.get("usage_count", 0)
        last_used = code_data.get("last_used_at")
        if last_used:
            last_used = datetime.fromisoformat(last_used.replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
        else:
            last_used = "未使用"
        
        # 显示绑定信息
        bound_email = code_data.get("bound_user_email", "")
        bound_phone = code_data.get("bound_user_phone", "")
        bound_at = code_data.get("bound_at")
        if bound_at:
            bound_at_str = datetime.fromisoformat(bound_at.replace('Z', '+00:00')).strftime("%Y-%m-%d")
        else:
            bound_at_str = ""
        
        bound_info = ""
        if bound_email:
            bound_info = f"邮箱: {bound_email}"
        if bound_phone:
            if bound_info:
                bound_info += f" | 手机: {bound_phone}"
            else:
                bound_info = f"手机: {bound_phone}"
        if not bound_info:
            bound_info = "未绑定"
        
        print(f"   {code_data['code']:12} | 状态: {code_data['status']:8} | "
              f"到期: {expires_str} | 使用: {usage:3}次 | 最后使用: {last_used}")
        print(f"   {'':12}   绑定: {bound_info}")
        if bound_at_str:
            print(f"   {'':12}   绑定时间: {bound_at_str}")
        if code_data.get("notes"):
            print(f"   {'':12}   备注: {code_data['notes']}")
    print("-" * 100)


def export_to_csv(supabase: Client, output_file: Optional[str] = None, status_filter: Optional[str] = None):
    """
    导出访问码到CSV文件
    
    Args:
        supabase: Supabase 客户端
        output_file: 输出文件路径（默认：tools/access_codes_YYYYMMDD.csv）
        status_filter: 状态过滤（active, expired, revoked），None表示全部
    """
    query = supabase.table("access_codes").select("*")
    
    if status_filter:
        query = query.eq("status", status_filter)
    
    result = query.order("created_at", desc=True).execute()
    codes = result.data if result.data else []
    
    if not codes:
        print("⚠️  没有符合条件的访问码")
        return
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(BASE_DIR, f"access_codes_{timestamp}.csv")
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "code", "status", "created_at", "expires_at", 
            "validity_days", "usage_count", "last_used_at", 
            "bound_user_email", "bound_user_phone", "bound_at", "notes"
        ])
        writer.writeheader()
        writer.writerows(codes)
    
    print(f"✅ 已导出 {len(codes)} 个访问码到: {output_file}")


def revoke_code(supabase: Client, code: str):
    """撤销访问码"""
    result = supabase.table("access_codes").update({"status": "revoked"}).eq("code", code).execute()
    
    if result.data:
        print(f"✅ 访问码 {code} 已撤销")
    else:
        print(f"⚠️  未找到访问码: {code}")


def set_expiry(supabase: Client, code: str, expires_at: str):
    """设置访问码的过期时间"""
    try:
        expires_datetime = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
        now = datetime.now()
        validity_days = (expires_datetime - now).days
        
        result = supabase.table("access_codes").update({
            "expires_at": expires_datetime.isoformat(),
            "validity_days": validity_days
        }).eq("code", code).execute()
        
        if result.data:
            print(f"✅ 访问码 {code} 的过期时间已设置为: {expires_at}")
        else:
            print(f"⚠️  未找到访问码: {code}")
    except ValueError as e:
        print(f"⚠️  日期格式错误: {e}")
        print("   请使用 ISO 格式，例如: 2027-12-31T23:59:59")


def main():
    parser = argparse.ArgumentParser(description="IELTS Novel Flow - 访问码生成与管理工具（Supabase 版本）")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 生成访问码
    gen_parser = subparsers.add_parser("generate", aliases=["gen", "g"], help="生成访问码")
    gen_parser.add_argument("-n", "--count", type=int, default=10, help="生成数量（默认: 10）")
    gen_parser.add_argument("-d", "--days", type=int, default=365, help="有效期天数（默认: 365）")
    gen_parser.add_argument("--expires-at", type=str, help="直接指定过期时间（ISO 格式，例如: 2027-12-31T23:59:59）")
    gen_parser.add_argument("--notes", type=str, help="备注信息（如批次号、客户名称等）")
    
    # 列出访问码
    list_parser = subparsers.add_parser("list", aliases=["ls", "l"], help="列出访问码")
    list_parser.add_argument("--status", choices=["active", "expired", "revoked"], help="按状态过滤")
    list_parser.add_argument("--no-stats", action="store_true", help="不显示统计信息")
    
    # 导出CSV
    export_parser = subparsers.add_parser("export", aliases=["exp", "e"], help="导出访问码到CSV")
    export_parser.add_argument("-o", "--output", type=str, help="输出文件路径")
    export_parser.add_argument("--status", choices=["active", "expired", "revoked"], help="按状态过滤")
    
    # 撤销访问码
    revoke_parser = subparsers.add_parser("revoke", aliases=["r"], help="撤销访问码")
    revoke_parser.add_argument("code", type=str, help="要撤销的访问码")
    
    # 设置过期时间
    expiry_parser = subparsers.add_parser("set-expiry", aliases=["expiry"], help="设置访问码的过期时间")
    expiry_parser.add_argument("code", type=str, help="访问码")
    expiry_parser.add_argument("expires_at", type=str, help="过期时间（ISO 格式，例如: 2027-12-31T23:59:59）")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        supabase = get_supabase_client()
    except ValueError as e:
        print(f"❌ 错误: {e}")
        print("\n💡 提示:")
        print("   1. 在项目根目录创建 .env.local 文件")
        print("   2. 添加以下内容:")
        print("      NEXT_PUBLIC_SUPABASE_URL=your_supabase_url")
        print("      SUPABASE_SERVICE_ROLE_KEY=your_service_role_key")
        print("   3. 或者通过环境变量设置这些值")
        return
    
    if args.command in ["generate", "gen", "g"]:
        print(f"🔑 正在生成 {args.count} 个访问码...")
        if args.expires_at:
            print(f"   过期时间: {args.expires_at}")
        else:
            print(f"   有效期: {args.days} 天")
        
        new_codes = generate_codes(
            supabase,
            args.count,
            args.days,
            args.expires_at,
            args.notes
        )
        print(f"\n✅ 成功生成 {len(new_codes)} 个访问码")
        print("\n生成的访问码:")
        for code_data in new_codes:
            print(f"   {code_data['code']}")
    
    elif args.command in ["list", "ls", "l"]:
        list_codes(supabase, args.status, show_stats=not args.no_stats)
    
    elif args.command in ["export", "exp", "e"]:
        export_to_csv(supabase, args.output, args.status)
    
    elif args.command in ["revoke", "r"]:
        revoke_code(supabase, args.code)
    
    elif args.command in ["set-expiry", "expiry"]:
        set_expiry(supabase, args.code, args.expires_at)


if __name__ == "__main__":
    main()
