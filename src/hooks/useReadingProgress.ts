"use client";

import { useState, useEffect, useCallback } from "react";
import { Chapter } from "@/types";

const STORAGE_KEY_PREFIX = "ielts-novel-flow:lastReadChapterId";

/**
 * 根据 bookId 生成存储 key
 */
function getStorageKey(bookId?: string): string {
  if (bookId) {
    return `${STORAGE_KEY_PREFIX}:${bookId}`;
  }
  return STORAGE_KEY_PREFIX;
}

/**
 * 阅读进度管理 Hook
 * 使用 localStorage 保存和读取用户的阅读位置
 */
export function useReadingProgress(
  defaultChapterId: string,
  getChapter: (chapterId: string) => Chapter | null,
  bookId?: string // 添加 bookId 参数
) {
  const [currentChapterId, setCurrentChapterId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const storageKey = getStorageKey(bookId);

  // 从 localStorage 读取上次阅读的章节（根据 bookId 区分）
  useEffect(() => {
    if (typeof window === "undefined") return;

    try {
      const savedChapterId = localStorage.getItem(storageKey);
      
      if (savedChapterId) {
        // 验证保存的章节是否存在
        const chapter = getChapter(savedChapterId);
        if (chapter) {
          // 如果是同一本书的章节，才使用保存的进度
          if (!bookId || (chapter as any).book_id === bookId) {
            setCurrentChapterId(savedChapterId);
            setIsLoading(false);
            return;
          } else {
            // 如果不是同一本书，清除旧记录
            localStorage.removeItem(storageKey);
          }
        } else {
          // 如果保存的章节不存在，清除无效记录
          localStorage.removeItem(storageKey);
        }
      }
      
      // 如果没有保存的记录或记录无效，使用默认章节
      setCurrentChapterId(defaultChapterId);
    } catch (error) {
      console.error("读取阅读进度失败:", error);
      setCurrentChapterId(defaultChapterId);
    } finally {
      setIsLoading(false);
    }
  }, [defaultChapterId, getChapter, storageKey, bookId]);

  // 保存阅读进度
  const saveProgress = useCallback((chapterId: string) => {
    if (typeof window === "undefined") return;

    try {
      localStorage.setItem(storageKey, chapterId);
      setCurrentChapterId(chapterId);
    } catch (error) {
      console.error("保存阅读进度失败:", error);
    }
  }, [storageKey]);

  // 清除阅读进度
  const clearProgress = useCallback(() => {
    if (typeof window === "undefined") return;

    try {
      localStorage.removeItem(storageKey);
      setCurrentChapterId(defaultChapterId);
    } catch (error) {
      console.error("清除阅读进度失败:", error);
    }
  }, [defaultChapterId, storageKey]);

  // 获取当前章节
  const currentChapter = currentChapterId ? getChapter(currentChapterId) : null;

  return {
    currentChapterId,
    currentChapter,
    isLoading,
    saveProgress,
    clearProgress,
  };
}


