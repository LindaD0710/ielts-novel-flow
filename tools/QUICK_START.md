# 快速开始 - 半自动工作流

## 三步走

### 1️⃣ 生成 Prompt

```bash
cd tools
python step1_get_prompt.py
```

**结果**：
- 控制台显示完整 Prompt
- 保存到 `current_prompt.txt`

### 2️⃣ 使用 ChatGPT 生成

1. 打开 `current_prompt.txt`
2. 复制全部内容
3. 粘贴到 ChatGPT（网页版）
4. 复制 ChatGPT 的回复
5. 粘贴到 `raw_story.txt`

### 3️⃣ 保存入库

```bash
python step2_save_chapter.py
```

**结果**：
- 验证格式
- 保存到 `src/data/generated/chapter_XXX.json`
- 更新学习进度

## 完成！

章节已保存，可以继续生成下一章。
