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

## `/webnovel-export`

用途：将正文导出为 Markdown/TXT/EPUB 格式。

示例：

```
/webnovel-export
/webnovel-export --format markdown
/webnovel-export --range 1-10 --format epub
/webnovel-export --volume 1 --format txt
```

参数：

| 参数 | 说明 |
|------|------|
| `--format` | 输出格式：markdown（默认）、txt、epub |
| `--range` | 章节范围，如 `1-10`、`1,3,5` |
| `--volume` | 导出指定卷 |
| `--output` | 输出文件路径 |
| `--author` | 作者名（仅 EPUB 需要） |
