---
name: webnovel-export
description: 将正文导出为 Markdown/TXT/EPUB 格式。当用户要求导出或发布章节时使用。
allowed-tools: Read Write Edit Bash
---

# 正文导出

## 目标

将网文正文导出为不同格式，便于发布或存档。

## 支持格式

| 格式 | 说明 | 依赖 |
|------|------|------|
| Markdown | Markdown 格式，可用任何编辑器打开 | 无 |
| TXT | 纯文本，最通用 | 无 |
| EPUB | 电子书，阅读器可用 | ebooklib |

## 使用方式

### 1. 交互式导出（推荐）

直接运行 `export` 命令不带任何参数，进入交互式导出向导：

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export
```

交互流程：
```
=== 正文导出 ===
项目: 我的小说
共 100 章，3 卷

请选择导出格式:
  [1] Markdown    [2] TXT    [3] EPUB
格式 [1]: 1
  -> markdown

请选择导出范围:
  [1] 全部章节 (100 章)
  [2] 按章节范围
  [3] 按卷 (第1卷(30章), 第2卷(40章), 第3卷(30章))
范围 [1]: 3
  请选择卷号 (1, 2, 3): 2
  -> 第2卷，共 40 章

导出文件路径 [导出/novel.md]:
路径 (回车使用默认): 导出/第二卷.md
  -> 导出/第二卷.md

确认导出? [Y/n]: y

OK: Exported Markdown: 导出/第二卷.md (40 chapters)
```

### 2. 列出可导出章节

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export list
```

### 3. 导出全部章节

```bash
# 导出为 Markdown
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format markdown

# 导出为 TXT
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format txt

# 导出为 EPUB
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format epub --author "作者名"
```

### 4. 导出指定章节

```bash
# 导出第 1-10 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1-10 --format markdown

# 导出第 1, 3, 5 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1,3,5 --format txt

# 导出第 20-30 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 20-30 --format epub
```

### 5. 导出指定卷

```bash
# 导出第 1 卷
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --volume 1 --format markdown

# 导出第 2 卷为 EPUB
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --volume 2 --format epub --author "作者名"
```

### 6. 指定输出路径

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format markdown --output 我的小说.md
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--range` | 章节范围，如 `1-10`、`1,3,5`、`20-30`，或 `all`（默认） |
| `--volume` | 导出指定卷，如 `1`、`2` |
| `--format` | 输出格式：`markdown`（默认）、`txt`、`epub` |
| `--output` | 输出文件路径（默认自动生成在 `导出/` 目录） |
| `--author` | 作者名（仅 EPUB 格式需要） |

## 输出位置

导出的文件默认保存在项目根目录的 `导出/` 文件夹下：
- `导出/novel.md`
- `导出/novel.txt`
- `导出/novel.epub`

## 示例

### 导出全部章节为 Markdown
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --format markdown
```

### 导出前 100 章为 EPUB
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --range 1-100 --format epub --output "小说.epub"
```

### 导出单章为 TXT
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --range 31 --format txt
```

### 导出第一卷为 Markdown
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --volume 1 --format markdown
```

## 安装可选依赖

```bash
# 安装 EPUB 支持
pip install ebooklib
```
