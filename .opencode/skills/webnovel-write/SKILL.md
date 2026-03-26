---
name: webnovel-write
description: 撰写网文章节（默认2000-2500字）。当用户要求撰写章节或执行/webnovel-write时使用。包含上下文搜集、草稿撰写、审查、润色、数据提取。
allowed-tools: Read Write Edit Grep Bash Task
---

# Chapter Writing (Structured Workflow)

## 目标

- 以稳定流程产出可发布章节：优先使用 `正文/第{NNNN}章-{title_safe}.md`，无标题时回退 `正文/第{NNNN}章.md`。
- 默认章节字数目标：2000-2500（用户或大纲明确覆盖时从其约定）。
- 保证审查、润色、数据回写完整闭环，避免“写完即丢上下文”。
- 输出直接可被后续章节消费的结构化数据：`review_metrics`、`summaries`、`chapter_meta`。

## 执行原则

1. 先校验输入完整性，再进入写作流程；缺关键输入时立即阻断。
2. 审查与数据回写是硬步骤，`--fast`/`--minimal` 只允许降级可选环节。
3. 参考资料严格按步骤按需加载，不一次性灌入全部文档。
4. Step 2B 与 Step 4 职责分离：2B 只做风格转译，4 只做问题修复与质控。
5. 任一步失败优先做最小回滚，不重跑全流程。

## 模式定义

- `/webnovel-write`：Step 0 → 1 → 2A → 2B → 3 → 4 → 5 → 6（单章模式）
- `/webnovel-write --fast`：Step 0 → 1 → 2A → 3 → 4 → 5 → 6（跳过 2B）
- `/webnovel-write --minimal`：Step 0 → 1 → 2A → 3（仅3个基础审查）→ 4 → 5 → 6
- `/webnovel-write --chapters N`：Step 0 → 0.1 → 7.1 → 7.2（循环N次）→ 7.3（如失败）→ 7.4（批量模式）

最小产物（单章）：
- `正文/第{NNNN}章-{title_safe}.md` 或 `正文/第{NNNN}章.md`
- `index.db.review_metrics` 新纪录（含 `overall_score`）
- `.webnovel/summaries/ch{NNNN}.md`
- `.webnovel/state.json` 的进度与 `chapter_meta` 更新

最小产物（批量）：
- N 个章节文件（每个章都经历完整写作流程）
- 批量执行日志（每章的评分和状态）

### 流程硬约束（禁止事项）

- **禁止并步**：不得将两个 Step 合并为一个动作执行（如同时做 2A 和 3）。
- **禁止跳步**：不得跳过未被模式定义标记为可跳过的 Step。
- **禁止临时改名**：不得将 Step 的输出产物改写为非标准文件名或格式。
- **禁止自创模式**：`--fast` / `--minimal` 只允许按上方定义裁剪步骤，不允许自创混合模式、"半步"或"简化版"。
- **禁止自审替代**：Step 3 审查必须由 Task 子代理执行，主流程不得内联伪造审查结论。
- **禁止源码探测**：脚本调用方式以本文档与 data-agent 文档中的命令示例为准，命令失败时查日志定位问题，不去翻源码学习调用方式。

## 引用加载等级（strict, lazy）

- L0：未进入对应步骤前，不加载任何参考文件。
- L1：每步仅加载该步“必读”文件。
- L2：仅在触发条件满足时加载“条件必读/可选”文件。

路径约定：
- `references/...` 相对当前 skill 目录。
- `../../references/...` 指向全局共享参考。

## References（逐文件引用清单）

### 根目录

- `../../checkers/registry.yaml`
  - 用途：审查器注册表，包含审查器列表、分类（core/conditional）、触发条件、模式配置，`file` 字段指向 agent 文件。
  - 触发：Step 3 必读（用于动态加载审查器列表）。
