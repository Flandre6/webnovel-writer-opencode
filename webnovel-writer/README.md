# Webnovel Writer (OpenCode 版本)

## 项目介绍

本项目是基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) 改编的 OpenCode 版本，目标是让 Webnovel Writer 可以在 OpenCode 中使用。

原项目是基于 Claude Code 的长篇网文创作系统，本版本保留核心功能并适配 OpenCode。

## 快速开始

### 安装

```bash
# 安装 Python 依赖
pip install aiohttp filelock pydantic fastapi uvicorn watchdog

# 或使用 requirements.txt
pip install -r requirements.txt
```

> 注意：本项目不需要 `pip install -e .`，脚本可直接运行。

### 配置 OpenCode Skills

将 `skills` 目录复制到 OpenCode 配置目录：

```bash
# 方式一：复制到项目内（项目级）
cp -r skills <your-project>/.opencode/skills/webnovel-writer

# 方式二：复制到全局配置（全局可用）
cp -r skills ~/.config/opencode/skills/webnovel-writer
```

### 使用 CLI

```bash
# 进入项目目录
cd <your-novel-project>

# 使用 Python 模块方式运行
python -m scripts.webnovel --help

# 或直接运行脚本
python scripts/webnovel.py --help
```

## 项目结构

```
webnovel-writer/
├── skills/           # OpenCode Skills (9个)
├── scripts/         # Python 核心脚本
│   └── data_modules/  # 数据模块
├── dashboard/       # 可视化面板
├── references/     # 共享参考文档
├── templates/      # 模板
├── genres/         # 题材参考
├── docs/           # 文档
├── README.md
├── AGENTS.md
└── requirements.txt
```

## 主要命令

- `/webnovel-init` - 初始化新项目
- `/webnovel-plan` - 规划大纲
- `/webnovel-write` - 撰写章节
- `/webnovel-review` - 审查润色
- `/webnovel-query` - 查询设定
- `/webnovel-dashboard` - 可视化面板

## 环境变量

| 变量 | 说明 |
|------|------|
| `EMBED_BASE_URL` | Embedding API 地址 |
| `EMBED_MODEL` | Embedding 模型 |
| `EMBED_API_KEY` | Embedding API Key |
| `RERANK_BASE_URL` | Rerank API 地址 |
| `RERANK_MODEL` | Rerank 模型 |
| `RERANK_API_KEY` | Rerank API Key |

## 更新日志

| 版本 | 说明 |
|------|------|
| **v5.5.2-opencode** | 改编自原版，支持 OpenCode |

## 开源协议

GPL v3 - 继承自原项目。

## 致谢

- 原作者 [lingfengQAQ](https://github.com/lingfengQAQ)
- [OpenCode](https://opencode.ai)
