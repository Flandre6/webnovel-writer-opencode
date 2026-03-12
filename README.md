# Webnovel Writer

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-purple.svg)](https://opencode.ai)

## 项目介绍

本项目是基于 [lingfengQAQ/webnovel-writer](https://github.com/lingfengQAQ/webnovel-writer) 改编的 OpenCode 版本，目标是让 Webnovel Writer 可以在 [OpenCode](https://github.com/lujih/webnovel-writer-opencode) 中使用。

## 特性

- **完整的写作工作流**：从项目初始化，大纲规划、章节写作到审查润色
- **RAG 上下文管理**：智能检索相关设定、角色、伏笔
- **多维度质量检查**：设定一致性、连贯性、OOC、爽点、节奏、追读力
- **可视化 Dashboard**：实时查看项目状态和进度

## 快速开始

### 最简单的方式（一行命令）

```bash
# 在你的小说项目目录运行
curl -sL https://raw.githubusercontent.com/lujih/webnovel-writer-opencode/main/init.sh | bash
```

或者下载 `init.bat` 双击运行（Windows）。

这会自动创建 `.opencode/` 目录并复制所有必要文件。

### 配置环境变量

```bash
# 复制配置
cp .env.example .env

# 编辑 .env，填入你的 API Key
```

### 开始使用

在 OpenCode 中直接使用命令：
- `/webnovel-init` - 初始化新项目
- `/webnovel-plan` - 规划大纲
- `/webnovel-write` - 撰写章节
- `/webnovel-review` - 审查润色
- `/webnovel-query` - 查询设定

## Skills (8个)

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

## 项目结构

```
项目目录/
├── .opencode/
│   ├── skills/          # 8个 Skills
│   ├── scripts/        # Python 核心脚本
│   ├── references/     # 参考文档
│   ├── genres/         # 题材参考
│   └── templates/      # 模板
├── .env.example
└── init.bat / init.sh
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `EMBED_BASE_URL` | Embedding API 地址 | https://api-inference.modelscope.cn/v1 |
| `EMBED_MODEL` | Embedding 模型 | Qwen/Qwen3-Embedding-8B |
| `EMBED_API_KEY` | Embedding API Key | - |
| `RERANK_BASE_URL` | Rerank API 地址 | https://api.jina.ai/v1 |
| `RERANK_MODEL` | Rerank 模型 | jina-reranker-v3 |
| `RERANK_API_KEY` | Rerank API Key | - |

## 开源协议

GPL v3 - 继承自原项目。

## 致谢

- 原作者 [lingfengQAQ](https://github.com/lingfengQAQ)
- [OpenCode](https://opencode.ai)
