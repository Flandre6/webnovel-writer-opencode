# AGENTS.md - Webnovel Writer 开发指南

## 项目概述

Webnovel Writer 是一个基于 OpenCode 的长篇网文 AI 创作系统，目标降低 AI 写作中的"遗忘"和"幻觉"，支持长周期连载创作。

## 构建/测试/开发命令

### Python

```bash
# 安装依赖
pip install -e .

# 运行所有测试
pytest

# 运行单个测试
pytest scripts/data_modules/tests/test_config.py::test_config_paths_and_defaults

# 运行测试并生成覆盖率报告（最低要求 90%）
pytest --cov --cov-report=term-missing

# 运行特定测试文件
pytest scripts/data_modules/tests/test_api_client.py
```

**测试配置** (`pytest.ini`):
- 测试路径: `scripts/data_modules/tests`
- Python 路径: `scripts`
- 覆盖率要求: 最低 90%

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

**导入顺序**: 标准库 → 第三方 → 本地
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

**类型注解**: 始终使用显式类型注解
```python
def process_entities(entities: List[EntityState]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    return result
```

**Dataclass**: 用于数据结构
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

**错误处理**: 使用 try/except 捕获具体异常
```python
try:
    config = DataModulesConfig.from_project_root(project_root)
except ValueError as e:
    logger.error("Invalid project root: %s", e)
    raise
```

**路径处理**: 使用 pathlib
```python
from pathlib import Path
config_dir = project_root / ".webnovel"
state_file = config_dir / "state.json"
```

**异步**: 用于 I/O 操作
```python
async def fetch_embeddings(self, texts: List[str]) -> List[List[float]]:
    async with self._semaphore:
        session = await self._get_session()
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
    
    return <div className="component">{/* JSX */}</div>
}
```

**命名规范**:
- 组件: PascalCase (`DashboardPage`)
- 函数: camelCase (`fetchJSON`)
- CSS 类: kebab-case (`sidebar-header`)

## 项目结构

```
项目目录/
├── .opencode/              # OpenCode 配置
│   ├── skills/            # 7个 Skills
│   ├── scripts/          # Python 核心
│   ├── references/       # 参考文档
│   ├── genres/           # 题材参考
│   └── templates/        # 模板
├── opencode.json          # Agents 配置
├── prompts/               # Agent 提示词
├── .env.example
├── init.sh / init.bat    # 安装脚本
├── AGENTS.md
└── README.md
```

## 关键约定

1. **状态管理**: 使用 `DataModulesConfig` 进行配置；使用 `StateManager` 管理小说状态
2. **RAG 流程**: 查询 → 检索 → 重排 → 构建上下文
3. **实体追踪**: 所有新实体必须通过 `EntityLinker` 注册
4. **文件编码**: 所有文件使用 UTF-8
5. **中文文档**: 所有用户面向的字符串和文档使用中文

## 测试最佳实践

1. 使用 `tmp_path` fixture 进行文件系统测试
2. 使用 `monkeypatch` 进行环境变量模拟
3. 测试成功和错误路径
4. 异步测试需要 `@pytest.mark.asyncio` 装饰器
