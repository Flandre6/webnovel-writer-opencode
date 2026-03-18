@echo off
chcp 65001 >nul 2>&1

echo.
echo ========================================
echo   Webnovel Writer Installer
echo ========================================
echo.

set "PROJECT_DIR=%CD%"
set "REPO=lujih/webnovel-writer-opencode"
set "SUCCESS=0"

echo [1/6] Downloading...
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/%REPO%/archive/refs/heads/master.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing -TimeoutSec 60 -ErrorAction Stop; exit 0 } catch { exit 1 }"
if %errorlevel% neq 0 (
    echo Trying mirror...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://github.akams.cn/%REPO%/archive/refs/heads/master.zip' -OutFile 'webnovel-writer.zip' -UseBasicParsing -TimeoutSec 60 -ErrorAction Stop; exit 0 } catch { exit 1 }"
)

if not exist "webnovel-writer.zip" (
    echo ERROR: Download failed
    echo.
    echo Solutions:
    echo   1. Check internet connection
    echo   2. Use VPN if in restricted region
    echo   3. Download manually from: https://github.com/%REPO%/archive/master.zip
    echo.
    pause
    exit /b 1
)

echo [2/6] Extracting...
powershell -Command "Expand-Archive -Path 'webnovel-writer.zip' -DestinationPath '.' -Force"
del /Q webnovel-writer.zip 2>nul

echo [3/6] Setting up directories...
if not exist ".opencode" mkdir ".opencode"

set "SOURCE_DIR="
for /d %%d in ("%PROJECT_DIR%\webnovel-writer-opencode-*") do (
    set "SOURCE_DIR=%%d"
)

if not defined SOURCE_DIR (
    echo ERROR: Extraction failed - source dir not found
    pause
    exit /b 1
)

echo [4/6] Copying files...
xcopy /E /I /Y "%SOURCE_DIR%\.opencode\skills" ".opencode\skills\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\.opencode\genres" ".opencode\genres\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\.opencode\references" ".opencode\references\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\.opencode\templates" ".opencode\templates\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\.opencode\scripts" ".opencode\scripts\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\opencode.json" "." >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\prompts" "prompts\" >nul 2>&1
xcopy /E /I /Y "%SOURCE_DIR%\init.bat" "." >nul 2>&1
echo   Files copied

REM Cleanup unwanted directories
if exist "docs" rmdir /S /Q "docs" 2>nul

echo [5/6] Installing Python dependencies...
if exist "%SOURCE_DIR%\requirements.txt" (
    pip install -r "%SOURCE_DIR%\requirements.txt" >nul 2>&1
    if %errorlevel% equ 0 (
        echo   Python deps: OK
    ) else (
        echo   Python deps: Already installed or skipped
    )
)

echo [6/6] Creating .env...
if exist "%SOURCE_DIR%\.env" (
    copy /Y "%SOURCE_DIR%\.env" ".env" >nul 2>&1
) else (
    (
        echo # Webnovel Writer Config
        echo # Fill in your API Key
        echo.
        echo EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
        echo EMBED_MODEL=Qwen/Qwen3-Embedding-8B
        echo EMBED_API_KEY=your_api_key
        echo.
        echo RERANK_BASE_URL=https://api.jina.ai/v1
        echo RERANK_MODEL=jina-reranker-v3
        echo RERANK_API_KEY=your_api_key
    ) > .env
)
echo   .env: OK

rmdir /S /Q "%SOURCE_DIR%" 2>nul

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env and add your API Key
echo   2. Restart OpenCode
echo.
pause
