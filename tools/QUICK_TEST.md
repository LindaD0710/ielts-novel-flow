# 快速测试指南 - 按类型独立追踪

## 🎯 核心机制：如何保证不同类型可以重新调用词库？

### 工作原理

**每个小说类型使用独立的进度文件：**

```
重生类型   → progress_tracker_reborn.json
悬疑类型   → progress_tracker_suspense.json  
言情类型   → progress_tracker_romance.json
商战类型   → progress_tracker_business.json
```

**关键点：**
- ✅ 所有类型**共享同一个词库**（`ielts_source.json` - 4000词）
- ✅ 但每个类型有**独立的进度文件**
- ✅ 每个类型都从**完整的4000词库重新开始**
- ✅ 不同类型之间**互不影响**

### 人工操作中的关键注意点

**⚠️ 最重要：选择正确的分类编号！**

在步骤2中，当你看到：
```
请选择分类编号（1-4）：__
```

**必须选择正确的数字**，因为：
- 选择 1（重生）→ 使用 `progress_tracker_reborn.json`
- 选择 2（悬疑）→ 使用 `progress_tracker_suspense.json`
- 选择 3（言情）→ 使用 `progress_tracker_romance.json`
- 选择 4（商战）→ 使用 `progress_tracker_business.json`

**如果选错：**
- 会使用错误的进度文件
- 可能导致词库无法正确重新调用

---

## 📋 完整测试步骤

### **步骤 1：生成 Prompt**

```bash
cd "/Users/lindadong/Desktop/小创意/【破局】AI编程出海/IELTS Novel Flow/tools"
python3 step1_get_prompt.py
```

**输出：** Prompt 保存到 `current_prompt.txt`

---

### **步骤 2：使用 ChatGPT 生成内容**

1. 复制 `current_prompt.txt` 的全部内容
2. 粘贴到 ChatGPT（网页版）
3. 复制 ChatGPT 生成的内容
4. 粘贴到 `raw_story.txt`

---

### **步骤 3：入库上架（⚠️ 关键步骤）**

```bash
python3 step2_save_chapter.py
```

#### 关键交互点：

**3.1 选择分类（类型）** ⚠️ **最重要！**

```
📚 选择书籍分类（类型）...
可选分类：
  1. 重生 (reborn)
  2. 悬疑 (suspense)
  3. 言情 (romance)
  4. 商战 (business)

请选择分类编号（1-4）：1  ← 这里选择正确的数字！
```

**你会看到：**
```
✅ 已选择分类：重生
💡 提示：此分类将使用独立的进度文件，确保可以重新调用完整的词库
📁 使用进度文件：progress_tracker_reborn.json
```

**这意味着：**
- 使用 `progress_tracker_reborn.json` 作为进度文件
- 如果这个文件不存在，会自动创建
- 该类型会从完整的词库（4000词）重新开始

**3.2 选择或创建书籍**

按照提示操作即可。

**3.3 查看进度更新**

```
📚 初始化课程管理器...
   使用分类进度文件：progress_tracker_reborn.json
   分类：重生 - 此分类使用独立的词库进度，不影响其他分类

📊 更新后的学习进度：
==================================================
总词汇量：4000 个  ← 注意：这是该类型的独立进度
已学习：20 个
待学习：3980 个
学习进度：0.5%
==================================================
```

---

### **步骤 4：验证类型独立追踪**

#### 测试场景：创建重生类型后，再创建悬疑类型

**4.1 创建重生类型小说**
```bash
python3 step2_save_chapter.py
# 选择：1. 重生
# 创建新书籍：重生小说1
```

**检查进度文件：**
```bash
cat progress_tracker_reborn.json
# 应该显示：已学习 20 个，待学习 3980 个
```

**4.2 创建悬疑类型小说**
```bash
python3 step2_save_chapter.py
# 选择：2. 悬疑  ← 选择不同的类型
# 创建新书籍：悬疑小说1
```

