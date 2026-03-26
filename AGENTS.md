# AGENTS.md - Webnovel Writer 开发指南

## 项目概述

Webnovel Writer 是一个基于 OpenCode 的长篇网文 AI 创作系统，目标降低 AI 写作中的"遗忘"和"幻觉"，支持长周期连载创作。

## 构建/测试/开发命令

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

# Windows: 运行测试脚本
powershell -File .opencode/scripts/run_tests.ps1
```

**测试配置**:
- 测试路径: `.opencode/scripts/data_modules/tests`
- Python 路径: `.opencode/scripts`
- 覆盖率要求: 最低 90%

## 代码风格规范

### 文件头
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块描述（中文）
"""
```

### 导入顺序: 标准库 → 第三方 → 本地（相对导入）
```python
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

import aiohttp

from .config import get_config
```

### 类型注解: 始终使用显式类型注解
```python
def process_entities(entities: List[EntityState]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    return result
```

### 错误处理: 捕获具体异常，避免裸 except
```python
try:
    config = DataModulesConfig.from_project_root(project_root)
except ValueError as e:
    logger.error("Invalid project root: %s", e)
    raise
```

### 路径处理: 使用 pathlib
```python
from pathlib import Path
config_dir = project_root / ".webnovel"
state_file = config_dir / "state.json"
```

### 日志记录: 使用 `logging.getLogger(__name__)`
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processing chapter %d", chapter_num)
```

### 异常兼容: 使用 try/except 处理跨平台兼容
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
│   ├── agents/           # 8个 Agent 定义（Markdown格式）
│   ├── checkers/        # 审查器配置驱动
│   ├── skills/          # 9个 Skills
│   ├── scripts/         # Python 核心脚本
│   │   └── data_modules/ # 核心模块
│   ├── references/     # 参考文档
│   ├── genres/         # 38+ 题材参考
│   └── templates/      # 输出模板
├── opencode.json        # Agent 配置
├── .env                 # API 配置
└── init.sh / init.bat  # 安装脚本
```

## 关键约定

1. **状态管理**: 使用 `DataModulesConfig` 进行配置；使用 `StateManager` 管理小说状态
2. **RAG 流程**: 查询 → 检索 → 重排 → 构建上下文
3. **实体追踪**: 所有新实体必须通过 `EntityLinker` 注册
4. **文件编码**: 所有文件使用 UTF-8
5. **中文文档**: 所有用户面向的字符串和文档使用中文
6. **审查器**: 通过 registry.yaml 配置，由 agents/*.md 实现

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

## 常用运维命令

```bash
# 索引重建
python .opencode/scripts/webnovel.py index process-chapter --chapter 1

# 索引统计
python .opencode/scripts/webnovel.py index stats

# 健康报告
python .opencode/scripts/webnovel.py status --focus all

# 向量重建
python .opencode/scripts/webnovel.py rag index-chapter --chapter 1
```

## Git 工作流

```bash
# 提交前运行测试
pytest

# 提交信息规范
git commit -m "type: description"

# type: feat, fix, docs, refactor, test, chore
```
