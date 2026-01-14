# 用户绑定功能使用指南

## 📋 功能说明

为了防止多人共用一个访问码，系统现在支持**访问码与用户身份绑定**功能。

### 工作原理

1. **首次使用**：用户输入访问码 + 邮箱/手机号 → 系统绑定访问码和用户身份
2. **后续使用**：用户输入访问码 + 绑定的邮箱/手机号 → 系统验证身份 → 登录成功
3. **防止共享**：如果其他人尝试使用已绑定的访问码，必须输入正确的绑定邮箱/手机号才能登录

---

## 🗄️ 数据库迁移

### 第一步：在 Supabase 中执行迁移 SQL

1. 打开 Supabase Dashboard → 你的项目
2. 点击左侧 **SQL Editor**
3. 打开项目中的 `supabase/migration_add_user_binding.sql` 文件
4. 复制全部 SQL 代码
5. 粘贴到 SQL Editor，点击 **Run**

这会添加以下字段到 `access_codes` 表：
- `bound_user_email` - 绑定的用户邮箱
- `bound_user_phone` - 绑定的用户手机号
- `bound_at` - 绑定时间

---

## 👤 用户使用流程

### 首次登录（绑定账户）

1. 访问登录页面
2. 输入访问码（例如：`YZP8-J6M9`）
3. 点击"进入图书馆"
4. 系统提示需要绑定账户
5. 输入邮箱或手机号（至少一个）
6. 点击"绑定并登录"
7. 登录成功，访问码已绑定到您的账户

### 后续登录（验证身份）

1. 访问登录页面
2. 输入访问码
3. 系统自动显示邮箱/手机号输入框
4. 输入**绑定时使用的邮箱或手机号**
5. 点击"绑定并登录"
6. 验证通过，登录成功

### 如果忘记绑定的邮箱/手机号

- 可以在 Supabase Table Editor 中查看访问码的绑定信息
- 或者联系管理员查询

---

## 🔧 管理员功能

### 查看访问码绑定信息

#### 方法 1：使用命令行工具

```bash
# 列出所有访问码（包含绑定信息）
python3 tools/access_code_manager.py list

# 只查看已绑定的访问码
python3 tools/access_code_manager.py list --status active
```

输出示例：
```
📋 访问码列表 (5 个):
--------------------------------------------------------------------------------
   YZP8-J6M9    | 状态: active   | 到期: 2027-01-14 | 使用:   5次 | 最后使用: 2026-01-15 10:30
                 绑定: 邮箱: user@example.com | 手机: 13800138000
                 绑定时间: 2026-01-14
                 备注: 批量生成-2026年1月
```

#### 方法 2：在 Supabase Table Editor 中查看

1. 打开 Supabase Dashboard → Table Editor → `access_codes` 表
2. 查看以下列：
   - `bound_user_email` - 绑定的邮箱
   - `bound_user_phone` - 绑定的手机号
   - `bound_at` - 绑定时间

### 导出访问码（包含绑定信息）

```bash
# 导出所有访问码到 CSV
python3 tools/access_code_manager.py export -o access_codes_with_binding.csv
```

CSV 文件会包含以下字段：
- `code` - 访问码
- `status` - 状态
- `bound_user_email` - 绑定的邮箱
- `bound_user_phone` - 绑定的手机号
- `bound_at` - 绑定时间
- `usage_count` - 使用次数
- 等等...

### 手动修改绑定信息

在 Supabase Table Editor 中：
1. 找到要修改的访问码行
2. 直接编辑 `bound_user_email` 或 `bound_user_phone` 字段
3. 保存更改

**注意**：修改绑定信息后，用户需要使用新的邮箱/手机号登录。

---

## 🔒 安全说明

### 绑定规则

- **一个访问码只能绑定一个用户**（通过邮箱或手机号）
- **绑定后无法更改**（除非管理员在 Supabase 中手动修改）
- **每次登录都需要验证绑定的邮箱/手机号**

### 防止共享机制

