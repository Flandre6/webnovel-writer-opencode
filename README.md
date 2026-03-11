# Webnovel Writer

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-purple.svg)](https://opencode.ai)

## 项目介绍

本项目是基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) 改编的 OpenCode 版本，目标是让 Webnovel Writer 可以在 OpenCode 中使用。

原项目是基于 Claude Code 的长篇网文创作系统，本版本保留核心功能并适配 OpenCode。

## 特性

- **完整的写作工作流**：从项目初始化、大纲规划、章节写作到审查润色
- **RAG 上下文管理**：智能检索相关设定、角色、伏笔
- **多维度质量检查**：设定一致性、连贯性、OOC、爽点、节奏、追读力
- **可视化 Dashboard**：实时查看项目状态和进度

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 OpenCode Skills

将 `skills` 目录复制到 OpenCode 配置目录：

```bash
# 方式一：项目级安装
cp -r webnovel-writer/skills <your-project>/.opencode/skills/webnovel-writer

# 方式二：全局安装
cp -r webnovel-writer/skills ~/.config/opencode/skills/webnovel-writer
```

### 3. 配置 OpenCode Agents（可选）

```bash
# 方式一：项目级安装
cp -r webnovel-writer/agents <your-project>/.opencode/agents/

# 方式二：全局安装
cp -r webnovel-writer/agents ~/.config/opencode/agents/
```

### 4. 配置 RAG 环境

在项目根目录创建 `.env` 文件：

```bash
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_api_key

RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_api_key
```

### 5. 使用 CLI

```bash
# 进入项目目录
cd <your-novel-project>

# 查看帮助
python webnovel-writer/scripts/webnovel.py --help

# 初始化项目
python webnovel-writer/scripts/webnovel.py init
```

## 项目结构

```
webnovel-writer/
├── webnovel-writer/              # 主代码目录
│   ├── scripts/                 # Python 核心脚本
│   │   ├── data_modules/       # 数据模块
│   │   └── webnovel.py        # CLI 入口
│   ├── skills/                 # OpenCode Skills
│   ├── agents/                 # OpenCode Agents
│   ├── dashboard/               # 可视化面板
│   ├── references/              # 共享参考
│   ├── templates/              # 模板
│   └── genres/                 # 题材参考
├── docs/                        # 文档
├── pytest.ini                   # 测试配置
├── requirements.txt            # Python 依赖
└── README.md                   # 本文件
```

## Skills

| Skill | 功能 |
|-------|------|
| `webnovel-init` | 初始化新项目 |
| `webnovel-plan` | 规划大纲 |
| `webnovel-write` | 撰写章节 |
| `webnovel-review` | 审查润色 |
| `webnovel-resume` | 恢复写作 |
| `webnovel-query` | 查询设定 |
| `webnovel-dashboard` | 可视化面板 |
| `webnovel-learn` | 学习模式 |

## Agents

| Agent | 功能 |
|-------|------|
| `context-agent` | 上下文搜集 |
| `data-agent` | 数据处理 |
| `consistency-checker` | 设定一致性 |
| `continuity-checker` | 连贯性检查 |
| `ooc-checker` | 人物 OOC |
| `high-point-checker` | 爽点检查 |
| `pacing-checker` | 节奏检查 |
| `reader-pull-checker` | 追读力检查 |

## 环境变量

| 变量 | 说明 |
|------|------|
| `EMBED_BASE_URL` | Embedding API 地址 |
| `EMBED_MODEL` | Embedding 模型 |
| `EMBED_API_KEY` | Embedding API Key |
| `RERANK_BASE_URL` | Rerank API 地址 |
| `RERANK_MODEL` | Rerank 模型 |
| `RERANK_API_KEY` | Rerank API Key |

## 开源协议

GPL v3 - 继承自原项目。

## 致谢

- 原作者 [lingfengQAQ](https://github.com/lingfengQAQ)
- [OpenCode](https://opencode.ai)
