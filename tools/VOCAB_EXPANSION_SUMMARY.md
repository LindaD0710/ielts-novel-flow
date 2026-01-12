# 词库扩充总结

## 🎯 目标
将 `ielts_source.json` 从当前 74 个单词扩充到 4000 个雅思核心词

## 📋 步骤

### 1. 获取词库资源

**推荐来源：**
- 雅思官方词汇表
- 在线资源（小站雅思等）
- 词库文件（JSON/TXT 格式）

### 2. 使用扩充工具

**如果有文本文件（每行一个单词）：**
\`\`\`bash
cd tools
python3 expand_vocab.py your_vocab_file.txt
\`\`\`

**如果手动添加：**
直接编辑 \`tools/ielts_source.json\`，添加单词到数组中

### 3. 验证扩充结果

\`\`\`bash
python3 -c "import json; w=json.load(open('ielts_source.json')); print(f'总词数: {len(set(w))} 个')"
\`\`\`

### 4. 更新配置（词库扩充后）

修改 \`step1_get_prompt.py\`：
\`\`\`python
batch_size = 60  # 新词
review_size = 20  # 复习词
\`\`\`

## 📝 详细文档

查看 \`tools/VOCAB_EXPANSION.md\` 获取完整指南
