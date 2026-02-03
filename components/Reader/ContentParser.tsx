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
  type: "text" | "word" | "bold";
  content: string;
  word?: string;
  meaning?: string;
}

/**
 * 解析文本中的单词标记（不包含粗体标记）
 * @param content 原始内容字符串
 * @returns 解析后的片段数组
 */
function parseWordsOnly(content: string): ParsedSegment[] {
  const segments: ParsedSegment[] = [];
  const wordRegex = /\{([^|]+)\|([^}]+)\}/g;
  let lastIndex = 0;
  let match;

  while ((match = wordRegex.exec(content)) !== null) {
    // 添加匹配前的普通文本
    if (match.index > lastIndex) {
      segments.push({
        type: "text",
        content: content.slice(lastIndex, match.index),
      });
    }

    // 添加匹配到的单词
    segments.push({
      type: "word",
      word: match[1].trim(),
      meaning: match[2].trim(),
      content: match[0],
    });

    lastIndex = wordRegex.lastIndex;
  }

  // 添加剩余的普通文本
  if (lastIndex < content.length) {
    segments.push({
      type: "text",
      content: content.slice(lastIndex),
    });
  }

  return segments;
}

/**
 * 解析章节内容，识别 {word|meaning} 格式和 **text** 粗体格式
 * @param content 原始内容字符串
 * @returns 解析后的片段数组
 */
function parseContent(content: string): ParsedSegment[] {
  const segments: ParsedSegment[] = [];
  // 先匹配粗体标记 **text**，然后再处理单词标记
  // 这样可以避免粗体标记被单词标记的正则干扰
  const boldRegex = /\*\*([^*]+)\*\*/g;
  const wordRegex = /\{([^|]+)\|([^}]+)\}/g;
  
  // 先找出所有粗体标记的位置
  const boldMatches: Array<{start: number, end: number, text: string}> = [];
  let boldMatch;
  while ((boldMatch = boldRegex.exec(content)) !== null) {
    boldMatches.push({
      start: boldMatch.index,
      end: boldMatch.index + boldMatch[0].length,
      text: boldMatch[1].trim(),
    });
  }
  
  // 找出所有单词标记的位置
  const wordMatches: Array<{start: number, end: number, word: string, meaning: string}> = [];
  let wordMatch;
  while ((wordMatch = wordRegex.exec(content)) !== null) {
    wordMatches.push({
      start: wordMatch.index,
      end: wordMatch.index + wordMatch[0].length,
      word: wordMatch[1].trim(),
      meaning: wordMatch[2].trim(),
    });
  }
  
  // 合并所有标记并按位置排序
  const allMatches: Array<{
    start: number;
    end: number;
    type: "bold" | "word";
    text?: string;
    word?: string;
    meaning?: string;
  }> = [
    ...boldMatches.map(m => ({ ...m, type: "bold" as const, text: m.text })),
    ...wordMatches.map(m => ({ ...m, type: "word" as const, word: m.word, meaning: m.meaning })),
  ].sort((a, b) => a.start - b.start);
  
  let lastIndex = 0;
  
  for (const match of allMatches) {
    // 添加匹配前的普通文本
    if (match.start > lastIndex) {
      segments.push({
        type: "text",
        content: content.slice(lastIndex, match.start),
      });
    }
    
    // 添加匹配到的标记
    if (match.type === "bold") {
      segments.push({
        type: "bold",
        content: match.text!,
      });
    } else {
      segments.push({
        type: "word",
        word: match.word!,
        meaning: match.meaning!,
        content: content.slice(match.start, match.end),
      });
    }
    
    lastIndex = match.end;
  }
  
  // 添加剩余的普通文本
  if (lastIndex < content.length) {
    segments.push({
      type: "text",
      content: content.slice(lastIndex),
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

        if (segment.type === "bold") {
          // 粗体文本：使用 strong 标签并应用粗体样式
          // 粗体文本内部可能也包含单词标记，需要解析（但不解析粗体标记）
          const boldContent = segment.content;
          const innerSegments = parseWordsOnly(boldContent);
          
          return (
            <strong key={index} className="font-bold text-slate-200">
              {innerSegments.map((innerSegment, innerIndex) => {
                if (innerSegment.type === "text") {
                  return (
                    <span key={innerIndex}>{innerSegment.content}</span>
                  );
                }
                // 粗体内部的单词标记
                return (
                  <span
                    key={innerIndex}
                    onClick={(e) => {
                      e.stopPropagation();
                      onWordClick(innerSegment.word!, innerSegment.meaning);
                    }}
                    className="inline-flex items-baseline gap-1.5 cursor-pointer group"
                  >
                    <span className="font-serif text-cyan-400 glow-cyan underline decoration-cyan-400/50 decoration-2 underline-offset-2 hover:text-cyan-300 hover:glow-cyan transition-all duration-200">
                      {innerSegment.word}
                    </span>
                    <span className="text-xs text-purple-300/70 group-hover:text-purple-300 group-hover:opacity-100 transition-all duration-200">
                      ({innerSegment.meaning})
                    </span>
                  </span>
                );
              })}
            </strong>
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

