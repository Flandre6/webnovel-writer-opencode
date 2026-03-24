# 命令详解

## `/webnovel-init`

用途：初始化小说项目（目录、设定模板、状态文件）。

产出：

- `.webnovel/state.json`
- `设定集/`
- `大纲/总纲.md`

## `/webnovel-plan [卷号]`

用途：生成卷级规划与章节大纲。

示例：

```
/webnovel-plan 1
/webnovel-plan 2-3
```

## `/webnovel-write [章号]`

用途：执行完整章节创作流程（上下文 → 草稿 → 审查 → 润色 → 数据落盘）。

示例：

```
/webnovel-write 1
/webnovel-write 45
```

## `/webnovel-review [范围]`

用途：对历史章节做多维质量审查。

示例：

```
/webnovel-review 1-5
/webnovel-review 45
```

## `/webnovel-query [关键词]`

用途：查询角色、伏笔、节奏、状态等运行时信息。

示例：

```
/webnovel-query 萧炎
/webnovel-query 伏笔
/webnovel-query 紧急
```

## `/webnovel-resume`

用途：任务中断后自动识别断点并恢复。

示例：

```
/webnovel-resume
```

## `/webnovel-learn [内容]`

用途：从当前会话或用户输入中提取可复用写作模式，并写入项目记忆。

示例：

```
/webnovel-learn "本章的危机钩设计很有效，悬念拉满"
```

产出：

- `.webnovel/project_memory.json`

## 正文导出命令

用途：将正文导出为 TXT/EPUB/DOCX 格式。

### CLI 命令

```bash
# 列出可导出章节
python .opencode/scripts/webnovel.py --project-root "项目路径" export list

# 导出全部章节（默认 TXT）
python .opencode/scripts/webnovel.py --project-root "项目路径" export

# 指定格式导出
python .opencode/scripts/webnovel.py --project-root "项目路径" export --format txt
python .opencode/scripts/webnovel.py --project-root "项目路径" export --format docx
python .opencode/scripts/webnovel.py --project-root "项目路径" export --format epub

# 导出指定章节范围
python .opencode/scripts/webnovel.py --project-root "项目路径" export --range 1-10 --format txt

# 指定输出路径
python .opencode/scripts/webnovel.py --project-root "项目路径" export --format epub --output novel.epub
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--range` | 章节范围，如 `1-10`、`1,3,5`、`all`（默认） |
| `--format` | 输出格式：`txt`（默认）、`docx`、`epub` |
| `--output` | 输出文件路径 |
| `--author` | 作者名（仅 EPUB/DOCX） |

### 输出位置

导出的文件保存在项目根目录的 `导出/` 文件夹下。
