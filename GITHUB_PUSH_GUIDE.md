# 🔐 GitHub 推送认证指南

## 问题说明

GitHub 现在需要使用 Personal Access Token（个人访问令牌）进行 HTTPS 认证，不再支持密码。

## 解决方案（选择一种）

### 方案 A：使用 Personal Access Token（推荐）

#### 步骤 1：创建 Personal Access Token

1. 访问 GitHub：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 填写信息：
   - **Note**（备注）: 例如 "Local Development"
   - **Expiration**（过期时间）: 选择 "90 days" 或更长
   - **Select scopes**（权限）: 勾选 **`repo`**（完全仓库访问权限）
4. 点击 "Generate token"（生成令牌）
5. **重要**：立即复制生成的 token（类似：`ghp_xxxxxxxxxxxxxxxxxxxx`），只会显示一次！

#### 步骤 2：使用 Token 推送

当 Git 提示输入密码时，**使用 Token 代替密码**：

```bash
git push -u origin main
```

- Username: `LindaD0710`
- Password: **粘贴你的 Token**（而不是你的GitHub密码）

---

### 方案 B：使用 GitHub Desktop（最简单）

如果你安装了 GitHub Desktop：

1. 打开 GitHub Desktop
2. File → Add Local Repository
3. 选择项目目录
4. 点击 "Publish repository" 或 "Push origin"

---

### 方案 C：使用 SSH（适合长期使用）

如果需要设置 SSH，我可以帮你配置。

---

## 推荐：方案 A（Personal Access Token）

这是最快速的方法。创建 Token 后，在推送时使用 Token 作为密码即可。
