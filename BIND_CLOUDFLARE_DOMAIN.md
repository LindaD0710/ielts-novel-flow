# 🌐 绑定 Cloudflare 域名到 Vercel

## ✅ 你的域名信息

- **域名**: `chuxiuxiaoji.com`
- **注册商**: Cloudflare
- **状态**: Active（活动）

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
3. 在弹出的输入框中，输入你的域名：
   ```
   chuxiuxiaoji.com
   ```
4. 如果你想同时支持 www 子域名，也添加：
   ```
   www.chuxiuxiaoji.com
   ```
5. 点击 **"Add"** 或 **"Continue"**

---

### 1.3 查看 DNS 配置要求

Vercel 会显示需要配置的 DNS 记录：

**对于主域名 `chuxiuxiaoji.com`：**
- 通常需要 **A 记录**
- 值：`76.76.21.21`（Vercel 会提供具体的 IP）

**对于 www 子域名 `www.chuxiuxiaoji.com`：**
- 使用 **CNAME 记录**
- 值：`cname.vercel-dns.com`（Vercel 会提供具体的值）

**注意：** Vercel 会显示具体的 DNS 配置要求，请按照 Vercel 显示的配置。

---

## 🎯 步骤 2：在 Cloudflare 中配置 DNS 记录

### 2.1 打开 Cloudflare DNS 设置

1. 在 Cloudflare 页面，点击你的域名 **`chuxiuxiaoji.com`**（蓝色的域名链接）
2. 进入域名管理页面
3. 在左侧菜单中，点击 **"DNS"**（或"DNS 记录"）

---

### 2.2 添加 DNS 记录

#### 情况 A：只绑定主域名 `chuxiuxiaoji.com`

1. 点击 **"Add record"**（添加记录）按钮
2. 配置：
   - **Type（类型）**: 选择 `A`
   - **Name（名称）**: 输入 `@` 或留空（表示主域名）
   - **IPv4 address（IPv4 地址）**: 输入 Vercel 提供的 IP（如：`76.76.21.21`）
   - **Proxy status（代理状态）**: ⚠️ **重要** - 选择 **"DNS only"**（灰色云朵，不是橙色）
     - 橙色云朵 = 开启 Cloudflare 代理（CDN）
     - 灰色云朵 = DNS only（直接解析到 Vercel）
   - **TTL**: 选择 `Auto` 或 `1 hour`
3. 点击 **"Save"**（保存）

---

#### 情况 B：同时绑定主域名和 www 子域名（推荐）

**主域名 `chuxiuxiaoji.com`：**

1. 添加 A 记录：
   - **Type**: `A`
   - **Name**: `@` 或留空
   - **IPv4 address**: Vercel 提供的 IP（如：`76.76.21.21`）
   - **Proxy status**: **"DNS only"**（灰色云朵）⚠️
   - **TTL**: `Auto`
   - 点击 **"Save"**

**www 子域名 `www.chuxiuxiaoji.com`：**

2. 添加 CNAME 记录：
   - **Type**: `CNAME`
   - **Name**: `www`
   - **Target（目标）**: Vercel 提供的 CNAME 值（如：`cname.vercel-dns.com`）
   - **Proxy status**: **"DNS only"**（灰色云朵）⚠️
   - **TTL**: `Auto`
   - 点击 **"Save"**

---

## ⚠️ 重要提示：Cloudflare 代理设置

### 必须使用 "DNS only"（灰色云朵）

**为什么？**
- 如果使用橙色云朵（Cloudflare 代理），Cloudflare 会作为 CDN 代理你的网站
- 这可能导致 Vercel 的 SSL 证书配置出现问题
- 使用灰色云朵（DNS only）直接解析到 Vercel，更简单可靠

**如何设置？**
- 添加记录时，确保 **Proxy status** 显示为灰色云朵（不是橙色）
- 如果已经添加的记录是橙色云朵，点击云朵图标可以切换为灰色

---

## 🎯 步骤 3：等待 DNS 生效

1. DNS 记录添加完成后，通常需要 **几分钟到半小时** 才能生效
2. 在 Vercel 的 Domains 页面，可以看到 DNS 配置状态
3. 如果配置正确，会显示 **"Valid Configuration"** 或 **"Valid"**（绿色勾）
4. 如果显示错误，检查 DNS 记录是否正确

---

## 🎯 步骤 4：SSL 证书自动配置

1. DNS 生效后，Vercel 会自动为你的域名配置 **HTTPS 证书**（免费）
2. 这个过程通常需要几分钟
3. 配置完成后，你的网站就可以通过 HTTPS 访问了

---

## 🎯 步骤 5：验证绑定成功

1. 在浏览器中访问：
   - `https://chuxiuxiaoji.com`
   - 或 `https://www.chuxiuxiaoji.com`（如果配置了 www）
2. 应该能看到你的网站正常加载
3. 地址栏应该显示 **锁图标**（HTTPS 已启用）

---

## 🐛 常见问题

### 问题 1：DNS 记录添加后 Vercel 显示 "Invalid Configuration"

**可能原因：**
- DNS 记录配置错误
- Cloudflare 代理（橙色云朵）导致的问题

**解决方法：**
- 确保使用 **"DNS only"**（灰色云朵）
- 检查 DNS 记录值是否正确
- 等待几分钟让 DNS 传播

---

### 问题 2：网站无法访问

**可能原因：**
- DNS 还未生效
- DNS 记录配置错误

**解决方法：**
- 等待 30 分钟到几小时
- 使用在线 DNS 检查工具验证（如：https://dnschecker.org/）
- 检查 Cloudflare DNS 记录是否正确

---

### 问题 3：SSL 证书配置失败

**可能原因：**
- Cloudflare 代理（橙色云朵）阻止了 Vercel 的 SSL 验证

**解决方法：**
- 确保使用 **"DNS only"**（灰色云朵）
- 等待 DNS 生效后再等待 SSL 证书配置

---

## 💡 Cloudflare 特殊说明

### 关于 Cloudflare 代理

- **灰色云朵（DNS only）**: 直接解析到 Vercel，推荐用于 Vercel 部署
- **橙色云朵（Proxied）**: Cloudflare CDN 代理，可能导致 SSL 问题

### 如果你需要使用 Cloudflare CDN

如果你确实想使用 Cloudflare 的 CDN 功能：

1. 可以使用橙色云朵（Proxied）
2. 但需要在 Cloudflare SSL/TLS 设置中：
   - 进入 Cloudflare → SSL/TLS
   - 设置为 **"Full"** 模式
   - 这样 Cloudflare 会正确处理 SSL

**但推荐方式：** 使用灰色云朵（DNS only），让 Vercel 直接处理 SSL。

---

## 🎯 操作步骤总结

1. ✅ 在 Vercel 中添加域名 `chuxiuxiaoji.com`
2. ✅ 查看 Vercel 提供的 DNS 配置要求
3. ✅ 在 Cloudflare DNS 中添加 A 记录（主域名）
4. ✅ 在 Cloudflare DNS 中添加 CNAME 记录（www，可选）
5. ✅ 确保使用 "DNS only"（灰色云朵）
6. ✅ 等待 DNS 生效（几分钟到半小时）
7. ✅ 等待 Vercel 配置 SSL 证书（几分钟）
8. ✅ 访问域名验证

---

**现在开始操作吧！先到 Vercel 添加域名，然后告诉我 Vercel 显示的 DNS 配置要求！**
