# Changelog / 更新记录

## 0.5.1 · Public preview / 公开预览

- 打包时拒绝悬空输出链接，避免把草案写到意外位置。
- 公开保存的开发快照、差异与版本标签，说明首次入库时间及缺失快照。
- Reject dangling output links when packaging to avoid writing drafts to unintended locations.
- Publish preserved development snapshots, diffs and tags with clear import dates and snapshot gaps.

## 0.5.0 — Local development / 本地开发版

- 用户在开场或后续明确指定技能时直接遵从，自动准入、排名、平局只作用于未指定场景。
- 评分器user_choice返回user_selected，能力缺口保留为advisories；移除choice_unavailable，不伪造能力判断。
- Explicit user choice bypasses admission and ranking; capability findings remain advisory.

## 0.4.0 — Local development / 本地开发版

- score-2协议：逐项核实交付条件，明确缺失或核心交付0档不参选；未知保留待核实，空候选返回no_match。
- 用户指定和单候选路径不绕过必要能力核实；不设总分及格线。
- 来源核对要求全部已收集入口有参评或排除理由，部分读取失败不冒称范围完整。
- 旧score-1被明确拒绝；历史测试资料仍按原版留存，升级需要重新核实证据。
- Add delivery requirement gates and inspected-scope accountability. Reject legacy input rather than silently bypass the new checks.

## 0.3.0 — Local development / 本地开发版

- 只读收集指定技能入口，去重真实实例，报告不完整范围；不执行候选内容。
- 真实评分核对文件快照，拒绝入口变更、缺失来源与重复实例。
- 明确交付验收条件、选择后验证与失败归因；不宣称质量或触发效果已被证明。
- Add scoped source inspection, snapshot checks and task acceptance guidance.

## 0.2.1 — Local development / 本地开发版

- 移除使用频次、台账、记录脚本和相关测试，聚焦技能选择。
- 明确证据范围、质量判断边界，新增可选宿主入口说明。
- Remove usage tracking and add evidence boundaries and optional harness integration guidance.

## 0.2.0 — Withdrawn local draft / 已撤回的本地草案

- 在适配分后显示本机已记录使用、近30天次数和最近使用时间；未知历史不填0。
- 新增SQLite台账，同一任务同一实例去重，频次不参与评分或破平局。
- Add local recorded usage, 30-day counts and last-used time without influencing fit scores.
- Read-only queries never create history; retries deduplicate by instance and stable task ID.

## 0.1.0 — Local development / 本地开发版

- 🎼 Conductor, 🎹 pianist and 🎻 first violin workflows with shared voice guidance.
- Evidence-backed task-fit rubric and a Python calculator for totals, unknown ranges, ties and explicit user choices.
- Bilingual documentation, synthetic example, regression tests, project checks and reproducible draft packaging.
- 指挥、钢琴师与首席琴师三个技能及统一表达约定。
- 有证据的适配评分与计算工具，保留未知、最高分平局和用户明确选择。
- 双语文档、合成示例、回归测试、项目检查与可重复草案打包。

Versions 0.1.0 through 0.5.0 are preserved local development snapshots, imported at initial repository publication; see [history](docs/history.md). Local program tests do not establish real harness routing quality.

0.1.0 至 0.5.0 是首次公开建库时补录的本地开发历史，详见[快照说明](docs/history.md)。本地程序验证不能替代真实宿主的技能选择与表达验收。
