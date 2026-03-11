#!/bin/bash
# Webnovel Writer 一键安装脚本
# 使用方式: curl -sL https://raw.githubusercontent.com/lingfengQAQ/webnovel-writer/main/init.sh | bash

set -e

# 配置
REPO="lingfengQAQ/webnovel-writer"
BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/${REPO}/${BRANCH}"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Webnovel Writer 安装脚本${NC}"
echo ""

# 检测是否为 Git Bash (Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PROJECT_DIR="$(pwd -W)"
else
    PROJECT_DIR="$(pwd)"
fi

echo -e "${YELLOW}项目目录: ${PROJECT_DIR}${NC}"
echo ""

# 创建目录
echo -e "${GREEN}📁 创建 .opencode 目录...${NC}"
mkdir -p "${PROJECT_DIR}/.opencode/skills/webnovel-writer"
mkdir -p "${PROJECT_DIR}/.opencode/agents"

# 下载 Skills
echo -e "${GREEN}📥 下载 Skills...${NC}"
curl -sL "${BASE_URL}/skills" -o ".opencode/skills.tmp" || true
if [ -d ".opencode/skills.tmp" ]; then
    cp -r .opencode/skills.tmp/* "${PROJECT_DIR}/.opencode/skills/webnovel-writer/" 2>/dev/null || true
    rm -rf .opencode/skills.tmp
fi

# 如果上面的方法不行，尝试直接复制（假设用户在克隆的仓库中）
if [ ! -f "${PROJECT_DIR}/.opencode/skills/webnovel-writer/SKILL.md" ]; then
    echo -e "${YELLOW}⚠️  Skills 文件未找到，请确保在正确的目录运行或手动复制${NC}"
fi

# 下载 Agents
echo -e "${GREEN}📥 下载 Agents...${NC}"
curl -sL "${BASE_URL}/agents" -o ".opencode/agents.tmp" || true
if [ -d ".opencode/agents.tmp" ]; then
    cp -r .opencode/agents.tmp/* "${PROJECT_DIR}/.opencode/agents/" 2>/dev/null || true
    rm -rf .opencode/agents.tmp
fi

# 如果上面的方法不行，尝试直接复制
if [ ! -f "${PROJECT_DIR}/.opencode/agents/context-agent.md" ]; then
    echo -e "${YELLOW}⚠️  Agents 文件未找到，请确保在正确的目录运行或手动复制${NC}"
fi

# 创建 .env.example
echo -e "${GREEN}📝 创建 .env.example...${NC}"
curl -sL "${BASE_URL}/../.env.example" -o "${PROJECT_DIR}/.env.example" 2>/dev/null || cat > "${PROJECT_DIR}/.env.example" << 'EOF'
# Webnovel Writer 配置
# 复制为 .env 后填入你的 API Key

# Embedding
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_embed_api_key

# Rerank
RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_rerank_api_key
EOF

echo ""
echo -e "${GREEN}✅ 安装完成!${NC}"
echo ""
echo -e "${YELLOW}📝 下一步:${NC}"
echo "  1. 复制 .env.example 为 .env 并填入 API Key"
echo "  2. 在 OpenCode 中使用 /webnovel-init 开始"
echo ""
