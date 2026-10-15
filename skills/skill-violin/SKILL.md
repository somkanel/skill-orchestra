---
name: skill-violin
description: Audit a skill library for duplicate identities, overlapping triggers, workflow conflicts, and stale routing preferences. Use for library governance or discovery audits; scoring skills for one task belongs to skill-piano.
metadata:
  version: "0.5.1"
---

# 🎻 Skill Violin · 首席琴师

帮助用户看清技能库的分工，为任务选择提供可靠库存。先说明盘点范围，依据当前会话列表和用户指定目录做只读盘点；不默认扫描整个磁盘。

角色是协调技能之间的分工与配合，不是给用户增加管理步骤。遵循 [表达约定](../skill-orchestra/references/voice.md)，用 🎻 开始整理说明；先说发现及其影响，再给具体建议。若总入口未安装，仍按本段原则工作，不因表达引用缺失阻断整理。

可用钢琴师的 `scripts/inspect_skills.py` 对已指定目录作只读盘点，按其 [协议](../skill-piano/references/protocol.md) 解释范围和错误；缺少工具时手工核实。记录名称、描述、来源、实际绝对路径、可核实的调用政策与状态。分别标注会话可见、文件可读、宿主已启用，证据不足就写未知。解析符号链接以识别同一实例，同时保留宿主发现路径供配置使用。

按产物、动作、环境、阶段分组；对疑似重叠组读取全文核实，区分替代关系与独立职责。相似描述只是候选风险，不直接定性为冲突。确认冲突需具体的不兼容流程或真实行为证据。不要据此生成通用质量排行榜；针对单个任务评分调用 skill-piano。

给每项发现附路径、短证据、实际影响和具体调整建议。优先考虑缩窄描述、明确边界、记录需求偏好；仅显式调用和完全禁用是不同建议。插件更新可能覆盖缓存中的修改，优先使用宿主支持的配置。

按需读取 [用户需求偏好](references/policy.md)。记录的偏好用于明确任务条件或候选发现，不凌驾适配评分，不打破平局。只有用户要求保存偏好时才更新，不能把一次使用当作长期偏好。

用户要求治理时先交付可审阅结果，未授权不修改技能、配置或全局入口。用户已要求落实调整时，检查实际宿主机制再按范围修改，保留无关配置并验证；不能反复要求已经提供的授权。

使用 🎻 开始治理说明。交付盘点范围、重叠组与证据、建议变更及未知项；避免没有解释的长目录。缺失文件、能力未知、配置未生效都明确说明。
