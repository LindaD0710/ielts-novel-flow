#!/usr/bin/env python3
"""
IELTS Novel Flow - 词汇详情生成器

读取雅思核心词源列表，调用 OpenAI/DeepSeek 接口，为每个新单词生成
符合前端 Vocabulary 接口的详细信息，并更新 vocab_db.json。

Vocabulary 接口字段：
- word: 单词原形
- meaning: 简明中文释义
- phonetic: 美式音标 (如 /æmˈbɪʃ.əs/)
- root: 词根助记 (如 "ambi(周围) + it(走) -> 野心勃勃")
- example: 简短英文例句
- exampleCn: 例句中文翻译
"""

import json
import os
import sys
from typing import Dict, Any, List

from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from openai import OpenAI

# ============== 配置 ==============

API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # DeepSeek: "https://api.deepseek.com/v1"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # DeepSeek: "deepseek-chat"

# 默认路径：
# - 词源：tools/ielts_source.json
# - 词库数据库：src/data/generated/vocab_db.json（前端直接读取的文件）
SOURCE_PATH = os.getenv("IELTS_SOURCE_PATH", "ielts_source.json")
DB_PATH = os.getenv("VOCAB_DB_PATH", os.path.join("..", "src", "data", "generated", "vocab_db.json"))


SYSTEM_PROMPT = """你是一名专业的英语词汇学专家和雅思教师，擅长用简洁、准确的方式解释单词，同时懂得如何设计适合中国学生的例句和词根助记。

你的任务是：
- 针对给定的英文单词，生成详细的词汇信息
- 输出必须是**严格的 JSON 对象**，不能包含任何多余文字

字段要求（所有字段必填）：
- word: 单词原形（保持输入形式）
- meaning: 简明中文释义（不超过 12 个汉字，口语化、易懂）
- phonetic: 美式音标，包含斜杠，例如 "/æmˈbɪʃ.əs/"
- root: 词根助记，简要说明构词关系，可以适当拟人，但要简洁
- example: 简短的英文例句，语气自然，难度约为雅思 6.5-7.5，长度控制在 1 句话
- exampleCn: 例句的自然中文翻译

输出格式：
- 只输出一个 JSON 对象，如：
{
  "word": "ambitious",
  "meaning": "有野心的",
  "phonetic": "/æmˈbɪʃ.əs/",
  "root": "ambi(周围) + it(走) -> 目标很多，野心勃勃",
  "example": "She is ambitious and works hard to achieve her goals.",
  "exampleCn": "她很有野心，并且努力实现自己的目标。"
}

禁止输出任何解释性文字、前后缀说明或 Markdown，只能输出 JSON。"""


def load_source_words(path: str) -> List[str]:
    """加载词源列表（JSON 数组）"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"词源文件不存在: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("词源文件必须是字符串数组，例如 [\"ambitious\", ...]")

    words: List[str] = []
    for item in data:
        if isinstance(item, str):
            w = item.strip()
            if w:
                words.append(w)
    return words


def load_vocab_db(path: str) -> Dict[str, Any]:
    """加载已有的词汇数据库（如果不存在则返回空字典）"""
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"警告：{path} 解析失败，将从空数据库开始", file=sys.stderr)
            return {}

    if not isinstance(data, dict):
        print(f"警告：{path} 不是字典结构，将从空数据库开始", file=sys.stderr)
        return {}

    # 统一转为小写 key
    normalized: Dict[str, Any] = {}
    for k, v in data.items():
        if isinstance(k, str):
            normalized[k.lower()] = v
    return normalized


def save_vocab_db(db: Dict[str, Any], path: str) -> None:
    """保存词汇数据库为 JSON 文件"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"✅ 词汇数据库已更新：{path}")


def build_enrich_prompt(word: str) -> str:
    """构建用户提示词，要求返回单词的详细信息"""
    return f"""请为下面这个雅思核心词汇生成详细信息：

单词：{word}

请按照 System Prompt 中的字段要求，只返回一个 JSON 对象。"""


def enrich_single_word(client: OpenAI, word: str) -> Dict[str, Any]:
    """调用 LLM，为单个单词生成 Vocabulary 详情。

    返回的 dict 必须包含：word, meaning, phonetic, root, example, exampleCn
    """
    user_prompt = build_enrich_prompt(word)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
        max_tokens=400,
    )

    content = resp.choices[0].message.content.strip()

    # 为了安全，尝试只截取 JSON 对象部分
    first_brace = content.find("{")
    last_brace = content.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        content = content[first_brace : last_brace + 1]

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM 返回的内容不是合法 JSON: {content}") from e

    # 基本字段校验
    required_fields = ["word", "meaning", "phonetic", "root", "example", "exampleCn"]
    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"字段缺失或无效: {field} in {data}")

    # 规范化 word
    data["word"] = data["word"].strip()

    return data


def main() -> None:
    print("=" * 60)
    print("IELTS Novel Flow - 词汇详情生成器")
    print("=" * 60)

    # 加载词源
    try:
        source_words = load_source_words(SOURCE_PATH)
    except Exception as e:
        print(f"❌ 无法加载词源: {e}")
        sys.exit(1)

    # 加载已有数据库
    vocab_db = load_vocab_db(DB_PATH)

    # 计算需要补充的单词（按小写去重）
    missing_words: List[str] = []
    for w in source_words:
        key = w.lower()
        if key not in vocab_db:
            if key not in missing_words:
                missing_words.append(w)

    print(f"总词数: {len(source_words)}，已存在: {len(vocab_db)}，待生成: {len(missing_words)}")

    if not missing_words:
        print("✅ 没有需要补充的新单词，vocab_db.json 已是最新。")
        return

    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # 逐个生成（考虑成本与控制力，暂不批量）
    success_count = 0
    fail_count = 0

    for idx, word in enumerate(missing_words, start=1):
        key = word.lower()
        print("-" * 60)
        print(f"[{idx}/{len(missing_words)}] 生成单词: {word} (key={key})")

        try:
            vocab = enrich_single_word(client, word)
        except Exception as e:
            fail_count += 1
            print(f"❌ 生成失败: {e}", file=sys.stderr)
            continue

        vocab_db[key] = vocab
        success_count += 1
        print(f"✅ 已生成: {vocab['word']} - {vocab['meaning']}")

        # 可选：每生成若干个就保存一次，防止中断丢失
        if success_count % 5 == 0:
            save_vocab_db(vocab_db, DB_PATH)

    # 最终保存
    save_vocab_db(vocab_db, DB_PATH)

    print("=" * 60)
    print("任务完成")
    print(f"成功: {success_count} 个，失败: {fail_count} 个")
    print(f"数据库位置: {DB_PATH}")


if __name__ == "__main__":
    main()
