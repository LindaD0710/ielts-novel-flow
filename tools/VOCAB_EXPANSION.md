# 扩充词库到 4000 词 - 完整指南

## 📊 当前状态

- **当前词库**：74 个单词
- **目标词库**：4000 个单词
- **需要扩充**：3926 个单词

---

## 🔍 词库来源

### 推荐的资源

1. **官方/权威资源**
   - 雅思官方词汇表
   - Cambridge IELTS Vocabulary
   - British Council 官方词汇

2. **在线资源**
   - 小站雅思（提供词汇分类和数量信息）
   - 各种雅思学习网站的词库
   - Quizlet 雅思词汇集
   - Anki 雅思词库

3. **视频/书籍**
   - YouTube: "IELTS雅思核心词汇及词组（3497词）"
   - 书籍: "4000 Essential English Words"

---

## 🔧 扩充方法

### 方法 1：使用扩充脚本（推荐）

如果你有文本格式的词库文件（每行一个单词）：

```bash
cd tools

# 假设你有一个 vocab_list.txt 文件（每行一个单词）
python3 expand_vocab.py vocab_list.txt
```

**文本文件格式示例：**
```
abandon
ability
abroad
absolute
absorb
...
```

### 方法 2：手动添加到 JSON 文件

如果你有少量单词，可以直接编辑 JSON 文件：

```bash
code tools/ielts_source.json
```

在数组中添加单词：
```json
[
  "existing_word1",
  "existing_word2",
  "new_word1",
  "new_word2",
  ...
]
```

### 方法 3：使用 Python 脚本批量添加

```python
# 如果你有单词列表（Python 列表格式）
import json
from expand_vocab import expand_vocab_manually

new_words = [
    "word1",
    "word2",
    "word3",
    # ... 更多单词
]

expand_vocab_manually(new_words)
```

---

## 📝 词库格式要求

**JSON 格式：**
```json
[
  "word1",
  "word2",
  "word3"
]
```

**要求：**
- 只包含单词（小写，不需要音标、释义等）
- 每个单词是独立的字符串
- 可以重复（脚本会自动去重）
- 建议使用小写字母

---

## ✅ 扩充后的验证

```bash
cd tools

# 检查词库数量
python3 << 'EOF'
import json
with open('ielts_source.json', 'r') as f:
    words = json.load(f)
unique_words = list(set(words))
print(f"总词数：{len(unique_words)} 个")
print(f"目标：4000 个")
if len(unique_words) >= 4000:
    print("✅ 已达到目标！")
else:
    print(f"⚠️  还需 {4000 - len(unique_words)} 个")
EOF
```

---

## 💡 建议的扩充流程

1. **获取词库资源**
   - 从上述资源中获取 4000 个雅思核心词
   - 整理为文本格式（每行一个单词）

2. **使用脚本导入**
   ```bash
   python3 expand_vocab.py vocab_list.txt
   ```

3. **验证词库**
   - 检查词库数量是否达到 4000
   - 检查是否有重复或格式错误

4. **更新配置**
   - 词库扩充后，可以修改 `step1_get_prompt.py`：
     ```python
     batch_size = 60  # 新词
     review_size = 20  # 复习词
     ```

---

## ⚠️ 注意事项

1. **版权问题**：确保使用的词库资源符合版权要求
2. **词库质量**：优先使用权威来源的词汇表
3. **格式统一**：确保所有单词都是小写、纯字母
4. **去重处理**：脚本会自动去重，无需担心重复

