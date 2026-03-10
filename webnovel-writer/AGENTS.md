# AGENTS.md - Webnovel Writer 开发指南

## 项目概述

Webnovel Writer 是一个基于 OpenCode 的长篇网文 AI 创作系统，目标降低 AI 写作中的"遗忘"和"幻觉"，支持长周期连载创作。

项目组成：
- **Python 核心**：数据管理、RAG、状态管理、CLI 命令
- **前端 Dashboard**：React + Vite 可视化面板
- **OpenCode Skills**：写作工作流命令集

## 构建/测试/开发命令

### Python

```bash
# 安装依赖
pip install -e .

# 开发模式安装（包含测试依赖）
pip install -e ".[dev]"

# 运行所有测试
pytest

# 运行单个测试
pytest webnovel-writer/webnovel_writer/scripts/data_modules/tests/test_config.py::test_config_paths_and_defaults

# 运行测试并生成覆盖率报告（最低要求 90%）
pytest --cov --cov-report=term-missing

# 运行特定测试文件
pytest webnovel_writer/scripts/data_modules/tests/test_api_client.py
```

**测试配置** (`pytest.ini`):
- 测试路径: `webnovel_writer/scripts/data_modules/tests`
- Python 路径: `webnovel_writer/scripts`
- 覆盖率要求: 最低 90%

### 前端 (Dashboard)

```bash
cd webnovel-writer/dashboard/frontend

# 安装依赖
npm install

# 开发服务器
npm run dev

# 生产构建
npm run build

# 预览生产构建
npm run preview
```

## 代码风格规范

### Python

**文件头**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块描述（中文）
"""
```

**导入顺序**：标准库 → 第三方 → 本地
```python
import os
import asyncio
from pathlib import Path
from typing import List, Dict, Optional, Any

import aiohttp
from pydantic import BaseModel

from .config import get_config
from .observability import logger
```

**类型注解**：始终使用显式类型注解
```python
def process_entities(entities: List[EntityState]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    return result
```

**Dataclass**：用于数据结构
```python
from dataclasses import dataclass, field

@dataclass
class EntityState:
    id: str
    name: str
    type: str
    tier: str = "装饰"
    aliases: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
```

**日志记录**:
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Processing chapter %d", chapter_num)
logger.error("Failed to load config: %s", error)
```

**错误处理**：使用 try/except 捕获具体异常
```python
try:
    config = DataModulesConfig.from_project_root(project_root)
except ValueError as e:
    logger.error("Invalid project root: %s", e)
    raise
```

**路径处理**：使用 pathlib
```python
from pathlib import Path
config_dir = project_root / ".webnovel"
state_file = config_dir / "state.json"
```

**异步/等待**：用于 I/O 操作
```python
async def fetch_embeddings(self, texts: List[str]) -> List[List[float]]:
    async with self._semaphore:
        session = await self._get_session()
        # ... implementation
```

### JavaScript/React

**组件结构**:
```jsx
import { useState, useEffect, useCallback } from 'react'

export default function ComponentName() {
    const [data, setData] = useState(null)
    
    useEffect(() => {
        fetchData()
    }, [])
    
    return (
        <div className="component">
            {/* JSX content */}
        </div>
    )
}
```

**命名规范**:
- 组件：PascalCase（`DashboardPage`、`EntitiesPage`）
- 函数：camelCase（`fetchJSON`、`formatNumber`）
- CSS 类：kebab-case（`sidebar-header`、`nav-item`）

**Hooks**:
- 始终在 useEffect/useCallback 中包含依赖数组
- 对于作为 props 传递的函数使用 useCallback

## 项目结构

```
webnovel-writer/
├── webnovel_writer/              # Python 包
│   ├── __init__.py
│   └── scripts/
│       ├── data_modules/        # 核心模块
│       │   ├── config.py        # 配置管理
│       │   ├── state_manager.py # 状态持久化
│       │   ├── context_manager.py # RAG 上下文
│       │   ├── api_client.py    # Embedding/Rerank API
│       │   └── tests/           # 单元测试
│       └── webnovel.py          # CLI 入口
├── skills/                      # OpenCode Skills
│   ├── webnovel-init/          # 项目初始化
│   ├── webnovel-plan/          # 大纲规划
│   ├── webnovel-write/         # 章节写作
│   ├── webnovel-review/        # 审查润色
│   ├── webnovel-resume/        # 恢复写作
│   ├── webnovel-query/         # RAG 查询
│   ├── webnovel-dashboard/     # 可视化面板
│   └── webnovel-learn/         # 学习模式
├── dashboard/                   # 可视化面板
│   ├── frontend/               # React + Vite 前端
│   │   ├── src/
│   │   │   ├── App.jsx
│   │   │   └── api.js
│   │   └── package.json
│   └── server.py               # FastAPI 后端
├── references/                  # 共享参考文档
├── docs/                        # 中文文档
├── templates/                   # 模板
├── genres/                      # 题材参考
├── pyproject.toml              # Python 包配置
├── install.py                  # 安装脚本
└── README.md                   # 入口文档
```

## 关键约定

1. **状态管理**：使用 `DataModulesConfig` 进行配置；使用 `StateManager` 管理小说状态
2. **RAG 流程**：查询 → 检索 → 重排 → 构建上下文
3. **实体追踪**：所有新实体必须通过 `EntityLinker` 注册
4. **文件编码**：所有文件使用 UTF-8
5. **中文文档**：所有用户面向的字符串和文档使用中文

## 常见任务

### 运行单个测试
```bash
pytest webnovel_writer/scripts/data_modules/tests/test_config.py::test_get_config_and_set_project_root
```

### 添加新 CLI 命令
1. 在 `webnovel.py` 中添加命令处理器
2. 在 `tests/test_webnovel_unified_cli.py` 中添加测试
3. 在 `docs/commands.md` 中更新文档

### 修改 RAG 配置
编辑环境变量或 `config.py`：
- `EMBED_BASE_URL`、`EMBED_MODEL`、`EMBED_API_KEY`
- `RERANK_BASE_URL`、`RERANK_MODEL`、`RERANK_API_KEY`

## 测试最佳实践

1. 使用 `tmp_path` fixture 进行文件系统测试
2. 使用 `monkeypatch` 进行环境变量模拟
3. 测试成功和错误路径
4. 保持测试函数专注（每个测试一个断言最好）
5. 异步测试需要 `@pytest.mark.asyncio` 装饰器
