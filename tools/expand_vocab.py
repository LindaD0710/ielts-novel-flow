#!/usr/bin/env python3
"""
词库扩充工具

功能：将文本格式的词库文件导入到 ielts_source.json
"""

import json
import os
import sys
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IELTS_SOURCE_FILE = os.path.join(BASE_DIR, "ielts_source.json")


def load_existing_words() -> List[str]:
    """加载现有词库"""
    if not os.path.exists(IELTS_SOURCE_FILE):
        return []
    
    try:
        with open(IELTS_SOURCE_FILE, 'r', encoding='utf-8') as f:
            words = json.load(f)
        return words if isinstance(words, list) else []
    except:
        return []


def load_words_from_text_file(text_file: str) -> List[str]:
    """从文本文件读取单词（每行一个）"""
    words = []
    with open(text_file, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip().lower()
            if word and word.isalpha():  # 只保留字母单词
                words.append(word)
    return words


def expand_vocab_from_text(text_file: str):
    """从文本文件扩充词库"""
    print("=" * 60)
    print("📚 词库扩充工具")
    print("=" * 60)
    print()
    
    # 加载现有词库
    existing_words = load_existing_words()
    print(f"📊 当前词库：{len(existing_words)} 个单词")
    
    # 读取新单词
    if not os.path.exists(text_file):
        print(f"❌ 错误：文件不存在：{text_file}")
        sys.exit(1)
    
    print(f"📖 读取文件：{text_file}")
    new_words = load_words_from_text_file(text_file)
    print(f"📊 新单词：{len(new_words)} 个")
    
    # 合并并去重
    all_words = list(set(existing_words + new_words))
    all_words.sort()  # 排序
    
    # 保存
    with open(IELTS_SOURCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print("✅ 扩充完成！")
    print("=" * 60)
    print(f"扩充前：{len(existing_words)} 个")
    print(f"新增：{len(new_words)} 个")
    print(f"扩充后：{len(all_words)} 个（去重后）")
    print(f"目标：4000 个")
    
    if len(all_words) >= 4000:
        print("✅ 已达到目标！")
    else:
        print(f"⚠️  还需 {4000 - len(all_words)} 个单词")
    print("=" * 60)


def expand_vocab_manually(words: List[str]):
    """手动添加单词列表"""
    print("=" * 60)
    print("📚 词库扩充工具（手动添加）")
    print("=" * 60)
    print()
    
    # 加载现有词库
    existing_words = load_existing_words()
    print(f"📊 当前词库：{len(existing_words)} 个单词")
    
    # 处理新单词
    new_words = [w.strip().lower() for w in words if w.strip() and w.strip().isalpha()]
    print(f"📊 新增单词：{len(new_words)} 个")
    
    # 合并并去重
    all_words = list(set(existing_words + new_words))
    all_words.sort()
    
    # 保存
    with open(IELTS_SOURCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print("✅ 扩充完成！")
    print("=" * 60)
    print(f"扩充前：{len(existing_words)} 个")
    print(f"新增：{len(new_words)} 个")
    print(f"扩充后：{len(all_words)} 个（去重后）")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：")
        print("  python3 expand_vocab.py <text_file>")
        print("")
        print("说明：")
        print("  text_file: 文本文件，每行一个单词")
        print("")
        print("示例：")
        print("  python3 expand_vocab.py vocab_list.txt")
        sys.exit(1)
    
    text_file = sys.argv[1]
    expand_vocab_from_text(text_file)

