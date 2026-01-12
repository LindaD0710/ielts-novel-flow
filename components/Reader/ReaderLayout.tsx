"use client";

import React from "react";

interface ReaderLayoutProps {
  title: string;
  author: string;
  chapterTitle: string;
  children: React.ReactNode;
}

/**
 * 阅读器布局组件
 * 参考微信读书的设计，提供优雅的阅读体验
 */
export default function ReaderLayout({
  title,
  author,
  chapterTitle,
  children,
}: ReaderLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* 书籍信息 */}
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-serif text-white mb-2 drop-shadow-lg">{title}</h1>
          <p className="text-sm text-slate-300 font-serif">{author}</p>
        </div>

        {/* 章节标题：如果和书名相同，就不重复显示 */}
        {chapterTitle && chapterTitle !== title && (
          <div className="mb-10 text-center">
            <h2 className="text-xl font-serif text-slate-200 drop-shadow-md">
              {chapterTitle}
            </h2>
          </div>
        )}

        {/* 阅读内容区域 - Glassmorphism 效果 */}
        <div className="bg-slate-900/40 backdrop-blur-md rounded-2xl shadow-2xl border border-white/10 p-12 md:p-16">
          <div className="prose prose-lg max-w-none text-slate-300 leading-loose text-lg">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

