# 正式生产指南

## 🎯 当前状态

✅ **已清空所有测试内容**
- 所有章节文件已删除
- 所有进度文件已删除
- library.ts 已清空
- novelService.ts 已清空章节导入

✅ **已保留的重要文件**
- `vocab_db.json` - 词汇库（保留）
- `ielts_source.json` - 词源库（3665 词，保留）
- 所有工具脚本（step1, step2 等）

---

## 📋 正式生产流程

### 步骤 1：生成 Prompt

```bash
cd tools
python3 step1_get_prompt.py
```

**输出：**
- 生成 `current_prompt.txt` 文件
- 包含 60 个新词 + 20 个复习词（80 词/篇）

---

### 步骤 2：使用 ChatGPT 生成内容

1. 打开 `tools/current_prompt.txt`
2. 复制全部内容到 ChatGPT
3. 等待生成内容
4. 复制生成的内容到 `tools/raw_story.txt`

**检查点：**
- ✅ 内容包含 `{word|meaning}` 格式标记
- ✅ 字数约 1400-1600 字
- ✅ 故事完整，有开头、发展、高潮、结尾

---

### 步骤 3：入库上架

```bash
python3 step2_save_chapter.py
```

**交互步骤：**
1. 验证字数（输入 `y` 继续）
2. **选择分类**（1-4，重要！）
3. 选择或创建书籍
4. 输入书名和作者
5. 完成入库

**输出：**
- 生成章节文件：`src/data/generated/book-{timestamp}.json`
- 自动更新：`src/data/library.ts`
- 更新进度：`tools/progress_tracker_{category}.json`

---

### 步骤 4：更新前端导入（重要！）

**每次生产新小说后，需要手动更新 `src/services/novelService.ts`：**

1. 打开 `src/services/novelService.ts`
2. 在文件顶部添加导入：
   ```typescript
   import bookXxxData from "../data/generated/book-{timestamp}.json";
   ```
3. 在 `allChaptersData` 数组中添加：
   ```typescript
   bookXxxData as Chapter,
   ```

**示例：**
```typescript
// 导入章节文件
import book20260111160439Data from "../data/generated/book-20260111160439.json";

const allChaptersData: Chapter[] = [
  book20260111160439Data as Chapter,
].filter((ch) => ch && ch.id);
```

**⚠️ 注意：** 如果不更新 `novelService.ts`，前端将无法加载新章节！

---

## 🔄 自动化改进建议

**未来可以改进：**
- 让 `step2_save_chapter.py` 自动更新 `novelService.ts`
- 或者改用动态导入（但 Next.js 静态导入更稳定）

**当前方案：**
- 手动更新 `novelService.ts`（每次生产后）
- 或者批量生产后再统一更新

---

## 📊 生产计划

### MVP 阶段（5-10 篇）

**目标：** 快速上线，验证市场

**建议：**
- 每天生产 2-3 篇
- 覆盖不同主题和爽点
- 确保质量 > 数量
- 生产完成后统一更新 `novelService.ts`

### 完整内容阶段（50 篇）

**目标：** 达到完整内容量

**建议：**
- 每天生产 2-3 篇
- 每周更新一次 `novelService.ts`
- 持续优化生产流程

---

## ✅ 生产检查清单

每次生产后检查：

- [ ] 章节文件已生成（`src/data/generated/book-*.json`）
- [ ] library.ts 已更新（新书籍已添加）
- [ ] 进度文件已更新（`tools/progress_tracker_{category}.json`）
- [ ] **novelService.ts 已更新（手动添加导入）**
- [ ] 前端可以正常显示新小说

---

## 🐛 常见问题

### 问题 1：前端看不到新小说

**原因：** `novelService.ts` 没有导入新章节文件

**解决：** 手动添加导入（见步骤 4）

### 问题 2：显示错误的小说内容

**原因：** localStorage 缓存了旧的章节 ID

**解决：** 清除浏览器 localStorage 或使用无痕模式

### 问题 3：进度文件冲突

**原因：** 不同分类使用不同的进度文件

**解决：** 这是正常的，每个分类独立追踪

---

## 💡 生产技巧

1. **批量生产**
   - 可以连续生产多篇，最后统一更新 `novelService.ts`
   - 提高效率

2. **质量优先**
   - 每篇都要检查质量
   - 确保故事完整、词汇正确

3. **主题多样化**
   - 不要重复相同的爽点
   - 保持内容新鲜感

4. **定期备份**
   - 定期备份 `src/data/generated/` 目录
   - 备份 `library.ts` 和 `novelService.ts`

---

祝你生产顺利！🎉

