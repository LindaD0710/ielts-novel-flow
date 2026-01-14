#!/usr/bin/env python3
"""
词汇覆盖检查工具
检查小说内容是否覆盖了所有核心词汇
"""

import re
import os
import sys
import json
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_STORY_FILE = os.path.join(BASE_DIR, "raw_story.txt")
PROMPT_FILE = os.path.join(BASE_DIR, "current_prompt.txt")
PROJECT_ROOT = os.path.dirname(BASE_DIR)
GENERATED_DIR = os.path.join(PROJECT_ROOT, "src", "data", "generated")


def extract_target_words_from_prompt() -> list:
    """从 prompt 文件中提取核心词汇列表"""
    if not os.path.exists(PROMPT_FILE):
        print(f"❌ 错误：找不到 {PROMPT_FILE}")
        return []
    
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 查找核心词汇部分
    if "## 核心词汇（必须全部使用）" not in content:
        print("❌ 错误：在 prompt 文件中找不到核心词汇部分")
        return []
    
    # 提取核心词汇部分
    vocab_section = content.split("## 核心词汇（必须全部使用）")[1]
    if "## 输出要求" in vocab_section:
        vocab_section = vocab_section.split("## 输出要求")[0]
    elif "## 复习词汇" in vocab_section:
        vocab_section = vocab_section.split("## 复习词汇")[0]
    
    # 提取所有单词（- word 格式）
    words = re.findall(r'-\s*(\w+)', vocab_section)
    target_words = [w.strip().lower() for w in words if w.strip()]
    
    return target_words


def extract_used_words_from_story(story_content: str) -> set:
    """从小说内容中提取所有使用的单词（{word|meaning} 格式）"""
    pattern = r'\{([^|]+)\|'
    matches = re.findall(pattern, story_content)
    used_words = set([m.strip().lower() for m in matches if m.strip()])
    return used_words