- `../../agents/*.md`（审查器 agent 文件）
  - 用途：审查器实际逻辑实现，包含 prompt 模板和输出格式定义。
  - 路径：由 registry.yaml 中各审查器的 `file` 字段指定（如 `../agents/consistency-checker.md`）。
  - 触发：Task 调用审查器时自动加载。
- `../../checkers/schema.yaml`
  - 用途：审查器输出 Schema 定义，包含 metrics 结构。
  - 触发：Step 3 必读（用于校验审查器输出格式）。
- `references/step-5-debt-switch.md`
  - 用途：Step 5 债务利息开关规则（默认关闭）。
  - 触发：Step 5 必读。
- `../../references/shared/core-constraints.md`
  - 用途：Step 2A 写作硬约束（大纲即法律 / 设定即物理 / 发明需识别）。
  - 触发：Step 2A 必读。
- `references/polish-guide.md`
  - 用途：Step 4 问题修复、Anti-AI 与 No-Poison 规则。
  - 触发：Step 4 必读。
- `references/writing/typesetting.md`
  - 用途：Step 4 移动端阅读排版与发布前速查。
  - 触发：Step 4 必读。
- `references/style-adapter.md`
  - 用途：Step 2B 风格转译规则，不改剧情事实。
  - 触发：Step 2B 执行时必读（`--fast`/`--minimal` 跳过）。
- `references/style-variants.md`
  - 用途：Step 1（内置 Contract）开头/钩子/节奏变体与重复风险控制。
  - 触发：Step 1 当需要做差异化设计时加载。
- `../../references/reading-power-taxonomy.md`
  - 用途：Step 1（内置 Contract）钩子、爽点、微兑现 taxonomy。
  - 触发：Step 1 当需要追读力设计时加载。
- `../../references/genre-profiles.md`
  - 用途：Step 1（内置 Contract）按题材配置节奏阈值与钩子偏好。
  - 触发：Step 1 当 `state.project.genre` 已知时加载。
- `references/writing/genre-hook-payoff-library.md`
  - 用途：电竞/直播文/克苏鲁的钩子与微兑现快速库。
  - 触发：Step 1 题材命中 `esports/livestream/cosmic-horror` 时必读。

### writing（问题定向加读）

- `references/writing/combat-scenes.md`
  - 触发：战斗章或审查命中“战斗可读性/镜头混乱”。
- `references/writing/dialogue-writing.md`
  - 触发：审查命中 OOC、对话说明书化、对白辨识差。
- `references/writing/emotion-psychology.md`
  - 触发：情绪转折生硬、动机断层、共情弱。
- `references/writing/scene-description.md`
  - 触发：场景空泛、空间方位不清、切场突兀。
- `references/writing/desire-description.md`
  - 触发：主角目标弱、欲望驱动力不足。

## 工具策略（按需）

- `Read/Grep`：读取 `state.json`、大纲、章节正文与参考文件。
- `Bash`：运行 `extract_chapter_context.py`、`index_manager`、`workflow_manager`。
- `Task`：调用 `context-agent`、审查 subagent、`data-agent` 并行执行。

## 交互流程

### Step 0：预检与上下文最小加载

必须做：
- 解析真实书项目根（book project_root）：必须包含 `.webnovel/state.json`。
- 校验核心输入：`大纲/总纲.md`、`extract_chapter_context.py` 存在。
- 规范化变量：
  - `WORKSPACE_ROOT`：OpenCode 打开的工作区根目录
  - `PROJECT_ROOT`：真实书项目根目录（必须包含 `.webnovel/state.json`）
  - `SKILL_ROOT`：skill 所在目录
  - `SCRIPTS_DIR`：脚本目录（`.opencode/scripts/`）
  - `chapter_num`：当前章号（整数）
  - `chapter_padded`：四位章号（如 `0007`）

环境设置（bash 命令执行前）：
```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"

# 获取 skill 所在目录
export SKILL_ROOT="$(cd "$(dirname "$0")" && pwd)"
# OpenCode 中 scripts 在 .opencode/scripts/
export SCRIPTS_DIR="${SKILL_ROOT}/../../scripts"

python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" preflight
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${WORKSPACE_ROOT}" where)"
```

