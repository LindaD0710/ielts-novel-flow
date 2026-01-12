# 半自动内容生产流使用指南

## 概述

为了节省 API 调用成本，我们采用"人机协同"模式：
- **Python 脚本**：负责选词和生成 Prompt
- **ChatGPT（网页版）**：负责生成内容
- **Python 脚本**：负责格式化和入库

## 工作流程

```
步骤1：运行 step1_get_prompt.py
    ↓
生成 Prompt（包含单词列表和剧情要求）
    ↓
复制 Prompt 到 ChatGPT（网页版）
    ↓
ChatGPT 生成章节内容
    ↓
将内容粘贴到 raw_story.txt
    ↓
步骤2：运行 step2_save_chapter.py
    ↓
验证格式 → 保存入库 → 更新进度
```

## 详细步骤

### 步骤1：生成 Prompt

```bash
cd tools
python step1_get_prompt.py
```

**输出**：
- 在控制台打印完整的 Prompt
- 保存到 `tools/current_prompt.txt` 文件

**Prompt 包含**：
- System Prompt（角色设定和写作要求）
- User Prompt（故事背景、单词列表、输出要求）

**重要**：此时**不更新**学习进度，因为内容还没生成。

### 步骤2：使用 ChatGPT 生成内容

1. 打开 `tools/current_prompt.txt`
2. 复制全部内容
3. 粘贴到 ChatGPT（网页版）
4. 等待 ChatGPT 生成章节内容
5. 复制 ChatGPT 的回复内容

### 步骤3：保存和入库

1. 将 ChatGPT 生成的内容粘贴到 `tools/raw_story.txt`
2. 运行入库脚本：

```bash
python step2_save_chapter.py
```

**脚本会自动**：
- 验证内容格式（检查 `{word|meaning}` 标记）
- 提取章节标题
- 保存到 `src/data/generated/chapter_XXX.json`
- 调用 `mark_as_learned()` 更新学习进度
- 增加章节计数

## 文件说明

### 输入文件

- `progress_tracker.json` - 学习进度追踪（自动管理）
- `story_config.json` - 故事配置（剧情大纲）
- `ielts_source.json` - 词源列表

### 中间文件

- `current_prompt.txt` - 生成的 Prompt（步骤1输出）
- `raw_story.txt` - 用户粘贴的原始内容（步骤2输入）

### 输出文件

- `src/data/generated/chapter_XXX.json` - 生成的章节数据

## 优势

✅ **节省成本**：使用免费的 ChatGPT 网页版，无需 API 费用  
✅ **质量控制**：可以人工审核 ChatGPT 生成的内容  
✅ **灵活调整**：可以要求 ChatGPT 重新生成或修改  
✅ **自动化**：选词、进度管理、入库全部自动化  

## 注意事项

1. **格式要求**：确保 ChatGPT 生成的内容使用了 `{word|meaning}` 格式
2. **进度更新**：只有运行 `step2_save_chapter.py` 后才会更新学习进度
3. **文件清理**：步骤2完成后可以选择清空 `raw_story.txt`
4. **Prompt 保留**：建议保留 `current_prompt.txt`，以便步骤2提取单词列表

## 故障排除

### 问题：步骤1 提示没有可用单词

- 检查 `progress_tracker.json` 是否存在
- 检查 `ielts_source.json` 是否存在
- 如果进度文件损坏，删除它让系统重新初始化

### 问题：步骤2 提示格式验证失败

- 检查 `raw_story.txt` 中是否包含 `{word|meaning}` 格式
- 确保 ChatGPT 严格按照 Prompt 要求生成内容
- 可以手动检查并修正格式

### 问题：步骤2 无法提取目标单词

- 确保 `current_prompt.txt` 文件存在（步骤1的输出）
- 如果文件丢失，可以手动在步骤2中指定单词列表

## 示例

### 完整流程示例

```bash
# 1. 生成 Prompt
cd tools
python step1_get_prompt.py

# 2. （手动）复制 Prompt 到 ChatGPT，生成内容，粘贴到 raw_story.txt

# 3. 保存入库
python step2_save_chapter.py
```

### 输出示例

**步骤1输出**：
```
📚 初始化课程管理器...
📊 学习进度统计
==================================================
总词汇量：74 个
已学习：0 个
待学习：74 个
学习进度：0.0%
当前章节：第 1 章
==================================================

📖 获取新单词批次（20个）...
新单词：['ambitious', 'meticulous', ...]

✅ Prompt 已保存到：tools/current_prompt.txt
```

**步骤2输出**：
```
📖 读取原始故事内容...
✅ 已读取 2345 字符

🔍 验证内容格式...
✅ 格式验证通过，发现 25 个单词标记

✅ 更新学习进度...
✅ 已标记 20 个单词为已学习

🎉 处理完成！
```

