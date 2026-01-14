"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, LogOut, Play } from "lucide-react";
import { 
  bookCategories, 
  DEFAULT_CATEGORY_ID, 
  getBooksByCategory 
} from "@/src/data/library";
import type { BookWithCategory } from "@/src/data/library";
import Link from "next/link";
import LoadingSpinner from "@/components/LoadingSpinner";

const AUTH_KEY = "ielts-novel-flow:authenticated";

export default function LibraryPage() {
  const router = useRouter();
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  
  // 当前选中的分类（默认重生）
  const [selectedCategory, setSelectedCategory] = useState<string>(DEFAULT_CATEGORY_ID);
  
  // 获取当前分类下的书籍
  const currentBooks = getBooksByCategory(selectedCategory);

  // 检查登录状态
  useEffect(() => {
    if (typeof window !== "undefined") {
      const isAuthenticated = localStorage.getItem(AUTH_KEY);
      if (isAuthenticated !== "true") {
        router.push("/login");
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
        message="正在加载图书馆..."
        subMessage="请稍候"
        showTimeoutWarning={false}
      />
    );
  }

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem(AUTH_KEY);
      router.push("/login");
    }
  };

  const handleCategoryClick = (categoryId: string) => {
    setSelectedCategory(categoryId);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-[#1a1b4b] to-[#2e1065]">
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* 头部 */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-serif text-white mb-2 drop-shadow-lg">
              我的图书馆
            </h1>
            <p className="text-slate-300">选择一本书开始阅读</p>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 rounded-xl transition-colors border border-white/10"
          >
            <LogOut className="w-4 h-4" />
            <span>退出</span>
          </button>
        </div>

        {/* 分类标签 */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-3">
            {bookCategories.map((category) => {
              const isSelected = selectedCategory === category.id;
              return (
                <button
                  key={category.id}
                  onClick={() => handleCategoryClick(category.id)}
                  className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isSelected
                      ? "bg-gradient-to-r from-cyan-500 to-purple-500 text-white shadow-lg shadow-cyan-500/30"
                      : "bg-slate-900/40 backdrop-blur-sm border border-white/10 text-slate-300 hover:border-cyan-400/50 hover:text-white"
                  }`}
                  style={
                    !isSelected
                      ? { borderColor: `${category.color}40` }
                      : undefined
                  }
                >
                  {category.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* 当前分类下的书籍列表 */}
        {currentBooks.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {currentBooks.map((book) => (
              <div
                key={book.id}
                className="group bg-slate-900/40 backdrop-blur-md rounded-2xl shadow-2xl border border-white/10 overflow-hidden hover:border-cyan-400/50 transition-all duration-300 hover:shadow-cyan-500/20 hover:shadow-2xl"
              >
                {/* 封面 */}
                <div
                  className="w-full h-64 rounded-t-2xl flex items-center justify-center shadow-lg relative overflow-hidden"
                  style={{
                    background: `linear-gradient(135deg, ${book.coverColor}40, ${book.coverColor}80)`,
                  }}
                >
                  <div
                    className="absolute inset-0 opacity-20"
                    style={{
                      backgroundImage: `radial-gradient(circle at 30% 50%, ${book.coverColor}60 0%, transparent 50%)`,
                    }}
                  />
                  <BookOpen className="w-20 h-20 text-white/90 relative z-10 group-hover:scale-110 transition-transform duration-300" />
                </div>

                {/* 书籍信息 */}
                <div className="p-6">
                  <h3 className="text-xl font-serif text-white mb-2 group-hover:text-cyan-400 transition-colors line-clamp-2">
                    {book.title}
                  </h3>
                  <p className="text-slate-400 text-sm mb-4">{book.author}</p>

                  {/* 开始阅读按钮 */}
                  <Link
                    href={`/read/${book.id}`}
                    className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white font-medium rounded-xl hover:from-cyan-400 hover:to-purple-400 transition-all duration-200 shadow-lg hover:shadow-cyan-500/30 group/btn"
                  >
                    <Play className="w-4 h-4" />
                    <span>开始阅读</span>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* 空状态提示 */
          <div className="text-center py-16 bg-slate-900/20 backdrop-blur-sm rounded-2xl border border-white/5">
            <BookOpen className="w-16 h-16 text-slate-600 mx-auto mb-4" />
            <p className="text-slate-400 text-lg mb-2">暂无该类型的书籍</p>
            <p className="text-slate-500 text-sm">请选择其他分类查看</p>
          </div>
        )}
      </div>
    </main>
  );
}


