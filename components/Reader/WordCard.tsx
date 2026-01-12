"use client";

import React, { useEffect } from "react";
import { Volume2, X } from "lucide-react";
import { Vocabulary } from "@/types";

interface WordCardProps {
  /** 单词数据 */
  vocabulary: Vocabulary | null;
  /** 是否显示 */
  isOpen: boolean;
  /** 关闭回调 */
  onClose: () => void;
}

/**
 * 单词卡片组件
 * 从底部滑出的抽屉，展示单词的完整信息
 */
export default function WordCard({
  vocabulary,
  isOpen,
  onClose,
}: WordCardProps) {
  // 处理发音功能
  const handlePronounce = () => {
    if (!vocabulary || typeof window === "undefined") return;

    if ("speechSynthesis" in window) {
      // 停止当前正在播放的语音
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(vocabulary.word);
      utterance.lang = "en-US";
      utterance.rate = 0.9; // 稍微慢一点，更清晰
      utterance.pitch = 1;

      window.speechSynthesis.speak(utterance);
    }
  };

  // 点击遮罩层关闭
  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  // 阻止背景滚动
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!vocabulary) return null;

  return (
    <>
      {/* 遮罩层 */}
      <div
        className={`fixed inset-0 bg-black/60 backdrop-blur-sm z-40 transition-opacity duration-300 ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={handleBackdropClick}
      />

      {/* 卡片抽屉 - 深色磨砂玻璃风格 */}
      <div
        className={`fixed bottom-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-md rounded-t-3xl shadow-2xl border-t border-white/10 transition-transform duration-300 ease-out ${
          isOpen ? "translate-y-0" : "translate-y-full"
        }`}
        style={{ maxHeight: "85vh" }}
      >
        <div className="overflow-y-auto h-full">
          {/* 拖拽指示器 */}
          <div className="flex justify-center pt-4 pb-2">
            <div className="w-12 h-1.5 bg-white/30 rounded-full" />
          </div>

          {/* 关闭按钮 */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 rounded-full hover:bg-white/10 transition-colors"
            aria-label="关闭"
          >
            <X className="w-5 h-5 text-slate-300" />
          </button>

          {/* 卡片内容 */}
          <div className="px-8 pb-8 pt-6">
            {/* 单词标题 */}
            <div className="mb-6">
              <div className="flex items-center gap-4 mb-3">
                <h2 className="text-4xl font-serif font-bold text-cyan-400 glow-cyan tracking-tight">
                  {vocabulary.word}
                </h2>
                <button
                  onClick={handlePronounce}
                  className="p-2.5 rounded-full bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-400 transition-colors shadow-lg border border-cyan-400/30"
                  aria-label="发音"
                >
                  <Volume2 className="w-5 h-5" />
                </button>
              </div>
              <p className="text-lg text-slate-400 font-serif">
                {vocabulary.phonetic}
              </p>
            </div>

            {/* 中文释义 */}
            <div className="mb-6 pb-6 border-b border-white/10">
              <p className="text-xl text-slate-200 font-medium">
                {vocabulary.meaning}
              </p>
            </div>

            {/* 词根/助记 */}
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-2">
                词根助记
              </h3>
              <div className="bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-xl p-4 border border-cyan-400/20 backdrop-blur-sm">
                <p className="text-base text-slate-300 font-mono">
                  {vocabulary.root && vocabulary.root.trim().length > 0
                    ? vocabulary.root
                    : "（该单词的词根/助记暂未录入，将在后续版本补全）"}
                </p>
              </div>
            </div>

            {/* 例句 */}
            <div>
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">
                例句
              </h3>
              <div className="space-y-3">
                <div className="bg-slate-800/40 backdrop-blur-sm rounded-xl p-5 border-l-4 border-cyan-400 shadow-lg">
                  <p className="text-base text-slate-200 font-serif leading-relaxed mb-2">
                    {vocabulary.example && vocabulary.example.trim().length > 0
                      ? vocabulary.example
                      : "Example sentence for this word will be added soon."}
                  </p>
                  <p className="text-sm text-slate-400 italic leading-relaxed">
                    {vocabulary.exampleCn && vocabulary.exampleCn.trim().length > 0
                      ? vocabulary.exampleCn
                      : "该单词的中文例句稍后会补充。"}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

