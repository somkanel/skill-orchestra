# 真实迭代与快照 / Development history

这个仓库保留首次公开发布前的本地开发演进。早期提交由已保存的 ZIP 快照依次导入，提交时间是本次入库时间，没有回填日期；历史标签和预览版不代表此前已公开发布。0.5.1 是建库审查后产生的新修复。

The early commits import preserved local development ZIPs at repository setup time. Commit dates are actual import dates, not reconstructed development dates. Historical tags and prereleases do not imply earlier public availability. Version 0.5.1 contains the subsequent release-review fix.

| 版本 | 真实变化 | 快照与标签 |
| --- | --- | --- |
| 0.1.0 | 三角色、评分器、双语说明与打包 | 保存快照，v0.1.0 |
| 0.2.0 | 使用频次与本地台账，后来撤回 | 保存快照，v0.2.0；不建议安装 |
| 0.2.1 | 撤掉频次统计，收拢证据边界 | 只有变更记录，没有独立冻结源码；不补造标签 |
| 0.3.0 | 来源收集、快照核对与交付验收 | 保存快照，包含 0.2.1 的调整，v0.3.0 |
| 0.4.0 | 必要能力核实、完整范围与真实 CLI 验证 | 两份连续快照，分别提交；v0.4.0 指向验证说明更新后的快照 |
| 0.5.0 | 用户明确指定优先，能力提示不阻拦 | 保存快照，v0.5.0 |
| 0.5.1 | 修复打包输出链接边界，整理公开入口与历史 | 建库后的真实修复提交，v0.5.1 |

0.4.0 曾对用户指定也核实准入，0.5.0 根据用户要求改为直接遵从；历史源码与说明保留当时行为。当前没有频次统计。每个版本的具体差异可在提交记录中查看。

## 原始 ZIP 指纹

以下 SHA-256 对应原始本地草案 ZIP，供来源追溯；GitHub Release 附件从相应 Git 标签重新构建，文件名、前缀和 ZIP 元信息不同，校验值也不同。原始草案不作为推荐安装附件。

These hashes identify the original local draft ZIPs. Release assets are rebuilt from Git tags and have separate checksums; different prefixes and ZIP metadata mean the bytes differ.

| 原始快照 | SHA-256 |
| --- | --- |
| local-0.1.0 | `bfcad7388840c0f7796f60fe81bc6293ac0f527782d02146db2567488dcb3b42` |
| local-0.2.0 | `15990159ece5c7869801734005a818b1aa1c4039f9d24f390e4a83e42ec1fa5b` |
| local-0.3.0 | `fcd81bf43b598cfb5a0bd511905dfbed2cc803200f85cf5ea4223d026622499e` |
| local-0.4.0 | `55fe8bbf6d213e23d9d09cdfb1e1fc9a1d395c85ddb66453e0ad9b2c2caca7c2` |
| local-0.4.0-verified | `4897d32cd580b2bbdebdc109885f8d7f633b46fff146bc20c8fcf811e6b0bb06` |
| local-0.5.0 | `758ba9b1ca96d9c302d78f8f412a80ed5c91294c90eef74fa0f29a596e2efb77` |

## 此后的版本如何产生

从这里开始，每次变更先形成真实提交，更新记录说明用户可见变化，CI 通过后创建新标签与预览版；已发布标签不移动。尚未完成的尝试留在分支或草案中，不提前编造版本、日期、PR 或测试结果。

Going forward, changes become real commits, then pass CI before a new tag and prerelease. Published tags do not move. Incomplete work stays in branches or drafts; versions, dates, PRs and test outcomes are not invented.