def load_story_from_generated(book_id: str) -> str:
    """
    从 src/data/generated/book-xxxx.json 读取章节内容
    """
    filename = f"{book_id}.json" if book_id.endswith(".json") is False else book_id
    path = os.path.join(GENERATED_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到章节文件：{path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "content" not in data:
        raise ValueError(f"章节文件格式不正确（缺少 content）：{path}")
    content = data.get("content", "")
    if not isinstance(content, str):
        raise ValueError(f"章节文件 content 字段不是字符串：{path}")
    return content


def find_latest_generated_book_file() -> str:
    """
    找到 src/data/generated 下最新的 book-*.json
    返回文件名（例如 book-20260112165132.json）
    """
    if not os.path.isdir(GENERATED_DIR):
        raise FileNotFoundError(f"找不到目录：{GENERATED_DIR}")
    candidates = []
    for name in os.listdir(GENERATED_DIR):
        if name.startswith("book-") and name.endswith(".json"):
            path = os.path.join(GENERATED_DIR, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            candidates.append((mtime, name))
    if not candidates:
        raise FileNotFoundError(f"{GENERATED_DIR} 下没有找到 book-*.json 章节文件")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def main():
    print("=" * 60)
    print("📊 词汇覆盖检查工具")
    print("=" * 60)
    print()

    parser = argparse.ArgumentParser(description="检查小说内容是否覆盖 current_prompt.txt 中的核心词汇")
    parser.add_argument("--book-id", type=str, default="", help="书籍ID，例如 book-20260112165132（对应 src/data/generated/book-*.json）")
    parser.add_argument("--latest", action="store_true", help="检查最新生成/上架的那本书（按 src/data/generated/book-*.json 修改时间）")
    parser.add_argument("--raw", action="store_true", help="强制从 tools/raw_story.txt 读取（中转文件）")
    args = parser.parse_args()
    
    # 1. 提取核心词汇
    print("📋 提取核心词汇列表...")
    target_words = extract_target_words_from_prompt()
    
    if not target_words:
        print("❌ 无法提取核心词汇，请检查 current_prompt.txt")
        sys.exit(1)
    
    print(f"✅ 找到 {len(target_words)} 个核心词汇")
    print(f"   示例：{', '.join(target_words[:10])}...")
    
    # 2. 读取小说内容（优先从已上架的 generated 章节文件读取）
    print(f"\n📖 读取小说内容...")
    story_content = ""
    source_hint = ""
    try:
        if args.raw:
            source_hint = RAW_STORY_FILE
            if not os.path.exists(RAW_STORY_FILE):
                raise FileNotFoundError(f"找不到 {RAW_STORY_FILE}")
            with open(RAW_STORY_FILE, "r", encoding="utf-8") as f:
                story_content = f.read().strip()
        elif args.book_id:
            source_hint = f"{args.book_id}.json"
            story_content = load_story_from_generated(args.book_id).strip()
        elif args.latest:
            latest = find_latest_generated_book_file()
            source_hint = latest
            story_content = load_story_from_generated(latest).strip()
        else:
            # 默认：如果 raw_story.txt 有内容就用 raw；否则用 latest
            if os.path.exists(RAW_STORY_FILE):
                with open(RAW_STORY_FILE, "r", encoding="utf-8") as f:
                    tmp = f.read().strip()
                if tmp:
                    source_hint = RAW_STORY_FILE
                    story_content = tmp
            if not story_content:
                latest = find_latest_generated_book_file()
                source_hint = latest
                story_content = load_story_from_generated(latest).strip()
    except Exception as e:
        print(f"❌ 读取小说内容失败：{e}")
        print("💡 你可以用以下任一方式运行：")
        print("   - 检查最新上架：python3 check_vocab_coverage.py --latest")
        print("   - 指定书籍ID：python3 check_vocab_coverage.py --book-id book-20260112165132")
        print("   - 强制用 raw_story：python3 check_vocab_coverage.py --raw")
        sys.exit(1)

    if not story_content:
        print("❌ 小说内容为空，无法检查覆盖率。")
        print(f"   当前来源：{source_hint or '未知'}")
        sys.exit(1)
    
    print(f"✅ 小说内容长度：{len(story_content)} 字符")
    if source_hint:
        print(f"   来源：{source_hint}")
    
    # 3. 提取使用的单词
    print(f"\n🔍 提取小说中使用的单词...")
    used_words = extract_used_words_from_story(story_content)
    print(f"✅ 找到 {len(used_words)} 个标记的单词")
    if used_words:
        print(f"   示例：{', '.join(list(used_words)[:10])}...")
    
    # 4. 检查覆盖情况
    print(f"\n{'='*60}")
    print(f"📊 词汇覆盖检查结果")
    print(f"{'='*60}")
    
    missing_words = []
    for word in target_words:
        if word.lower() not in used_words:
            missing_words.append(word)
    
    used_count = len(target_words) - len(missing_words)
    coverage_percent = (used_count / len(target_words) * 100) if target_words else 0
    
    print(f"📋 核心词汇总数：{len(target_words)} 个")
    print(f"✅ 已使用：{used_count} 个 ({coverage_percent:.1f}%)")
    print(f"❌ 缺失：{len(missing_words)} 个")
    
    if missing_words:
        print(f"\n⚠️  缺失的单词列表：")
        for i, word in enumerate(missing_words, 1):
            print(f"   {i:2d}. {word}")
        print(f"\n💡 建议：请检查小说内容，确保所有核心词汇都已使用")
    else:
        print(f"\n🎉 完美！所有 {len(target_words)} 个核心词汇都已使用！")
    
    # 5. 检查额外单词（不在核心列表中的）
    extra_words = used_words - set([w.lower() for w in target_words])
    if extra_words:
        print(f"\n💡 额外使用的单词（不在核心列表中的）：{len(extra_words)} 个")
        print(f"   {', '.join(list(extra_words)[:15])}")
        if len(extra_words) > 15:
            print(f"   ... 还有 {len(extra_words) - 15} 个")
    
    # 6. 字数统计
    char_count = len(story_content)
    word_count = len(story_content.replace(" ", "").replace("\n", ""))
    print(f"\n📏 字数统计：")
    print(f"   字符数：{char_count}")
    print(f"   估算字数：约 {word_count // 2} 字（中文）")
    
    if word_count < 1400:
        print(f"   ⚠️  字数可能过少（建议 1400-1600 字）")
    elif word_count > 2000:
        print(f"   ⚠️  字数可能过多（建议 1400-1600 字）")
    else:
        print(f"   ✅ 字数符合要求")
    
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
