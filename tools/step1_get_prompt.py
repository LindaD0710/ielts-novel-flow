#!/usr/bin/env python3
"""
IELTS Novel Flow - 步骤1：智能选词与 Prompt 生成器

功能：准备原材料，生成可以直接发给 ChatGPT 的 Prompt
注意：此时不更新学习进度，因为用户还没真正生成小说
"""

import json
import os
import sys
import argparse
from typing import Dict, List

# 导入课程管理器
from curriculum_manager import CurriculumManager

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

STORY_CONFIG_FILE = os.path.join(BASE_DIR, "story_config.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "progress_tracker.json")
PROMPT_OUTPUT_FILE = os.path.join(BASE_DIR, "current_prompt.txt")
MISSING_POOL_FILE = os.path.join(BASE_DIR, "missing_ielts_words.txt")

# System Prompt（用于 ChatGPT）
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

编写一个引人入胜的"爽文"短篇小说（完整故事，不是章节），必须自然地通过上下文教会用户列表中的单词。

**重要说明**：这是一本完整的短篇小说，不是章节。要求：
- 必须是一个完整的故事，有开头、发展、高潮、结尾
- 字数严格控制在 1500 字左右（1400-1600字）
- 故事要完整，能够独立阅读，不需要续集
- 不要留下悬念或未完成的剧情

## 硬性要求

### 1. 剧情要求（爽感优先）
- **必须紧凑**：开篇3句话内抓住读者，不能拖沓
- **必须有冲突**：可以是打脸、逆袭、反转、误会等经典爽点
- **必须有高潮**：故事要有精彩的转折和高潮部分，让读者感到爽快
- **必须有完整结局**：故事必须有完整的结尾，所有冲突都要解决，不要留下悬念或钩子
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

### 5. 长度要求（重要）
- **完整短篇小说**：这不是章节，而是一本完整的短篇小说
- **字数控制**：严格控制在 1500 字左右（1400-1600字），不要超过或少于这个范围
- **故事完整性**：必须有完整的开头、发展、高潮、结尾，形成一个完整的故事闭环
- **独立阅读**：故事要能独立阅读，不依赖续集或前文，给读者完整的阅读体验
- **段落长度**：每段3-5句话，保持节奏感

## 输出格式

直接输出小说内容（完整故事），不需要额外的说明文字。内容必须是纯文本，使用 {word|meaning} 格式标记所有雅思单词。

## 写作技巧

1. **开篇抓人**：用动作、对话或冲突开场，不要用环境描写
2. **中段推进**：通过事件推进剧情，在事件中自然引入单词，制造冲突和转折
3. **结尾完整**：用圆满的结局、反转或爽点结尾，解决所有冲突，给读者完整的阅读体验（不要留悬念）
4. **词汇融入**：在人物心理、对话、动作、环境等不同场景中分散使用单词
5. **上下文提示**：确保单词出现时，上下文足够清晰，让读者能理解含义

记住：你的目标是写出一篇让读者感到爽快和满足的完整短篇小说，同时让读者在不知不觉中学会这些雅思单词。每篇故事都是独立的，不需要续集。"""


def load_story_config() -> Dict:
    """加载故事配置文件"""
    if not os.path.exists(STORY_CONFIG_FILE):
        raise FileNotFoundError(
            f"故事配置文件 {STORY_CONFIG_FILE} 不存在，请先创建配置文件"
        )
    
    with open(STORY_CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_full_prompt(
    target_vocab: List[str],
    review_vocab: List[str],
    story_context: Dict
) -> str:
    """
    构建完整的 Prompt（包含 System Prompt 和 User Prompt）
    
    Args:
        target_vocab: 核心词表
        review_vocab: 复习词表
        story_context: 故事上下文
    
    Returns:
        完整的 Prompt 文本
    """
    prompt_parts = []
    
    # System Prompt
    prompt_parts.append("=== System Prompt ===")
    prompt_parts.append(SYSTEM_PROMPT)
    prompt_parts.append("")
    prompt_parts.append("=" * 60)
    prompt_parts.append("")
    
    # User Prompt
    prompt_parts.append("=== User Prompt ===")
    prompt_parts.append("")
    
    # 1. 故事上下文
    prompt_parts.append("## 故事背景")
    if story_context.get("genre"):
        prompt_parts.append(f"**流派**：{story_context['genre']}")
    if story_context.get("theme"):
        prompt_parts.append(f"**故事主题/爽点**：{story_context['theme']}")
    elif story_context.get("chapter_outline"):  # 兼容旧配置
        prompt_parts.append(f"**故事主题/爽点**：{story_context['chapter_outline']}")
    prompt_parts.append("")
    
    # 2. 核心词汇
    prompt_parts.append("## 核心词汇（必须全部使用）")
    vocab_list = "\n".join([f"- {word}" for word in target_vocab])
    prompt_parts.append(vocab_list)
    prompt_parts.append("")
    
    # 3. 复习词汇
    if review_vocab:
        prompt_parts.append("## 复习词汇（自然融入，可适当降低密度）")
        review_list = "\n".join([f"- {word}" for word in review_vocab])
        prompt_parts.append(review_list)
        prompt_parts.append("")
    
    # 4. 输出要求
    prompt_parts.append("## 输出要求")
    prompt_parts.append("1. 直接输出小说内容，不要任何说明文字")
    prompt_parts.append("2. 所有雅思单词必须使用 {word|meaning} 格式")
    prompt_parts.append("3. 确保剧情紧凑、有冲突、有高潮，结局完整（不要留悬念）")
    prompt_parts.append("4. 确保所有核心词汇都被使用，且分布均匀")
    prompt_parts.append("5. **重要：这是一个完整的短篇小说，不是章节，要求：**")
    prompt_parts.append("   - 字数严格控制在 1500 字左右（1400-1600字），不要超过或少于这个范围")
    prompt_parts.append("   - 必须是一个完整的故事，有开头、发展、高潮、完整结尾")
    prompt_parts.append("   - 故事要完整，能够独立阅读，不需要续集")
    prompt_parts.append("   - 所有冲突都要在故事中解决，不要留下悬念、钩子或未完成的剧情")
    prompt_parts.append("   - 要给读者一个完整、圆满的阅读体验")
    
    return "\n".join(prompt_parts)


def main():
    """主函数"""
    print("=" * 60)
    print("📝 步骤1：智能选词与 Prompt 生成器")
    print("=" * 60)
    print()
    
    try:
        parser = argparse.ArgumentParser(description="步骤1：智能选词与 Prompt 生成器")
        parser.add_argument(
            "--prefer-missing",
            action="store_true",
            help="优先从 missing_ielts_words.txt（补漏词池）里抽取新词，不够再从 pending 补齐",
        )
        parser.add_argument(
            "--missing-file",
            type=str,
            default=MISSING_POOL_FILE,
            help="补漏词池文件路径（默认 tools/missing_ielts_words.txt）",
        )
        args = parser.parse_args()

        # 1. 初始化课程管理器
        print("📚 初始化课程管理器...")
        manager = CurriculumManager(PROGRESS_FILE)
        manager.print_statistics()
        
        # 2. 获取单词批次
        # 目标：覆盖4000词/50篇 = 80词/篇
        # 配置：60新词 + 20复习词 = 80词/篇
        batch_size = 60  # 新词
        review_size = 20  # 复习词
        
        print(f"\n📖 获取新单词批次（{batch_size}个）...")
        prefer_pool: List[str] = []
        if args.prefer_missing and os.path.exists(args.missing_file):
            with open(args.missing_file, "r", encoding="utf-8") as f:
                prefer_pool = [line.strip() for line in f.readlines() if line.strip()]
            print(f"🎯 补漏模式开启：优先词池 {len(prefer_pool)} 个（来自 {args.missing_file}）")
        elif args.prefer_missing:
            print(f"⚠️  补漏模式开启，但找不到词池文件：{args.missing_file}（将退化为正常顺序选词）")

        target_vocab = manager.get_next_batch(batch_size, prefer_pool=prefer_pool)
        
        if not target_vocab:
            raise ValueError("没有可用的新单词，请检查进度追踪文件")
        
        print(f"新单词：{target_vocab}")
        
        # 获取复习单词
        review_vocab = manager.get_review_batch(review_size)
        if review_vocab:
            print(f"\n🔄 获取复习单词（{len(review_vocab)}个）...")
            print(f"复习单词：{review_vocab}")
        else:
            print(f"\n⚠️  提示：暂无复习单词（首次生成）")
            review_vocab = []
        
        # 3. 加载故事配置
        print(f"\n📝 加载故事配置...")
        story_context = load_story_config()
        print(f"流派：{story_context.get('genre', 'N/A')}")
        
        # 4. 构建完整 Prompt
        print(f"\n✨ 生成 Prompt...")
        full_prompt = build_full_prompt(target_vocab, review_vocab, story_context)
        
        # 5. 保存 Prompt 到文件
        with open(PROMPT_OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(full_prompt)
        
        print(f"\n✅ Prompt 已保存到：{PROMPT_OUTPUT_FILE}")
        print()
        print("=" * 60)
        print("📋 生成的 Prompt（可直接复制到 ChatGPT）：")
        print("=" * 60)
        print()
        print(full_prompt)
        print()
        print("=" * 60)
        print()
        print("💡 使用说明：")
        print("1. 复制上面的 Prompt 到 ChatGPT（网页版）")
        print("2. 将 ChatGPT 生成的内容复制到 tools/raw_story.txt")
        print("3. 运行 python tools/step2_save_chapter.py 完成入库")
        print()
        print("⚠️  注意：此时尚未更新学习进度，需等待步骤2完成")
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