**硬门槛**：`preflight` 必须成功。它统一校验 `SCRIPTS_DIR`、`webnovel.py`、`extract_chapter_context.py` 和解析出的 `PROJECT_ROOT`。任一失败都立即阻断。

输出：
- “已就绪输入”与“缺失输入”清单；缺失则阻断并提示先补齐。

### Step 0.5：工作流断点记录（best-effort，不阻断）

```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-task --command webnovel-write --chapter {chapter_num} || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow start-step --step-id "Step 1" --step-name "Context Agent" || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-step --step-id "Step 1" --artifacts '{"ok":true}' || true
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" workflow complete-task --artifacts '{"ok":true}' || true
```

要求：
- `--step-id` 仅允许：`Step 1` / `Step 2A` / `Step 2B` / `Step 3` / `Step 4` / `Step 5` / `Step 6` / `Step 7`。
- 任何记录失败只记警告，不阻断写作。
- 每个 Step 执行结束后，同样需要 `complete-step`（失败不阻断）。

### Step 0.1：批量模式参数解析（仅当 `--chapters > 1` 时执行）

**此 Step 仅在批量模式下执行**。单章模式（`--chapters=1` 或无参数）跳过此 Step。

```bash
# 解析 --chapters 参数
BATCH_COUNT="${BATCH_COUNT:-1}"

# 参数校验
if [ "${BATCH_COUNT}" -le 0 ]; then
    echo "错误：--chapters 必须大于 0"
    exit 1
fi

# 从 state.json 获取当前章节号
CURRENT_CHAPTER=$(python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" state get-progress 2>/dev/null | grep -oE 'current_chapter[": ]+[0-9]+' | grep -oE '[0-9]+' || echo "0")
START_CHAPTER=$((CURRENT_CHAPTER + 1))

echo "批量写作模式：将从第 ${START_CHAPTER} 章开始，连续写入 ${BATCH_COUNT} 章"
```

**进入条件**：`BATCH_COUNT > 1`

### Step 1：Context Agent（内置 Context Contract，生成直写执行包）

使用 Task 调用 `context-agent`，参数：
- `chapter`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

硬要求：
- 若 `state` 或大纲不可用，立即阻断并返回缺失项。
- 输出必须同时包含：
  - 7 板块任务书（目标/冲突/承接/角色/场景约束/伏笔/追读力）；
  - Context Contract 全字段（目标/阻力/代价/本章变化/未闭合问题/开头类型/情绪节奏/信息密度/过渡章判定/追读力设计）；
  - Step 2A 可直接消费的“写作执行包”（章节节拍、不可变事实清单、禁止事项、终检清单）。
- 合同与任务书出现冲突时，以“大纲与设定约束更严格者”为准。

输出：
- 单一“创作执行包”（任务书 + Context Contract + 直写提示词），供 Step 2A 直接消费，不再拆分独立 Step 1.5。

### Step 2A：正文起草

执行前必须加载：
```bash
cat "${SKILL_ROOT}/../../references/shared/core-constraints.md"
```

硬要求：
- 只输出纯正文到章节正文文件；若详细大纲已有章节名，优先使用 `正文/第{chapter_padded}章-{title_safe}.md`，否则回退为 `正文/第{chapter_padded}章.md`。
- 默认按 2000-2500 字执行；若大纲为关键战斗章/高潮章/卷末章或用户明确指定，则按大纲/用户优先。
- 禁止占位符正文（如 `[TODO]`、`[待补充]`）。
- 保留承接关系：若上章有明确钩子，本章必须回应（可部分兑现）。

