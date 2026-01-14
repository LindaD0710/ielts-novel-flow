#!/usr/bin/env python3
"""
IELTS Novel Flow - 全库词汇覆盖率检查

需求：
检查“已上架的全部小说（src/data/generated/book-*.json）”中出现的英文单词，
是否覆盖了 IELTS 核心词库（tools/ielts_source.json）。

统计口径：
- 从每本书的章节 JSON（book-*.json）的 content 字段中提取 {word|meaning} 的 word
- word 统一 lower + strip
- 与 ielts_source.json（字符串数组）做对比

输出：
- 总书籍数、总标记次数、去重后的已覆盖词数
- 覆盖率（覆盖词数 / 词库总数）
- 缺失词数量，并将缺失词写入 tools/missing_ielts_words.txt
- 同时写入 tools/coverage_summary.json（便于留档）

用法：
  cd tools
  python3 check_library_vocab_coverage.py
"""

import json
import os
import re
import sys
from typing import Dict, List, Set, Tuple


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

IELTS_SOURCE_PATH = os.path.join(BASE_DIR, "ielts_source.json")
GENERATED_DIR = os.path.join(PROJECT_ROOT, "src", "data", "generated")

OUT_MISSING_TXT = os.path.join(BASE_DIR, "missing_ielts_words.txt")
OUT_SUMMARY_JSON = os.path.join(BASE_DIR, "coverage_summary.json")


WORD_MARK_PATTERN = re.compile(r"\{([^|{}]+)\|([^}]+)\}")


def load_ielts_source_words(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"找不到 IELTS 词库文件：{path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("ielts_source.json 必须是字符串数组")
    words: List[str] = []
    for item in data:
        if isinstance(item, str):
            w = item.strip()
            if w:
                words.append(w)
    return words


def list_generated_books(dir_path: str) -> List[str]:
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"找不到章节生成目录：{dir_path}")
    files = []
    for name in os.listdir(dir_path):
        if name.startswith("book-") and name.endswith(".json"):
            files.append(os.path.join(dir_path, name))
    # 按修改时间排序（旧->新）
    files.sort(key=lambda p: os.path.getmtime(p))
    return files


def extract_words_from_content(content: str) -> Tuple[Set[str], int]:
    """
    Returns: (unique_words_in_content, total_mark_count)
    """
    unique: Set[str] = set()
    total_marks = 0
    for m in WORD_MARK_PATTERN.finditer(content):
        total_marks += 1
        w = m.group(1).strip().lower()
        if w:
            unique.add(w)
    return unique, total_marks


def load_book_content(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"章节文件不是对象：{path}")
    content = data.get("content", "")
    if not isinstance(content, str):
        raise ValueError(f"章节文件 content 不是字符串：{path}")
    return content


def main() -> None:
    print("=" * 60)
    print("📚 全库词汇覆盖率检查（已上架小说 vs IELTS 核心词库）")
    print("=" * 60)

    try:
        source_words = load_ielts_source_words(IELTS_SOURCE_PATH)
        source_set = set([w.lower() for w in source_words])
    except Exception as e:
        print(f"❌ 无法加载 IELTS 词库：{e}")
        sys.exit(1)

    try:
        book_files = list_generated_books(GENERATED_DIR)
    except Exception as e:
        print(f"❌ 无法读取已上架书籍：{e}")
        sys.exit(1)

    if not book_files:
        print("⚠️  src/data/generated 下没有 book-*.json，当前没有可检查的上架小说。")
        sys.exit(0)

    covered_words: Set[str] = set()
    total_marks_all = 0
    per_book: List[Dict[str, int]] = []

    for path in book_files:
        try:
            content = load_book_content(path)
            uniq, marks = extract_words_from_content(content)
            total_marks_all += marks
            covered_words |= uniq
            per_book.append(
                {
                    "file": os.path.basename(path),
                    "unique_words": len(uniq),
                    "marks": marks,
                }
            )
        except Exception as e:
            print(f"⚠️  跳过文件（解析失败）：{os.path.basename(path)} -> {e}")

    covered_in_source = covered_words & source_set
    missing = sorted(list(source_set - covered_in_source))

    total_source = len(source_set)
    covered_count = len(covered_in_source)
    coverage_pct = (covered_count / total_source * 100) if total_source else 0.0

    print(f"\n📦 已上架书籍数：{len(book_files)}")
    print(f"🔖 总标记次数（{ '{word|meaning}' }）：{total_marks_all}")
    print(f"✅ 去重后已出现英文词：{len(covered_words)}")
    print(f"🎯 命中 IELTS 核心词：{covered_count} / {total_source}（{coverage_pct:.2f}%）")
    print(f"❌ IELTS 核心词缺失：{len(missing)}")

    # 写缺失词清单（便于后续补漏）
    try:
        with open(OUT_MISSING_TXT, "w", encoding="utf-8") as f:
            for w in missing:
                f.write(w + "\n")
        print(f"\n📝 缺失词清单已写入：{OUT_MISSING_TXT}")
    except Exception as e:
        print(f"⚠️  无法写入缺失词文件：{e}")

    # 写摘要 JSON（留档）
    try:
        summary = {
            "source_total": total_source,
            "books_total": len(book_files),
            "total_marks": total_marks_all,
            "covered_unique_total": len(covered_words),
            "covered_in_source": covered_count,
            "coverage_percent": round(coverage_pct, 4),
            "missing_count": len(missing),
            "missing_words_file": os.path.basename(OUT_MISSING_TXT),
            "per_book": per_book,
        }
        with open(OUT_SUMMARY_JSON, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"🧾 覆盖率摘要已写入：{OUT_SUMMARY_JSON}")
    except Exception as e:
        print(f"⚠️  无法写入摘要文件：{e}")

    # 高信号提示：如果没满，给出下一步建议
    if missing:
        print("\n下一步建议：")
        print("- 你可以把 missing_ielts_words.txt 按批次喂给模型，生成新的小说或补写短段落来覆盖缺失词。")
        print("- 或者在 step1 选词阶段，优先从缺失词里抽取，确保每篇都在补漏。")


if __name__ == "__main__":
    main()

