# 🚀 一步一步部署指南

## ✅ 步骤 1：配置 Git 用户信息（必需）

在执行以下命令之前，请告诉我你的：
- GitHub 用户名（或你想使用的名字）
- GitHub 邮箱（或你想使用的邮箱）

或者你可以运行以下命令自己配置：

```bash
git config user.name "你的名字"
git config user.email "your.email@example.com"
```

---

## 📝 步骤 2：添加文件到 Git

```bash
git add .
```

---

## 💾 步骤 3：创建首次提交

```bash
git commit -m "Initial commit: 32 novels ready for deployment"
```

---

## 🌐 步骤 4：在 GitHub 上创建新仓库

1. 访问 [https://github.com/new](https://github.com/new)
2. 填写仓库信息：
   - **Repository name**: 例如 `ielts-novel-flow`（建议使用小写和连字符）
   - **Description**: 例如 "IELTS Novel Reading Platform - 32 novels"
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了代码）
3. 点击 "Create repository"

---

## 🔗 步骤 5：连接到 GitHub 并推送代码

GitHub 会显示命令，通常是这样（**用你实际的仓库URL替换**）：

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

---

## 🚀 步骤 6：在 Vercel 中连接 GitHub

1. 访问 [https://vercel.com](https://vercel.com) 并登录
2. 点击 "Add New..." → "Project"
3. 选择 "Import Git Repository"
4. 找到你刚创建的仓库，点击 "Import"
5. 确认配置（通常不需要修改）：
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
6. 点击 "Deploy"
7. 等待 2-5 分钟
8. 部署成功后，你会得到一个 URL（如：`your-project.vercel.app`）

---

## ✨ 完成！

部署成功后，你的网站就可以通过 Vercel 提供的 URL 访问了！

---

**提示：** 如果你遇到任何问题，随时告诉我！
