# Webnovel Writer for OpenCode

基于 OpenCode 的长篇网文 AI 创作系统，让 AI 写作不再"遗忘"和"幻觉"。

### 核心功能

| 模块 | 说明 |
|------|------|
| **8 个 Skills** | /webnovel-init 初始化 · /webnovel-plan 规划 · /webnovel-write 写作 · /webnovel-review 审查 · /webnovel-query 查询 · /webnovel-resume 恢复 · /webnovel-learn 学习 · /webnovel-export 导出 |
| **8 个 Agents** | 上下文搜集 · 数据处理 · 设定一致性 · 连贯性 · 人物OOC · 爽点密度 · 节奏检查 · 追读力 |
| **38+ 题材** | 修仙、都市、宫斗、悬疑、狗血言情等主流网文题材 |
| **RAG 管理** | 智能检索设定、角色、伏笔，保持长篇一致性 |

### 快速开始

```bash
# Linux/macOS
curl -sL https://raw.githubusercontent.com/lujih/webnovel-writer-opencode/master/init.sh | bash

# Windows - 下载 init.bat 双击运行
```
安装后配置 .env 中的 API Key（ModelScope / Jina），即可在 OpenCode 中使用 /webnovel-write 开始创作。

### 技术栈
OpenCode Agent Framework
Python 3.8+
SQLite（RAG 向量存储）
ModelScope / Jina API

### 致谢
原作者 [lingfengQAQ](https://github.com/lingfengQAQ)
[OpenCode](https://opencode.ai/)