# 项目结构与运维

## 目录层级（真实运行）

在 OpenCode 安装下，有以下几层概念：

1. `WORKSPACE_ROOT`（OpenCode 工作区根，通常是项目目录）
2. `WORKSPACE_ROOT/.opencode/`（OpenCode 配置与资源目录）
3. `PROJECT_ROOT`（真实小说项目根，`/webnovel-init` 按书名创建）

### A) Workspace 目录（含 `.opencode`）

```text
workspace-root/
├── .opencode/
│   ├── skills/           # Skills 目录
│   ├── scripts/          # Python 脚本
│   ├── references/       # 参考文档
│   ├── genres/           # 题材参考
│   └── templates/        # 模板
├── 小说A/
├── 小说B/
└── ...
```

### B) 小说项目目录（`PROJECT_ROOT`）

```text
project-root/
├── .webnovel/            # 运行时数据（state/index/vectors/summaries）
├── 正文/                  # 正文章节
├── 大纲/                  # 总纲与卷纲
└── 设定集/                # 世界观、角色、力量体系
```

## OpenCode 目录结构

安装后 `.opencode/` 目录结构如下：

```text
.opencode/
├── skills/
│   └── webnovel-init/
│   └── webnovel-plan/
│   └── webnovel-write/
│   └── ...
├── scripts/
│   ├── webnovel.py
│   ├── data_modules/
│   └── ...
├── references/
├── genres/
└── templates/
```

### C) 用户级全局映射（兜底）

当工作区没有可用指针时，会使用用户级 registry 做 `workspace -> current_project_root` 映射：

```text
${CLAUDE_HOME:-~/.claude}/webnovel-writer/workspaces.json
```

## 模拟目录实测（2026-03-03）

基于 `D:\wk\novel skill\plugin-sim-20260303-012048` 的实际结果：

- `WORKSPACE_ROOT`：`D:\wk\novel skill\plugin-sim-20260303-012048`
- 指针文件：`D:\wk\novel skill\plugin-sim-20260303-012048\.claude\.webnovel-current-project`
- 指针内容：`D:\wk\novel skill\plugin-sim-20260303-012048\凡人资本论-二测`
- 已创建项目示例：`凡人资本论/`、`凡人资本论-二测/`

## 常用运维命令

统一前置（手动 CLI 场景）：

```bash
export WORKSPACE_ROOT="${WEBNOVEL_PROJECT_ROOT:-$PWD}"
export SCRIPTS_DIR="${WORKSPACE_ROOT}/.opencode/scripts"
export PROJECT_ROOT="$(python "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

### 索引重建

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index process-chapter --chapter 1
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index stats
```

### 健康报告

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus all
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" status -- --focus urgency
```

### 向量重建

```bash
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag index-chapter --chapter 1
python "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" rag stats
```

### 测试入口

```bash
cd .opencode/scripts
pytest
```
