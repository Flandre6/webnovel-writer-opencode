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

# 运行单个测试（推荐方式）
pytest .opencode/scripts/data_modules/tests/test_config.py::test_config_paths_and_defaults

# 运行特定测试文件
pytest .opencode/scripts/data_modules/tests/test_api_client.py

# 运行测试并生成覆盖率报告（最低要求 90%）
pytest --cov --cov-report=term-missing .opencode/scripts/data_modules/tests/

# 只运行失败的测试
pytest --lf
```

**测试配置**:
- 测试路径: `.opencode/scripts/data_modules/tests`
- Python 路径: `.opencode/scripts`
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

**导入顺序**: 标准库 → 第三方 → 本地（相对导入）
```python
import os
import asyncio
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

import aiohttp
from pydantic import BaseModel

from .config import get_config
from .observability import logger
```

**类型注解**: 始终使用显式类型注解，避免 `Any`
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

**日志记录**: 使用 `logging.getLogger(__name__)`
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Processing chapter %d", chapter_num)
logger.error("Failed to load config: %s", error)
```

**错误处理**: 捕获具体异常，避免裸 except
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

**异常兼容**: 使用 try/except 处理跨平台兼容
```python
try:
    from ..runtime_compat import normalize_windows_path
except ImportError:
    from runtime_compat import normalize_windows_path
```

## 项目结构

```
项目目录/
├── .opencode/              # OpenCode 配置
│   ├── skills/            # 7个 Skills
│   ├── scripts/           # Python 核心
│   │   └── data_modules/  # 核心模块
│   │       ├── state_manager.py
│   │       ├── context_manager.py
│   │       ├── index_manager.py
│   │       ├── api_client.py
│   │       └── tests/     # 测试文件
│   ├── references/        # 参考文档
│   ├── genres/            # 题材参考
│   └── templates/         # 输出模板
├── opencode.json          # Agents 配置
├── prompts/               # Agent 提示词
├── .env                   # API 配置
└── init.sh / init.bat    # 安装脚本
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
5. 测试函数命名: `test_function_name_when_condition()`

## 配置约定

- API 配置通过环境变量读取，支持 `.env` 文件
- `.env` 加载顺序: 当前目录 → 用户全局目录
- 已有环境变量不会被 `.env` 覆盖（显式优先）
