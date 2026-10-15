# Contributing / 参与贡献

Python 3.10+，仅标准库。修改评分或交互状态时，请加入能证明实际行为的案例，不只匹配提示词字面。

```bash
python3 tools/check.py
python3 -m unittest discover -s tests -v
```

同步三个技能的引用、协议和中英文首页。行为反馈请记录任务、预期技能、实际读取、选择依据和最终产物；公开问题使用合成数据，不提交个人路径、真实技能库存、私有任务、会话记录、凭据或账户配置。评分工具不会判断证据真假；不要用测试通过数推断语义判断能力。

Python 3.10+ and the standard library are sufficient. Include behavioral regression cases for scoring and state changes; keep both READMEs and skill references aligned. Use synthetic evidence in public fixtures. Never commit private tasks, inventories, paths, transcripts, credentials or account configuration. Report actual harness observations separately from calculator tests.

发布流程见 [releasing.md](docs/releasing.md)。
