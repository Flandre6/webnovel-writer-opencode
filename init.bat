@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo 🚀 Webnovel Writer 安装脚本
echo.

set "REPO=lingfengQAQ/webnovel-writer"
set "BRANCH=main"
set "BASE_URL=https://raw.githubusercontent.com/%REPO%/%BRANCH%"

set "PROJECT_DIR=%CD%"

echo 📁 项目目录: %PROJECT_DIR%
echo.

REM 创建目录
echo 📁 创建 .opencode 目录...
if not exist ".opencode\skills\webnovel-writer" mkdir ".opencode\skills\webnovel-writer"
if not exist ".opencode\agents" mkdir ".opencode\agents"

REM 下载 Skills (使用 PowerShell)
echo 📥 下载 Skills...
powershell -Command "Invoke-WebRequest -Uri '%BASE_URL%/skills' -OutFile 'skills.zip' -UseBasicParsing" 2>nul
if exist "skills.zip" (
    powershell -Command "Expand-Archive -Path 'skills.zip' -DestinationPath '.opencode\temp_skills' -Force" 2>nul
    if exist ".opencode\temp_skills" (
        xcopy /E /I /Y ".opencode\temp_skills\*" ".opencode\skills\webnovel-writer\" 2>nul
        rmdir /S /Q ".opencode\temp_skills" 2>nul
    )
    del skills.zip 2>nul
)

REM 如果下载失败，尝试从当前目录复制
if not exist ".opencode\skills\webnovel-writer\SKILL.md" (
    if exist "skills" (
        xcopy /E /I /Y "skills\*" ".opencode\skills\webnovel-writer\" 2>nul
    )
)

REM 下载 Agents
echo 📥 下载 Agents...
powershell -Command "Invoke-WebRequest -Uri '%BASE_URL%/agents' -OutFile 'agents.zip' -UseBasicParsing" 2>nul
if exist "agents.zip" (
    powershell -Command "Expand-Archive -Path 'agents.zip' -DestinationPath '.opencode\temp_agents' -Force" 2>nul
    if exist ".opencode\temp_agents" (
        xcopy /E /I /Y ".opencode\temp_agents\*" ".opencode\agents\" 2>nul
        rmdir /S /Q ".opencode\temp_agents" 2>nul
    )
    del agents.zip 2>nul
)

REM 如果下载失败，尝试从当前目录复制
if not exist ".opencode\agents\context-agent.md" (
    if exist "agents" (
        xcopy /E /I /Y "agents\*" ".opencode\agents\" 2>nul
    )
)

REM 创建 .env.example
echo 📝 创建 .env.example...
if not exist ".env.example" (
    (
        echo # Webnovel Writer 配置
        echo # 复制为 .env 后填入你的 API Key
        echo.
        echo # Embedding
        echo EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
        echo EMBED_MODEL=Qwen/Qwen3-Embedding-8B
        echo EMBED_API_KEY=your_embed_api_key
        echo.
        echo # Rerank
        echo RERANK_BASE_URL=https://api.jina.ai/v1
        echo RERANK_MODEL=jina-reranker-v3
        echo RERANK_API_KEY=your_rerank_api_key
    ) > .env.example
)

echo.
echo ✅ 安装完成!
echo.
echo 📝 下一步:
echo  1. 复制 .env.example 为 .env 并填入 API Key
echo  2. 在 OpenCode 中使用 /webnovel-init 开始
echo.

endlocal
pause
