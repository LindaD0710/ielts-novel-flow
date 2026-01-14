"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, Mail, Phone } from "lucide-react";
import LoadingSpinner from "@/components/LoadingSpinner";

const AUTH_KEY = "ielts-novel-flow:authenticated";

export default function LoginPage() {
  const [accessCode, setAccessCode] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [userPhone, setUserPhone] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [requiresUserInfo, setRequiresUserInfo] = useState(false);
  const router = useRouter();

  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // 检查是否已登录
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuthenticated = localStorage.getItem(AUTH_KEY);
      if (isAuthenticated === "true") {
        router.push("/library");
      } else {
        setIsCheckingAuth(false);
      }
    } else {
      setIsCheckingAuth(false);
    }
  }, [router]);

  // 如果正在检查认证状态，显示加载
  if (isCheckingAuth) {
    return (
      <LoadingSpinner
        message="正在检查登录状态..."
        showTimeoutWarning={false}
      />
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!accessCode.trim()) {
      setError("请输入访问码");
      return;
    }

    // 如果API要求用户信息，但用户没有输入，先检查访问码
    if (!requiresUserInfo && !userEmail.trim() && !userPhone.trim()) {
      // 先检查访问码是否需要绑定
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await fetch("/api/validate-code", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ accessCode: accessCode.trim() }),
        });

        const data = await response.json();

        if (data.requiresUserInfo) {
          // 需要用户信息（首次使用或已绑定需要验证）
          setRequiresUserInfo(true);
          setError(data.error || "请输入您的邮箱或手机号");
          setIsLoading(false);
          return;
        } else if (response.ok && data.success) {
          // 直接成功（理论上不应该发生，因为现在都需要绑定）
          handleSuccess(data);
          return;
        } else {
          setError(data.error || "访问码验证失败");
          setIsLoading(false);
          return;
        }
      } catch (err) {
        console.error("验证访问码时发生错误:", err);
        setError("网络错误，请稍后重试");
        setIsLoading(false);
        return;
      }
    }

    // 有用户信息，进行完整验证
    if (!userEmail.trim() && !userPhone.trim()) {
      setError("请输入邮箱或手机号");
      return;
    }

    setIsLoading(true);
    setError(null);
    
    try {
      // 调用API验证访问码并绑定/验证用户
      const response = await fetch("/api/validate-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          accessCode: accessCode.trim(),
          userEmail: userEmail.trim() || undefined,
          userPhone: userPhone.trim() || undefined,
        }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        handleSuccess(data);
      } else {
        // 验证失败，显示错误信息
        setError(data.error || "访问码验证失败，请检查后重试");
        if (data.requiresUserInfo) {
          setRequiresUserInfo(true);
        }
      }
    } catch (err) {
      console.error("验证访问码时发生错误:", err);
      setError("网络错误，请稍后重试");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuccess = (data: any) => {
    // 验证成功，保存认证状态
    if (typeof window !== "undefined") {
      localStorage.setItem(AUTH_KEY, "true");
      localStorage.setItem("ielts-novel-flow:access-code", data.code);
      if (data.expires_at) {
        localStorage.setItem("ielts-novel-flow:expires-at", data.expires_at);
      }
      if (data.boundUserEmail) {
        localStorage.setItem("ielts-novel-flow:bound-email", data.boundUserEmail);
      }
      if (data.boundUserPhone) {
        localStorage.setItem("ielts-novel-flow:bound-phone", data.boundUserPhone);
      }
    }
    router.push("/library");
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
      <div className="max-w-md w-full mx-auto px-6">
        <div className="bg-slate-900/40 backdrop-blur-md rounded-2xl shadow-2xl border border-white/10 p-8">
          {/* Logo/标题 */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-cyan-400 to-purple-500 rounded-2xl mb-4 shadow-lg">
              <BookOpen className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-serif text-white mb-2 drop-shadow-lg">
              IELTS Novel Flow
            </h1>
            <p className="text-slate-300 text-sm">
              通过阅读小说学习雅思词汇
            </p>
          </div>

          {/* 登录表单 */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="accessCode"
                className="block text-sm font-medium text-slate-300 mb-2"
              >
                访问码
              </label>
              <input
                id="accessCode"
                type="text"
                value={accessCode}
                onChange={(e) => {
                  setAccessCode(e.target.value);
                  setRequiresUserInfo(false);
                  setError(null);
                }}
                placeholder="请输入访问码"
                className="w-full px-4 py-3 bg-slate-800/50 border border-white/10 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all"
                autoFocus
              />
              <p className="mt-2 text-xs text-slate-400">
                请输入您购买的访问码（格式：XXXX-XXXX）
              </p>
            </div>

            {/* 用户信息输入（邮箱或手机号） */}
            {(requiresUserInfo || userEmail || userPhone) && (
              <div className="space-y-4">
                <div>
                  <label
                    htmlFor="userEmail"
                    className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2"
                  >
                    <Mail className="w-4 h-4" />
                    邮箱（推荐）
                  </label>
                  <input
                    id="userEmail"
                    type="email"
                    value={userEmail}
                    onChange={(e) => setUserEmail(e.target.value)}
                    placeholder="your@email.com"
                    className="w-full px-4 py-3 bg-slate-800/50 border border-white/10 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all"
                  />
                </div>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-slate-600"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-slate-900/40 text-slate-400">或</span>
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="userPhone"
                    className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2"
                  >
                    <Phone className="w-4 h-4" />
                    手机号
                  </label>
                  <input
                    id="userPhone"
                    type="tel"
                    value={userPhone}
                    onChange={(e) => setUserPhone(e.target.value)}
                    placeholder="13800138000"
                    className="w-full px-4 py-3 bg-slate-800/50 border border-white/10 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all"
                  />
                </div>

                <p className="text-xs text-slate-400">
                  {requiresUserInfo 
                    ? "此访问码需要绑定您的账户，请输入邮箱或手机号（至少一个）"
                    : "首次使用将绑定您的账户，防止多人共用访问码"}
                </p>
              </div>
            )}

            {error && (
              <div className="text-xs text-red-400 bg-red-900/20 border border-red-500/30 rounded-lg px-3 py-2">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={!accessCode.trim() || isLoading || (requiresUserInfo && !userEmail.trim() && !userPhone.trim())}
              className="w-full py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-xl shadow-lg hover:from-cyan-400 hover:to-purple-400 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed relative"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>验证中...</span>
                </span>
              ) : (
                <span>{requiresUserInfo ? "绑定并登录" : "进入图书馆"}</span>
              )}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
