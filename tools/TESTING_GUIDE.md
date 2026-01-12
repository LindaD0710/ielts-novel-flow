# 半自动内容生产流 - 完整测试指南（按类型独立追踪）

## 🎯 核心机制说明

### 按类型独立追踪词库

**工作原理：**
- 每个小说类型使用**独立的进度文件**
- 重生类型：`progress_tracker_reborn.json`
- 悬疑类型：`progress_tracker_suspense.json`
- 言情类型：`progress_tracker_romance.json`
- 商战类型：`progress_tracker_business.json`

**优势：**
- ✅ 每类小说都从完整的词库（4000词）重新开始
- ✅ 用户只读一类小说也能学完所有词
- ✅ 不同类型之间互不影响
- ✅ 每类小说都有完整的学习路径

---

## 📋 完整测试步骤

### **步骤 1：生成 Prompt（获取原材料）**

```bash
cd "/Users/lindadong/Desktop/小创意/【破局】AI编程出海/IELTS Novel Flow/tools"
python3 step1_get_prompt.py
```

**预期输出：**
- 显示学习进度统计（使用默认的全局进度文件）
- 生成包含 20 个新词和 5 个复习词的 Prompt
- 保存到 `current_prompt.txt`

**注意：**
- 步骤1使用全局进度文件（不影响类型独立追踪）
- 实际的类型独立追踪在步骤2中生效

---

### **步骤 2：使用 ChatGPT 生成内容**

1. **打开 Prompt 文件**
   ```bash
   cat current_prompt.txt
   # 或使用编辑器
   code current_prompt.txt
   ```

2. **复制完整 Prompt**（包括 System Prompt 和 User Prompt）

3. **访问 ChatGPT**：https://chat.openai.com

4. **粘贴 Prompt**，等待生成内容

5. **复制生成的内容**到 `raw_story.txt`

**重要检查点：**
- ✅ 内容包含 `{word|meaning}` 格式标记
- ✅ 字数约 1400-1600 字
- ✅ 只复制小说内容，不要其他说明

---

### **步骤 3：入库上架（关键步骤 - 选择类型）**

```bash
python3 step2_save_chapter.py
```

#### 3.1 交互流程

**3.1.1 验证格式和字数**
```
📖 读取原始故事内容...
✅ 已读取 2845 字符

🔍 验证内容格式...
✅ 格式验证通过，发现 25 个单词标记

📏 验证字数...
✅ 字数符合要求（约 1422 字）
```

**3.1.2 选择分类（类型）** ⚠️ **关键步骤**
```
📚 选择书籍分类（类型）...
可选分类：
  1. 重生 (reborn)
  2. 悬疑 (suspense)
  3. 言情 (romance)
  4. 商战 (business)

请选择分类编号（1-4）：1
✅ 已选择分类：重生
💡 提示：此分类将使用独立的进度文件，确保可以重新调用完整的词库
📁 使用进度文件：progress_tracker_reborn.json
```

**重要说明：**
- ✅ 选择的类型决定了使用哪个进度文件
- ✅ 每个类型都有独立的进度文件
- ✅ 第一次使用某类型时，会自动创建该类型的进度文件
- ✅ 该类型会从完整的词库（4000词）重新开始

**3.1.3 选择或创建书籍**
```
📖 选择或创建书籍...

找到 3 本同分类书籍：
  1. 顶级豪门的继承人 - 流年 (ID: book-001)
  2. 重生之商业女王 - 佚名 (ID: book-002)
  3. 创建新书籍

请选择书籍编号（1-3）：3
```

**如果选择"创建新书籍"：**
- 输入书名（或直接回车使用自动提取）
- 输入作者（或直接回车使用默认）

**3.1.4 处理数据（使用类型对应的进度文件）**
```
📚 初始化课程管理器...
   使用分类进度文件：progress_tracker_reborn.json
当前章节号：1
   分类：重生 - 此分类使用独立的词库进度，不影响其他分类

🔍 提取目标单词列表...
✅ 从 Prompt 文件提取到 20 个目标单词

💾 保存章节...
✅ 章节已保存：../src/data/generated/book-20240108123456.json

✅ 更新学习进度...
✅ 已标记 20 个单词为已学习

📊 更新后的学习进度：
==================================================
总词汇量：4000 个  # 注意：这是该类型独立的进度
已学习：20 个
待学习：3980 个
学习进度：0.5%
当前章节：第 2 章
==================================================
```

**关键点：**
- ✅ 进度文件是 `progress_tracker_reborn.json`（而不是全局的 `progress_tracker.json`）
- ✅ 该类型的进度从 0 开始（如果是第一次）
- ✅ 已学习的单词只记录在该类型的进度文件中
- ✅ 其他类型的进度不受影响

---

### **步骤 4：验证结果**

#### 4.1 检查进度文件

```bash
# 查看重生类型的进度文件
cat progress_tracker_reborn.json

# 查看其他类型的进度文件（如果存在）
ls -la progress_tracker_*.json

# 对比不同类型（如果有多个类型）
cat progress_tracker_reborn.json | head -20
cat progress_tracker_suspense.json | head -20  # 如果有
```

**预期结果：**
- 每个类型有独立的进度文件
- 每个类型的 `pending_words` 都包含完整的词库（4000词）
- 每个类型的 `learned_words` 独立记录该类型已学习的单词

#### 4.2 检查生成的文件

```bash
# 检查章节文件
ls -la ../src/data/generated/book-*.json

# 检查 library.ts
cat ../src/data/library.ts | tail -20
```

#### 4.3 前端验证

```bash
cd ..
npm run dev
```

