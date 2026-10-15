# 评分计算协议

Python 3.10+，仅标准库。Agent 先依评分规则判断档位并保留证据，再调用 `scripts/score.py`；程序不读取其他技能、不检查宿主配置，也不执行所选技能。

```bash
python3 <skill-piano绝对路径>/scripts/score.py <评分输入.json>
```

也支持通过 stdin 输入。结果写 stdout，输入错误写 stderr，退出码 2；有效结果退出码 0。不得把退出码 0 当成已经选择：必须读取 state。

输入字段：

- `schema`：`skill-orchestra/score-1`。
- `task`、`stage`：非空的任务与阶段说明，一次仅比较同一阶段。
- `candidates`：非空数组，每项包含唯一 `id`、`name`、真实绝对 `path`、`eligibility`、`eligibility_evidence` 和 `scores`。程序按记录区分路径，不证明路径真实可读；Agent 负责核实和解析同一实例。
- `eligibility`：`eligible`、`ineligible` 或 `unknown`；证据说明硬性条件符合、不符合或尚未知的原因。
- `scores`：必须含 delivery、coverage、environment、constraints、workflow 五项；每项为 `{"grade": 2, "evidence": "实际依据"}`。grade 仅为整数 0、1、2 或 null；未知原因也必须写 evidence。不适用候选可使用 null 并说明为何无需继续评分。
- 可选 `user_choice`：真实用户明确选择的候选 id；不得从默认偏好、界面预选或沉默生成此字段。

五项权重固定，未知字段被拒绝。当前版本不支持自定义权重；用户要求时先解释限制，不自行改程序或声称已应用新权重。

结果状态：

| state | 下一步 |
| --- | --- |
| ready | 唯一最高分可行候选，优先调用 selected |
| user_selected | 尊重用户明确选择的可行候选 selected |
| awaiting_choice | options 为全部最高分并列项，解释取舍并等待用户选择 |
| needs_evidence | options 为可能改变结果的待核实项，先补证据 |
| choice_unavailable | 用户所选候选不满足必要条件，解释并请求新选择，不自动替换 |
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
