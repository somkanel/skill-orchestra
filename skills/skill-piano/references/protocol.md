# 评分计算协议

Python 3.10+，仅标准库。Agent 先明确交付条件、逐项判断能力，再依评分规则判断档位并保留证据，再调用 `scripts/score.py`；程序不读取其他技能、不检查宿主配置，也不执行所选技能。

```bash
python3 <skill-piano绝对路径>/scripts/score.py <评分输入.json>
```

也支持通过 stdin 输入。结果写 stdout，输入错误写 stderr，退出码 2；有效结果退出码 0。不得把退出码 0 当成已经选择：必须读取 state。

输入字段：

- `schema`：`skill-orchestra/score-2`。
- `requirements`：非空且不重复的交付条件字符串列表，来自本次主要产物和用户要求。
- `checks`：每个候选必须逐项覆盖 requirements；每项为 `{"status": "supported", "evidence": "具体依据"}`，status 可为 supported、missing、unknown。明确缺失则有效 eligibility 为 ineligible；未知则为 unknown。正文支持只证明指令适配，不等于产出质量已实测。
- 可选 `exclusions`：以已收集但不参评的技能绝对路径为键、排除理由为值的对象。来源核对要求全部快照参加比较或有排除理由；同阶段但能力差的候选应进入比较并标记不适用，不能偷偷排除。
- `task`、`stage`：非空的任务与阶段说明，一次仅比较同一阶段。
- `candidates`：数组（允许空，返回 no_match），每项包含唯一 `id`、`name`、真实绝对 `path`、`eligibility`、`eligibility_evidence`、`checks` 和 `scores`。程序按记录区分路径，不证明路径真实可读；Agent 负责核实和解析同一实例。
- `eligibility`：`eligible`、`ineligible` 或 `unknown`；证据说明硬性条件符合、不符合或尚未知的原因。
- `scores`：必须含 delivery、coverage、environment、constraints、workflow 五项；每项为 `{"grade": 2, "evidence": "实际依据"}`。grade 仅为整数 0、1、2 或 null；未知原因也必须写 evidence。不适用候选可使用 null 并说明为何无需继续评分。
- 可选 `user_choice`：真实用户明确选择的候选 id；不得从默认偏好、界面预选或沉默生成此字段。

输出使用 `skill-orchestra/result-2`，保留声明和有效 eligibility、decision_reasons、requirements 及 exclusions。delivery 或 coverage 为0表示核心交付明确不匹配，候选不参选；这不是总分阈值。未知交付可行性不可因分数低而跳过核实。

旧 score-1 输入被拒绝，需重新核实交付条件并生成 score-2，不能只改版本号补占位证据。五项权重固定，未知字段被拒绝。当前版本不支持自定义权重；用户要求时先解释限制，不自行改程序或声称已应用新权重。

结果状态：

| state | 下一步 |
| --- | --- |
| ready | 唯一最高分可行候选，优先调用 selected |
| user_selected | 遵从用户明确指定的 selected；advisories 仅提示能力缺口，不要求重选 |
| awaiting_choice | options 为全部最高分并列项，解释取舍并等待用户选择 |
| needs_evidence | options 为可能改变结果的待核实项，先补证据 |
| no_match | 无可行候选，说明缺口与可行途径 |

结果保留输入顺序和证据，含总分、分项和未知区间；展示时按结果排序，但不把输入顺序作为破平局依据。计算不会验证证据语义、文件存在或档位是否公正，Agent 仍需如实判断。


没有 Python 时可以按评分规则手算并明确未经过程序校验，不自动安装依赖。比较记录保存在任务目录，不写入安装的技能目录或公共发布包，避免包含私人任务材料。

## 真实候选的来源核对

先用 `scripts/inspect_skills.py` 收集宿主列表中已确认的路径：

```bash
python3 <skill-piano绝对路径>/scripts/inspect_skills.py <候选A的SKILL.md> <候选B的SKILL.md> > <任务目录>/sources.json
python3 <skill-piano绝对路径>/scripts/score.py <评分输入.json> --sources <任务目录>/sources.json
```

用户指定技能根目录时可用重复的 `--root <目录>` 盘点。工具不默认扫描磁盘，不执行技能内容；快照含完整入口、真实路径、发现路径和SHA-256。同一实例的链接去重，同名不同实例保留。错误列表必须报告，退出码2表示盘点不完整；不能把本地文件可读当作宿主已启用。工具不解析技能语义，完整技能名单仍以宿主会话列表为准。

Agent 必须读取完整快照和相关引用后再判断，不能仅生成快照就声称已理解。调用评分时携带 `--sources`：程序拒绝缺少入口快照、快照损坏、入口已变更或同一实例重复参选的候选。变更后重新读取并重评，不只刷新哈希。该检查不覆盖引用文件或依赖变化；决定性引用和依赖仍需另行核实。

CLI结果 `source_check.status` 为 `entrypoints_unchanged` 仅表示入口快照与当前文件一致，不证明模型读过全文、证据语义正确或质量优秀；不带 `--sources` 时为 `not_checked`，不得称为来源已核对。合成测试可不带快照。工具不可用时如实说明手工核对范围。

快照包含本机路径和技能全文，放在私有任务目录，不写入公共包或安装目录。不持久化使用事件、不修改被比较的技能。

来源核对要求快照 errors 为空，且已收集入口均进入候选或 exclusions。返回 inspected_scope_accounted_for 只证明这个已收集范围有交代，不能证明宿主名单完整、排除理由正确或 Agent 已读懂全文。读取错误先解决；无法解决时明确不完整范围，不声称获得完整来源核对。

根目录盘点默认跳过 `.git`、`__pycache__`、`node_modules`、`dist` 子目录，实际跳过路径记录在 skipped_subtrees，来源核对结果也保留该范围。若宿主名单包含其中的技能，按显式入口路径补收集，不把默认目录盘点当作宿主全量名单。目录符号链接仅检查直接的SKILL.md，不递归链接树；嵌套技能按宿主具体路径显式补入。

## 显式指定与自动选择分支

user_choice 来自用户开场或后续对话中的明确调用或选择时，返回 user_selected，即使候选当前有效eligibility为ineligible或unknown。advisories附已知缺口；不改变原能力判断或伪造高分。选择权与能力事实分开：程序不执行技能，也不保证其能完成交付。用户指定无需调用评分器，只有需要比较/留存分析时才走这个完整记录协议；不强迫为显式调用补齐一份排行榜。

不再使用choice_unavailable状态。实际入口不存在时澄清/说明定位问题；缺必要输入、授权或确实无法继续时再提出具体问题，不能只因评分不合格要求用户重选。自动选择的missing/unknown/0档规则保持有效。
