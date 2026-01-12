# IELTS Novel Flow - 内容生成工具

这个工具用于生成包含雅思词汇的爽文章节。

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或者使用虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 配置

### 方式一：环境变量（推荐）

```bash
# 使用 OpenAI
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o"

# 或使用 DeepSeek
export OPENAI_API_KEY="your-deepseek-api-key"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
export OPENAI_MODEL="deepseek-chat"
```

### 方式二：.env 文件

在 `tools` 目录下创建 `.env` 文件：

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
```

然后在代码中添加：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 使用方法

### 基本用法

直接运行脚本（使用示例数据）：

```bash
python novel_generator.py
```

### 自定义用法

修改 `main()` 函数中的参数：

```python
# 核心词汇（必须全部使用）
target_vocab = [
    "ambitious", "meticulous", "prestigious", "sophisticated",
    "resilient", "elaborate", "profound", "intricate"
]

# 复习词汇（可选，自然融入）
review_vocab = [
    "ambitious", "meticulous"
]

# 故事上下文
story_context = {
    "genre": "重生霸总",
    "prev_summary": "前情提要...",
    "chapter_outline": "本章大纲/爽点..."
}

# 生成章节
chapter = generate_chapter(
    target_vocab=target_vocab,
    review_vocab=review_vocab,
    story_context=story_context,
    chapter_title="第三章：商业晚宴"  # 可选，不提供则自动生成
)

# 保存章节
save_chapter(chapter, filename="chapter_003.json")
```

### 作为模块导入

```python
from novel_generator import generate_chapter, save_chapter

# 生成章节
chapter = generate_chapter(
    target_vocab=["word1", "word2", ...],
    review_vocab=["review1", "review2", ...],
    story_context={
        "genre": "重生霸总",
        "prev_summary": "...",
        "chapter_outline": "..."
    }
)

# 保存
save_chapter(chapter)
```

## 输出格式

生成的章节会保存为 JSON 文件，格式符合 TypeScript 的 `Chapter` 接口：

```json
{
  "id": "chapter-20250105-143022",
  "title": "第三章：商业晚宴",
  "content": "章节内容，包含 {word|meaning} 格式的标记..."
}
```

文件保存在 `generated_chapters/` 目录下。

## 核心特性

1. **平衡爽感和学习效率**：强大的 System Prompt 确保剧情紧凑有冲突，同时自然融入词汇
2. **词汇覆盖验证**：自动检查所有核心词汇是否都被使用
3. **格式严格**：确保所有单词都使用 `{word|meaning}` 格式
4. **密度控制**：避免词汇堆砌，确保阅读体验流畅
5. **支持复习**：可指定复习词汇，实现艾宾浩斯复现

## 注意事项

1. **API Key**：请确保设置了正确的 API Key
2. **成本控制**：生成一个章节大约消耗 2000-4000 tokens，请注意成本
3. **词汇验证**：如果某些词汇未出现，脚本会警告，建议检查或重新生成
4. **内容质量**：首次生成可能不完美，可以多次尝试或手动调整

## 故障排除

### 问题：API 调用失败

- 检查 API Key 是否正确
- 检查网络连接
- 检查 BASE_URL 是否正确（OpenAI vs DeepSeek）

### 问题：词汇未全部使用

- 检查词汇列表是否过长（建议 15-25 个）
- 尝试增加章节长度要求
- 手动检查生成的内容，可能需要重新生成

### 问题：内容质量不佳

- 调整 `temperature` 参数（0.7-0.9）
- 优化 `story_context` 中的大纲和爽点
- 多次生成并选择最佳结果

