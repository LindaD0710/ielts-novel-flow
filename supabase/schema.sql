-- IELTS Novel Flow - 访问码表结构
-- 在 Supabase SQL Editor 中执行此 SQL 创建表

-- 创建 access_codes 表
CREATE TABLE IF NOT EXISTS access_codes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'revoked')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  validity_days INTEGER NOT NULL DEFAULT 365,
  usage_count INTEGER NOT NULL DEFAULT 0,
  last_used_at TIMESTAMPTZ,
  notes TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_access_codes_code ON access_codes(code);
CREATE INDEX IF NOT EXISTS idx_access_codes_status ON access_codes(status);
CREATE INDEX IF NOT EXISTS idx_access_codes_expires_at ON access_codes(expires_at);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_access_codes_updated_at
  BEFORE UPDATE ON access_codes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 添加注释
COMMENT ON TABLE access_codes IS '访问码表，存储用户访问码及其使用情况';
COMMENT ON COLUMN access_codes.code IS '访问码（格式：XXXX-XXXX）';
COMMENT ON COLUMN access_codes.status IS '状态：active(有效), expired(已过期), revoked(已撤销)';
COMMENT ON COLUMN access_codes.expires_at IS '过期时间（用户可在此时间前多次使用）';
COMMENT ON COLUMN access_codes.usage_count IS '使用次数统计';
COMMENT ON COLUMN access_codes.last_used_at IS '最后使用时间';
