# 🚀 部署指南 - 将项目部署到域名

## 📋 部署前检查清单

在开始部署之前，请确认以下事项：

### ✅ 代码检查
- [x] 项目编译成功（`npm run build` 通过）
- [x] 32篇小说已正确导入到 `src/services/novelService.ts`
- [x] 无 TypeScript 错误
- [x] 无 Linter 错误

### 📁 文件检查
确保以下重要文件存在：
- ✅ `package.json` - 项目配置
- ✅ `next.config.js` - Next.js 配置
- ✅ `src/data/generated/*.json` - 32个小说数据文件
- ✅ `src/services/novelService.ts` - 服务文件（已导入所有小说）

---

## 🎯 部署方案：Vercel（推荐）

Vercel 是 Next.js 官方推荐的部署平台，具有以下优势：
- ✅ 完全免费（个人项目）
- ✅ 自动 HTTPS
- ✅ 全球 CDN 加速
- ✅ 自动部署（连接 Git 后）
- ✅ 自定义域名支持

---

## 📝 部署步骤

### 方式一：通过 Vercel Dashboard（推荐，最简单）

#### 步骤 1：准备工作

1. **确保代码已准备好**
   ```bash
   # 在项目目录下运行，确保构建成功
   npm run build
   ```

2. **（可选）初始化 Git 仓库并推送到 GitHub**
   
   如果你想使用自动部署功能，需要先推送到 GitHub：

   ```bash
   # 初始化 Git 仓库
   git init
   
   # 添加所有文件
   git add .
   
   # 提交
   git commit -m "Initial commit: 32 novels ready for deployment"
   
   # 在 GitHub 上创建新仓库，然后：
   git remote add origin https://github.com/你的用户名/你的仓库名.git
   git branch -M main
   git push -u origin main
   ```

   **注意：** 如果你不想使用 GitHub，可以跳过这一步，直接上传代码到 Vercel。

#### 步骤 2：注册/登录 Vercel

