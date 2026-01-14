# 🌐 绑定自定义域名指南

## 📋 准备工作

在开始之前，请确认：

1. ✅ 你已经有域名（如：`ielts-novel.com`）
2. ✅ 域名注册商（如：GoDaddy, Namecheap, Cloudflare, 阿里云等）
3. ✅ 可以访问域名管理后台

---

## 🎯 步骤 1：在 Vercel 中添加域名

### 1.1 打开 Vercel 项目设置

1. 访问：https://vercel.com/dashboard
2. 找到并进入 `ielts-novel-flow` 项目
3. 点击顶部导航栏的 **"Settings"**（设置）标签
4. 在左侧菜单中，点击 **"Domains"**（域名）

---

### 1.2 添加域名

1. 在 "Domains" 页面，找到 **"Add"** 或 **"Add Domain"** 按钮
2. 点击按钮
3. 在弹出的输入框中，输入你的域名，例如：
   - `ielts-novel.com`（主域名）
   - 或 `www.ielts-novel.com`（带 www 的子域名）
4. 点击 **"Add"** 或 **"Continue"**

---

### 1.3 选择配置方式

Vercel 会显示两种配置方式：

**方式 A：使用 CNAME 记录（推荐）**
- 适用于子域名（如 `www.ielts-novel.com`）
- 或者主域名（如果 DNS 提供商支持）

**方式 B：使用 A 记录**
- 适用于主域名（如 `ielts-novel.com`）
- 需要添加 A 记录指向 Vercel 的 IP

---

## 🎯 步骤 2：配置 DNS 记录

Vercel 会显示你需要添加的 DNS 记录。根据你的域名配置方式：

### 情况 A：使用 CNAME 记录（推荐）

如果 Vercel 建议使用 CNAME：

1. **记录类型**: CNAME
2. **名称/主机**: 
   - 如果是 `www.ielts-novel.com`，填写 `www`
   - 如果是主域名 `ielts-novel.com`，填写 `@` 或留空
3. **值/目标**: Vercel 提供的值（类似：`cname.vercel-dns.com`）
4. **TTL**: 使用默认值（通常是 3600 或 Auto）

---

### 情况 B：使用 A 记录

如果 Vercel 建议使用 A 记录：

1. **记录类型**: A
2. **名称/主机**: `@` 或留空（表示主域名）
3. **值/目标**: Vercel 提供的 IP 地址（如：`76.76.21.21`）
4. **TTL**: 使用默认值

---

### 情况 C：同时添加主域名和 www 子域名（推荐）

为了同时支持 `ielts-novel.com` 和 `www.ielts-novel.com`：

1. **主域名** (`ielts-novel.com`):
   - 使用 A 记录，指向 Vercel 的 IP
   - 或使用 CNAME（如果 DNS 提供商支持）

2. **www 子域名** (`www.ielts-novel.com`):
   - 使用 CNAME 记录
   - 值：`cname.vercel-dns.com`

---

## 🎯 步骤 3：在域名注册商中添加 DNS 记录

### 常见域名注册商的 DNS 配置位置

**GoDaddy:**
1. 登录 GoDaddy
2. My Products → Domains
3. 点击你的域名 → DNS
4. 添加 DNS 记录

**Namecheap:**
1. 登录 Namecheap
2. Domain List
3. 点击你的域名 → Advanced DNS
4. 添加 DNS 记录

**Cloudflare:**
1. 登录 Cloudflare
2. 选择你的域名
3. DNS → Records
4. 添加 DNS 记录

**阿里云（万网）:**
1. 登录阿里云
2. 域名控制台
3. 域名列表 → 解析设置
4. 添加解析记录

**腾讯云:**
1. 登录腾讯云
2. 域名注册 → 我的域名
3. 解析 → 添加记录

---

## 🎯 步骤 4：等待 DNS 生效

1. DNS 记录添加完成后，通常需要 **几分钟到几小时** 才能生效
2. 在 Vercel 的 Domains 页面，可以看到 DNS 配置状态
3. 如果配置正确，会显示 **"Valid Configuration"** 或 **"Valid"**（绿色勾）
4. 如果显示错误，检查 DNS 记录是否正确

---

## 🎯 步骤 5：SSL 证书自动配置

1. DNS 生效后，Vercel 会自动为你的域名配置 **HTTPS 证书**（免费）
2. 这个过程通常需要几分钟
3. 配置完成后，你的网站就可以通过 HTTPS 访问了

---

## 🎯 步骤 6：验证绑定成功

1. 在浏览器中访问你的域名（如：`https://ielts-novel.com`）
2. 应该能看到你的网站正常加载
3. 地址栏应该显示 **锁图标**（HTTPS 已启用）

---

## 🐛 常见问题

### 问题 1：DNS 记录添加后没有生效

**可能原因：**
- DNS 传播需要时间（最多 48 小时）
- DNS 记录配置错误

**解决方法：**
- 等待 24-48 小时
- 使用在线 DNS 检查工具验证（如：https://dnschecker.org/）
- 检查 DNS 记录是否正确

---

### 问题 2：Vercel 显示 "Invalid Configuration"

**可能原因：**
- DNS 记录配置错误
- 记录值不正确

**解决方法：**
- 检查 Vercel 提供的 DNS 值是否正确复制
- 确保记录类型正确（CNAME 或 A）
- 等待 DNS 生效后再检查

---

### 问题 3：主域名无法使用 CNAME

**原因：**
- 主域名（如 `ielts-novel.com`）通常不能直接使用 CNAME 记录
- 需要使用 A 记录

**解决方法：**
- 使用 A 记录指向 Vercel 的 IP
- 或者使用 CNAME 指向 `www` 子域名

---

### 问题 4：想要同时支持主域名和 www

**解决方法：**
1. 在 Vercel 中添加两个域名：
   - `ielts-novel.com`
   - `www.ielts-novel.com`
2. 配置相应的 DNS 记录
3. 在 Vercel Settings → Domains 中可以设置重定向（如将主域名重定向到 www）

---

## 💡 最佳实践

### 推荐配置

1. **同时添加主域名和 www 子域名**
   - `ielts-novel.com`（使用 A 记录）
   - `www.ielts-novel.com`（使用 CNAME 记录）

2. **设置重定向**
   - 将主域名重定向到 www（或反之）
   - 在 Vercel Settings → Domains 中设置

3. **使用 Cloudflare（可选）**
   - 如果域名在 Cloudflare，可以使用 Cloudflare 的 CDN
   - 但需要正确配置 DNS 记录

---

## 📝 你需要的信息

在开始之前，请告诉我：

1. **你的域名是什么？**（如：`ielts-novel.com`）
2. **域名注册商是什么？**（如：GoDaddy, Namecheap, Cloudflare, 阿里云等）
3. **你想同时绑定主域名和 www 吗？**

告诉我这些信息，我可以提供更详细的指导！

---

**准备好后，告诉我你的域名和注册商，我会一步步指导你！**
