"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // 检查是否已登录
    if (typeof window !== "undefined") {
      const isAuthenticated = localStorage.getItem("ielts-novel-flow:authenticated");
      if (isAuthenticated === "true") {
        router.push("/library");
      } else {
        router.push("/login");
      }
    }
  }, [router]);

  // 显示加载状态
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
      <div className="text-center">
        <p className="text-slate-300 text-lg">加载中...</p>
      </div>
    </main>
  );
}
