"use client";

import React from "react";

interface ContentParserProps {
  /** 章节内容字符串，包含 {word|meaning} 格式的标记 */
  content: string;
  /**
   * 点击单词时的回调函数
   * 第二个参数会把标记里的中文释义一并传出，便于兜底展示
   */
  onWordClick: (word: string, meaning?: string) => void;
}

interface ParsedSegment {
  type: "text" | "word";
  content: string;
  word?: string;
  meaning?: string;
}

/**
 * 解析章节内容，识别 {word|meaning} 格式
 * 同时删除 **text** 格式的粗体标记（当它们出现在单词标记之前时）
 * @param content 原始内容字符串
 * @returns 解析后的片段数组
 */
function parseContent(content: string): ParsedSegment[] {
  // 先删除 **text** 格式的粗体标记（当它们紧跟在单词标记之前时）
  // 匹配模式：**text** {word|meaning} 或 **text** `{word|meaning}`
  // 删除 **text** 部分，只保留后面的单词标记
  let cleanedContent = content;
  
  // 匹配 **text** 后面跟着 {word|meaning} 或 `{word|meaning}` 的模式
  // 允许中间有空白字符、反引号等
  cleanedContent = cleanedContent.replace(/\*\*([^*]+)\*\*\s*`?\{([^|]+)\|([^}]+)\}`?/g, (match, boldText, word, meaning) => {
    // 如果粗体文本和释义相同，则删除粗体部分，只保留单词标记
    if (boldText.trim() === meaning.trim()) {
      return `{${word}|${meaning}}`;
    }
    // 否则保留原样（虽然这种情况应该很少）
    return match;
  });
  
  // 也处理没有反引号的情况：**text** {word|meaning}
  cleanedContent = cleanedContent.replace(/\*\*([^*]+)\*\*\s*\{([^|]+)\|([^}]+)\}/g, (match, boldText, word, meaning) => {
    if (boldText.trim() === meaning.trim()) {
      return `{${word}|${meaning}}`;
    }
    return match;
  });
  
  // 如果还有单独的 **text** 标记（后面没有单词标记），也删除它们
  cleanedContent = cleanedContent.replace(/\*\*([^*]+)\*\*/g, '');
  
  const segments: ParsedSegment[] = [];
  // 正则表达式：匹配 {word|meaning} 格式
  // \{ 匹配左花括号，[^|]+ 匹配单词（不包含 |），\| 匹配分隔符，[^}]+ 匹配释义（不包含 }），\} 匹配右花括号
  const regex = /\{([^|]+)\|([^}]+)\}/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(cleanedContent)) !== null) {
    // 添加匹配前的普通文本
    if (match.index > lastIndex) {
      segments.push({
        type: "text",
        content: cleanedContent.slice(lastIndex, match.index),
      });
    }

    // 添加匹配到的单词
    segments.push({
      type: "word",
      word: match[1].trim(),
      meaning: match[2].trim(),
      content: match[0], // 保留原始格式用于调试
    });

    lastIndex = regex.lastIndex;
  }

  // 添加剩余的普通文本
  if (lastIndex < cleanedContent.length) {
    segments.push({
      type: "text",
      content: cleanedContent.slice(lastIndex),
    });
  }

  return segments;
}

/**
 * 内容解析器组件
 * 解析并渲染包含雅思单词标记的小说内容
 */
export default function ContentParser({
  content,
  onWordClick,
}: ContentParserProps) {
  const segments = parseContent(content);

  return (
    <div className="leading-relaxed whitespace-pre-wrap text-slate-300">
      {segments.map((segment, index) => {
        if (segment.type === "text") {
          return (
            <span key={index} className="text-slate-300">
              {segment.content}
            </span>
          );
        }

        // 单词组件：荧光紫/青色、发光效果、带中文提示
        return (
          <span
            key={index}
            onClick={() => onWordClick(segment.word!, segment.meaning)}
            className="inline-flex items-baseline gap-1.5 cursor-pointer group"
          >
            <span className="font-serif text-cyan-400 glow-cyan underline decoration-cyan-400/50 decoration-2 underline-offset-2 hover:text-cyan-300 hover:glow-cyan transition-all duration-200">
              {segment.word}
            </span>
            <span className="text-xs text-purple-300/70 group-hover:text-purple-300 group-hover:opacity-100 transition-all duration-200">
              ({segment.meaning})
            </span>
          </span>
        );
      })}
    </div>
  );
}

