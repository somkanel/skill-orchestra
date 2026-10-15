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
