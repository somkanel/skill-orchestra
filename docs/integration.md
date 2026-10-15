# 宿主入口与证据边界 / Harness integration

技能描述帮助发现，不具备调度优先权。仅安装技能不能保证普通任务先经过乐团。推荐显式调用，或用户选择启用一条宿主常驻路由约定。无需守护进程、调用台账或新日志。

## 可选常驻约定

Codex 可放入生效的用户级或项目级 AGENTS.md；Claude Code 可放入生效的用户级或项目级 CLAUDE.md。合并到已有指令，不覆盖现有文件。安装技能和修改常驻指令是两个独立步骤，本项目不自动修改配置。将下方占位符换成已安装总入口的真实绝对路径：

```text
选择任务技能前，先浏览当前会话可用技能的名称和描述。
用户在开场或后续对话明确 @、调用或点名使用技能时，直接读取并遵从，不启动自动准入或排名，不要求重复确认。
没有指定时，只有一个明确匹配就核实必要交付能力后直接使用。
仅在用户未指定时，若两个或更多技能可能独立完成同一阶段的主要交付，
先读取 <已安装的 skill-orchestra/SKILL.md 的绝对路径>，
按其流程核实候选、解释任务适配分与证据范围，再继续完成任务。
不同阶段的互补技能无需争同一个名次。
入口不可读时说明一次并按现有指令继续，不声称已完成乐团比较。
此约定遵循上层指令，不授予技能额外权限。
```

这将触发判断放入会话常驻约定，仍由模型执行，不是强制拦截器。指令未加载、技能不可见、上下文限额、指令冲突或模型未遵循时仍可能漏触发。强制执行顺序属于宿主编排职责，单个技能无法保证。

显式入口：Codex 使用 `$skill-orchestra`；Claude Code 使用 `/skill-orchestra`（未加插件命名空间的安装）。插件安装以实际命令列表为准。

## 描述

总入口实际使用的 description：

> Resolve competing skills when several available skills could perform the same task stage. Compare task fit from full instructions and relevant supporting evidence, explain tradeoffs, and continue with the selected skill. Also use for explicit skill selection or library governance; skip comparisons for clear single-skill tasks.

描述表达选择和协调职责。常驻约定解决入口，技能正文负责具体比较。

## 质量与验证

描述发现候选 → 完整入口和相关引用检查 → 决定性实现/依赖核实 → 标注证据范围并评分 → 执行所选技能 → 验收本次产物。

检查按需进行，不把所有候选都运行一遍作为普通路由前置条件。适配分不包含未经验证的质量保证；100分也可能尚未验收实际产出。程序只检查记录和算术，模型判断与证据真实性仍需评测。

## 新会话验收（部分完成）

分别在两种宿主的新会话验证：明确单技能直接使用；同阶段重叠触发乐团；跨阶段互补不误判竞争；用户显式指定不被替换；最高分同分等待选择；入口缺失说明降级。用描述好看但实现不满足硬性要求的合成候选，检查是否依据实现排除；用较短但功能完整的候选，检查是否避免因篇幅扣分。

记录漏触发、误触发和判断错误，不把本地评分程序测试等同于宿主验收。已在Codex CLI一次新启动中验证项目级常驻约定引导普通任务读取乐团，并完成产物；裸安装触发、桌面端普遍表现与Claude Code仍未验证。各场景的实际完成范围见 [验证记录](validation.md)。

## English

Descriptions discover candidates; full instructions and relevant implementation evidence support task-fit judgments. Document inspection and fit scores do not prove output quality. State the evidence coverage and validate the selected skill's deliverable.

Optionally merge a small routing instruction into the effective AGENTS.md (Codex) or CLAUDE.md (Claude Code): inspect available skill summaries before selection; follow explicit user choice; use one clear match directly; when multiple skills can independently perform the same stage, read the installed conductor at its confirmed absolute path and follow its comparison workflow. Complementary stages do not compete. This is model guidance, not enforced scheduling. Do not overwrite existing configuration.

## 官方机制参考

- [Codex 技能发现与调用](https://learn.chatgpt.com/docs/build-skills)
- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code CLAUDE.md](https://code.claude.com/docs/en/memory)

核对日期：2026-10-14。机制文档不等于本项目已通过跨宿主测试。