**检查进度文件：**
```bash
# 查看悬疑类型的进度文件（新创建的）
cat progress_tracker_suspense.json
# 应该显示：已学习 20 个，待学习 3980 个
# 注意：这是悬疑类型的独立进度，和重生类型互不影响

# 对比重生类型的进度（应该不变）
cat progress_tracker_reborn.json
# 应该显示：已学习 20 个，待学习 3980 个
# 注意：重生类型的进度没有改变
```

**验证成功标准：**
- ✅ `progress_tracker_suspense.json` 已创建
- ✅ 悬疑类型的 `pending_words` 包含完整的 4000 词
- ✅ 悬疑类型和重生类型的进度文件都存在且独立
- ✅ 两个类型的 `learned_words` 互不影响

---

## 🔍 如何查看词库和进度？

### 查看词库列表（所有类型共享）

```bash
# 查看完整词库
cat ielts_source.json

# 查看词库数量
python3 -c "import json; words = json.load(open('ielts_source.json')); print(f'总词数: {len(words)}')"
```

### 查看某个类型的进度

```bash
# 查看重生类型进度
cat progress_tracker_reborn.json

# 查看悬疑类型进度（如果存在）
cat progress_tracker_suspense.json

# 查看所有类型的进度文件
ls -la progress_tracker_*.json
```

### 使用 Python 查看进度统计

```bash
python3 << 'EOF'
from curriculum_manager import CurriculumManager, get_progress_file_for_category

# 查看重生类型进度
manager = CurriculumManager(get_progress_file_for_category('reborn'))
manager.print_statistics()

# 查看悬疑类型进度（如果存在）
# manager = CurriculumManager(get_progress_file_for_category('suspense'))
# manager.print_statistics()
EOF
```

---

## ⚠️ 人工操作注意事项总结

### 1. 选择正确的分类编号（最重要！）

- ⚠️ 在步骤2中，**必须选择正确的分类编号**
- ⚠️ 选择错误的类型会导致使用错误的进度文件
- ✅ 每个类型都有独立的进度，互不影响

### 2. 进度文件自动管理

- ✅ 第一次使用某类型时，会自动创建该类型的进度文件
- ✅ 不需要手动创建进度文件
- ✅ 每个类型的进度文件是独立的，互不干扰

### 3. 词库共享，进度独立

- ✅ 所有类型共享同一个词库文件（`ielts_source.json`）
- ✅ 但每个类型有独立的进度文件
- ✅ 这样确保每类小说都能从完整的词库重新开始

### 4. 重置某个类型的进度

如果需要重置某个类型的进度：
```bash
# 删除该类型的进度文件
rm progress_tracker_reborn.json

# 下次使用该类型时，会自动重新初始化
```

---

## ✅ 测试检查清单

### 单类型测试
- [ ] 选择类型（如重生），创建小说
- [ ] 检查对应的进度文件已创建（如 `progress_tracker_reborn.json`）
- [ ] 验证进度从 0 开始（如果是第一次）
- [ ] 验证 `pending_words` 包含完整的词库

### 多类型测试
- [ ] 创建重生类型小说 → 检查 `progress_tracker_reborn.json`
- [ ] 创建悬疑类型小说 → 检查 `progress_tracker_suspense.json`
- [ ] 验证两个进度文件独立存在
- [ ] 验证悬疑类型从完整的词库重新开始
- [ ] 验证两个类型的进度互不影响

---

## 🎯 快速测试命令

```bash
# 1. 生成 Prompt
cd tools && python3 step1_get_prompt.py

# 2. （手动）复制 Prompt → ChatGPT → 粘贴到 raw_story.txt

# 3. 入库上架（选择类型）
python3 step2_save_chapter.py

# 4. 检查进度文件
ls -la progress_tracker_*.json
cat progress_tracker_reborn.json  # 或你选择的类型

# 5. 验证前端
cd .. && npm run dev
```

---

详细文档请查看：`tools/TESTING_GUIDE.md`

