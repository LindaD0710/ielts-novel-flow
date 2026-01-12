#!/usr/bin/env python3
"""
从 GitHub 项目提取雅思词汇

从 https://github.com/hefengxian/my-ielts 项目提取词汇列表
"""

import json
import os
import re
import requests
from typing import Set, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IELTS_SOURCE_FILE = os.path.join(BASE_DIR, "ielts_source.json")
GITHUB_REPO = "hefengxian/my-ielts"
GITHUB_BRANCH = "master"


def load_existing_words() -> Set[str]:
    """加载现有词库"""
    if not os.path.exists(IELTS_SOURCE_FILE):
        return set()
    
    try:
        with open(IELTS_SOURCE_FILE, 'r', encoding='utf-8') as f:
            words = json.load(f)
        return set(w.lower() for w in words if w.strip())
    except:
        return set()


def get_github_file_tree(path: str) -> List[dict]:
    """获取GitHub仓库的目录树"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/git/trees/{GITHUB_BRANCH}?recursive=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('tree', [])
    except Exception as e:
        print(f"⚠️  警告：无法从GitHub获取文件列表：{e}")
        return []


def extract_words_from_paths(file_paths: List[str]) -> Set[str]:
    """从文件路径中提取单词"""
    words = set()
    
    for path in file_paths:
        # 提取文件名（不含扩展名和目录）
        filename = os.path.basename(path)
        # 移除扩展名
        name_without_ext = os.path.splitext(filename)[0]
        
        # 跳过非单词文件名（包含中文字符、特殊字符等）
        if re.match(r'^[a-zA-Z][a-zA-Z\s]*[a-zA-Z]$', name_without_ext) or re.match(r'^[a-zA-Z]+$', name_without_ext):
            # 处理可能包含多个单词的情况（用空格或下划线分隔）
            potential_words = re.split(r'[\s_\-]+', name_without_ext)
            for word in potential_words:
                word = word.strip()
                # 只保留看起来像英文单词的（至少2个字母，只包含字母）
                if len(word) >= 2 and word.isalpha() and word.islower():
                    words.add(word.lower())
                elif len(word) >= 2 and word.isalpha():
                    # 处理首字母大写的单词（如专有名词）
                    # 只提取全小写的单词，首字母大写的可能是专有名词
                    if word[0].isupper() and word[1:].islower():
                        words.add(word.lower())
    
    return words


def extract_from_github():
    """从GitHub仓库提取词汇"""
    print("=" * 60)
    print("📚 从 GitHub 提取雅思词汇")
    print("=" * 60)
    print(f"仓库：{GITHUB_REPO}")
    print(f"分支：{GITHUB_BRANCH}")
    print()
    
    # 获取文件树
    print("📡 正在获取文件列表...")
    tree = get_github_file_tree("")
    
    if not tree:
        print("❌ 无法获取文件列表")
        return
    
    # 筛选词汇相关的文件
    print("🔍 正在筛选词汇文件...")
    vocab_paths = []
    for item in tree:
        path = item.get('path', '')
        # 查找 vocabulary 相关的文件
        if 'vocabulary' in path.lower() or 'vocab' in path.lower():
            # 音频文件或JSON文件
            if path.endswith('.mp3') or path.endswith('.json') or path.endswith('.txt'):
                vocab_paths.append(path)
    
    print(f"✅ 找到 {len(vocab_paths)} 个相关文件")
    
    # 从文件路径中提取单词
    print("📝 正在提取单词...")
    extracted_words = extract_words_from_paths(vocab_paths)
    print(f"✅ 提取到 {len(extracted_words)} 个单词")
    
    # 加载现有词库
    existing_words = load_existing_words()
    print(f"📊 现有词库：{len(existing_words)} 个单词")
    
    # 合并
    all_words = existing_words | extracted_words
    all_words_list = sorted(list(all_words))
    
    # 保存
    with open(IELTS_SOURCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_words_list, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print("✅ 提取完成！")
    print("=" * 60)
    print(f"提取的新单词：{len(extracted_words)} 个")
    print(f"扩充前：{len(existing_words)} 个")
    print(f"扩充后：{len(all_words_list)} 个（去重后）")
    print(f"目标：4000 个")
    
    if len(all_words_list) >= 4000:
        print("✅ 已达到目标！")
    else:
        print(f"⚠️  还需 {4000 - len(all_words_list)} 个单词")
    
    print()
    print("📋 提取的单词示例（前20个）：")
    for i, word in enumerate(all_words_list[:20], 1):
        print(f"   {i:2}. {word}")
    if len(all_words_list) > 20:
        print(f"   ... 还有 {len(all_words_list) - 20} 个单词")
    
    print("=" * 60)


def extract_from_github_raw():
    """直接从GitHub raw文件提取（更直接的方法）"""
    print("=" * 60)
    print("📚 从 GitHub Raw 文件提取词汇")
    print("=" * 60)
    print()
    
    # 尝试从已知的路径获取词汇文件
    # 通常词汇可能在 JSON 或文本文件中
    possible_paths = [
        "public/vocabulary/data.json",
        "src/data/vocabulary.json",
        "src/vocabulary.json",
        "vocabulary.json",
        "data/vocabulary.json",
    ]
    
    extracted_words = set()
    
    for path in possible_paths:
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{path}"
        try:
            print(f"📡 尝试获取：{path}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # 尝试不同的JSON结构
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str):
                            extracted_words.add(item.lower())
                        elif isinstance(item, dict):
                            # 查找可能的单词字段
                            for key in ['word', 'name', 'vocab', 'term']:
                                if key in item and isinstance(item[key], str):
                                    extracted_words.add(item[key].lower())
                elif isinstance(data, dict):
                    # 可能是对象，键或值可能是单词
                    for key, value in data.items():
                        if isinstance(key, str) and key.isalpha():
                            extracted_words.add(key.lower())
                        if isinstance(value, str) and value.isalpha():
                            extracted_words.add(value.lower())
                print(f"✅ 成功从 {path} 提取 {len(extracted_words)} 个单词")
                break
        except:
            continue
    
    if not extracted_words:
        print("⚠️  无法从标准路径获取，尝试从文件树提取...")
        extract_from_github()
        return
    
    # 加载现有词库
    existing_words = load_existing_words()
    print(f"📊 现有词库：{len(existing_words)} 个单词")
    
    # 合并
    all_words = existing_words | extracted_words
    all_words_list = sorted(list(all_words))
    
    # 保存
    with open(IELTS_SOURCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_words_list, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 60)
    print("✅ 提取完成！")
    print("=" * 60)
    print(f"扩充后：{len(all_words_list)} 个（去重后）")
    print("=" * 60)


if __name__ == "__main__":
    try:
        # 先尝试从 raw 文件提取（更快）
        extract_from_github_raw()
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

