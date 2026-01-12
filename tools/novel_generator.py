#!/usr/bin/env python3
"""
IELTS Novel Flow - 小说生成器
使用 OpenAI/DeepSeek API 生成包含雅思词汇的爽文章节
"""

import json
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
import openai
from openai import OpenAI

# 尝试加载 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv 是可选的

# 导入课程管理器
from curriculum_manager import CurriculumManager

# ==================== 路径配置 ====================
# 获取脚本所在目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 输出目录：指向项目根目录下的 src/data/generated
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # tools 的父目录（项目根目录）
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "src", "data", "generated")

# 配置文件路径（相对于 tools 目录）
STORY_CONFIG_FILE = os.path.join(BASE_DIR, "story_config.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress_tracker.json")

# ==================== API 配置 ====================
# API 配置（使用占位符，实际使用时请替换）
API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # DeepSeek: "https://api.deepseek.com/v1"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # DeepSeek: "deepseek-chat"


# ==================== System Prompt ====================
SYSTEM_PROMPT = """你是晋江文学城金牌写手，同时也是一名深谙"二语习得理论"的雅思名师。

## 你的双重身份

### 身份一：晋江文学城金牌写手
- 你擅长创作引人入胜的爽文，深谙读者心理
- 你懂得如何制造冲突、悬念、打脸、逆袭等爽点
- 你的文笔流畅，节奏紧凑，绝不拖泥带水
- 你擅长塑造人物，让角色立体生动

### 身份二：雅思名师
- 你精通"二语习得理论"，知道如何通过上下文自然习得词汇
- 你理解"三明治英语法"的精髓：在母语语境中嵌入目标语言
- 你懂得词汇的"可理解性输入"原则：通过上下文让单词意义自明
- 你掌握艾宾浩斯遗忘曲线，知道如何安排词汇复现

## 核心任务

编写一个引人入胜的"爽文"章节，必须自然地通过上下文教会用户列表中的单词。

## 硬性要求

### 1. 剧情要求（爽感优先）
- **必须紧凑**：开篇3句话内抓住读者，不能拖沓
- **必须有冲突**：可以是打脸、逆袭、反转、误会等经典爽点
- **必须有悬念**：在章节结尾留下钩子，让读者想继续读
- **必须有人物**：主角要有行动力，配角要有存在感
- **禁止流水账**：不能为了塞单词而写流水账，剧情必须自洽

### 2. 词汇要求（学习效率）
- **必须覆盖所有 target_vocab**：列表中的每个单词都必须出现
- **必须自然嵌入**：单词出现要符合语境，不能生硬
- **必须均匀分布**：不要堆砌在一段话里，确保阅读体验流畅
- **必须使用格式**：严格使用 {word|meaning} 格式标记
- **复习词汇**：如果提供了 review_vocab，也要自然融入（可适当降低密度）

### 3. 格式要求
- **严格格式**：所有雅思单词必须使用 {word|meaning} 格式
- **中文释义**：meaning 必须是简明的中文释义（不超过8个字）
- **示例**：她感到非常 {ambitious|有野心}，决定要...

### 4. 密度控制
- **理想密度**：每100-150字出现1个新单词
- **避免堆砌**：同一段落最多出现2-3个新单词
- **自然过渡**：单词之间要有足够的上下文，让读者理解

### 5. 长度要求
- **章节长度**：1500-2500字（确保有足够空间自然融入词汇）
- **段落长度**：每段3-5句话，保持节奏感

## 输出格式

直接输出章节内容，不需要额外的说明文字。内容必须是纯文本，使用 {word|meaning} 格式标记所有雅思单词。

## 写作技巧

1. **开篇抓人**：用动作、对话或冲突开场，不要用环境描写
2. **中段推进**：通过事件推进剧情，在事件中自然引入单词
3. **结尾留钩**：用悬念、反转或新冲突结尾，让读者想继续
4. **词汇融入**：在人物心理、对话、动作、环境等不同场景中分散使用单词
5. **上下文提示**：确保单词出现时，上下文足够清晰，让读者能理解含义

记住：你的目标是写出一篇让读者欲罢不能的爽文，同时让读者在不知不觉中学会这些雅思单词。"""


