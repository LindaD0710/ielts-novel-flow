#!/usr/bin/env python3
"""
IELTS Novel Flow - 词汇手动导入工具（配合 ChatGPT / Gemini 网页会员使用）

使用场景：
 你不用任何 API，只在浏览器里用 ChatGPT / Gemini 生成词汇信息，
 然后把模型返回的 JSON 保存到一个文件里，本脚本负责把这些结果
 合并进项目使用的 vocab_db.json。

使用步骤（推荐流程）：

1. 在浏览器中打开 ChatGPT 或 Gemini，对它发送类似这样的提示词：

   （系统 / 第一条）
   你是一名专业的英语词汇学专家和雅思教师，擅长用简洁、准确的方式解释单词，
   同时懂得如何设计适合中国学生的例句和词根助记。
   请严格按照我给的 JSON 模板返回，不要输出任何额外解释或 Markdown。

   （用户）
   请为下面这些单词生成详细词汇信息。返回一个 JSON 对象，key 是小写单词，
   value 是一个对象，字段为：
   - word: 单词原形
   - meaning: 简明中文释义（不超过 12 个汉字）
   - phonetic: 美式音标，带斜杠，如 "/æmˈbɪʃ.əs/"
   - root: 词根助记，简短中文说明
   - example: 简短英文例句（1 句）
   - exampleCn: 例句中文翻译

   请严格返回如下格式的 JSON（示例）：
   {
     "ambitious": {
       "word": "ambitious",
       "meaning": "有野心的",
       "phonetic": "/æmˈbɪʃ.əs/",
       "root": "ambi(周围)+it(走)->目标很多，野心勃勃",
       "example": "She is ambitious and works hard to achieve her goals.",
       "exampleCn": "她很有野心，并且努力实现自己的目标。"
     },
     "consistent": {
       "word": "consistent",
       "meaning": "一贯的；始终如一的",
       "phonetic": "/kənˈsɪstənt/",
       "root": "con(一起)+sist(站)->立场始终站在一起",
       "example": "Her performance has been consistent this year.",
       "exampleCn": "她今年的表现一直很稳定。"
     }
   }

   下面是本批次的单词列表：
   ambitious, consistent, ...

2. 得到模型的 JSON 回复后，复制整段 JSON（从 { 到 }），保存为一个文件，例如：

   tools/vocab_batch_001.json

3. 在命令行运行本脚本，将该批次合并进项目的词汇库：

   cd tools
   python3 vocab_manual_import.py vocab_batch_001.json

4. 脚本会自动：
   - 读取 src/data/generated/vocab_db.json（如果不存在则新建）
   - 合并本批次 JSON（按小写单词去重）
   - 保存回 src/data/generated/vocab_db.json
   - 打印本次新增 / 覆盖的词数
"""

import json
import os
import sys
from typing import Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_DB_PATH = os.path.join(PROJECT_ROOT, "src", "data", "generated", "vocab_db.json")


def load_vocab_db(path: str) -> Dict[str, Any]:
  """加载现有词库（如果不存在则返回空字典）"""
  if not os.path.exists(path):
    return {}

  with open(path, "r", encoding="utf-8") as f:
    try:
      data = json.load(f)
    except json.JSONDecodeError:
      print(f"⚠️  警告：{path} 解析失败，将从空词库开始", file=sys.stderr)
      return {}

  if not isinstance(data, dict):
    print(f"⚠️  警告：{path} 不是字典结构，将从空词库开始", file=sys.stderr)
    return {}

  # key 统一转为小写
  normalized: Dict[str, Any] = {}
  for k, v in data.items():
    if isinstance(k, str):
      normalized[k.lower()] = v
  return normalized


def load_batch(path: str) -> Dict[str, Any]:
  """加载单次从 ChatGPT / Gemini 拷贝下来的 JSON 批次"""
  if not os.path.exists(path):
    raise FileNotFoundError(f"找不到批次文件：{path}")

  with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

  if not isinstance(data, dict):
    raise ValueError("批次文件必须是一个 JSON 对象，例如 {\"word\": {...}, ...}")

  normalized: Dict[str, Any] = {}
  for k, v in data.items():
    if not isinstance(k, str):
      continue
    key = k.strip().lower()
    if not key:
      continue
    if not isinstance(v, dict):
      raise ValueError(f"单词 {k} 的值必须是对象，如 {{\"word\": \"...\", ...}}")
    normalized[key] = v

  return normalized


def save_vocab_db(db: Dict[str, Any], path: str) -> None:
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
  print(f"✅ 词汇库已保存：{path}")


def merge_batch(db: Dict[str, Any], batch: Dict[str, Any]) -> None:
  added = 0
  updated = 0

  for key, value in batch.items():
    if key in db:
      updated += 1
    else:
      added += 1
    db[key] = value

  print(f"📊 本次合并结果：新增 {added} 个，更新 {updated} 个，总计 {len(db)} 个单词。")


def main() -> None:
  if len(sys.argv) < 2:
    print("用法：python3 vocab_manual_import.py 批次文件.json")
    print("示例：python3 vocab_manual_import.py vocab_batch_001.json")
    sys.exit(1)

  batch_path = sys.argv[1]

  print("=" * 60)
  print("IELTS Novel Flow - 词汇手动导入工具")
  print("=" * 60)
  print(f"📁 批次文件：{batch_path}")
  print(f"📚 词库文件：{VOCAB_DB_PATH}")

  try:
    db = load_vocab_db(VOCAB_DB_PATH)
    batch = load_batch(batch_path)
  except Exception as e:
    print(f"❌ 加载数据失败：{e}")
    sys.exit(1)

  print(f"当前词库已有：{len(db)} 个单词，本批次：{len(batch)} 个单词")

  merge_batch(db, batch)
  save_vocab_db(db, VOCAB_DB_PATH)


if __name__ == "__main__":
  main()


