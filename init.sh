#!/bin/bash
# Webnovel Writer Installer
# Usage: curl -sL https://raw.githubusercontent.com/lujih/webnovel-writer-opencode/main/init.sh | bash

set -e

REPO="lujih/webnovel-writer-opencode"
BRANCH="main"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.zip"

echo "Webnovel Writer Installer"
echo ""

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PROJECT_DIR="$(pwd -W)"
else
    PROJECT_DIR="$(pwd)"
fi

echo "Project: $PROJECT_DIR"

TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "Downloading..."
curl -sL "$ARCHIVE_URL" -o "repo.zip"
unzip -q "repo.zip"
cd "webnovel-writer-${BRANCH}"

echo "Installing..."
mkdir -p "${PROJECT_DIR}/.opencode"

cp -r skills "${PROJECT_DIR}/.opencode/"
cp -r genres "${PROJECT_DIR}/.opencode/"
cp -r references "${PROJECT_DIR}/.opencode/"
cp -r templates "${PROJECT_DIR}/.opencode/"
cp -r scripts "${PROJECT_DIR}/.opencode/"

if [ -f ".env.example" ]; then
    cp ".env.example" "${PROJECT_DIR}/.env.example"
else
    cat > "${PROJECT_DIR}/.env.example" << 'EOF'
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_api_key
EOF
fi

cd "$PROJECT_DIR"
rm -rf "$TEMP_DIR"

echo ""
echo "Done!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and add API Key"
echo "  2. In OpenCode, use /webnovel-init"
