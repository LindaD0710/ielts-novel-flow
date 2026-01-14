"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import ContentParser from "@/components/Reader/ContentParser";
import ReaderLayout from "@/components/Reader/ReaderLayout";
import WordCard from "@/components/Reader/WordCard";
import { Vocabulary } from "@/types";
import {
  getChapter,
  defaultChapterId,
  getVocabulary,
  getAllChapters,
  getChapterByNumber,
  getFirstChapterByBookId,
  getChaptersByBookId,
} from "@/src/services/novelService";
import { useReadingProgress } from "@/src/hooks/useReadingProgress";
import { getBookById } from "@/src/data/library";
import { ArrowLeft, ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";
import LoadingSpinner from "@/components/LoadingSpinner";

const AUTH_KEY = "ielts-novel-flow:authenticated";

export default function ReadPage() {
  const params = useParams();
  const router = useRouter();
  const bookId = params?.bookId as string;

  const [selectedWord, setSelectedWord] = useState<Vocabulary | null>(null);
  const [isWordCardOpen, setIsWordCardOpen] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);

  // 检查登录状态
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuthenticated = localStorage.getItem(AUTH_KEY);
      if (isAuthenticated !== "true") {
        router.push("/login");
        return;
      }
    }
  }, [router]);

  // 获取书籍信息
  const book = bookId ? getBookById(bookId) : null;

  // 根据 bookId 获取该书籍的章节
  const bookChapters = bookId ? getChaptersByBookId(bookId) : [];
  const bookFirstChapter = bookId ? getFirstChapterByBookId(bookId) : null;
  
  // 获取章节列表：优先使用该书籍的章节，否则使用所有章节
  const allChapters = bookId && bookChapters.length > 0 ? bookChapters : getAllChapters();
  
  // 确定默认章节 ID：优先使用该书籍的第一章，否则使用全局默认章节
  const initialChapterId = bookFirstChapter?.id || defaultChapterId;

  // 使用阅读进度 Hook（传入 bookId 以区分不同书籍的进度）
  const { currentChapter, isLoading, saveProgress, currentChapterId } = useReadingProgress(
    initialChapterId,
    getChapter,
    bookId // 传入 bookId，让 Hook 根据书籍区分进度
  );

  // 页面初始化：等待书籍和章节数据准备好
  useEffect(() => {
    // 如果书籍不存在，不需要等待
    if (!book) {
      setIsInitializing(false);
      return;
    }

    // 如果章节数据已准备好，结束初始化
    if (!isLoading && currentChapter) {
      // 稍微延迟一下，确保所有数据都已渲染
      const timer = setTimeout(() => {
        setIsInitializing(false);
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [book, isLoading, currentChapter]);

  // 当章节加载完成时，自动保存进度
  useEffect(() => {
    if (currentChapter && !isLoading) {
      saveProgress(currentChapter.id);
    }
  }, [currentChapter, isLoading, saveProgress]);

  const handleWordClick = (word: string, inlineMeaning?: string) => {
    // 1. 先从词汇库中查找
    const vocabulary = getVocabulary(word);
    if (vocabulary) {
      setSelectedWord(vocabulary);
      setIsWordCardOpen(true);
      return;
    }

    // 2. 如果词汇库里暂时没有这个词，用正文里的释义兜底，构造一个临时词卡
    if (inlineMeaning) {
      const fallback: Vocabulary = {
        word,
        meaning: inlineMeaning,
        phonetic: "",
        root: "",
        example: "",
        exampleCn: "",
      };
      setSelectedWord(fallback);
      setIsWordCardOpen(true);
      return;
    }

    // 3. 完全找不到时，仅给出控制台提示，避免前端报错
    console.warn(`未找到单词 "${word}" 的词汇数据`);
  };

  const handleCloseWordCard = () => {
    setIsWordCardOpen(false);
    setTimeout(() => {
      setSelectedWord(null);
    }, 300);
  };

  // 章节导航
  const currentChapterNum = currentChapter ? (currentChapter as any).chapter_num : null;
  const currentIndex = currentChapterNum 
    ? allChapters.findIndex((ch) => (ch as any).chapter_num === currentChapterNum)
    : -1;
  
  const prevChapter = currentIndex > 0 ? allChapters[currentIndex - 1] : null;
  const nextChapter = currentIndex >= 0 && currentIndex < allChapters.length - 1 
    ? allChapters[currentIndex + 1] 
    : null;

  const handleChapterChange = (chapterId: string) => {
    saveProgress(chapterId);
    // saveProgress 会更新 localStorage，useReadingProgress 会自动检测并更新 currentChapter
    // 由于 useReadingProgress 依赖 localStorage，我们需要触发重新渲染
    // 最简单的方式是刷新页面，但更好的方式是使用状态管理
    router.refresh(); // Next.js 的刷新方法，不会丢失状态
  };

  // 初始加载状态（页面首次加载时）
  if (isInitializing || isLoading) {
    return (
      <LoadingSpinner
        message="正在加载小说..."
        subMessage={isLoading ? "正在读取阅读进度" : "正在准备章节内容"}
        showTimeoutWarning={true}
        timeoutMs={6000}
      />
    );
  }

  // 书籍不存在
  if (!book) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
        <div className="max-w-md mx-auto px-6 text-center">
          <div className="bg-slate-900/40 backdrop-blur-md rounded-2xl shadow-2xl border border-white/10 p-8">
            <h2 className="text-2xl font-serif text-slate-200 mb-4">书籍不存在</h2>
            <p className="text-slate-300 mb-6">未找到该书籍</p>
            <Link
              href="/library"
              className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-xl hover:from-cyan-400 hover:to-purple-400 transition-all"
            >
              返回书架
            </Link>
          </div>
        </div>
      </main>
    );
  }

  // 章节不存在或数据为空
  if (!currentChapter) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
        <div className="max-w-md mx-auto px-6 text-center">
          <div className="bg-slate-900/40 backdrop-blur-md rounded-2xl shadow-2xl border border-white/10 p-8">
            <h2 className="text-2xl font-serif text-slate-200 mb-4">暂无内容</h2>
            <p className="text-slate-300 mb-6">
              请运行 Python 脚本生成章节数据。
            </p>
            <Link
              href="/library"
              className="inline-block px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-semibold rounded-xl hover:from-cyan-400 hover:to-purple-400 transition-all"
            >
              返回书架
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <>
      {/* 返回按钮 */}
      <div className="fixed top-6 left-6 z-30">
        <Link
          href="/library"
          className="flex items-center gap-2 px-4 py-2 bg-slate-900/60 backdrop-blur-md border border-white/10 rounded-xl text-slate-300 hover:text-white hover:border-cyan-400/50 transition-all shadow-lg"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>返回书架</span>
        </Link>
      </div>

      <ReaderLayout
        title={book.title}
        author={book.author}
        chapterTitle={currentChapter.title}
      >
        <ContentParser content={currentChapter.content} onWordClick={handleWordClick} />
        
        {/* 章节导航 */}
        <div className="mt-12 pt-8 border-t border-slate-700/50 flex items-center justify-between">
          {prevChapter ? (
            <button
              onClick={() => handleChapterChange(prevChapter.id)}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800/60 border border-white/10 rounded-xl text-slate-300 hover:text-white hover:border-cyan-400/50 transition-all"
            >
              <ChevronLeft className="w-4 h-4" />
              <span className="text-sm">上一章</span>
            </button>
          ) : (
            <div></div>
          )}
          
          <div className="text-sm text-slate-400">
            第 {currentChapterNum || '?'} 章 / 共 {allChapters.length} 章
          </div>
          
          {nextChapter ? (
            <button
              onClick={() => handleChapterChange(nextChapter.id)}
              className="flex items-center gap-2 px-4 py-2 bg-slate-800/60 border border-white/10 rounded-xl text-slate-300 hover:text-white hover:border-cyan-400/50 transition-all"
            >
              <span className="text-sm">下一章</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <div></div>
          )}
        </div>
      </ReaderLayout>

      <WordCard
        vocabulary={selectedWord}
        isOpen={isWordCardOpen}
        onClose={handleCloseWordCard}
      />
    </>
  );
}


