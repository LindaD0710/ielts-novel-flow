/**
 * 词汇数据结构
 * 用于存储雅思核心单词的完整信息
 */
export interface Vocabulary {
  /** 英文单词 */
  word: string;
  /** 简明中文释义 */
  meaning: string;
  /** 音标（国际音标格式） */
  phonetic: string;
  /** 词根或助记方法 */
  root: string;
  /** 英文例句 */
  example: string;
  /** 例句的中文翻译 */
  exampleCn: string;
}

/**
 * 章节数据结构
 * 包含章节的基本信息和内容
 */
export interface Chapter {
  /** 章节唯一标识 */
  id: string;
  /** 章节标题 */
  title: string;
  /**
   * 章节正文内容
   * 
   * 关键格式说明：
   * - 内容为长字符串，其中雅思单词使用特殊标记格式：{word|meaning}
   * - 例如：她感到非常 {ambitious|有野心}，决定要...
   * - 这种格式用于在中文文本中无缝嵌入英文单词及其释义
   * - 解析时需要识别并提取这些标记，转换为可交互的单词元素
   */
  content: string;
}

/**
 * 书籍数据结构
 * 包含整本小说的元信息和章节列表
 */
export interface Book {
  /** 书籍唯一标识 */
  id: string;
  /** 书籍标题 */
  title: string;
  /** 作者 */
  author: string;
  /** 封面主题色（用于UI设计） */
  coverColor: string;
  /** 章节列表 */
  chapters: Chapter[];
}


