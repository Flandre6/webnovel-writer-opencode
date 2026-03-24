---
name: webnovel-export
description: 将正文导出为 TXT/EPUB/DOCX 格式。当用户要求导出或发布章节时使用。
allowed-tools: Read Write Edit Bash
---

# 正文导出

## 目标

将网文正文导出为不同格式，便于发布或存档。

## 支持格式

| 格式 | 说明 | 依赖 |
|------|------|------|
| TXT | 纯文本，最通用 | 无 |
| DOCX | Word 文档，便于编辑 | python-docx |
| EPUB | 电子书，阅读器可用 | ebooklib |

## 使用方式

### 1. 列出可导出章节

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export list
```

### 2. 导出全部章节

```bash
# 导出为 TXT
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format txt

# 导出为 DOCX
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format docx

# 导出为 EPUB
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format epub --author "作者名"
```

### 3. 导出指定章节

```bash
# 导出第 1-10 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1-10 --format txt

# 导出第 1, 3, 5 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1,3,5 --format txt

# 导出第 20-30 章
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 20-30 --format epub
```

### 4. 指定输出路径

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format txt --output mynovel.txt
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--range` | 章节范围，如 `1-10`、`1,3,5`、`20-30`，或 `all`（默认） |
| `--format` | 输出格式：`txt`（默认）、`docx`、`epub` |
| `--output` | 输出文件路径（默认自动生成在 `导出/` 目录） |
| `--author` | 作者名（仅 EPUB/DOCX 格式需要） |

## 输出位置

导出的文件默认保存在项目根目录的 `导出/` 文件夹下：
- `导出/novel.txt`
- `导出/novel.docx`
- `导出/novel.epub`

## 示例

### 导出全部章节为 TXT
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --format txt
```

### 导出前 100 章为 EPUB
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --range 1-100 --format epub --output "小说.epub"
```

### 导出单章为 DOCX
```bash
python -X utf8 ".opencode/scripts/webnovel.py" --project-root "D:/wk/我的小说" export --chapter 31 --format docx
```

## 安装可选依赖

```bash
# 安装 DOCX 支持
pip install python-docx

# 安装 EPUB 支持
pip install ebooklib
```