# ==================== 核心函数 ====================

def build_user_prompt(
    target_vocab: List[str],
    review_vocab: Optional[List[str]] = None,
    story_context: Optional[Dict] = None
) -> str:
    """
    构建用户提示词
    
    Args:
        target_vocab: 本章核心词表
        review_vocab: 复习词表（可选）
        story_context: 故事上下文（流派、大纲、前情提要）
    
    Returns:
        完整的用户提示词
    """
    prompt_parts = []
    
    # 1. 故事上下文
    if story_context:
        prompt_parts.append("## 故事背景")
        if story_context.get("genre"):
            prompt_parts.append(f"**流派**：{story_context['genre']}")
        if story_context.get("prev_summary"):
            prompt_parts.append(f"**前情提要**：{story_context['prev_summary']}")
        if story_context.get("chapter_outline"):
            prompt_parts.append(f"**本章大纲/爽点**：{story_context['chapter_outline']}")
        prompt_parts.append("")
    
    # 2. 核心词汇
    prompt_parts.append("## 核心词汇（必须全部使用）")
    vocab_list = "\n".join([f"- {word}" for word in target_vocab])
    prompt_parts.append(vocab_list)
    prompt_parts.append("")
    
    # 3. 复习词汇（如果有）
    if review_vocab:
        prompt_parts.append("## 复习词汇（自然融入，可适当降低密度）")
        review_list = "\n".join([f"- {word}" for word in review_vocab])
        prompt_parts.append(review_list)
        prompt_parts.append("")
    
    # 4. 输出要求
    prompt_parts.append("## 输出要求")
    prompt_parts.append("1. 直接输出章节内容，不要任何说明文字")
    prompt_parts.append("2. 所有雅思单词必须使用 {word|meaning} 格式")
    prompt_parts.append("3. 确保剧情紧凑、有冲突、有悬念")
    prompt_parts.append("4. 确保所有核心词汇都被使用，且分布均匀")
    prompt_parts.append("5. 章节长度：1500-2500字")
    
    return "\n".join(prompt_parts)


def generate_chapter(
    target_vocab: List[str],
    review_vocab: Optional[List[str]] = None,
    story_context: Optional[Dict] = None,
    chapter_title: Optional[str] = None
) -> Dict:
    """
    生成章节内容
    
    Args:
        target_vocab: 本章核心词表
        review_vocab: 复习词表（可选）
        story_context: 故事上下文
        chapter_title: 章节标题（可选，如果不提供则让AI生成）
    
    Returns:
        符合 Chapter 接口的字典
    """
    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )
    
    # 构建提示词
    user_prompt = build_user_prompt(target_vocab, review_vocab, story_context)
    
    # 如果需要生成标题，先让AI生成标题
    if not chapter_title:
        title_prompt = f"""根据以下信息，生成一个吸引人的章节标题（不超过15字）：
        
{user_prompt}

只输出标题，不要其他内容。"""
        
        title_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个擅长起标题的编辑。"},
                {"role": "user", "content": title_prompt}
            ],
            temperature=0.7,
            max_tokens=50
        )
        chapter_title = title_response.choices[0].message.content.strip()
    
    # 生成章节内容
    print(f"正在生成章节：{chapter_title}...")
    print(f"核心词汇数量：{len(target_vocab)}")
    if review_vocab:
        print(f"复习词汇数量：{len(review_vocab)}")
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8,  # 稍高的温度保证创意和爽感
        max_tokens=4000   # 足够生成2500字的内容
    )
    
    content = response.choices[0].message.content.strip()
    
    # 验证词汇覆盖
    missing_words = []
    for word in target_vocab:
        if word.lower() not in content.lower():
            missing_words.append(word)
    
    if missing_words:
        print(f"⚠️  警告：以下词汇未在内容中出现：{missing_words}")
        print("建议：重新生成或手动检查内容")
    
    # 生成章节ID
    chapter_id = f"chapter-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # 构建章节数据
    chapter = {
        "id": chapter_id,
        "title": chapter_title,
        "content": content
    }
    
    return chapter


