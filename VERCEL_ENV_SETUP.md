# Vercel 环境变量配置指南

## 📋 步骤详解

### 1. 登录 Vercel Dashboard

访问：https://vercel.com/dashboard

### 2. 进入你的项目

- 在项目列表中找到 `ielts-novel-flow`（或你的项目名）
- 点击进入项目详情页

### 3. 进入设置页面

- 点击顶部导航栏的 **"Settings"** 标签
- 在左侧菜单中找到 **"Environment Variables"**

### 4. 添加环境变量

点击 **"Add New"** 按钮，依次添加以下三个变量：

#### 变量 1：Supabase URL

- **Key（变量名）**: `NEXT_PUBLIC_SUPABASE_URL`
- **Value（值）**: `https://exidxhgxozmuwacdfuad.supabase.co`
- **Environment（环境）**: 
  - ✅ Production（生产环境）
  - ✅ Preview（预览环境）
  - ✅ Development（开发环境）
- 点击 **"Save"**

#### 变量 2：Supabase Anon Key

- **Key**: `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Value**: `sb_publishable_fHA55-Zz0iTZZYDA3U2SoA_mgj0BBWw`
- **Environment**: 全选（Production、Preview、Development）
- 点击 **"Save"**

#### 变量 3：Supabase Service Role Key（重要：保密！）

- **Key**: `SUPABASE_SERVICE_ROLE_KEY`
- **Value**: `sb_secret_9O0mgiMwtkEuqCF2FQa5cQ_wS7feVs5`
- **Environment**: 全选（Production、Preview、Development）
- 点击 **"Save"**

⚠️ **注意**：Service Role Key 是敏感密钥，有完整数据库访问权限，不要在前端代码中使用！

### 5. 验证环境变量

添加完成后，你应该在列表中看到这三个变量：

```
NEXT_PUBLIC_SUPABASE_URL          [Production, Preview, Development]
NEXT_PUBLIC_SUPABASE_ANON_KEY      [Production, Preview, Development]
SUPABASE_SERVICE_ROLE_KEY          [Production, Preview, Development]
```

### 6. 重新部署项目

环境变量添加后，需要重新部署才能生效：

#### 方法 A：通过 Dashboard 重新部署

1. 点击顶部导航栏的 **"Deployments"** 标签
2. 找到最新的部署记录
3. 点击右侧的 **"..."** 菜单
4. 选择 **"Redeploy"**
5. 确认重新部署

#### 方法 B：通过 Git 推送触发部署

```bash
# 在本地项目目录执行
git add .
git commit -m "Add Supabase environment variables"
git push origin main
```

Vercel 会自动检测到新的推送并触发部署。

### 7. 验证部署

部署完成后：

1. 访问你的网站（例如：`https://ielts-novel-flow.vercel.app`）
2. 尝试登录功能
3. 如果登录成功，说明环境变量配置正确 ✅

---

## 🔍 如何确认环境变量已生效？

### 方法 1：查看部署日志

1. 进入 **Deployments** 标签
2. 点击最新的部署记录
3. 查看 **"Build Logs"**
4. 如果看到 Supabase 相关的日志且没有报错，说明环境变量已加载

### 方法 2：在代码中临时打印（仅用于调试）

在 `app/api/validate-code/route.ts` 中临时添加：

```typescript
console.log("Supabase URL:", process.env.NEXT_PUBLIC_SUPABASE_URL ? "✅ 已设置" : "❌ 未设置");
```

⚠️ **注意**：调试完成后记得删除这行代码，不要在生产环境打印敏感信息！

---

## ❓ 常见问题

### Q: 环境变量添加后，网站还是报错？

**A**: 确保：
1. 三个环境变量都已添加
2. 每个变量都勾选了所有环境（Production、Preview、Development）
3. 已经重新部署了项目（环境变量不会自动应用到已部署的版本）

### Q: 如何修改环境变量？

**A**: 
1. 在 **Environment Variables** 页面找到要修改的变量
2. 点击变量右侧的 **"..."** 菜单
3. 选择 **"Edit"** 或 **"Delete"**
4. 修改后需要重新部署

### Q: 环境变量在本地和 Vercel 中需要分别设置吗？

**A**: 是的：
- **本地开发**：使用 `.env.local` 文件（已在 `.gitignore` 中，不会提交到 Git）
- **Vercel 部署**：在 Dashboard 中设置环境变量

两者互不影响，但值应该保持一致。

### Q: 可以只设置 Production 环境吗？

**A**: 可以，但建议全选，因为：
- Preview 环境用于测试 Pull Request
- Development 环境用于本地开发（如果使用 Vercel CLI）

---

## 🔒 安全提示

1. **Service Role Key 保密**：
   - 永远不要提交到 Git
   - 只在服务器端 API 路由中使用
   - 不要在前端代码中暴露

2. **环境变量加密**：
   - Vercel 会自动加密存储环境变量
   - 只有项目成员可以查看和编辑

3. **定期轮换密钥**：
   - 如果密钥泄露，立即在 Supabase Dashboard 中重新生成
   - 然后更新 Vercel 中的环境变量

---

## 📝 快速检查清单

- [ ] 已添加 `NEXT_PUBLIC_SUPABASE_URL`
- [ ] 已添加 `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- [ ] 已添加 `SUPABASE_SERVICE_ROLE_KEY`
- [ ] 所有变量都勾选了三个环境
- [ ] 已重新部署项目
- [ ] 测试登录功能正常

完成以上步骤后，你的网站就可以使用 Supabase 访问码系统了！🎉
