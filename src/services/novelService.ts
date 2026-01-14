import { Chapter, Vocabulary } from "@/types";

// 静态导入 JSON 文件（Next.js 会自动处理）
// 导入所有章节文件
// 注意：正式生产的章节文件需要手动导入到这里
// 格式：import bookXxxData from "../data/generated/book-xxx.json";
import book20260113030011Data from "../data/generated/book-20260113030011.json";
import book20260113030536Data from "../data/generated/book-20260113030536.json";
import book20260113030951Data from "../data/generated/book-20260113030951.json";
import book20260113031320Data from "../data/generated/book-20260113031320.json";
import book20260113031750Data from "../data/generated/book-20260113031750.json";
import book20260113032419Data from "../data/generated/book-20260113032419.json";
import book20260113033126Data from "../data/generated/book-20260113033126.json";
import book20260113033446Data from "../data/generated/book-20260113033446.json";
import book20260113034204Data from "../data/generated/book-20260113034204.json";
import book20260113034530Data from "../data/generated/book-20260113034530.json";
import book20260113035126Data from "../data/generated/book-20260113035126.json";
import book20260113035348Data from "../data/generated/book-20260113035348.json";
import book20260113035820Data from "../data/generated/book-20260113035820.json";
import book20260113040035Data from "../data/generated/book-20260113040035.json";
import book20260113065513Data from "../data/generated/book-20260113065513.json";
import book20260113065730Data from "../data/generated/book-20260113065730.json";
import book20260113070329Data from "../data/generated/book-20260113070329.json";
import book20260113070541Data from "../data/generated/book-20260113070541.json";
import book20260113070917Data from "../data/generated/book-20260113070917.json";
import book20260113071334Data from "../data/generated/book-20260113071334.json";
import book20260113071602Data from "../data/generated/book-20260113071602.json";
import book20260113071756Data from "../data/generated/book-20260113071756.json";
import book20260113071956Data from "../data/generated/book-20260113071956.json";
import book20260113072209Data from "../data/generated/book-20260113072209.json";
import book20260113072527Data from "../data/generated/book-20260113072527.json";
import book20260113072736Data from "../data/generated/book-20260113072736.json";
import book20260113073001Data from "../data/generated/book-20260113073001.json";
import book20260113073349Data from "../data/generated/book-20260113073349.json";
import book20260113073610Data from "../data/generated/book-20260113073610.json";
import book20260113073842Data from "../data/generated/book-20260113073842.json";
import book20260113074059Data from "../data/generated/book-20260113074059.json";
import book20260113074318Data from "../data/generated/book-20260113074318.json";
import book20260114105722Data from "../data/generated/book-20260114105722.json";
import book20260114111034Data from "../data/generated/book-20260114111034.json";
import book20260114113008Data from "../data/generated/book-20260114113008.json";
import book20260114113217Data from "../data/generated/book-20260114113217.json";
import book20260114113431Data from "../data/generated/book-20260114113431.json";
import book20260114114158Data from "../data/generated/book-20260114114158.json";
import book20260114114729Data from "../data/generated/book-20260114114729.json";
import book20260114115000Data from "../data/generated/book-20260114115000.json";
import book20260114131712Data from "../data/generated/book-20260114131712.json";
import book20260114132741Data from "../data/generated/book-20260114132741.json";
import book20260114132952Data from "../data/generated/book-20260114132952.json";
import book20260114133149Data from "../data/generated/book-20260114133149.json";
import book20260114133455Data from "../data/generated/book-20260114133455.json";
import book20260114133804Data from "../data/generated/book-20260114133804.json";
import book20260114134055Data from "../data/generated/book-20260114134055.json";
import book20260114134431Data from "../data/generated/book-20260114134431.json";
import book20260114134648Data from "../data/generated/book-20260114134648.json";
import book20260114134942Data from "../data/generated/book-20260114134942.json";
import book20260114135214Data from "../data/generated/book-20260114135214.json";
import book20260114135411Data from "../data/generated/book-20260114135411.json";
import book20260114135651Data from "../data/generated/book-20260114135651.json";
import book20260114135920Data from "../data/generated/book-20260114135920.json";
import book20260114140110Data from "../data/generated/book-20260114140110.json";
import book20260114140414Data from "../data/generated/book-20260114140414.json";
import book20260114140808Data from "../data/generated/book-20260114140808.json";
import book20260114141016Data from "../data/generated/book-20260114141016.json";
import book20260114141247Data from "../data/generated/book-20260114141247.json";
import book20260114141525Data from "../data/generated/book-20260114141525.json";
import vocabDbRawData from "../data/generated/vocab_db.json";

