---
name: webnovel-export
description: 将正文导出为 Markdown/TXT/EPUB 格式。当用户要求导出或发布章节时使用。按步骤执行导出流程，包含预检、导出、验证、workflow 记录。
allowed-tools: Read Write Edit Bash Task
---

# 正文导出（Structured Workflow）

## 目标

将网文正文导出为不同格式，便于发布或存档。流程包含预检、导出执行、输出验证、workflow 记录。

## 支持格式

| 格式 | 说明 | 依赖 |
|------|------|------|
| Markdown | Markdown 格式，可用任何编辑器打开 | 无 |
| TXT | 纯文本，最通用 | 无 |
| EPUB | 电子书，阅读器可用 | ebooklib |

## 执行原则

1. 先校验项目存在性和章节文件，再执行导出
2. 导出是只读操作，不需要审查/润色/数据回写
3. 导出失败时提供明确错误信息，不静默失败
4. 输出文件路径规范化，默认放在 `导出/` 目录

## 模式定义

- `/webnovel-export`：Step 1 → 2 → 3 → 4（完整流程）
- `/webnovel-export --list`：仅列出可导出章节（跳过导出）
- `/webnovel-export --check`：仅验证导出能力，不生成文件

最小产物（所有模式）：
- 导出文件：`导出/{filename}.{ext}`
- workflow 任务记录完成

## 环境设置

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

# 获取 skill 所在目录
export SKILL_ROOT="$(cd "$(dirname "$0")" && pwd)"
export SCRIPTS_DIR="${SKILL_ROOT}/../../scripts"
```

## 交互流程

### Step 0：预检与项目解析

必须做：
- 解析真实书项目根（book project_root）：必须包含 `.webnovel/state.json` 或 `正文/` 目录
- 校验核心输入：章节文件存在性
- 规范化变量：
  - `WORKSPACE_ROOT`：OpenCode 打开的工作区根目录
  - `PROJECT_ROOT`：真实书项目根目录
  - `SKILL_ROOT`：skill 所在目录
  - `SCRIPTS_DIR`：脚本目录（`.opencode/scripts/`）

环境设置（bash 命令执行前）：
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" preflight
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

**硬门槛**：`preflight` 必须成功。校验 `SCRIPTS_DIR`、`webnovel.py` 和解析出的 `PROJECT_ROOT`。任一失败都立即阻断。

输出：
- 项目根目录路径
- 可导出章节列表

### Step 0.5：工作流断点记录（best-effort，不阻断）

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-task --command webnovel-export || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 1" --step-name "Collect Export Info" || true
```

要求：
- `--step-id` 仅允许：`Step 1` / `Step 2` / `Step 3` / `Step 4`
- 任何记录失败只记警告，不阻断导出
- 每个 Step 执行结束后，同样需要 `complete-step`

### Step 1：收集导出信息

确定导出参数：
- 格式（`--format`）：markdown / txt / epub
- 范围（`--range` 或 `--volume`）：全部 / 章节范围 / 卷号
- 输出路径（`--output`）
- 作者名（`--author`，仅 EPUB 需要）

获取可导出章节列表：
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export list
```

交互式获取（推荐）：
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export
```

### Step 2：执行导出

根据参数执行导出：

```bash
# 交互式导出（推荐）
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export

# 导出全部章节
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format markdown
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format txt
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format epub --author "作者名"

# 导出指定章节
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1-10 --format markdown
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --range 1,3,5 --format txt

# 导出指定卷
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --volume 1 --format markdown
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --volume 2 --format epub --author "作者名"

# 指定输出路径
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export --format markdown --output 我的小说.md
```

参数说明：

| 参数 | 说明 |
|------|------|
| `--range` | 章节范围，如 `1-10`、`1,3,5`、`20-30`，或 `all`（默认） |
| `--volume` | 导出指定卷，如 `1`、`2` |
| `--format` | 输出格式：`markdown`（默认）、`txt`、`epub` |
| `--output` | 输出文件路径（默认自动生成在 `导出/` 目录） |
| `--author` | 作者名（仅 EPUB 格式需要） |

### Step 3：验证输出文件

导出完成后，验证输出文件：

```bash
# 检查输出目录存在
test -d "${PROJECT_ROOT}/导出"

# 检查输出文件存在且非空
test -s "${PROJECT_ROOT}/导出/novel.md"
test -s "${PROJECT_ROOT}/导出/novel.txt"
test -s "${PROJECT_ROOT}/导出/novel.epub"
```

记录导出结果到 workflow：
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 2" --artifacts '{"export_file": "导出/novel.md", "chapters": 100}' || true
```

### Step 4：完成 workflow

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok": true, "export_count": 1}' || true
```

## 充分性闸门

未满足以下条件前，不得结束流程：

1. 预检成功：项目根目录和章节文件可访问
2. 导出命令执行成功（返回码为 0）
3. 输出文件存在且非空
4. workflow 任务记录已更新

## 验证与交付

执行检查：

```bash
# 验证项目可访问
test -f "${PROJECT_ROOT}/.webnovel/state.json" || test -d "${PROJECT_ROOT}/正文"

# 验证输出文件
test -s "${PROJECT_ROOT}/导出/novel.md" || test -s "${PROJECT_ROOT}/导出/novel.txt" || test -s "${PROJECT_ROOT}/导出/novel.epub"

# 列出可导出章节
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export list
```

成功标准：
- 输出文件存在且内容可读
- 导出章节数与请求范围一致

## 失败处理

触发条件：
- 预检失败（项目根目录不存在）
- 章节文件缺失
- 导出命令执行失败
- 输出文件不存在或为空

恢复流程：
1. 检查预检输出，确认项目可访问
2. 使用 `export list` 确认章节文件存在
3. 检查导出命令输出中的错误信息
4. 确认输出目录权限和磁盘空间
5. 重跑导出步骤

## 安装可选依赖

```bash
# 安装 EPUB 支持
pip install ebooklib
```