中文思维写作约束（硬规则）：
- **禁止"先英后中"**：不得先用英文工程化骨架（如 ABCDE 分段、Summary/Conclusion 框架）组织内容，再翻译成中文。
- **中文叙事单元优先**：以"动作、反应、代价、情绪、场景、关系位移"为基本叙事单元，不使用英文结构标签驱动正文生成。
- **禁止英文结论话术**：正文、审查说明、润色说明、变更摘要、最终报告中不得出现 Overall / PASS / FAIL / Summary / Conclusion 等英文结论标题。
- **英文仅限机器标识**：CLI flag（`--fast`）、checker id（`consistency-checker`）、DB 字段名（`anti_ai_force_check`）、JSON 键名等不可改的接口名保持英文，其余一律使用简体中文。

输出：
- 章节草稿（可进入 Step 2B 或 Step 3）。

### Step 2B：风格适配（`--fast` / `--minimal` 跳过）

执行前加载：
```bash
cat "${SKILL_ROOT}/references/style-adapter.md"
```

硬要求：
- 只做表达层转译，不改剧情事实、事件顺序、角色行为结果、设定规则。
- 对“模板腔、说明腔、机械腔”做定向改写，为 Step 4 留出问题修复空间。

输出：
- 风格化正文（覆盖原章节文件）。

### Step 3：审查（必须由 Task 子代理执行）

#### 3.1 确定应执行的审查器

执行前加载审查器配置：
```bash
# 获取标准模式审查器列表
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" checkers list --mode standard --format json

# 验证审查器配置完整性
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" checkers validate
```

审查器配置来源：`../../checkers/registry.yaml`（配置） + `../../agents/*.md`（实现）

**模式判定**：
- `--minimal`：`--mode minimal`（只执行核心审查器）
- `--fast`/标准：`--mode standard`（执行核心 + 条件命中）

**审查器分类**：
- 核心审查器（始终执行）：由 registry.yaml 中 `category: core` 定义
- 条件审查器（满足任一条件则执行）：
  - `reader-pull-checker`：非过渡章、有未闭合问题
  - `high-point-checker`：关键章/高潮章、有战斗/打脸/反转信号
  - `pacing-checker`：章号 >= 10 或节奏失衡风险

#### 3.2 调用审查器（关键）

**⚠️ 重要约束**：
- 必须让 OpenCode 加载 agent 文件的完整定义
- **不要**在 prompt 中包含具体检查项、JSON 模板、评分标准
- prompt 中只传递必要参数（章节号、文件路径、项目根）
- 如需传递额外上下文（如上章钩子、大纲标签），只放在 prompt 最后作为"背景信息"

**Task 调用模板**：
```
并行调用审查器（使用 Task 工具）：

Task 1:
  - agent/subagent: consistency-checker
  - prompt: |
      对第 {chapter} 章执行设定一致性审查。
      - 章节文件：{chapter_file}
      - 项目根：{PROJECT_ROOT}
      - 审查器实现见：.opencode/agents/consistency-checker.md（由 registry.yaml 的 file 字段指定）

Task 2:
  - agent/subagent: continuity-checker
  - prompt: |
      对第 {chapter} 章执行连贯性审查。
      - 章节文件：{chapter_file}
      - 项目根：{PROJECT_ROOT}
      - 审查器实现见：.opencode/agents/continuity-checker.md（由 registry.yaml 的 file 字段指定）

Task 3:
  - agent/subagent: ooc-checker
  - prompt: |
      对第 {chapter} 章执行人物OOC审查。
      - 章节文件：{chapter_file}
      - 项目根：{PROJECT_ROOT}
      - 审查器实现见：.opencode/agents/ooc-checker.md（由 registry.yaml 的 file 字段指定）

（条件审查器若有触发，按同样方式调用）
```

#### 3.3 审查器输出格式约束

所有审查器必须返回符合 schema.yaml 的统一格式：

```json
{
  "agent": "审查器ID（必须与 registry.yaml 一致）",
  "chapter": 章节号,
  "overall_score": 0-100,
  "pass": true/false,
  "issues": [
    {
      "id": "ISSUE_001",
      "type": "问题类型",
      "severity": "critical|high|medium|low",
      "description": "问题描述",
      "location": "位置（如第5段）",
      "suggestion": "修复建议"
    }
  ],
  "metrics": {...},
  "summary": "一句话总结"
}
```

