"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { BookOpen } from "lucide-react";

const AUTH_KEY = "ielts-novel-flow:authenticated";

export default function LoginPage() {
  const [accessCode, setAccessCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  // 检查是否已登录
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuthenticated = localStorage.getItem(AUTH_KEY);
      if (isAuthenticated === "true") {
        router.push("/library");
      }
    }
  }, [router]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!accessCode.trim()) {
      return;
    }

    setIsLoading(true);
    
    // 模拟验证（输入任意字符即可）
    setTimeout(() => {
      if (typeof window !== "undefined") {
        localStorage.setItem(AUTH_KEY, "true");
        router.push("/library");
      }
    }, 500);
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
                onChange={(e) => setAccessCode(e.target.value)}
                placeholder="请输入访问码"
                className="w-full px-4 py-3 bg-slate-800/50 border border-white/10 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all"
                autoFocus
              />
              <p className="mt-2 text-xs text-slate-400">
                输入任意字符即可进入（演示模式）
              </p>
            </div>

            <button
              type="submit"
              disabled={!accessCode.trim() || isLoading}
              className="w-full py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-xl shadow-lg hover:from-cyan-400 hover:to-purple-400 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "验证中..." : "进入图书馆"}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}


