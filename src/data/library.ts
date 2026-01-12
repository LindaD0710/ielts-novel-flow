import { Book } from "@/types";

/**
 * 书籍分类配置
 */
export const bookCategories = [
  { id: "reborn", name: "重生", color: "#8B5CF6" },
  { id: "suspense", name: "悬疑", color: "#06B6D4" },
  { id: "romance", name: "言情", color: "#EC4899" },
  { id: "business", name: "商战", color: "#10B981" },
] as const;

/**
 * 默认分类（重生）
 */
export const DEFAULT_CATEGORY_ID = "reborn";

/**
 * 扩展书籍类型（添加分类字段）
 */
export interface BookWithCategory extends Book {
  category: string; // 分类 ID，对应 bookCategories 的 id
}

/**
 * 书架 Mock 数据
 * 包含不同分类的小说列表
 * 
 * 注意：正式生产的小说将通过 step2_save_chapter.py 自动添加到这里
 */
export const libraryBooks: BookWithCategory[] = [
  // 正式生产的小说将自动添加到这里
  {
    id: "book-20260113030011",
    title: "重生后，我绑定了“反派演技系统”",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113030536",
    title: "重生后，我给豪门安了监控",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113030951",
    title: "贤妻重生，在离婚直播里普法",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113031320",
    title: "重生在选秀淘汰夜",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113031750",
    title: "我重生回了闺蜜的婚礼",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113032419",
    title: "重生后，我不争了",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113033126",
    title: "婚礼重生，逆转未来",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113033446",
    title: "重生后绑定【反派救赎系统】",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113034204",
    title: "重生在顶流塌房夜",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113034530",
    title: "重生之我有全行业黑名单",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113035126",
    title: "记忆拍卖行",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113035348",
    title: "重生在自杀干预热线",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113035820",
    title: "我重生在金融诈骗现场",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113040035",
    title: "重生后专治“道德绑架”",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113065513",
    title: "我成了疯批反派的“镇定剂”",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113065730",
    title: "重生后我签下死对头的卖身契",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113070329",
    title: "重生后我和影帝互换了心跳",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113070541",
    title: "重生后我发现影帝是我榜一",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113070917",
    title: "影帝的手机锁屏是我",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113071334",
    title: "重生后我发现甲方是我老公",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113071602",
    title: "重生后我和死对头合伙人结婚了",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113071756",
    title: "我发现老板的屏保是我毕业照",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113071956",
    title: "重生后我发现邻居在画我",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113072209",
    title: "咖啡师每天给我的杯底写暗号",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113072527",
    title: "我重生在学术打假现场",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113072736",
    title: "全网嘲我傍金主，金主发来结婚证",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113073001",
    title: "全网赌我什么时候被甩，他押了永远",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113073349",
    title: "我听见了死对头的心声",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113073610",
    title: "听见顶流在脑内打榜",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113073842",
    title: "我的合租室友是心口不一患者",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113074059",
    title: "首富在深夜搜索“如何和喜欢的女孩说话”",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
  {
    id: "book-20260113074318",
    title: "我的房东是隐形富豪",
    author: "半夏",
    coverColor: "#8B5CF6",
    category: "reborn",
    chapters: [],
  },
];

/**
 * 根据 bookId 获取书籍信息
 */
export function getBookById(bookId: string): BookWithCategory | null {
  return libraryBooks.find((book) => book.id === bookId) ?? null;
}

/**
 * 根据分类 ID 获取该分类下的所有书籍
 */
export function getBooksByCategory(categoryId: string): BookWithCategory[] {
  return libraryBooks.filter((book) => book.category === categoryId);
}


