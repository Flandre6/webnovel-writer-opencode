# 项目结构与运维

## 目录层级

```
WORKSPACE_ROOT/
├── .opencode/            # OpenCode 配置（Skills/Scripts/References）
├── opencode.json         # Agents 配置
├── prompts/              # Agent 提示词
├── .env                  # API 配置
└── 小说项目/             # 用户小说项目
    ├── .webnovel/        # 运行时数据
    ├── 正文/              # 正文章节
    ├── 大纲/              # 总纲与卷纲
    └── 设定集/            # 世界观、角色、力量体系
```

## .opencode 目录结构

```
.opencode/
├── skills/              # 7个 Skills
│   ├── webnovel-init/
│   ├── webnovel-plan/
│   ├── webnovel-write/
│   ├── webnovel-review/
│   ├── webnovel-query/
│   ├── webnovel-resume/
│   └── webnovel-learn/
├── scripts/             # Python 核心脚本
│   ├── data_modules/    # 核心模块
│   └── webnovel.py     # CLI 入口
├── references/          # 参考文档
│   ├── shared/         # 共享规范
│   ├── creativity/      # 创意约束
│   └── worldbuilding/   # 世界观设计
├── genres/              # 题材参考（38+）
└── templates/           # 输出模板
    ├── genres/         # 题材模板
    └── output/         # 输出格式
```

## 常用运维命令

```bash
# 进入小说项目目录后

# 索引重建
python .opencode/scripts/webnovel.py index process-chapter --chapter 1

# 索引统计
python .opencode/scripts/webnovel.py index stats

# 健康报告
python .opencode/scripts/webnovel.py status --focus all
python .opencode/scripts/webnovel.py status --focus urgency

# 向量重建
python .opencode/scripts/webnovel.py rag index-chapter --chapter 1
python .opencode/scripts/webnovel.py rag stats
```

## 测试

```bash
# 运行所有测试
pytest

# 运行单个测试
pytest .opencode/scripts/data_modules/tests/test_config.py::test_config_paths_and_defaults

# 覆盖率报告
pytest --cov .opencode/scripts/data_modules/tests/
```
