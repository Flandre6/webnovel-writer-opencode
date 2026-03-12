@echo off

echo.
echo ========================================
echo   Webnovel Writer Installer
echo ========================================
echo.

set "PROJECT_DIR=%CD%"
set "REPO=lujih/webnovel-writer-opencode"

echo [1/5] Downloading...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/%REPO%/archive/refs/heads/main.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing"
if not exist "webnovel-writer.zip" (
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/%REPO%/archive/refs/heads/master.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing"
)

if not exist "webnovel-writer.zip" (
    echo ERROR: Download failed
    pause
    exit /b 1
)

echo [2/5] Extracting...
powershell -Command "Expand-Archive -Path 'webnovel-writer.zip' -DestinationPath '.' -Force"
del /Q webnovel-writer.zip

echo [3/5] Creating directories...
if not exist ".opencode" mkdir ".opencode"
if not exist ".opencode\skills" mkdir ".opencode\skills"
if not exist ".opencode\skills\webnovel-writer" mkdir ".opencode\skills\webnovel-writer"
if not exist ".opencode\agents" mkdir ".opencode\agents"

echo [4/5] Copying files...

REM Find source directory
set "SOURCE_DIR="
for /d %%d in ("%PROJECT_DIR%\webnovel-writer-opencode-*") do (
    set "SOURCE_DIR=%%d"
)

if not defined SOURCE_DIR (
    echo ERROR: Source directory not found
    dir /b "%PROJECT_DIR%"
    pause
    exit /b 1
)

echo Source: %SOURCE_DIR%

REM Copy each skill folder individually
for /d %%d in ("%SOURCE_DIR%\skills\*") do (
    echo   Copying %%~nxd...
    xcopy /E /I /Y "%%d" ".opencode\skills\webnovel-writer\%%~nxd\" >nul 2>&1
)

REM Check if skills were copied
if exist ".opencode\skills\webnovel-writer\webnovel-init\SKILL.md" (
    echo   Skills: OK
) else (
    echo   Skills: FAILED
    dir /s /b ".opencode\skills"
)

REM Copy agents
if exist "%SOURCE_DIR%\agents" (
    xcopy /E /I /Y "%SOURCE_DIR%\agents\*" ".opencode\agents\" >nul 2>&1
    echo   Agents: OK
) else (
    echo   Agents: NOT FOUND
)

REM Copy .env.example
if exist "%SOURCE_DIR%\.env.example" (
    copy /Y "%SOURCE_DIR%\.env.example" ".env.example" >nul 2>&1
    echo   .env.example: OK
) else (
    (
        echo # Webnovel Writer Config
        echo EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
        echo EMBED_MODEL=Qwen/Qwen3-Embedding-8B
        echo EMBED_API_KEY=your_api_key
        echo.
        echo RERANK_BASE_URL=https://api.jina.ai/v1
        echo RERANK_MODEL=jina-reranker-v3
        echo RERANK_API_KEY=your_api_key
    ) > .env.example
    echo   .env.example: CREATED
)

REM Clean up
if exist "%SOURCE_DIR%" rmdir /S /Q "%SOURCE_DIR%"

echo [5/5] Done!
echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.

dir /b ".opencode\skills\webnovel-writer"

echo.
echo Next steps:
echo   1. Copy .env.example to .env and add API Key
echo   2. In OpenCode, use /webnovel-init

pause
