# Changelog / 更新记录

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

This version is not a published release. Local program tests do not establish real harness routing quality.

本版尚未公开发布。本地程序验证不能替代真实宿主的技能选择与表达验收。