def save_chapter(chapter: Dict, output_dir: Optional[str] = None, filename: Optional[str] = None):
    """
    保存章节到JSON文件
    
    Args:
        chapter: 章节数据
        output_dir: 输出目录（可选，默认使用配置的输出目录）
        filename: 文件名（可选，默认使用章节ID）
    """
    # 使用默认输出目录（如果未指定）
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名
    if not filename:
        filename = f"{chapter['id']}.json"
    
    filepath = os.path.join(output_dir, filename)
    
    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chapter, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 章节已保存：{filepath}")
    return filepath


# ==================== 主程序 ====================

def load_story_config(config_file: str = STORY_CONFIG_FILE) -> Dict:
    """
    加载故事配置文件
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        故事配置字典
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(
            f"故事配置文件 {config_file} 不存在，请先创建配置文件"
        )
    
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_chapter_with_curriculum(
    batch_size: int = 20,
    review_size: int = 5,
    chapter_title: Optional[str] = None,
    story_config_file: str = STORY_CONFIG_FILE,
    progress_file: str = PROGRESS_FILE
) -> Dict:
    """
    使用课程管理器自动生成章节
    
    Args:
        batch_size: 新单词批次大小
        review_size: 复习单词批次大小
        chapter_title: 章节标题（可选）
        story_config_file: 故事配置文件路径
        progress_file: 进度追踪文件路径
    
    Returns:
        生成的章节数据
    """
    # 1. 初始化课程管理器
    print("📚 初始化课程管理器...")
    manager = CurriculumManager(progress_file)
    manager.print_statistics()
    
    # 2. 获取单词批次
    print(f"\n📖 获取新单词批次（{batch_size}个）...")
    target_vocab = manager.get_next_batch(batch_size)
    
    if not target_vocab:
        raise ValueError("没有可用的新单词，请检查进度追踪文件")
    
    print(f"新单词：{target_vocab}")
    
    # 获取复习单词
    review_vocab = manager.get_review_batch(review_size)
    if review_vocab:
        print(f"\n🔄 获取复习单词（{len(review_vocab)}个）...")
        print(f"复习单词：{review_vocab}")
    
    # 3. 加载故事配置
    print(f"\n📝 加载故事配置...")
    story_context = load_story_config(story_config_file)
    print(f"流派：{story_context.get('genre', 'N/A')}")
    
    # 4. 生成章节
    print(f"\n✨ 开始生成章节...")
    chapter = generate_chapter(
        target_vocab=target_vocab,
        review_vocab=review_vocab if review_vocab else None,
        story_context=story_context,
        chapter_title=chapter_title
    )
    
    # 5. 标记单词为已学习
    print(f"\n✅ 标记单词为已学习...")
    manager.mark_as_learned(target_vocab)
    
    # 6. 增加章节计数
    manager.increment_chapter()
    
    # 7. 打印更新后的统计
    manager.print_statistics()
    
    return chapter


def main():
    """主函数 - 使用课程管理器自动生成"""
    
    try:
        # 使用课程管理器生成章节
        chapter = generate_chapter_with_curriculum(
            batch_size=20,  # 每章20个新单词
            review_size=5,  # 每章5个复习单词
            chapter_title=None  # 让AI自动生成
        )
        
        # 保存章节
        save_chapter(chapter)
        
        print("\n" + "="*50)
        print("🎉 生成完成！")
        print("="*50)
        print(f"章节标题：{chapter['title']}")
        print(f"内容长度：{len(chapter['content'])} 字符")
        print(f"章节ID：{chapter['id']}")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

