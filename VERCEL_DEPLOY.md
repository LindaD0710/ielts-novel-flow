# Vercel 部署检查清单

## ✅ 已完成的配置

### 1. 静态数据处理 ✅
- ✅ 使用静态 `import` 导入 JSON 文件（`src/services/novelService.ts`）
- ✅ Next.js 会自动将 JSON 文件打包到构建中
- ✅ `tsconfig.json` 中已配置 `resolveJsonModule: true`

### 2. Package.json 配置 ✅
- ✅ `build`: `next build` - 生产构建
- ✅ `start`: `next start` - 启动生产服务器
- ✅ `dev`: `next dev` - 开发服务器

### 3. 数据文件 ✅
- ✅ `src/data/generated/chapter_1.json` 存在
- ✅ `src/data/generated/vocab_db.json` 存在

### 4. TypeScript 配置 ✅
- ✅ 无 TypeScript 错误
- ✅ 无 Linter 错误
- ✅ 路径别名 `@/*` 配置正确

## 部署步骤

### 方式一：通过 Vercel CLI

```bash
# 1. 安装 Vercel CLI（如果还没安装）
npm i -g vercel

# 2. 登录 Vercel
vercel login

# 3. 部署
vercel

# 4. 生产环境部署
vercel --prod
```

### 方式二：通过 Vercel Dashboard

1. 访问 https://vercel.com
2. 点击 "New Project"
3. 导入你的 Git 仓库（GitHub/GitLab/Bitbucket）
4. Vercel 会自动检测 Next.js 项目
5. 点击 "Deploy"

## 构建命令

Vercel 会自动使用 `package.json` 中的 `build` 脚本：
```json
"build": "next build"
```

## 环境变量（如果需要）

如果将来需要 API Key 等环境变量：
1. 在 Vercel Dashboard → Project Settings → Environment Variables
2. 添加变量（如 `OPENAI_API_KEY`）
3. 重新部署

## 注意事项

1. **JSON 文件必须提交到 Git**：确保 `src/data/generated/*.json` 在版本控制中
2. **构建时间**：首次构建可能需要 2-3 分钟
3. **自动部署**：如果连接了 Git 仓库，每次 push 都会自动部署

## 验证部署

部署成功后，访问 Vercel 提供的 URL，检查：
- ✅ 页面正常加载
- ✅ 章节内容显示正常
- ✅ 点击单词可以弹出单词卡片
- ✅ 阅读进度保存功能正常


