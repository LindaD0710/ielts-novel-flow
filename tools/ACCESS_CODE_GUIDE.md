# 访问码生成与管理工具使用指南

## 概述

`access_code_manager.py` 是一个用于生成、管理和导出访问码的 Python 工具。每个访问码有效期为 1 年（365天），用户可以在有效期内多次使用。

## 安装要求

- Python 3.7+
- 无需额外依赖（仅使用标准库）

## 使用方法

### 1. 生成访问码

生成指定数量的访问码（默认有效期 365 天）：

```bash
# 生成 10 个访问码（默认）
python3 tools/access_code_manager.py generate

# 生成 50 个访问码
python3 tools/access_code_manager.py generate -n 50

# 生成访问码并添加备注（如客户名称、批次号等）
python3 tools/access_code_manager.py generate -n 20 --notes "客户A-2026年1月批次"

# 自定义有效期（如 180 天）
python3 tools/access_code_manager.py generate -n 10 -d 180
```

**访问码格式**：`XXXX-XXXX`（字母数字混合，大写，排除易混淆字符 0/O/I/1）

### 2. 列出访问码

查看所有访问码及其状态：

```bash
# 列出所有访问码
python3 tools/access_code_manager.py list

# 只列出有效的访问码
python3 tools/access_code_manager.py list --status active

# 只列出已过期的访问码
python3 tools/access_code_manager.py list --status expired

# 只列出已撤销的访问码
python3 tools/access_code_manager.py list --status revoked

# 不显示统计信息
python3 tools/access_code_manager.py list --no-stats
```

### 3. 导出访问码到 CSV

将访问码导出为 CSV 文件，方便发给客户或用于记录：

```bash
# 导出所有访问码（默认保存到 tools/access_codes_YYYYMMDD_HHMMSS.csv）
python3 tools/access_code_manager.py export

# 指定输出文件路径
python3 tools/access_code_manager.py export -o /path/to/output.csv

# 只导出有效的访问码
python3 tools/access_code_manager.py export --status active -o active_codes.csv
```

**CSV 文件包含字段**：
- `code`: 访问码
- `status`: 状态（active/expired/revoked）
- `created_at`: 创建时间
- `expires_at`: 到期时间
- `validity_days`: 有效期（天数）
- `usage_count`: 使用次数
- `last_used_at`: 最后使用时间
- `notes`: 备注

### 4. 撤销访问码

如果某个访问码需要立即失效（如客户退款、违规使用等）：

```bash
python3 tools/access_code_manager.py revoke A3F7-K9M2
```

## 数据存储

访问码数据存储在：`src/data/access_codes.json`

**文件结构**：
```json
{
  "codes": [
    {
      "code": "A3F7-K9M2",
      "status": "active",
      "created_at": "2026-01-14T10:00:00",
      "expires_at": "2027-01-14T10:00:00",
      "validity_days": 365,
      "usage_count": 5,
      "last_used_at": "2026-01-20T15:30:00",
      "notes": "客户A-2026年1月批次"
    }
  ],
  "last_updated": "2026-01-14T10:00:00"
}
```

## 访问码状态说明

- **active**: 有效，可以使用
- **expired**: 已过期（超过 `expires_at` 时间）
- **revoked**: 已撤销（手动撤销或违规使用）

## 网站验证逻辑

1. 用户在前端输入访问码
2. 前端调用 `/api/validate-code` API
3. API 验证访问码：
   - 检查访问码是否存在
   - 检查状态是否为 `active`
   - 检查是否过期（当前时间 < `expires_at`）
   - 如果通过，更新 `usage_count` 和 `last_used_at`
4. 验证成功后，用户可以在 1 年内多次使用该访问码登录

## 注意事项

1. **文件权限**：确保 `src/data/access_codes.json` 文件可读写
2. **备份**：定期备份访问码数据文件
3. **生产环境**：在生产环境中，建议使用数据库（如 PostgreSQL、MongoDB）替代 JSON 文件存储
4. **安全性**：访问码数据文件不应提交到公开的 Git 仓库（可添加到 `.gitignore`）

## 快速开始示例

```bash
# 1. 生成 20 个访问码给新客户
python3 tools/access_code_manager.py generate -n 20 --notes "新客户-2026年1月"

# 2. 查看生成的访问码
python3 tools/access_code_manager.py list --status active

# 3. 导出为 CSV 发给客户
python3 tools/access_code_manager.py export --status active -o customer_codes.csv

# 4. 如果某个访问码需要撤销
python3 tools/access_code_manager.py revoke A3F7-K9M2
```

## 常见问题

**Q: 访问码可以多次使用吗？**  
A: 是的，在有效期内（默认 1 年）可以无限次使用。

**Q: 如何查看某个访问码的使用情况？**  
A: 使用 `list` 命令查看，或直接查看 `src/data/access_codes.json` 文件。

**Q: 访问码过期后会自动更新状态吗？**  
A: 不会自动更新文件中的状态，但在验证时会检查是否过期。如果需要批量标记过期，可以手动编辑 JSON 文件或扩展脚本功能。

**Q: 可以修改访问码的有效期吗？**  
A: 可以手动编辑 `src/data/access_codes.json` 文件中的 `expires_at` 字段，或使用脚本重新生成。
