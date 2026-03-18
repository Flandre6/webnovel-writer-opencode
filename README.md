# Webnovel Writer

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-purple.svg)](https://opencode.ai)
[![GitHub Stars](https://img.shields.io/github/stars/lujih/webnovel-writer-opencode)](https://github.com/lujih/webnovel-writer-opencode/stargazers)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

## 项目介绍

Webnovel Writer 是一个基于 OpenCode 的长篇网文 AI 创作系统，目标降低 AI 写作中的"遗忘"和"幻觉"，支持长周期连载创作。

本项目是基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) 改编的 OpenCode 版本。

## 核心特性

| 特性 | 说明 |
|------|------|
| **完整写作工作流** | 项目初始化 → 大纲规划 → 章节写作 → 审查润色 |
| **RAG 上下文管理** | 智能检索相关设定、角色、伏笔，保持长篇一致性 |
| **多维度质量检查** | 设定一致性、连贯性、OOC、爽点、节奏、追读力 |
| **38+ 题材模板** | 修仙、都市、宫斗、悬疑等主流网文题材 |

## 快速开始

### 一键安装

```bash
# Linux/macOS
curl -sL https://raw.githubusercontent.com/lujih/webnovel-writer-opencode/master/init.sh | bash

# Windows - 下载 init.bat 双击运行
```

安装脚本会自动：
- 下载并配置 OpenCode Skills 和 Agents
- 创建项目目录结构
- 安装 Python 依赖
- 生成 `.env` 配置文件

### 配置 API Key

编辑 `.env` 文件：

```bash
# Embedding 模型（向量化章节内容）
EMBED_BASE_URL=https://api-inference.modelscope.cn/v1
EMBED_MODEL=Qwen/Qwen3-Embedding-8B
EMBED_API_KEY=your_api_key

# Rerank 模型（检索结果重排）
RERANK_BASE_URL=https://api.jina.ai/v1
RERANK_MODEL=jina-reranker-v3
RERANK_API_KEY=your_api_key
```

### 在 OpenCode 中使用

```
/webnovel-init    # 初始化新项目
/webnovel-plan    # 规划大纲
/webnovel-write   # 撰写章节
/webnovel-review  # 审查润色
/webnovel-query   # 查询设定
/webnovel-resume  # 恢复写作
/webnovel-learn   # 学习模式
```

## Skills（7个）

| 命令 | 功能描述 |
|------|----------|
| `/webnovel-init` | 深度初始化网文项目，收集创作信息生成项目骨架 |
| `/webnovel-plan` | 构建卷纲和章节大纲，继承创意约束 |
| `/webnovel-write` | 撰写章节，包含风格转译与质量控制 |
| `/webnovel-review` | 使用检查器审查章节质量 |
| `/webnovel-query` | 查询项目设定、角色、伏笔信息 |
| `/webnovel-resume` | 恢复中断的写作任务 |
| `/webnovel-learn` | 从当前会话提取可复用写作模式 |

## Agents（8个）

| Agent | 功能描述 |
|-------|----------|
| `context-agent` | 上下文搜集，生成创作执行包 |
| `data-agent` | 数据处理，实体提取与索引构建 |
| `consistency-checker` | 设定一致性检查 |
| `continuity-checker` | 连贯性检查 |
| `ooc-checker` | 人物 OOC 检查 |
| `high-point-checker` | 爽点密度检查 |
| `pacing-checker` | 节奏检查 |
| `reader-pull-checker` | 追读力检查 |

## 项目结构

```
项目目录/
├── .opencode/              # OpenCode 配置
│   ├── skills/            # 7个 Skills
│   ├── scripts/           # Python 核心脚本
│   ├── references/        # 参考文档
│   ├── genres/            # 题材参考（38+）
│   └── templates/         # 输出模板
├── opencode.json          # Agents 配置
├── prompts/               # Agent 提示词
├── .env                   # API 配置
└── init.sh / init.bat    # 安装脚本
```

## 工作流程

```
1. 项目初始化 (/webnovel-init)
   └─→ 生成设定集、大纲、创意约束

2. 大纲规划 (/webnovel-plan)
   └─→ 生成卷纲、章纲

3. 章节写作 (/webnovel-write)
   ├─→ context-agent 搜集上下文
   ├─→ 撰写章节正文
   ├─→ 多维度审查（6个检查器）
   └─→ data-agent 更新索引

4. 查询设定 (/webnovel-query)
   └─→ RAG 检索相关上下文
```

## 卸载

```bash
# 删除安装文件
rm -rf .opencode/ prompts/ opencode.json .env

# 卸载 Python 依赖
pip uninstall aiohttp filelock pydantic pytest pytest-asyncio pytest-cov -y
```

> 卸载不会影响你已创建的网文项目文件（正文、大纲、设定集等）。

## 开发

```bash
# 安装依赖
pip install -e .

# 运行测试（覆盖率要求 90%）
pytest --cov .opencode/scripts/data_modules/tests/

# 运行单个测试
pytest .opencode/scripts/data_modules/tests/test_config.py::test_config_paths_and_defaults
```

## 开源协议

[GPL v3](LICENSE) - 继承自原项目

## 致谢

- 原作者 [lingfengQAQ](https://github.com/lingfengQAQ)
- [OpenCode](https://opencode.ai)