1. 访问 [https://vercel.com](https://vercel.com)
2. 点击 "Sign Up" 注册（可以使用 GitHub 账号快速注册）
3. 登录到 Vercel Dashboard

#### 步骤 3：创建新项目

1. 在 Vercel Dashboard 点击 **"Add New..."** → **"Project"**
2. 选择导入方式：

   **选项 A：从 GitHub 导入（推荐）**
   - 连接你的 GitHub 账号（如果还没连接）
   - 选择你的仓库
   - 点击 "Import"

   **选项 B：直接上传代码**
   - 点击 "Browse" 或直接拖拽项目文件夹
   - 或者选择 "Upload" 上传 ZIP 文件

#### 步骤 4：配置项目

Vercel 会自动检测 Next.js 项目，配置如下：

- **Framework Preset**: Next.js（自动检测）
- **Build Command**: `npm run build`（自动填充）
- **Output Directory**: `.next`（自动填充）
- **Install Command**: `npm install`（自动填充）

**通常不需要修改任何配置，直接点击 "Deploy" 即可。**

#### 步骤 5：等待部署

- 部署过程大约需要 2-5 分钟
- 你可以看到实时构建日志
- 构建成功后，Vercel 会提供一个临时域名（如：`your-project.vercel.app`）

#### 步骤 6：测试部署

访问 Vercel 提供的 URL，检查：
- ✅ 首页正常加载
- ✅ 登录页面正常
- ✅ 图书馆页面可以显示所有小说
- ✅ 可以正常阅读小说
- ✅ 单词卡片功能正常

---

### 方式二：通过 Vercel CLI（命令行）

如果你更喜欢使用命令行：

```bash
# 1. 全局安装 Vercel CLI
npm i -g vercel

# 2. 在项目目录下登录
vercel login

# 3. 部署（预览环境）
vercel

# 4. 部署到生产环境
vercel --prod
```

---

## 🌐 绑定自定义域名

如果你想使用自己的域名（如：`ielts-novel.com`）：

### 步骤 1：在 Vercel 添加域名

1. 进入项目 Dashboard
2. 点击 **"Settings"** → **"Domains"**
3. 输入你的域名（如：`ielts-novel.com`）
4. 点击 "Add"

### 步骤 2：配置 DNS

Vercel 会提供 DNS 配置说明，通常有两种方式：

**方式 A：使用 CNAME 记录（推荐）**
```
类型: CNAME
名称: @ 或 www
值: cname.vercel-dns.com
```

**方式 B：使用 A 记录**
```
类型: A
名称: @
值: 76.76.21.21（Vercel 提供的 IP）
```

### 步骤 3：等待 DNS 生效

- DNS 传播通常需要几分钟到几小时
- 可以在 Vercel Dashboard 查看 DNS 状态
- 配置成功后，HTTPS 证书会自动生成

---

## 🔄 自动部署（可选）

如果你使用 GitHub 导入项目，Vercel 会自动：

1. **自动部署**：每次你 `git push` 代码，Vercel 会自动重新部署
2. **预览部署**：每个 Pull Request 会创建一个预览 URL
3. **部署历史**：可以查看每次部署的日志和回滚

**启用自动部署：**
- 在项目 Settings → Git
- 确保 "Production Branch" 设置为 `main` 或 `master`
- 每次 push 到主分支都会自动部署

---

## 🛠️ 环境变量配置（如果需要）

如果你的项目将来需要 API Key 等环境变量：

1. 进入项目 Dashboard
2. 点击 **"Settings"** → **"Environment Variables"**
3. 添加变量：
   - **Name**: 变量名（如：`OPENAI_API_KEY`）
   - **Value**: 变量值
   - **Environment**: 选择环境（Production, Preview, Development）
4. 点击 "Save"
5. 重新部署项目

**注意：** 当前项目不需要环境变量，但可以预先了解。

---

## 📊 部署后验证

部署成功后，请全面测试：

### 功能测试
- [ ] 首页加载正常
- [ ] 登录功能正常
- [ ] 图书馆页面显示所有32篇小说
- [ ] 可以打开并阅读小说
- [ ] 点击单词可以弹出单词卡片
- [ ] 阅读进度保存功能正常
- [ ] 响应式设计在不同设备上正常显示

### 性能测试
- [ ] 页面加载速度正常
- [ ] 图片加载正常（如果有）
- [ ] 交互流畅，无卡顿

---

## 🐛 常见问题排查

### 问题 1：构建失败

**错误信息：** Build failed

**可能原因：**
- TypeScript 错误
- 缺少依赖
- JSON 文件格式错误

**解决方法：**
```bash
# 本地测试构建
npm run build

# 查看详细错误信息
npm run build 2>&1 | tee build.log
```

### 问题 2：页面 404

**可能原因：**
- 路由配置问题
- 文件路径错误

**解决方法：**
- 检查 `app/` 目录下的页面文件
- 确认路由路径正确

### 问题 3：小说无法加载

**可能原因：**
- `novelService.ts` 导入错误
- JSON 文件路径错误

**解决方法：**
- 检查 `src/services/novelService.ts` 中的所有导入
- 确认 JSON 文件存在于 `src/data/generated/` 目录

### 问题 4：域名无法访问

**可能原因：**
- DNS 配置错误
- DNS 还未生效

**解决方法：**
- 检查 DNS 配置是否正确
- 使用 `nslookup` 或在线工具检查 DNS 解析
- 等待 DNS 传播（最多 48 小时）

---

## 📝 部署后维护

### 更新内容

1. **添加新小说后：**
   - 更新 `src/services/novelService.ts`
   - 提交代码到 Git
   - Vercel 会自动重新部署（如果已连接 Git）

2. **手动重新部署：**
   - 在 Vercel Dashboard 点击 "Redeploy"
   - 或运行 `vercel --prod`（如果使用 CLI）

### 监控

- **Analytics（分析）**：Vercel 提供基础的访问统计
- **Logs（日志）**：可以查看实时日志和错误
- **Speed Insights**：性能监控（可能需要付费）

---

## 🎉 完成！

部署成功后，你的项目就可以通过域名访问了！

**下一步建议：**
1. 分享给你的用户
2. 收集反馈
3. 持续优化和添加新内容

---

## 📚 参考资源

- [Vercel 官方文档](https://vercel.com/docs)
- [Next.js 部署文档](https://nextjs.org/docs/deployment)
- [Vercel 定价](https://vercel.com/pricing)（个人项目免费）

---

**祝你部署顺利！🚀**