1. **首次使用即绑定**：用户第一次使用访问码时，必须提供邮箱/手机号，系统自动绑定
2. **后续验证身份**：再次使用时，必须输入绑定时使用的邮箱/手机号
3. **无法绕过**：如果输入错误的邮箱/手机号，系统会拒绝登录

### 注意事项

- ⚠️ **用户必须记住绑定时使用的邮箱/手机号**，否则无法登录
- ⚠️ **建议用户使用常用邮箱**，避免忘记
- ⚠️ **管理员可以在 Supabase 中查看和修改绑定信息**，用于客服支持

---

## 🧪 测试流程

### 1. 测试首次绑定

1. 清除浏览器 localStorage：`localStorage.clear()`
2. 访问登录页面
3. 输入一个未使用的访问码
4. 输入邮箱（例如：`test@example.com`）
5. 点击"绑定并登录"
6. 应该成功登录

### 2. 测试后续登录

1. 清除浏览器 localStorage：`localStorage.clear()`
2. 访问登录页面
3. 输入刚才使用的访问码
4. 系统应该提示输入邮箱/手机号
5. 输入**相同的邮箱**（`test@example.com`）
6. 点击"绑定并登录"
7. 应该成功登录

### 3. 测试防止共享

1. 清除浏览器 localStorage：`localStorage.clear()`
2. 访问登录页面
3. 输入已绑定的访问码
4. 输入**不同的邮箱**（例如：`other@example.com`）
5. 点击"绑定并登录"
6. 应该显示错误："此访问码已绑定其他用户"

---

## ❓ 常见问题

### Q: 用户可以更换绑定的邮箱/手机号吗？

**A**: 不可以。绑定后无法由用户自行更改。如果需要更换，需要管理员在 Supabase Table Editor 中手动修改。

### Q: 如果用户忘记绑定的邮箱/手机号怎么办？

**A**: 
1. 管理员可以在 Supabase Table Editor 中查看访问码的绑定信息
2. 管理员可以手动修改绑定信息，让用户使用新的邮箱/手机号

### Q: 一个邮箱/手机号可以绑定多个访问码吗？

**A**: 可以。一个用户（邮箱/手机号）可以拥有多个访问码，每个访问码独立绑定。

### Q: 如何解除绑定？

**A**: 在 Supabase Table Editor 中，将 `bound_user_email` 和 `bound_user_phone` 字段清空即可。

### Q: 绑定信息会泄露用户隐私吗？

**A**: 
- 绑定信息存储在 Supabase 数据库中，只有管理员可以查看
- 前端不会显示其他用户的绑定信息
- 建议遵守隐私保护法规

---

## 📝 技术细节

### API 端点

**POST** `/api/validate-code`

**请求体**：
```json
{
  "accessCode": "YZP8-J6M9",
  "userEmail": "user@example.com",  // 可选
  "userPhone": "13800138000"        // 可选（与邮箱二选一）
}
```

**响应**：
```json
{
  "success": true,
  "message": "访问码验证成功，已绑定您的账户",
  "code": "YZP8-J6M9",
  "expires_at": "2027-01-14T20:27:44.906513",
  "usage_count": 1,
  "isBound": true,
  "boundUserEmail": "user@example.com",
  "boundUserPhone": null
}
```

### 数据库字段

- `bound_user_email` (TEXT, nullable) - 绑定的用户邮箱（小写存储）
- `bound_user_phone` (TEXT, nullable) - 绑定的用户手机号
- `bound_at` (TIMESTAMPTZ, nullable) - 绑定时间

---

## ✅ 完成检查清单

- [ ] 已在 Supabase 中执行迁移 SQL
- [ ] 测试首次绑定功能
- [ ] 测试后续登录验证功能
- [ ] 测试防止共享机制
- [ ] 了解如何在 Supabase 中查看绑定信息
- [ ] 了解如何手动修改绑定信息

完成以上步骤后，用户绑定功能就可以正常使用了！🎉
