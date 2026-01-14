# Supabase 访问码系统设置指南

## 📋 步骤概览

1. 在 Supabase 中创建数据库表
2. 获取 Supabase 连接信息
3. 配置环境变量
4. 安装依赖
5. 测试系统

---

## 1️⃣ 创建数据库表

### 方法 A：使用 SQL Editor（推荐）

1. 登录 Supabase Dashboard
2. 进入你的项目（例如：`chuxiuxiaoji`）
3. 点击左侧边栏的 **"SQL Editor"**
4. 点击 **"New query"**
5. 复制 `supabase/schema.sql` 文件中的全部 SQL 代码
6. 粘贴到 SQL Editor 中
7. 点击 **"Run"** 执行

### 方法 B：使用 Table Editor（可视化）

1. 进入 **"Table Editor"**
2. 点击 **"New table"**
3. 表名：`access_codes`
4. 手动添加以下列：

| 列名 | 类型 | 默认值 | 约束 |
|------|------|--------|------|
| id | uuid | `gen_random_uuid()` | PRIMARY KEY |
| code | text | - | UNIQUE, NOT NULL |
| status | text | `'active'` | CHECK (status IN ('active', 'expired', 'revoked')) |
| created_at | timestamptz | `NOW()` | NOT NULL |
| expires_at | timestamptz | - | NOT NULL |
| validity_days | integer | `365` | NOT NULL |
| usage_count | integer | `0` | NOT NULL |
| last_used_at | timestamptz | - | - |
| notes | text | - | - |
| updated_at | timestamptz | `NOW()` | NOT NULL |

5. 创建索引：
   - `idx_access_codes_code` on `code`
   - `idx_access_codes_status` on `status`
   - `idx_access_codes_expires_at` on `expires_at`

---

## 2️⃣ 获取 Supabase 连接信息

1. 在 Supabase Dashboard 顶部，点击 **"Connect"** 按钮
2. 或者进入 **Settings → API**
3. 记录以下信息：

   - **Project URL**: `https://chuxiuxiaoji.supabase.co`（你的项目 URL）
   - **anon key**: 公开密钥（用于客户端）
   - **service_role key**: 服务端密钥（**保密！**用于服务器端 API）

---

## 3️⃣ 配置环境变量

### 本地开发（.env.local）

1. 在项目根目录创建 `.env.local` 文件（如果不存在）
2. 复制 `env.example` 的内容到 `.env.local`
3. 填入实际值：

```env
NEXT_PUBLIC_SUPABASE_URL=https://chuxiuxiaoji.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=你的_anon_key
SUPABASE_SERVICE_ROLE_KEY=你的_service_role_key
```

### Vercel 部署

1. 进入 Vercel Dashboard → 你的项目 → **Settings → Environment Variables**
2. 添加以下环境变量：

   - `NEXT_PUBLIC_SUPABASE_URL` = `https://chuxiuxiaoji.supabase.co`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` = 你的 anon key
   - `SUPABASE_SERVICE_ROLE_KEY` = 你的 service_role key（**保密！**）

3. 为所有环境（Production, Preview, Development）设置这些变量
4. 重新部署项目

---

## 4️⃣ 安装依赖

### Node.js 依赖（Next.js 项目）

```bash
npm install
# 或
yarn install
```

这会安装 `@supabase/supabase-js`。

### Python 依赖（访问码管理工具）

```bash
pip install -r tools/requirements.txt
# 或
pip3 install -r tools/requirements.txt
```

这会安装 `supabase` Python 客户端。

---

## 5️⃣ 测试系统

### 测试访问码生成工具

```bash
# 生成 5 个测试访问码
python3 tools/access_code_manager.py generate -n 5 --notes "测试"

# 列出所有访问码
python3 tools/access_code_manager.py list

# 查看 Supabase Dashboard → Table Editor，确认数据已写入
```

### 测试网站登录

1. 启动开发服务器：
   ```bash
   npm run dev
   ```

2. 访问 `http://localhost:3000/login`

3. 输入刚才生成的访问码（例如：`PQRH-ZGJS`）

4. 应该能成功登录

---

## 🎯 使用场景示例

### 场景 1：用户购买访问码，有效期 1 年

```bash
# 生成 1 个访问码，有效期 365 天
python3 tools/access_code_manager.py generate -n 1 --notes "客户A-2026年1月购买"
```

### 场景 2：用户购买访问码，指定具体到期日期

```bash
# 生成 1 个访问码，2027年12月31日到期
python3 tools/access_code_manager.py generate -n 1 --expires-at "2027-12-31T23:59:59" --notes "客户B-2026年1月购买"
```

### 场景 3：修改已有访问码的到期时间

```bash
# 将访问码的到期时间改为 2028-01-01
python3 tools/access_code_manager.py set-expiry PQRH-ZGJS "2028-01-01T23:59:59"
```

### 场景 4：撤销访问码（如退款）

```bash
python3 tools/access_code_manager.py revoke PQRH-ZGJS
```

### 场景 5：导出访问码给客户

```bash
# 导出所有有效访问码
python3 tools/access_code_manager.py export --status active -o customer_codes.csv
```

---

## 🔒 安全注意事项

1. **Service Role Key 保密**：
   - 永远不要提交到 Git
   - 只在服务器端使用
   - 不要在前端代码中使用

2. **环境变量**：
   - `.env.local` 已在 `.gitignore` 中，不会被提交
   - Vercel 环境变量是加密存储的

3. **数据库权限**：
   - 建议在 Supabase 中设置 Row Level Security (RLS) 策略
   - 限制 `access_codes` 表的直接访问

---

## ❓ 常见问题

**Q: 访问码可以多次使用吗？**  
A: 是的，在有效期内（`expires_at` 之前）可以无限次使用。

**Q: 如何查看访问码的使用情况？**  
A: 使用 `list` 命令，或直接在 Supabase Table Editor 中查看 `usage_count` 和 `last_used_at` 字段。

**Q: 访问码过期后会自动更新状态吗？**  
A: 在 API 验证时会检查是否过期，如果过期会自动更新状态为 `expired`。

**Q: 可以在 Supabase Dashboard 中手动添加访问码吗？**  
A: 可以！在 Table Editor 中直接添加一行即可。但建议使用脚本生成，确保格式一致。

---

## 📚 相关文件

- `supabase/schema.sql` - 数据库表结构
- `tools/access_code_manager.py` - 访问码管理工具
- `app/api/validate-code/route.ts` - 访问码验证 API
- `src/lib/supabase.ts` - Supabase 客户端工具
