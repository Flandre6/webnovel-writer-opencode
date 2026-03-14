@echo off

echo.
echo ========================================
echo   Webnovel Writer Installer
echo ========================================
echo.

set "PROJECT_DIR=%CD%"
set "REPO=lujih/webnovel-writer-opencode"

echo [1/5] Downloading...
set "DOWNLOADED=0"

REM Try GitHub master branch
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/%REPO%/archive/refs/heads/master.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing -TimeoutSec 60 -ErrorAction Stop; if (Test-Path 'webnovel-writer.zip') { exit 0 } else { exit 1 } } catch { exit 1 }"
if %errorlevel% equ 0 set "DOWNLOADED=1"

REM Try China mirror (ghproxy)
if %DOWNLOADED% equ 0 (
    powershell -Command "try { Invoke-WebRequest -Uri 'https://ghproxy.com/https://github.com/%REPO%/archive/refs/heads/master.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing -TimeoutSec 60 -ErrorAction Stop; if (Test-Path 'webnovel-writer.zip') { exit 0 } else { exit 1 } } catch { exit 1 }"
    if %errorlevel% equ 0 set "DOWNLOADED=1"
)

if %DOWNLOADED% equ 0 (
    powershell -Command "try { Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/%REPO%/master/init.bat' -OutFile 'init.bat' -UseBasicParsing -TimeoutSec 60; exit 0 } catch { exit 1 }"
    if %errorlevel% equ 0 (
        echo.
        echo NOTE: GitHub download failed, but init.bat is accessible.
        echo This may be a network issue. Please try:
        echo   1. Using a VPN or proxy
        echo   2. Manually downloading the repo from GitHub
        echo.
        pause
        exit /b 1
    )
)

if not exist "webnovel-writer.zip" (
    echo ERROR: Download failed - network issue or repo not found
    echo.
    echo Possible solutions:
    echo   1. Check your internet connection
    echo   2. Use a VPN if you're in a restricted region
    echo   3. Manually download from: https://github.com/%REPO%/archive/master.zip
    echo.
    pause
    exit /b 1
)

echo [2/5] Extracting...
powershell -Command "Expand-Archive -Path 'webnovel-writer.zip' -DestinationPath '.' -Force"
del /Q webnovel-writer.zip 2>nul

echo [3/5] Creating .opencode directory...
if not exist ".opencode" mkdir ".opencode"

REM Find source directory
set "SOURCE_DIR="
for /d %%d in ("%PROJECT_DIR%\webnovel-writer-opencode-*") do (
    set "SOURCE_DIR=%%d"
)

if not defined SOURCE_DIR (
    echo ERROR: Source directory not found after extraction
    dir /b "%PROJECT_DIR%"
    pause
    exit /b 1
)

echo [4/5] Copying files from %SOURCE_DIR%...

REM Copy each directory
if exist "%SOURCE_DIR%\skills" (
    xcopy /E /I /Y "%SOURCE_DIR%\skills\*" ".opencode\skills\" >nul 2>&1
    echo   skills: OK
) else (
    echo   skills: NOT FOUND
)

if exist "%SOURCE_DIR%\genres" (
    xcopy /E /I /Y "%SOURCE_DIR%\genres\*" ".opencode\genres\" >nul 2>&1
    echo   genres: OK
)

if exist "%SOURCE_DIR%\references" (
    xcopy /E /I /Y "%SOURCE_DIR%\references\*" ".opencode\references\" >nul 2>&1
    echo   references: OK
)

if exist "%SOURCE_DIR%\templates" (
    xcopy /E /I /Y "%SOURCE_DIR%\templates\*" ".opencode\templates\" >nul 2>&1
    echo   templates: OK
)

if exist "%SOURCE_DIR%\scripts" (
    xcopy /E /I /Y "%SOURCE_DIR%\scripts" ".opencode\scripts\" >nul 2>&1
    echo   scripts: OK
)

REM Copy opencode.json and prompts to project root
if exist "%SOURCE_DIR%\opencode.json" (
    copy /Y "%SOURCE_DIR%\opencode.json" "opencode.json" >nul 2>&1
    echo   opencode.json: OK
)

if exist "%SOURCE_DIR%\prompts" (
    xcopy /E /I /Y "%SOURCE_DIR%\prompts" "prompts\" >nul 2>&1
    echo   prompts: OK
)

REM Install Python dependencies
echo.
echo [5/6] Installing Python dependencies...
pip install -r https://raw.githubusercontent.com/%REPO%/master/requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo   Python dependencies: OK
) else (
    echo   Python dependencies: SKIPPED (may already be installed)
)

REM Copy .env
if exist "%SOURCE_DIR%\.env" (
    copy /Y "%SOURCE_DIR%\.env" ".env" >nul 2>&1
    echo   .env: OK
) else (
    (
        echo # Webnovel Writer Config
        echo # 编辑填入你的 API Key
        echo.
        echo EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
        echo EMBED_MODEL=Qwen/Qwen3-Embedding-8B
        echo EMBED_API_KEY=your_api_key
        echo.
        echo RERANK_BASE_URL=https://api.jina.ai/v1
        echo RERANK_MODEL=jina-reranker-v3
        echo RERANK_API_KEY=your_api_key
    ) > .env
    echo   .env: CREATED
)

REM Clean up
if exist "%SOURCE_DIR%" rmdir /S /Q "%SOURCE_DIR%"

echo [6/6] Done!
echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.

dir /b ".opencode"

echo.
echo Next steps:
echo   1. Edit .env and add your API Key
echo   2. In OpenCode, use /webnovel-init

pause