**字段统一性要求**：
- ✅ 使用 `overall_score`（不是 `score`）
- ✅ `severity` 使用 `critical/high/medium/low`（全小写）
- ✅ `issues` 是数组，每个 issue 包含 `severity` 和 `suggestion`

#### 3.4 汇总审查结果

各审查器返回后，按以下格式汇总：

```json
{
  "checker_results": [
    {"agent": "审查器ID", "overall_score": 85, "pass": true, "issues": [...]},
    ...
  ],
  "overall_score": "各审查器评分的平均值",
  "severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 0},
  "critical_issues": ["关键问题列表"],
  "can_proceed": "severity_counts.critical == 0"
}
```

**汇总规则**：
- `overall_score` = 各审查器 `overall_score` 的加权平均
- dimension_scores 按 registry.yaml 中的 dimension_mapping 映射
- 若 `critical > 0`，必须修复后才能进入 Step 4

#### 3.5 保存审查指标

审查指标落库（必做）：
```bash
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index save-review-metrics --data "@${PROJECT_ROOT}/.webnovel/tmp/review_metrics.json"
```

review_metrics 字段约束：
```json
{
  "start_chapter": 100,
  "end_chapter": 100,
  "overall_score": 85.0,
  "dimension_scores": {"爽点密度": 8.5, "设定一致性": 8.0, "节奏控制": 7.8, "人物塑造": 8.2, "连贯性": 9.0, "追读力": 8.7},
  "severity_counts": {"critical": 0, "high": 1, "medium": 2, "low": 0},
  "critical_issues": ["问题描述"],
  "report_file": "审查报告/第100-100章审查报告.md",
  "notes": "单个字符串；selected_checkers / timeline_gate 等扩展信息压成单行"
}
```

**硬要求**：
- `--minimal` 也必须产出 `overall_score`
- 未落库 `review_metrics` 不得进入 Step 5

### Step 4：润色（问题修复优先）

执行前必须加载：
```bash
cat "${SKILL_ROOT}/references/polish-guide.md"
cat "${SKILL_ROOT}/references/writing/typesetting.md"
```

执行顺序：
1. 修复 `critical`（必须）
2. 修复 `high`（不能修复则记录 deviation）
3. 处理 `medium/low`（按收益择优）
4. 执行 Anti-AI 与 No-Poison 全文终检（必须输出 `anti_ai_force_check: pass/fail`）

输出：
- 润色后正文（覆盖章节文件）
- 变更摘要（至少含：修复项、保留项、deviation、`anti_ai_force_check`）

### Step 5：Data Agent（状态与索引回写）

使用 Task 调用 `data-agent`，参数：
- `chapter`
- `chapter_file` 必须传入实际章节文件路径；若详细大纲已有章节名，优先传 `正文/第{chapter_padded}章-{title_safe}.md`，否则传 `正文/第{chapter_padded}章.md`
- `review_score=Step 3 overall_score`
- `project_root`
- `storage_path=.webnovel/`
- `state_file=.webnovel/state.json`

Data Agent 默认子步骤（全部执行）：
- A. 加载上下文
- B. AI 实体提取
- C. 实体消歧
- D. 写入 state/index
- E. 写入章节摘要
- F. AI 场景切片
- G. RAG 向量索引（`rag index-chapter --scenes ...`）
- H. 风格样本评估（`style extract --scenes ...`，仅 `review_score >= 80` 时）
- I. 债务利息（默认跳过）

`--scenes` 来源优先级（G/H 步骤共用）：
1. 优先从 `index.db` 的 scenes 记录获取（Step F 写入的结果）
2. 其次按 `start_line` / `end_line` 从正文切片构造
3. 最后允许单场景退化（整章作为一个 scene）

