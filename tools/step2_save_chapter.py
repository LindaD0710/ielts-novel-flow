#!/usr/bin/env python3
"""
IELTS Novel Flow - 步骤2：章节处理与入库工具

功能：处理用户从 ChatGPT 生成的内容，验证格式，保存入库，更新学习进度
"""

import json
import os
import sys
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import uuid

# 导入课程管理器
from curriculum_manager import CurriculumManager

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

PROGRESS_FILE = os.path.join(BASE_DIR, "progress_tracker.json")
RAW_STORY_FILE = os.path.join(BASE_DIR, "raw_story.txt")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "src", "data", "generated")
LIBRARY_FILE = os.path.join(PROJECT_ROOT, "src", "data", "library.ts")
NOVEL_SERVICE_FILE = os.path.join(PROJECT_ROOT, "src", "services", "novelService.ts")

# 书籍分类配置（与前端保持一致）
BOOK_CATEGORIES = [
    {"id": "reborn", "name": "重生", "color": "#8B5CF6"},
    {"id": "suspense", "name": "悬疑", "color": "#06B6D4"},
    {"id": "romance", "name": "言情", "color": "#EC4899"},
    {"id": "business", "name": "商战", "color": "#10B981"},
]


def extract_title_from_content(content: str) -> str:
    """
    从内容中提取标题（尝试从第一行提取，或使用默认标题）
    
    Args:
        content: 章节内容
    
    Returns:
        章节标题
    """
    lines = content.strip().split("\n")
    
    # 尝试从第一行提取标题（如果看起来像标题）
    if lines:
        first_line = lines[0].strip()
        # 如果第一行较短且不包含 {word|meaning} 格式，可能是标题
        if len(first_line) < 30 and "{" not in first_line:
            return first_line
    
    # 默认标题
    return "新章节"


def validate_content_format(content: str) -> Tuple[bool, List[str]]:
    """
    验证内容格式，检查是否包含 {word|meaning} 格式
    
    Args:
        content: 章节内容
    
    Returns:
        (是否有效, 发现的单词列表)
    """
    # 正则表达式：匹配 {word|meaning} 格式
    pattern = r"\{([^|]+)\|([^}]+)\}"
    matches = re.findall(pattern, content)
    
    if not matches:
        return False, []
    
    # 提取单词列表
    words = [word.strip() for word, _ in matches]
    
    return True, words