// 类型断言：确保导入的数据符合接口定义
// 正式生产的章节数据将添加到这里
// 注意：当数组为空时，TypeScript 会推断为 never[]，所以需要明确类型
const allChaptersData: Chapter[] = (
  [
    // 正式生产的章节将添加到这里
    book20260114141525Data as Chapter,
    book20260114141247Data as Chapter,
    book20260114141016Data as Chapter,
    book20260114140808Data as Chapter,
    book20260114140414Data as Chapter,
    book20260114140110Data as Chapter,
    book20260114135920Data as Chapter,
    book20260114135651Data as Chapter,
    book20260114135411Data as Chapter,
    book20260114135214Data as Chapter,
    book20260114134942Data as Chapter,
    book20260114134648Data as Chapter,
    book20260114134431Data as Chapter,
    book20260114134055Data as Chapter,
    book20260114133804Data as Chapter,
    book20260114133455Data as Chapter,
    book20260114133149Data as Chapter,
    book20260114132952Data as Chapter,
    book20260114132741Data as Chapter,
    book20260114131712Data as Chapter,
    book20260114115000Data as Chapter,
    book20260114114729Data as Chapter,
    book20260114114158Data as Chapter,
    book20260114113431Data as Chapter,
    book20260114113217Data as Chapter,
    book20260114113008Data as Chapter,
    book20260114111034Data as Chapter,
    book20260114105722Data as Chapter,
    book20260113074318Data as Chapter,
    book20260113074059Data as Chapter,
    book20260113073842Data as Chapter,
    book20260113073610Data as Chapter,
    book20260113073349Data as Chapter,
    book20260113073001Data as Chapter,
    book20260113072736Data as Chapter,
    book20260113072527Data as Chapter,
    book20260113072209Data as Chapter,
    book20260113071956Data as Chapter,
    book20260113071756Data as Chapter,
    book20260113071602Data as Chapter,
    book20260113071334Data as Chapter,
    book20260113070917Data as Chapter,
    book20260113070541Data as Chapter,
    book20260113070329Data as Chapter,
    book20260113065730Data as Chapter,
    book20260113065513Data as Chapter,
    book20260113040035Data as Chapter,
    book20260113035820Data as Chapter,
    book20260113035348Data as Chapter,
    book20260113035126Data as Chapter,
    book20260113034530Data as Chapter,
    book20260113034204Data as Chapter,
    book20260113033446Data as Chapter,
    book20260113033126Data as Chapter,
    book20260113032419Data as Chapter,
    book20260113031750Data as Chapter,
    book20260113031320Data as Chapter,
    book20260113030951Data as Chapter,
    book20260113030536Data as Chapter,
    book20260113030011Data as Chapter,
  ] as Chapter[]
).filter((ch) => ch && ch.id); // 过滤掉无效的章节

const vocabDbRaw = vocabDbRawData as Record<string, Vocabulary>;

// 词汇数据库：key 统一转为小写，便于查找
const vocabDb: Record<string, Vocabulary> = Object.fromEntries(
  Object.entries(vocabDbRaw).map(([key, value]) => [
    key.toLowerCase(),
    value,
  ])
);

// 章节数据库：按章节号排序，支持多章节
const chaptersById: Record<string, Chapter> = {};
allChaptersData.forEach((chapter) => {
  chaptersById[chapter.id] = chapter;
});

// 获取所有章节并按章节号排序（如果有 chapter_num 字段）
const sortedChapters = allChaptersData.sort((a, b) => {
  const aNum = (a as any).chapter_num || 0;
  const bNum = (b as any).chapter_num || 0;
  return aNum - bNum;
});

// 默认章节 ID：使用第一个章节（按章节号排序后的第一个）
export const defaultChapterId: string = sortedChapters[0]?.id || allChaptersData[0]?.id || "";

// 导出所有章节列表（用于章节导航）
export const allChapters: Chapter[] = sortedChapters;

/**
 * 获取章节数据
 * @param chapterId 章节 ID
 */
export function getChapter(chapterId: string): Chapter | null {
  return chaptersById[chapterId] ?? null;
}

/**
 * 获取默认章节（返回第一个章节）
 */
export function getDefaultChapter(): Chapter | null {
  if (!defaultChapterId) {
    return sortedChapters[0] || null;
  }
  return getChapter(defaultChapterId);
}

/**
 * 获取所有章节列表
 */
export function getAllChapters(): Chapter[] {
  return sortedChapters;
}

/**
 * 根据章节号获取章节
 */
export function getChapterByNumber(chapterNum: number): Chapter | null {
  return sortedChapters.find((ch) => (ch as any).chapter_num === chapterNum) || null;
}

/**
 * 根据 book_id 获取该书籍的章节列表
 * @param bookId 书籍 ID
 */
export function getChaptersByBookId(bookId: string): Chapter[] {
  return allChaptersData.filter((ch) => (ch as any).book_id === bookId);
}

/**
 * 根据 book_id 获取该书籍的第一个章节
 * @param bookId 书籍 ID
 */
export function getFirstChapterByBookId(bookId: string): Chapter | null {
  const chapters = getChaptersByBookId(bookId);
  if (chapters.length === 0) {
    return null;
  }
  // 按 chapter_num 排序，返回第一个
  const sorted = chapters.sort((a, b) => {
    const aNum = (a as any).chapter_num || 0;
    const bNum = (b as any).chapter_num || 0;
    return aNum - bNum;
  });
  return sorted[0] || chapters[0];
}

/**
 * 根据单词获取词汇详情
 * @param word 单词字符串（大小写不敏感）
 */
export function getVocabulary(word: string): Vocabulary | null {
  if (!word || typeof word !== "string") {
    return null;
  }
  const key = word.toLowerCase();
  return vocabDb[key] ?? null;
}
