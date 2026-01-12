# 智能课程管理系统使用指南

## 概述

智能课程管理系统实现了自动化的学习进度追踪和章节生成，无需手动管理单词列表。

## 系统架构

### 1. 进度追踪文件 (`progress_tracker.json`)

记录全局学习进度：
- `total_words`: 总词汇量
- `learned_words`: 已学习的单词列表
- `pending_words`: 待学习的单词列表
- `current_book_chapter`: 当前章节号

### 2. 课程管理器 (`curriculum_manager.py`)

核心功能：
- `get_next_batch(batch_size=20)`: 获取下一批新单词
- `get_review_batch(batch_size=5)`: 获取复习单词（随机）
- `mark_as_learned(word_list)`: 标记单词为已学习
- `increment_chapter()`: 增加章节计数
- `get_statistics()`: 获取学习统计

### 3. 故事配置 (`story_config.json`)

专注于剧情设定：
- `genre`: 小说流派
- `prev_summary`: 前情提要
- `chapter_outline`: 本章大纲/爽点

### 4. 升级后的生成器 (`novel_generator.py`)

自动化的生成流程：
1. 读取故事配置
2. 从课程管理器获取单词（新词 + 复习词）
3. 生成章节
4. 自动标记单词为已学习
5. 更新进度追踪

## 使用流程

### 首次使用

1. **初始化进度追踪**（如果不存在会自动从 `ielts_source.json` 初始化）

2. **配置故事**：编辑 `story_config.json`

3. **生成章节**：
```bash
python novel_generator.py
```

### 工作流程

```
运行 novel_generator.py
    ↓
读取 progress_tracker.json（如果不存在，从 ielts_source.json 初始化）
    ↓
读取 story_config.json 获取剧情设定
    ↓
调用课程管理器：
  - get_next_batch(20) → 获取20个新单词
  - get_review_batch(5) → 获取5个复习单词
    ↓
调用 LLM 生成章节（包含新词和复习词）
    ↓
生成成功后：
  - mark_as_learned(新单词列表)
  - increment_chapter()
  - 更新 progress_tracker.json
    ↓
保存章节到 generated_chapters/
```

## 示例

### 生成第一章

```bash
python novel_generator.py
```

输出：
```
📚 初始化课程管理器...
📊 学习进度统计
==================================================
总词汇量：70 个
已学习：0 个
待学习：70 个
学习进度：0.0%
当前章节：第 1 章
==================================================

📖 获取新单词批次（20个）...
新单词：['ambitious', 'meticulous', ...]

🔄 获取复习单词（5个）...
（首次运行，没有复习单词）

📝 加载故事配置...
流派：都市重生

✨ 开始生成章节...
正在生成章节：第一章：命运的转折...
核心词汇数量：20

✅ 标记单词为已学习...
✅ 已标记 20 个单词为已学习
   待学习：50 个，已学习：20 个

📊 学习进度统计
==================================================
总词汇量：70 个
已学习：20 个
待学习：50 个
学习进度：28.57%
当前章节：第 2 章
==================================================
```

### 生成第二章

再次运行：
```bash
python novel_generator.py
```

系统会自动：
- 从剩余的 50 个单词中取出 20 个新单词
- 从已学习的 20 个单词中随机选择 5 个复习
- 生成第二章
- 更新进度

## 自定义配置

### 调整批次大小

编辑 `novel_generator.py` 的 `main()` 函数：

```python
chapter = generate_chapter_with_curriculum(
    batch_size=25,  # 每章25个新单词
    review_size=8,  # 每章8个复习单词
)
```

### 更新故事配置

编辑 `story_config.json`：

```json
{
  "genre": "悬疑推理",
  "prev_summary": "上一章主角发现了关键线索...",
  "chapter_outline": "主角追踪线索，发现真相，但陷入更大的危机..."
}
```

## 进度管理

### 查看进度

```python
from curriculum_manager import CurriculumManager

manager = CurriculumManager()
manager.print_statistics()
```

### 手动重置进度

删除 `progress_tracker.json`，系统会在下次运行时从 `ielts_source.json` 重新初始化。

### 手动标记单词

```python
from curriculum_manager import CurriculumManager

manager = CurriculumManager()
manager.mark_as_learned(["word1", "word2"])
```

## 注意事项

1. **首次运行**：确保 `ielts_source.json` 存在
2. **配置文件**：确保 `story_config.json` 存在
3. **进度文件**：`progress_tracker.json` 会自动创建和更新
4. **词汇覆盖**：系统会验证所有新单词是否在生成的内容中出现

## 优势

✅ **自动化**：无需手动管理单词列表  
✅ **进度追踪**：自动记录学习进度  
✅ **复习机制**：自动安排复习单词  
✅ **系统化**：确保完整覆盖词汇库  
✅ **可扩展**：易于添加新功能