Step 5 失败隔离规则：
- 若 G/H 失败原因是 `--scenes` 缺失、scene 为空、scene JSON 格式错误：只补跑 G/H 子步骤，不回滚或重跑 Step 1-4。
- 若 A-E 失败（state/index/summary 写入失败）：仅重跑 Step 5，不回滚已通过的 Step 1-4。
- 禁止因 RAG/style 子步骤失败而重跑整个写作链。

执行后检查（最小白名单）：
- `.webnovel/state.json`
- `.webnovel/index.db`
- `.webnovel/summaries/ch{chapter_padded}.md`
- `.webnovel/observability/data_agent_timing.jsonl`（观测日志）

性能要求：
- 读取 timing 日志最近一条；
- 当 `TOTAL > 30000ms` 时，输出最慢 2-3 个环节与原因说明。

观测日志说明：
- `call_trace.jsonl`：外层流程调用链（agent 启动、排队、环境探测等系统开销）。
- `data_agent_timing.jsonl`：Data Agent 内部各子步骤耗时。
- 当外层总耗时远大于内层 timing 之和时，默认先归因为 agent 启动与环境探测开销，不误判为正文或数据处理慢。

债务利息：
- 默认关闭，仅在用户明确要求或开启追踪时执行（见 `step-5-debt-switch.md`）。

### Step 6：Git 备份（可失败但需说明）

```bash
git add .
git -c i18n.commitEncoding=UTF-8 commit -m "第{chapter_num}章: {title}"
```

规则：
- 提交时机：验证、回写、清理全部完成后最后执行。
- 提交信息默认中文，格式：`第{chapter_num}章: {title}`。
- 若 commit 失败，必须给出失败原因与未提交文件范围。

### Step 7：批量子代理调度（仅当 `--chapters > 1` 时执行）

**此 Step 仅在批量模式下执行**。单章模式跳过此 Step。

#### 7.1 检测已有章节

```bash
# 获取已存在章节列表
EXISTING_CHAPTERS=$(python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" export list 2>/dev/null || echo "")

echo "已存在章节: ${EXISTING_CHAPTERS}"
```

#### 7.2 循环调用子代理

```bash
# 初始化计数器
SUCCESS_COUNT=0
FAILED_CHAPTER=""

for i in $(seq 1 ${BATCH_COUNT}); do
    CHAPTER_NUM=$((START_CHAPTER + i - 1))
    chapter_padded=$(printf "%04d" ${CHAPTER_NUM})
    
    # 检查是否已存在
    if echo "${EXISTING_CHAPTERS}" | grep -qw "${CHAPTER_NUM}"; then
        echo "[跳过] 第 ${CHAPTER_NUM} 章已存在"
        continue
    fi
    
    echo ""
    echo "[${i}/${BATCH_COUNT}] 正在写第 ${CHAPTER_NUM} 章..."
    
    # 调用子代理执行单章写作
    # 使用 Task 工具调用 webnovel-write（单章模式）
    # 传递当前章节号作为参数
    Task(
        subagent="webnovel-write",
        prompt="请执行单章写作流程，写第 ${CHAPTER_NUM} 章。
                项目根目录: ${PROJECT_ROOT}
                使用标准流程: 预检 → 上下文搜集 → 起草 → 审查 → 润色 → 数据回写
                注意：只需写一章，不要尝试写多章。"
    )
    
    # 检查子代理执行结果
    # 如果失败，记录并回滚
    if [ $? -ne 0 ]; then
        echo "[失败] 第 ${CHAPTER_NUM} 章写作失败"
        FAILED_CHAPTER=${CHAPTER_NUM}
        break
    fi
    
    # 成功，收集评分（从最近的 review_metrics 或 workflow 记录）
    echo "[完成] 第 ${CHAPTER_NUM} 章"
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    
    # 更新已存在章节列表（供下一轮检查）
    EXISTING_CHAPTERS="${EXISTING_CHAPTERS} ${CHAPTER_NUM}"
done
```

