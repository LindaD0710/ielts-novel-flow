#!/bin/bash
# 半自动内容生产流 - 快速测试脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}半自动内容生产流 - 测试脚本${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# 检查 Python 版本
echo -e "${YELLOW}检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 已安装: $(python3 --version)${NC}"
echo ""

# 检查必需文件
echo -e "${YELLOW}检查必需文件...${NC}"
REQUIRED_FILES=("step1_get_prompt.py" "step2_save_chapter.py" "curriculum_manager.py" "ielts_source.json" "story_config.json")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file 不存在${NC}"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}缺少必需文件，请先创建${NC}"
    exit 1
fi
echo ""

# 步骤 1：生成 Prompt
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}步骤 1：生成 Prompt${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
read -p "按 Enter 键开始生成 Prompt..."
python3 step1_get_prompt.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Prompt 生成失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Prompt 已生成到: current_prompt.txt${NC}"
echo ""

# 提示用户使用 ChatGPT
echo -e "${YELLOW}============================================================${NC}"
echo -e "${YELLOW}下一步：使用 ChatGPT 生成内容${NC}"
echo -e "${YELLOW}============================================================${NC}"
echo ""
echo "1. 打开 current_prompt.txt，复制全部内容"
echo "2. 访问 https://chat.openai.com"
echo "3. 粘贴 Prompt 到 ChatGPT"
echo "4. 等待 ChatGPT 生成内容"
echo "5. 复制生成的内容到 raw_story.txt"
echo ""
read -p "完成后按 Enter 键继续..."

# 检查 raw_story.txt 是否有内容
if [ ! -s raw_story.txt ]; then
    echo -e "${RED}❌ raw_story.txt 为空或不存在${NC}"
    echo "请先粘贴 ChatGPT 生成的内容到 raw_story.txt"
    exit 1
fi

echo -e "${GREEN}✅ 检测到 raw_story.txt 有内容${NC}"
echo ""

# 步骤 2：入库上架
echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}步骤 2：入库上架${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
read -p "按 Enter 键开始入库上架..."
python3 step2_save_chapter.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 入库上架失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ 入库上架完成！${NC}"
echo ""

# 检查生成的文件
echo -e "${YELLOW}检查生成的文件...${NC}"
GENERATED_DIR="../src/data/generated"
if [ -d "$GENERATED_DIR" ]; then
    LATEST_FILE=$(ls -t "$GENERATED_DIR"/book-*.json 2>/dev/null | head -1)
    if [ -n "$LATEST_FILE" ]; then
        echo -e "${GREEN}✅ 最新章节文件: $LATEST_FILE${NC}"
        echo -e "${BLUE}   文件大小: $(wc -c < "$LATEST_FILE") 字节${NC}"
    else
        echo -e "${YELLOW}⚠️  未找到生成的章节文件${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  生成目录不存在${NC}"
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}测试完成！${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "下一步："
echo "1. 检查 library.ts 是否已更新"
echo "2. 启动前端: cd .. && npm run dev"
echo "3. 访问 http://localhost:3000 验证结果"

