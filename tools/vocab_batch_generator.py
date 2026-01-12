#!/usr/bin/env python3
"""
IELTS Novel Flow - 词汇批次生成器

功能：从 ielts_source.json 中找出还未录入 vocab_db.json 的单词，
      按批次输出，方便复制粘贴给 ChatGPT/Gemini 生成词汇详情。

使用方法：
    python3 vocab_batch_generator.py [批次大小] [批次编号]
    
示例：
    python3 vocab_batch_generator.py 50        # 输出第一批 50 个未生成的单词
    python3 vocab_batch_generator.py 50 2      # 输出第二批 50 个未生成的单词
"""

import json
import os
import sys
from typing import List, Dict, Any

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SOURCE_FILE = os.path.join(BASE_DIR, "ielts_source.json")
VOCAB_DB_FILE = os.path.join(PROJECT_ROOT, "src", "data", "generated", "vocab_db.json")


def load_source_words() -> List[str]:
    """加载词源列表"""
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ 错误：词源文件不存在：{SOURCE_FILE}")
        sys.exit(1)
    
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print(f"❌ 错误：词源文件必须是字符串数组")
        sys.exit(1)
    
    words = [w.strip() for w in data if isinstance(w, str) and w.strip()]
    return words


def load_vocab_db() -> Dict[str, Any]:
    """加载已有的词汇数据库"""
    if not os.path.exists(VOCAB_DB_FILE):
        return {}
    
    with open(VOCAB_DB_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {}
    
    if not isinstance(data, dict):
        return {}
    
    # 统一转为小写 key
    normalized = {}
    for k, v in data.items():
        if isinstance(k, str):
            normalized[k.lower()] = v
    return normalized


def get_missing_words(source_words: List[str], vocab_db: Dict[str, Any]) -> List[str]:
    """找出还未录入的单词"""
    missing = []
    for word in source_words:
        key = word.lower()
        if key not in vocab_db:
            missing.append(word)
    return missing


def format_words_for_chat(words: List[str], format_type: str = "comma") -> str:
    """
    格式化单词列表，方便复制粘贴给 ChatGPT/Gemini
    
    Args:
        words: 单词列表
        format_type: 格式类型
            - "comma": 逗号分隔（一行）
            - "comma_space": 逗号+空格分隔（一行）
            - "newline": 每行一个单词
            - "numbered": 带编号的列表
    """
    if format_type == "comma":
        return ", ".join(words)
    elif format_type == "comma_space":
        return ", ".join(words)
    elif format_type == "newline":
        return "\n".join(words)
    elif format_type == "numbered":
        return "\n".join([f"{i+1}. {word}" for i, word in enumerate(words)])
    else:
        return ", ".join(words)


def get_next_batch_number(batch_size: int) -> int:
    """
    自动检测下一个批次编号
    通过检查已存在的批次文件，找到最大的编号，然后+1
    """
    import glob
    pattern = os.path.join(BASE_DIR, "vocab_batch_*.json")
    existing_files = glob.glob(pattern)
    
    max_num = 0
    for filepath in existing_files:
        filename = os.path.basename(filepath)
        # 提取编号：vocab_batch_001.json -> 1
        try:
            num_str = filename.replace("vocab_batch_", "").replace(".json", "")
            num = int(num_str)
            if num > max_num:
                max_num = num
        except ValueError:
            continue
    
    return max_num + 1


def main():
    print("=" * 60)
    print("IELTS Novel Flow - 词汇批次生成器")
    print("=" * 60)
    print()
    
    # 解析命令行参数
    batch_size = 50  # 默认每批 50 个
    batch_num = None  # 如果未指定，则自动检测
    
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            print(f"❌ 错误：批次大小必须是数字，你输入的是：{sys.argv[1]}")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            batch_num = int(sys.argv[2])
        except ValueError:
            print(f"❌ 错误：批次编号必须是数字，你输入的是：{sys.argv[2]}")
            sys.exit(1)
    
    # 加载数据
    print("📖 加载词源列表...")
    source_words = load_source_words()
    print(f"✅ 词源总数：{len(source_words)}")
    
    print("\n📚 加载已有词汇库...")
    vocab_db = load_vocab_db()
    print(f"✅ 已录入：{len(vocab_db)} 个单词")
    
    # 找出缺失的单词
    print("\n🔍 查找未录入的单词...")
    missing_words = get_missing_words(source_words, vocab_db)
    print(f"✅ 待生成：{len(missing_words)} 个单词")
    
    if not missing_words:
        print("\n🎉 恭喜！所有单词都已录入，vocab_db.json 已完整。")
        return
    
    # 计算实际批次（基于待生成的单词）
    total_batches = (len(missing_words) + batch_size - 1) // batch_size
    
    # 如果未指定批次编号，自动检测下一个文件编号
    if batch_num is None:
        file_batch_num = get_next_batch_number(batch_size)
        print(f"\n💡 自动检测：下一个文件编号为 {file_batch_num}")
        # 批次内容从第1批开始（基于待生成的单词）
        content_batch_num = 1
    else:
        # 用户指定了批次编号，用于文件命名
        file_batch_num = batch_num
        # 计算这是第几个"待生成批次"
        # 如果用户之前已经导入了很多批次，我们需要计算这是第几个待生成的批次
        # 简单方式：假设用户想从第1个待生成的批次开始
        content_batch_num = 1
        print(f"\n💡 使用文件编号：{file_batch_num}，内容批次：{content_batch_num}")
    
    # 计算批次内容（基于待生成的单词，从第1批开始）
    start_idx = (content_batch_num - 1) * batch_size
    end_idx = min(start_idx + batch_size, len(missing_words))
    
    if start_idx >= len(missing_words):
        print(f"\n❌ 错误：没有更多待生成的单词了（总共只有 {total_batches} 批）")
        return
    
    # 使用文件编号用于显示和文件命名
    batch_num = file_batch_num
    
    batch_words = missing_words[start_idx:end_idx]
    
    print(f"\n📦 文件编号：vocab_batch_{batch_num:03d}.json")
    print(f"   内容批次：第 {content_batch_num} 批 / 共 {total_batches} 批（基于待生成的单词）")
    print(f"   单词范围：第 {start_idx + 1} - {end_idx} 个（共 {len(batch_words)} 个）")
    print()
    print("=" * 60)
    print("📋 单词列表（可直接复制给 ChatGPT/Gemini）：")
    print("=" * 60)
    print()
    
    # 输出格式1：逗号分隔（最常用）
    print("【格式1：逗号分隔（推荐）】")
    print(format_words_for_chat(batch_words, "comma"))
    print()
    
    # 输出格式2：每行一个（备用）
    print("=" * 60)
    print("【格式2：每行一个（备用）】")
    print(format_words_for_chat(batch_words, "newline"))
    print()
    
    print("=" * 60)
    print("\n💡 使用提示：")
    print(f"   1. 复制上面的单词列表（推荐用格式1）")
    print(f"   2. 在 ChatGPT/Gemini 中生成词汇详情 JSON")
    print(f"   3. 保存为文件：vocab_batch_{batch_num:03d}.json")
    print(f"   4. 运行：python3 vocab_manual_import.py vocab_batch_{batch_num:03d}.json")
    print()
    if content_batch_num < total_batches:
        next_file_num = batch_num + 1
        print(f"   5. 生成下一批（自动编号）：python3 vocab_batch_generator.py {batch_size}")
        print(f"      下一批文件将保存为：vocab_batch_{next_file_num:03d}.json")
        print(f"      （还有 {total_batches - content_batch_num} 批待生成）")
    else:
        print(f"   ✅ 这是最后一批了！所有待生成的单词都已完成。")
    print()


if __name__ == "__main__":
    main()