def read_raw_story() -> str:
    """
    读取 raw_story.txt 文件
    
    Returns:
        章节内容文本
    """
    if not os.path.exists(RAW_STORY_FILE):
        raise FileNotFoundError(
            f"原始故事文件 {RAW_STORY_FILE} 不存在\n"
            f"请将 ChatGPT 生成的内容粘贴到该文件中"
        )
    
    with open(RAW_STORY_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        raise ValueError(
            f"文件 {RAW_STORY_FILE} 为空\n"
            f"请将 ChatGPT 生成的内容粘贴到该文件中"
        )
    
    return content


def extract_target_words_from_prompt() -> Optional[List[str]]:
    """
    尝试从 current_prompt.txt 中提取目标单词列表
    用于验证和标记已学习
    
    Returns:
        目标单词列表，如果无法提取则返回 None
    """
    prompt_file = os.path.join(BASE_DIR, "current_prompt.txt")
    
    if not os.path.exists(prompt_file):
        return None
    
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_content = f.read()
        
        # 查找 "## 核心词汇（必须全部使用）" 部分
        core_vocab_match = re.search(
            r"## 核心词汇.*?\n(.*?)(?=\n## |$)",
            prompt_content,
            re.DOTALL
        )
        
        if core_vocab_match:
            vocab_section = core_vocab_match.group(1)
            # 提取单词（格式：- word）
            words = re.findall(r"-\s*(\w+)", vocab_section)
            return [w.strip() for w in words if w.strip()]
    except Exception as e:
        print(f"⚠️  警告：无法从 Prompt 文件提取单词列表：{e}")
    
    return None


def save_chapter(chapter: Dict, output_dir: str = OUTPUT_DIR, book_id: Optional[str] = None) -> str:
    """
    保存章节到JSON文件（每本书只有一个章节，文件名使用book_id）
    
    Args:
        chapter: 章节数据
        output_dir: 输出目录
        book_id: 书籍ID（如果提供，用于命名文件）
    
    Returns:
        保存的文件路径
    """
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    if book_id:
        filename = f"{book_id}.json"  # 使用book_id作为文件名
    else:
        # 如果没有book_id，使用章节号（兼容旧逻辑）
        chapter_num = chapter.get("chapter_num", 1)
        filename = f"chapter_{chapter_num:03d}.json"
    
    filepath = os.path.join(output_dir, filename)
    
    # 保存文件
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chapter, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 章节已保存：{filepath}")
    return filepath


def load_existing_books() -> List[Dict]:
    """从library.ts读取现有书籍列表"""
    books = []
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 使用正则表达式提取书籍信息
        pattern = r'id:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*author:\s*"([^"]+)",\s*coverColor:\s*"([^"]+)",\s*category:\s*"([^"]+)"'
        matches = re.findall(pattern, content)
        
        for match in matches:
            books.append({
                "id": match[0],
                "title": match[1],
                "author": match[2],
                "coverColor": match[3],
                "category": match[4],
            })
        
        return books
    except Exception as e:
        print(f"⚠️  警告：无法读取现有书籍列表：{e}")
        return []


def add_book_to_library(book_id: str, title: str, author: str, category: str, cover_color: str):
    """将新书添加到library.ts"""
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 找到 libraryBooks 数组的结束位置
        insert_index = -1
        for i, line in enumerate(lines):
            if line.strip() == "];":
                # 找到 libraryBooks 数组的 ]; 
                if i > 0 and "libraryBooks" in lines[i-10:i]:  # 检查前面几行是否有libraryBooks
                    insert_index = i
                    break
        
        if insert_index == -1:
            # 如果找不到，尝试其他方式
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() == "];" and i > 0:
                    insert_index = i
                    break
        
        if insert_index > 0:
            # 在 ]; 之前插入新书
            new_book_lines = [
                "  {\n",
                f'    id: "{book_id}",\n',
                f'    title: "{title}",\n',
                f'    author: "{author}",\n',
                f'    coverColor: "{cover_color}",\n',
                f'    category: "{category}",\n',
                "    chapters: [],\n",
                "  },\n",
            ]
            lines[insert_index:insert_index] = new_book_lines
            
            with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
                f.writelines(lines)
            
            print(f"✅ 已更新 library.ts，添加新书：{title}")
        else:
            raise ValueError("无法找到插入位置")
    except Exception as e:
        print(f"❌ 错误：无法自动更新 library.ts：{e}")
        print(f"\n请手动在 library.ts 的 libraryBooks 数组中添加以下内容：")
        print(f"  {{")
        print(f'    id: "{book_id}",')
        print(f'    title: "{title}",')
        print(f'    author: "{author}",')
        print(f'    coverColor: "{cover_color}",')
        print(f'    category: "{category}",')
        print(f"    chapters: [],")
        print(f"  }},")


def update_novel_service(book_id: str):
    """
    自动更新 novelService.ts，添加新章节的导入和数据
    
    Args:
        book_id: 书籍ID（也是章节文件名，不含扩展名）
    """
    try:
        # 生成导入变量名（book_id 转换为驼峰命名）
        # book-20260112165132 -> book20260112165132Data
        import_var_name = f"{book_id.replace('-', '')}Data"
        import_path = f"../data/generated/{book_id}.json"
        
        # 读取文件
        with open(NOVEL_SERVICE_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            content = "".join(lines)
        
        # 检查是否已经导入过（避免重复）
        if f"import {import_var_name}" in content:
            print(f"⚠️  提示：{book_id} 已在 novelService.ts 中导入，跳过更新")
            return
        
        # 1. 添加导入语句（在 vocabDbRawData 导入之前）
        import_insert_index = -1
        for i, line in enumerate(lines):
            if "import vocabDbRawData" in line:
                import_insert_index = i
                break
        
        if import_insert_index > 0:
            # 在 vocabDbRawData 导入之前插入新导入
            new_import = f"import {import_var_name} from \"{import_path}\";\n"
            lines.insert(import_insert_index, new_import)
            print(f"✅ 已添加导入：{import_var_name}")
        else:
            raise ValueError("无法找到导入插入位置（找不到 vocabDbRawData 导入）")
        
        # 2. 在 allChaptersData 数组中添加章节数据
        # 查找数组开始位置和插入位置
        array_insert_index = -1
        array_start_line = -1
        
        # 查找 allChaptersData 数组定义
        for i, line in enumerate(lines):
            if "const allChaptersData" in line or ("allChaptersData" in line and "Chapter[]" in line):
                array_start_line = i
                # 找到数组定义行，继续查找数组内容
                # 先找到数组开始的 [
                array_bracket_start = -1
                for j in range(i, min(i + 10, len(lines))):
                    if "[" in lines[j] and "allChaptersData" in "".join(lines[i:j+1]):
                        array_bracket_start = j
                        break
                
                if array_bracket_start == -1:
                    continue
                
                # 从数组开始后查找插入位置
                for j in range(array_bracket_start + 1, min(array_bracket_start + 20, len(lines))):
                    # 查找注释行（优先插入位置）
                    if "// 正式生产的章节将添加到这里" in lines[j] or "// 格式：bookXxxData as Chapter," in lines[j]:
                        array_insert_index = j + 1
                        break
                    # 如果已经有章节数据，在最后一个数据后插入
                    if "as Chapter" in lines[j]:
                        # 检查下一行是否是数组结束
                        if j + 1 < len(lines) and "]" in lines[j + 1] and "as Chapter[]" in lines[j + 1]:
                            # 数组结束前，在当前行后插入
                            array_insert_index = j + 1
                            break
                        else:
                            # 还有更多数据，继续查找最后一个
                            array_insert_index = j + 1
                    # 如果找到数组结束（但还没找到插入位置），在前面插入
                    elif "]" in lines[j] and "as Chapter[]" in lines[j] and array_insert_index == -1:
                        array_insert_index = j
                        break
                break
        
        if array_insert_index > 0:
            # 插入新章节数据（带正确的缩进）
            new_chapter_line = f"    {import_var_name} as Chapter,\n"
            lines.insert(array_insert_index, new_chapter_line)
            print(f"✅ 已添加章节数据到数组：{import_var_name}")
        else:
            raise ValueError("无法找到数组插入位置")
        
        # 保存文件
        with open(NOVEL_SERVICE_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"✅ 已自动更新 novelService.ts")
        
    except Exception as e:
        print(f"❌ 错误：无法自动更新 novelService.ts：{e}")
        print(f"\n请手动在 novelService.ts 中添加以下内容：")
        print(f"\n1. 在导入部分添加：")
        print(f"   import {import_var_name} from \"{import_path}\";")
        print(f"\n2. 在 allChaptersData 数组中添加：")
        print(f"   {import_var_name} as Chapter,")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("=" * 60)
    print("💾 步骤2：章节处理与入库工具")
    print("=" * 60)
    print()
    
    try:
        # 1. 读取原始故事内容
        print("📖 读取原始故事内容...")
        raw_content = read_raw_story()
        print(f"✅ 已读取 {len(raw_content)} 字符")
        
        # 2. 验证格式
        print("\n🔍 验证内容格式...")
        is_valid, found_words = validate_content_format(raw_content)
        
        if not is_valid:
            print("❌ 错误：内容中未找到 {word|meaning} 格式的标记")
            print("请确保 ChatGPT 生成的内容使用了正确的格式")
            sys.exit(1)
        
        print(f"✅ 格式验证通过，发现 {len(found_words)} 个单词标记")
        print(f"   示例单词：{', '.join(found_words[:5])}...")
        
        # 3. 验证字数（1500字左右）
        print("\n📏 验证字数...")
        char_count = len(raw_content)
        word_count = len(raw_content.replace(" ", "").replace("\n", ""))  # 粗略计算中文字数
        print(f"字符数：{char_count}")
        print(f"估算字数：约 {word_count // 2} 字（中文）")
        
        if word_count < 1400:
            print(f"⚠️  警告：字数可能过少（建议 1400-1600 字）")
            confirm = input("是否继续？(y/N): ").strip().lower()
            if confirm != "y":
                print("已取消")
                sys.exit(0)
        elif word_count > 2000:
            print(f"⚠️  警告：字数可能过多（建议 1400-1600 字）")
            confirm = input("是否继续？(y/N): ").strip().lower()
            if confirm != "y":
                print("已取消")
                sys.exit(0)
        else:
            print(f"✅ 字数符合要求（约 {word_count // 2} 字）")
        
        # 4. 选择分类（类型）
        print("\n📚 选择书籍分类（类型）...")
        print("可选分类：")
        for i, cat in enumerate(BOOK_CATEGORIES, 1):
            print(f"  {i}. {cat['name']} ({cat['id']})")
        
        while True:
            try:
                choice = input("\n请选择分类编号（1-4）：").strip()
                cat_index = int(choice) - 1
                if 0 <= cat_index < len(BOOK_CATEGORIES):
                    selected_category = BOOK_CATEGORIES[cat_index]
                    print(f"✅ 已选择分类：{selected_category['name']}")
                    print(f"💡 提示：此分类将使用独立的进度文件，确保可以重新调用完整的词库")
                    break
                else:
                    print("❌ 无效的选择，请输入 1-4")
            except ValueError:
                print("❌ 请输入数字")
        
        # 根据选择的分类，使用对应的进度文件
        from curriculum_manager import get_progress_file_for_category
        category_progress_file = get_progress_file_for_category(selected_category["id"])
        print(f"📁 使用进度文件：{category_progress_file}")
        
        # 5. 选择或创建书籍
        print("\n📖 选择或创建书籍...")
        existing_books = load_existing_books()
        
        # 筛选当前分类下的书籍
        same_category_books = [b for b in existing_books if b["category"] == selected_category["id"]]
        
        if same_category_books:
            print(f"\n找到 {len(same_category_books)} 本同分类书籍：")
            for i, book in enumerate(same_category_books, 1):
                print(f"  {i}. {book['title']} - {book['author']} (ID: {book['id']})")
            print(f"  {len(same_category_books) + 1}. 创建新书籍")
            
            while True:
                try:
                    choice = input(f"\n请选择书籍编号（1-{len(same_category_books) + 1}）：").strip()
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(same_category_books):
                        selected_book = same_category_books[choice_num - 1]
                        print(f"✅ 已选择书籍：{selected_book['title']}")
                        book_id = selected_book["id"]
                        book_title = selected_book["title"]
                        book_author = selected_book["author"]
                        book_color = selected_book["coverColor"]
                        break
                    elif choice_num == len(same_category_books) + 1:
                        # 创建新书籍
                        print("\n创建新书籍：")
                        book_title = input("请输入书名：").strip()
                        if not book_title:
                            book_title = extract_title_from_content(raw_content)
                            print(f"使用默认书名：{book_title}")
                        book_author = input("请输入作者（可选，直接回车使用默认）：").strip()
                        if not book_author:
                            book_author = "佚名"
                        
                        # 生成唯一的 book_id
                        book_id = f"book-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        book_color = selected_category["color"]
                        
                        # 添加到 library.ts
                        add_book_to_library(book_id, book_title, book_author, selected_category["id"], book_color)
                        break
                    else:
                        print(f"❌ 无效的选择，请输入 1-{len(same_category_books) + 1}")
                except ValueError:
                    print("❌ 请输入数字")
        else:
            # 没有同分类书籍，直接创建新书
            print("当前分类下暂无书籍，创建新书籍：")
            book_title = input("请输入书名（直接回车使用自动提取）：").strip()
            if not book_title:
                book_title = extract_title_from_content(raw_content)
                print(f"使用自动提取的书名：{book_title}")
            
            book_author = input("请输入作者（可选，直接回车使用默认）：").strip()
            if not book_author:
                book_author = "佚名"
            
            # 生成唯一的 book_id
            book_id = f"book-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            book_color = selected_category["color"]
            
            # 添加到 library.ts
            add_book_to_library(book_id, book_title, book_author, selected_category["id"], book_color)
        
        # 6. 提取章节标题（用于章节数据）
        print("\n📝 提取章节标题...")
        chapter_title = book_title  # 使用书名作为章节标题（因为每本书只有一个章节）
        print(f"✅ 章节标题：{chapter_title}")
        
        # 7. 初始化课程管理器（使用分类对应的进度文件）
        print("\n📚 初始化课程管理器...")
        print(f"   使用分类进度文件：{category_progress_file}")
        manager = CurriculumManager(category_progress_file)
        current_chapter = manager.get_current_chapter()
        print(f"当前章节号：{current_chapter}")
        print(f"   分类：{selected_category['name']} - 此分类使用独立的词库进度，不影响其他分类")
        
        # 8. 尝试从 Prompt 文件提取目标单词
        print("\n🔍 提取目标单词列表...")
        target_words = extract_target_words_from_prompt()
        
        if target_words:
            print(f"✅ 从 Prompt 文件提取到 {len(target_words)} 个目标单词")
            print(f"   单词列表：{target_words}")
        else:
            print("⚠️  警告：无法从 Prompt 文件提取单词列表")
            print("   将使用内容中发现的单词进行标记")
            # 使用内容中发现的单词（去重）
            target_words = list(set([w.lower() for w in found_words]))
        
        # 9. 构建章节数据
        print("\n📦 构建章节数据...")
        chapter_id = f"{book_id}-chapter-1"  # 每本书只有一个章节，所以是 chapter-1
        
        chapter = {
            "id": chapter_id,
            "title": chapter_title,
            "content": raw_content
        }
        
        # 10. 保存章节（使用 book_id 作为文件名）
        print("\n💾 保存章节...")
        chapter["chapter_num"] = 1  # 每本书只有一个章节
        chapter["book_id"] = book_id  # 添加 book_id 到章节数据中
        filepath = save_chapter(chapter, OUTPUT_DIR, book_id)
        
        # 10.5. 自动更新 novelService.ts
        print("\n🔄 自动更新 novelService.ts...")
        update_novel_service(book_id)
        
        # 11. 标记单词为已学习
        print("\n✅ 更新学习进度...")
        if target_words:
            manager.mark_as_learned(target_words)
        else:
            print("⚠️  警告：无法确定目标单词，跳过进度更新")
            print("   建议：确保运行了 step1_get_prompt.py 并保留了 current_prompt.txt")
        
        # 12. 增加章节计数（虽然每本书只有一个章节，但仍需要更新计数）
        manager.increment_chapter()
        
        # 13. 打印更新后的统计
        print("\n📊 更新后的学习进度：")
        manager.print_statistics()
        
        # 14. 清空 raw_story.txt（可选）
        print("\n🧹 清理临时文件...")
        clear_raw = input("是否清空 raw_story.txt？(y/N): ").strip().lower()
        if clear_raw == "y":
            with open(RAW_STORY_FILE, "w", encoding="utf-8") as f:
                f.write("")
            print("✅ 已清空 raw_story.txt")
        else:
            print("⏭️  保留 raw_story.txt 内容")
        
        print("\n" + "=" * 60)
        print("🎉 处理完成！")
        print("=" * 60)
        print(f"📚 书籍信息：")
        print(f"   书名：{book_title}")
        print(f"   作者：{book_author}")
        print(f"   分类：{selected_category['name']}")
        print(f"   书籍ID：{book_id}")
        print(f"\n📖 章节信息：")
        print(f"   章节标题：{chapter_title}")
        print(f"   内容长度：约 {word_count // 2} 字（{char_count} 字符）")
        print(f"   保存位置：{filepath}")
        print(f"\n💡 提示：请检查 library.ts 是否已正确更新")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