#### 7.3 失败回滚

**当某章失败时，执行回滚**：

```bash
if [ -n "${FAILED_CHAPTER}" ]; then
    echo ""
    echo "========================================"
    echo "批量写作中断：第 ${FAILED_CHAPTER} 章失败"
    echo "========================================"
    
    # 回滚已成功写入的章节
    ROLLBACK_START=${START_CHAPTER}
    ROLLBACK_END=$((FAILED_CHAPTER - 1))
    
    if [ ${ROLLBACK_START} -le ${ROLLBACK_END} ]; then
        echo "正在回滚第 ${ROLLBACK_START}-${ROLLBACK_END} 章..."
        
        for n in $(seq ${ROLLBACK_START} ${ROLLBACK_END}); do
            n_padded=$(printf "%04d" ${n})
            # 删除章节文件
            rm -f "${PROJECT_ROOT}/正文/第${n_padded}章"*.md 2>/dev/null || true
            # 删除摘要文件
            rm -f "${PROJECT_ROOT}/.webnovel/summaries/ch${n_padded}.md" 2>/dev/null || true
        done
        
        echo "已回滚 ${SUCCESS_COUNT} 章"
    fi
    
    exit 1
fi
```

#### 7.4 结果汇总

```bash
echo ""
echo "========================================"
echo "批量写作完成"
echo "成功: ${SUCCESS_COUNT}/${BATCH_COUNT} 章"
echo "起始章节: ${START_CHAPTER}"
echo "========================================"
```

#### 批量模式流程图

```
批量模式 (--chapters=N):
  Step 0 → Step 0.1 (解析参数) → Step 7.1 (检测已有章节)
       ↘ Step 7.2 (循环调用子代理 N 次)
           ↘ 成功 → 继续下一章
           ↘ 失败 → Step 7.3 (回滚) → exit 1
       ↘ Step 7.4 (结果汇总)
```

## 充分性闸门（必须通过）

未满足以下条件前，不得结束流程：

1. 章节正文文件存在且非空：`正文/第{chapter_padded}章-{title_safe}.md` 或 `正文/第{chapter_padded}章.md`
2. Step 3 已产出 `overall_score` 且 `review_metrics` 成功落库
3. Step 4 已处理全部 `critical`，`high` 未修项有 deviation 记录
4. Step 4 的 `anti_ai_force_check=pass`（基于全文检查；fail 时不得进入 Step 5）
5. Step 5 已回写 `state.json`、`index.db`、`summaries/ch{chapter_padded}.md`
6. 若开启性能观测，已读取最新 timing 记录并输出结论

## 验证与交付

执行检查：

```bash
test -f "${PROJECT_ROOT}/.webnovel/state.json"
test -f "${PROJECT_ROOT}/正文/第${chapter_padded}章.md"
test -f "${PROJECT_ROOT}/.webnovel/summaries/ch${chapter_padded}.md"
python -X utf8 "${SCRIPTS_DIR}/webnovel.py" --project-root "${PROJECT_ROOT}" index get-recent-review-metrics --limit 1
tail -n 1 "${PROJECT_ROOT}/.webnovel/observability/data_agent_timing.jsonl" || true
```

成功标准：
- 章节文件、摘要文件、状态文件齐全且内容可读。
- 审查分数可追溯，`overall_score` 与 Step 5 输入一致。
- 润色后未破坏大纲与设定约束。

## 失败处理（最小回滚）

触发条件：
- 章节文件缺失或空文件；
- 审查结果未落库；
- Data Agent 关键产物缺失；
- 润色引入设定冲突。

恢复流程：
1. 仅重跑失败步骤，不回滚已通过步骤。
2. 常见最小修复：
   - 审查缺失：只重跑 Step 3 并落库；
   - 润色失真：恢复 Step 2A 输出并重做 Step 4；
   - 摘要/状态缺失：只重跑 Step 5；
3. 重新执行“验证与交付”全部检查，通过后结束。
