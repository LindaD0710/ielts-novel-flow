-- IELTS Novel Flow - 添加用户绑定功能
-- 在 Supabase SQL Editor 中执行此 SQL 添加用户绑定字段

-- 添加用户绑定相关字段
ALTER TABLE access_codes 
ADD COLUMN IF NOT EXISTS bound_user_email TEXT,
ADD COLUMN IF NOT EXISTS bound_user_phone TEXT,
ADD COLUMN IF NOT EXISTS bound_at TIMESTAMPTZ;

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_access_codes_bound_user_email ON access_codes(bound_user_email);
CREATE INDEX IF NOT EXISTS idx_access_codes_bound_user_phone ON access_codes(bound_user_phone);

-- 添加注释
COMMENT ON COLUMN access_codes.bound_user_email IS '绑定的用户邮箱（用于防止多人共用访问码）';
COMMENT ON COLUMN access_codes.bound_user_phone IS '绑定的用户手机号（用于防止多人共用访问码）';
COMMENT ON COLUMN access_codes.bound_at IS '绑定时间';
