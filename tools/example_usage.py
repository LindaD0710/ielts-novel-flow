#!/usr/bin/env python3
"""
使用示例：演示如何使用 novel_generator 生成章节
"""

from novel_generator import generate_chapter, save_chapter

# 示例 1：基础用法
def example_basic():
    """基础用法示例"""
    target_vocab = [
        "ambitious", "meticulous", "prestigious", "sophisticated",
        "resilient", "elaborate", "profound", "intricate"
    ]
    
    story_context = {
        "genre": "重生霸总",
        "prev_summary": "林晚晚刚刚发现自己是一个顶级豪门的继承人。",
        "chapter_outline": "林晚晚参加商业晚宴，遇到前世的仇人，通过智慧和实力打脸。"
    }
    
    chapter = generate_chapter(
        target_vocab=target_vocab,
        story_context=story_context
    )
    
    save_chapter(chapter, filename="example_basic.json")
    print("✅ 基础示例完成")


# 示例 2：带复习词汇
def example_with_review():
    """带复习词汇的示例"""
    target_vocab = [
        "substantial", "comprehensive", "remarkable", "exceptional",
        "formidable", "influential", "strategic", "innovative"
    ]
    
    review_vocab = [
        "ambitious", "meticulous", "prestigious"  # 前几章学过的词
    ]
    
    story_context = {
        "genre": "重生霸总",
        "prev_summary": "林晚晚在商业晚宴上成功打脸仇人，展现了商业天赋。",
        "chapter_outline": "林晚晚接手第一个重要项目，展现领导力和战略思维，获得家族认可。"
    }
    
    chapter = generate_chapter(
        target_vocab=target_vocab,
        review_vocab=review_vocab,
        story_context=story_context,
        chapter_title="第三章：战略布局"
    )
    
    save_chapter(chapter, filename="example_with_review.json")
    print("✅ 复习词汇示例完成")


# 示例 3：大量词汇（20个）
def example_large_vocab():
    """大量词汇示例"""
    target_vocab = [
        "ambitious", "meticulous", "prestigious", "sophisticated",
        "resilient", "elaborate", "profound", "intricate",
        "substantial", "comprehensive", "remarkable", "exceptional",
        "formidable", "influential", "strategic", "innovative",
        "transformative", "outstanding", "distinguished", "eminent"
    ]
    
    story_context = {
        "genre": "重生霸总",
        "prev_summary": "林晚晚已经成功接手了第一个项目，正在逐步展现自己的实力。",
        "chapter_outline": "林晚晚面临重大危机，通过智慧和坚韧化解，同时发现家族秘密。"
    }
    
    chapter = generate_chapter(
        target_vocab=target_vocab,
        story_context=story_context
    )
    
    save_chapter(chapter, filename="example_large_vocab.json")
    print("✅ 大量词汇示例完成")


if __name__ == "__main__":
    print("=" * 50)
    print("IELTS Novel Flow - 使用示例")
    print("=" * 50)
    print()
    
    # 运行示例（根据需要取消注释）
    # example_basic()
    # example_with_review()
    # example_large_vocab()
    
    print("\n提示：取消注释上面的函数调用来运行示例")

