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

echo [3/5] Creating .opencode directory...
if not exist ".opencode" mkdir ".opencode"

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

echo [4/5] Copying all files to .opencode...

REM Copy skills
if exist "%SOURCE_DIR%\skills" (
    xcopy /E /I /Y "%SOURCE_DIR%\skills\*" ".opencode\skills\" >nul 2>&1
    echo   skills: OK
)

REM Copy genres
if exist "%SOURCE_DIR%\genres" (
    xcopy /E /I /Y "%SOURCE_DIR%\genres\*" ".opencode\genres\" >nul 2>&1
    echo   genres: OK
)

REM Copy references
if exist "%SOURCE_DIR%\references" (
    xcopy /E /I /Y "%SOURCE_DIR%\references\*" ".opencode\references\" >nul 2>&1
    echo   references: OK
)

REM Copy templates
if exist "%SOURCE_DIR%\templates" (
    xcopy /E /I /Y "%SOURCE_DIR%\templates\*" ".opencode\templates\" >nul 2>&1
    echo   templates: OK
)

REM Copy scripts
if exist "%SOURCE_DIR%\scripts" (
    xcopy /E /I /Y "%SOURCE_DIR%\scripts" ".opencode\scripts\" >nul 2>&1
    echo   scripts: OK
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

REM Clean up source directory
if exist "%SOURCE_DIR%" rmdir /S /Q "%SOURCE_DIR%"

echo [5/5] Done!
echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.

dir /b ".opencode"

echo.
echo Next steps:
echo   1. Copy .env.example to .env and add API Key
echo   2. In OpenCode, use /webnovel-init

pause
