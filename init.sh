#!/bin/bash
# Webnovel Writer Installer
# Usage: curl -sL https://raw.githubusercontent.com/lujih/webnovel-writer-opencode/master/init.sh | bash

REPO="lujih/webnovel-writer-opencode"
BRANCH="master"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/${BRANCH}.zip"

echo "Webnovel Writer Installer"
echo ""

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PROJECT_DIR="$(pwd -W)"
else
    PROJECT_DIR="$(pwd)"
fi

echo "Project: $PROJECT_DIR"

# Download with retry and fallback
MAX_RETRIES=3
RETRY_COUNT=0
SUCCESS=0

# Try GitHub master first
while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ $SUCCESS -eq 0 ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Downloading from GitHub (attempt $RETRY_COUNT/$MAX_RETRIES)..."
    
    if curl -sL --max-time 120 "$ARCHIVE_URL" -o "repo.zip" 2>/dev/null; then
        if [ -s "repo.zip" ]; then
            SUCCESS=1
        fi
    fi
    
    if [ $SUCCESS -eq 0 ]; then
        sleep 2
    fi
done

# Try China mirror as fallback
if [ $SUCCESS -eq 0 ]; then
    echo "Trying China mirror (github.akams.cn)..."
    if curl -sL --max-time 120 "https://github.akams.cn/${REPO}/archive/refs/heads/${BRANCH}.zip" -o "repo.zip" 2>/dev/null; then
        if [ -s "repo.zip" ]; then
            SUCCESS=1
        fi
    fi
fi

if [ $SUCCESS -eq 0 ]; then
    echo ""
    echo "ERROR: Download failed after all attempts"
    echo "Possible solutions:"
    echo "  1. Check your internet connection"
    echo "  2. Use a VPN if you're in a restricted region"
    echo "  3. Manually download from: https://github.com/$REPO/archive/$BRANCH.zip"
    exit 1
fi

echo "Extracting..."
unzip -q "repo.zip"
rm -f "repo.zip"

# Find extracted directory
SOURCE_DIR=""
for d in "$PROJECT_DIR"/webnovel-writer-opencode-*; do
    if [ -d "$d" ]; then
        SOURCE_DIR="$d"
        break
    fi
done

if [ -z "$SOURCE_DIR" ]; then
    echo "ERROR: Could not find extracted directory"
    exit 1
fi

echo "Installing to .opencode..."
mkdir -p "${PROJECT_DIR}/.opencode"

# Copy directories from .opencode/
[ -d "$SOURCE_DIR/.opencode/skills" ] && cp -r "$SOURCE_DIR/.opencode/skills" "${PROJECT_DIR}/.opencode/" && echo "skills: OK"
[ -d "$SOURCE_DIR/.opencode/genres" ] && cp -r "$SOURCE_DIR/.opencode/genres" "${PROJECT_DIR}/.opencode/" && echo "genres: OK"
[ -d "$SOURCE_DIR/.opencode/references" ] && cp -r "$SOURCE_DIR/.opencode/references" "${PROJECT_DIR}/.opencode/" && echo "references: OK"
[ -d "$SOURCE_DIR/.opencode/templates" ] && cp -r "$SOURCE_DIR/.opencode/templates" "${PROJECT_DIR}/.opencode/" && echo "templates: OK"
[ -d "$SOURCE_DIR/.opencode/scripts" ] && cp -r "$SOURCE_DIR/.opencode/scripts" "${PROJECT_DIR}/.opencode/" && echo "scripts: OK"

# Copy root files
[ -f "$SOURCE_DIR/opencode.json" ] && cp "$SOURCE_DIR/opencode.json" "${PROJECT_DIR}/" && echo "opencode.json: OK"
[ -d "$SOURCE_DIR/prompts" ] && cp -r "$SOURCE_DIR/prompts" "${PROJECT_DIR}/" && echo "prompts: OK"
[ -f "$SOURCE_DIR/init.sh" ] && cp "$SOURCE_DIR/init.sh" "${PROJECT_DIR}/" && echo "init.sh: OK"
[ -f "$SOURCE_DIR/init.bat" ] && cp "$SOURCE_DIR/init.bat" "${PROJECT_DIR}/" && echo "init.bat: OK"

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "$SOURCE_DIR/requirements.txt" ]; then
    pip install -r "$SOURCE_DIR/requirements.txt" 2>/dev/null && echo "Python dependencies: OK" || echo "Python dependencies: SKIPPED"
else
    pip install -r "https://raw.githubusercontent.com/${REPO}/${BRANCH}/requirements.txt" 2>/dev/null && echo "Python dependencies: OK" || echo "Python dependencies: SKIPPED"
fi

# Copy or create .env
if [ -f "$SOURCE_DIR/.env" ]; then
    cp "$SOURCE_DIR/.env" "${PROJECT_DIR}/.env"
    echo ".env: OK"
else
    cat > "${PROJECT_DIR}/.env" << 'EOF'
# Webnovel Writer Config
# Fill in your API Key

EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_api_key
EOF
    echo ".env: CREATED"
fi

# Cleanup
rm -rf "$SOURCE_DIR"

echo ""
echo "Done!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API Key"
echo "  2. Restart OpenCode"
