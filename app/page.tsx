"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import LoadingSpinner from "@/components/LoadingSpinner";

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
    <LoadingSpinner
      message="正在初始化..."
      subMessage="请稍候"
      showTimeoutWarning={true}
      timeoutMs={6000}
    />
  );
}
