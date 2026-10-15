# Changelog / 更新记录

## 0.2.0 — Local development / 本地开发版

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