访问：
1. `http://localhost:3000` → 登录
2. `http://localhost:3000/library` → 查看图书馆
3. 选择对应的分类 → 应该能看到新创建的书籍
4. 点击"开始阅读" → 验证内容显示

---

## 🔄 测试不同类别

### 测试场景：创建重生类型小说后，再创建悬疑类型小说

**步骤：**

1. **创建重生类型小说**
   ```bash
   python3 step2_save_chapter.py
   # 选择：1. 重生
   # 创建新书籍：重生小说1
   ```

2. **检查重生类型进度**
   ```bash
   cat progress_tracker_reborn.json
   # 应该显示：已学习 20 个单词，待学习 3980 个
   ```

3. **创建悬疑类型小说**
   ```bash
   python3 step2_save_chapter.py
   # 选择：2. 悬疑
   # 创建新书籍：悬疑小说1
   ```

4. **检查悬疑类型进度**
   ```bash
   cat progress_tracker_suspense.json
   # 应该显示：已学习 20 个单词，待学习 3980 个
   # 注意：这是悬疑类型的独立进度，和重生类型互不影响
   ```

5. **验证词库重新调用**
   - 悬疑类型从完整的 4000 词库重新开始
   - 悬疑类型的 `pending_words` 包含完整的 4000 词
   - 悬疑类型和重生类型的进度互不影响

---

## ⚠️ 人工操作注意事项

### 关键注意事项

1. **选择正确的类型**
   - ⚠️ 在步骤2中，**必须选择正确的分类编号**
   - ⚠️ 选择错误的类型会导致使用错误的进度文件
   - ✅ 每个类型都有独立的进度，互不影响

2. **进度文件管理**
   - ✅ 第一次使用某类型时，会自动创建该类型的进度文件
   - ✅ 每个类型的进度文件是独立的，互不干扰
   - ✅ 如果要重置某类型的进度，删除对应的进度文件即可：
     ```bash
     rm progress_tracker_reborn.json  # 重置重生类型进度
     ```

3. **词库共享，进度独立**
   - ✅ 所有类型共享同一个词库文件（`ielts_source.json`）
   - ✅ 但每个类型有独立的进度文件（`progress_tracker_{category}.json`）
   - ✅ 这样确保每类小说都能从完整的词库重新开始

4. **词汇量配置（如果词库已扩充到4000词）**
   - 如果 `ielts_source.json` 已扩充到 4000 词
   - 建议修改 `step1_get_prompt.py`：
     ```python
     batch_size = 60  # 新词（从20增加到60）
     review_size = 20  # 复习词（从5增加到20）
     ```
   - 这样每篇80词，50篇可以覆盖4000词

---

## 📊 进度文件说明

### 进度文件命名规则

```
progress_tracker_{category_id}.json
```

**示例：**
- `progress_tracker_reborn.json` - 重生类型
- `progress_tracker_suspense.json` - 悬疑类型
- `progress_tracker_romance.json` - 言情类型
- `progress_tracker_business.json` - 商战类型

### 进度文件结构

```json
{
  "total_words": 4000,
  "learned_words": ["ambitious", "meticulous", ...],
  "pending_words": ["word1", "word2", ...],
  "current_book_chapter": 1
}
```

**说明：**
- `total_words`: 总词汇量（应该是4000）
- `learned_words`: 该类型已学习的单词列表
- `pending_words`: 该类型待学习的单词列表
- `current_book_chapter`: 该类型的小说计数（用于命名）

---

## ✅ 测试检查清单

### 单类型测试
- [ ] 选择重生类型，创建小说
- [ ] 检查 `progress_tracker_reborn.json` 已创建
- [ ] 验证进度从 0 开始（如果是第一次）
- [ ] 验证已学习的单词只记录在该类型的进度文件中

### 多类型测试
- [ ] 创建重生类型小说（使用 `progress_tracker_reborn.json`）
- [ ] 创建悬疑类型小说（使用 `progress_tracker_suspense.json`）
- [ ] 验证两个进度文件独立存在
- [ ] 验证悬疑类型从完整的4000词库重新开始
- [ ] 验证两个类型的进度互不影响

### 前端验证
- [ ] 前端能显示不同分类的书籍
- [ ] 点击书籍能正常阅读
- [ ] 单词标记能正确点击和显示

---

## 🐛 常见问题

### 问题1：选错类型了怎么办？

**解决：**
- 如果还没完成入库，直接重新运行 `step2_save_chapter.py`
- 如果已完成入库，可以手动移动进度文件，或者接受结果（每类小说都需要50篇）

### 问题2：如何重置某类型的进度？

**解决：**
```bash
# 删除该类型的进度文件
rm progress_tracker_reborn.json

# 下次使用该类型时，会自动重新初始化
```

### 问题3：如何查看某个类型的进度？

**解决：**
```bash
# 查看进度文件
cat progress_tracker_reborn.json

# 或使用 Python 查看统计
python3 -c "
from curriculum_manager import CurriculumManager, get_progress_file_for_category
manager = CurriculumManager(get_progress_file_for_category('reborn'))
manager.print_statistics()
"
```

---

## 💡 最佳实践

1. **保持一致的类型选择**
   - 同一批小说使用同一类型，便于管理

2. **定期检查进度**
   - 检查每个类型的进度文件，确保学习进度正常

3. **词库扩充**
   - 优先扩充 `ielts_source.json` 到 4000 词
   - 然后修改词汇量配置（60+20）

4. **进度备份**
   - 定期备份进度文件，避免意外丢失

---

祝你测试顺利！如有问题，请参考常见问题部分或告诉我具体情况。

