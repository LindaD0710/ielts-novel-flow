"use client";

import { useEffect, useState } from "react";
import { BookOpen, Wifi, WifiOff } from "lucide-react";

interface LoadingSpinnerProps {
  message?: string;
  subMessage?: string;
  showTimeoutWarning?: boolean;
  timeoutMs?: number;
  variant?: "default" | "fullscreen" | "inline";
}

export default function LoadingSpinner({
  message = "加载中...",
  subMessage,
  showTimeoutWarning = true,
  timeoutMs = 6000, // 6秒后显示超时提示
  variant = "fullscreen",
}: LoadingSpinnerProps) {
  const [showTimeout, setShowTimeout] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    if (!showTimeoutWarning) return;

    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      setElapsedTime(elapsed);
      
      if (elapsed >= timeoutMs) {
        setShowTimeout(true);
      }
    }, 100);

    return () => clearInterval(interval);
  }, [showTimeoutWarning, timeoutMs]);

  const spinnerContent = (
    <div className="flex flex-col items-center justify-center">
      {/* 主加载动画 */}
      <div className="relative mb-6">
        {/* 外圈旋转动画 */}
        <div className="w-16 h-16 border-4 border-slate-700/30 border-t-cyan-400 border-r-purple-500 rounded-full animate-spin"></div>
        {/* 内圈旋转动画（反向） */}
        <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-b-purple-400 border-l-cyan-500 rounded-full animate-spin" style={{ animationDirection: "reverse", animationDuration: "0.8s" }}></div>
        {/* 中心图标 */}
        <div className="absolute inset-0 flex items-center justify-center">
          <BookOpen className="w-6 h-6 text-cyan-400 animate-pulse" />
        </div>
      </div>

      {/* 文字提示 */}
      <div className="text-center">
        <p className="text-slate-200 text-lg font-medium mb-2">{message}</p>
        {subMessage && (
          <p className="text-slate-400 text-sm">{subMessage}</p>
        )}
        
        {/* 超时提示 */}
        {showTimeout && (
          <div className="mt-4 p-3 bg-amber-900/20 border border-amber-500/30 rounded-lg max-w-sm">
            <div className="flex items-center gap-2 text-amber-400 text-sm">
              <WifiOff className="w-4 h-4" />
              <span>网络连接较慢，请耐心等待...</span>
            </div>
            <p className="text-amber-500/70 text-xs mt-2">
              如果长时间无法加载，请检查网络连接或稍后重试
            </p>
          </div>
        )}

        {/* 进度点动画 */}
        {!showTimeout && (
          <div className="flex items-center justify-center gap-1 mt-4">
            <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: "0s" }}></div>
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
            <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
          </div>
        )}
      </div>
    </div>
  );

  if (variant === "inline") {
    return <div className="py-8">{spinnerContent}</div>;
  }

  if (variant === "fullscreen") {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
        <div className="max-w-md mx-auto px-6">
          {spinnerContent}
        </div>
      </main>
    );
  }

  // default variant
  return (
    <div className="flex items-center justify-center p-8">
      {spinnerContent}
    </div>
  );
}
