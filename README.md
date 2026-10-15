<div align="center">
  <h1>🎼 Skill Orchestra · 技能乐团</h1>
  <p><b>让合适的技能，各司其职。</b></p>
  <p>中文 · <a href="README.en.md">English</a></p>
  <p>
    <a href="https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1"><img src="https://img.shields.io/github/v/release/somkanel/skill-orchestra?include_prereleases&amp;label=preview" alt="Public preview"></a>
    <a href="https://github.com/somkanel/skill-orchestra/actions/workflows/checks.yml"><img src="https://github.com/somkanel/skill-orchestra/actions/workflows/checks.yml/badge.svg?branch=main" alt="Checks"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
    <a href="#runtime"><img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10 or newer"></a>
  </p>
  <p><a href="#install">安装</a> · <a href="#use">使用</a> · <a href="#output">看看输出</a> · <a href="#how-it-works">评分依据</a> · <a href="#docs">文档</a></p>
</div>

面向 **Codex 等 Agent Harness** 的技能组：**理解任务 → 核实能力 → 解释选择 → 完成交付**。

安装了几个相近的技能，遇到任务却不知道该用哪一个？乐团帮助 Agent 找出同一阶段的候选、读懂其指令和相关实现，再按本次交付要求比较，让选择有据可查。

- **看交付能力**：描述用于发现候选，必要能力还要核实，不能靠文案赢得推荐。
- **把取舍讲清楚**：说明任务需要什么、命中哪些技能、为何优先某项；最高分同分时，由你决定。
- **遵从你的选择**：你在开场或后续明确 @ 或指定技能时，直接遵从，能力差距作为提示。
- **选择后继续完成**：通过总入口交办任务，会继续执行并按完成条件验收；也可以只做比较或整理技能库。

> **当前为 [v0.5.1 公开预览版](https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1)。** 已有有限的 Codex CLI 行为验证；Claude Code 的调用约定列在下方，实际行为尚未验证。仅安装技能不能保证自动触发，详见[验证记录](docs/validation.md)。

## 为什么叫 Orchestra

一首作品不需要所有乐器同时登场。🎼 **指挥**串联全程；🎹 **钢琴师**试奏比较，为任务择技；🎻 **首席琴师**梳理分工，让不同技能配合得当。进度消息沿用这些符号，解释保持具体、平实。

只需记住 `orchestra`、`piano`、`violin`，技能名统一以 `skill-` 开头。三个角色可独立使用，也可以交给总入口协调。

<a id="install"></a>

## 安装

[下载 v0.5.1](https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1) · [更新记录](CHANGELOG.md) · [真实迭代](docs/history.md)

使用 [Skills CLI](https://github.com/vercel-labs/skills)，需要 Node.js / npm 和 Git。以下固定安装当前推荐的预览版：

```bash
npx skills add https://github.com/somkanel/skill-orchestra/tree/v0.5.1 --skill '*' -a codex claude-code -g
```

这会安装总入口和两个子技能。只使用一个 Harness 时，保留 `-a` 后对应的名称；去掉 `-g` 可安装到当前项目。安装后新建会话，检查三个技能是否可见。

**也可以把下面这段直接发给你的 Codex 或 Claude Code：**

```text
请从 https://github.com/somkanel/skill-orchestra 的 v0.5.1 标签安装技能乐团。
将 skill-orchestra、skill-piano、skill-violin 三个完整技能目录
安装到当前 Harness 的用户级技能目录，保留已有同名技能的自定义修改。
检查 Python 是否为 3.10 或更新版本，并运行附带的合成评分示例。
不要覆盖现有 AGENTS.md 或 CLAUDE.md；需要自动协调时，先说明可选入口约定。
```

<details>
<summary>手动安装、更新与其他 Harness</summary>

下载 [源码 ZIP](https://github.com/somkanel/skill-orchestra/releases/download/v0.5.1/skill-orchestra-0.5.1.zip) 和 [SHA-256 文件](https://github.com/somkanel/skill-orchestra/releases/download/v0.5.1/skill-orchestra-0.5.1.sha256)，核对校验值后解压；也可以拉取相同标签：

```bash
git clone --branch v0.5.1 --depth 1 https://github.com/somkanel/skill-orchestra.git
```

将 `skills/` 下三个完整目录复制到目标位置，保留脚本、引用、元信息和 LICENSE：

| Harness | 用户级安装 | 项目级安装 |
| --- | --- | --- |
| [Codex](https://developers.openai.com/codex/skills/) | `~/.agents/skills/` | `.agents/skills/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/` | `.claude/skills/` |

其他支持 Agent Skills 的宿主，以其实际技能目录和发现列表为准。不要把 `docs/` 或历史归档当作技能目录复制。

更新前备份同名目录，比较并保留自定义内容；同一实例只安装到一个发现位置，避免重复。完整安装可共享表达约定；单独安装子技能仍可使用其核心流程。历史版本用于查看演进，0.2.0 的使用统计已撤回，当前没有频次记录功能。

</details>

<a id="use"></a>

## 使用

**Codex**，用 `$` 调用：

```text
$skill-orchestra 我要设计一个产品首页，请比较适合本次任务的技能，说明依据后继续完成。
```

**Claude Code**，普通技能安装使用 `/` 调用：

```text
/skill-orchestra 我要设计一个产品首页，请比较适合本次任务的技能，说明依据后继续完成。
```

给出目标产物、已有项目、技术栈和重要限制，会让比较更有依据。例如“沿用现有 React 项目”“必须可编辑”“只做方案，不写代码”。通过插件安装时，以实际带命名空间的命令为准。

### 想单独使用一个角色

| 技能 | 何时使用 | 交付结果 |
| --- | --- | --- |
| [🎼 skill-orchestra · 指挥](skills/skill-orchestra/SKILL.md) | 为实际任务协调选择，并继续执行 | 选择说明、本次任务产物与验收结果 |
| [🎹 skill-piano · 钢琴师](skills/skill-piano/SKILL.md) | 只比较同一阶段的多个技能 | 适配分、证据范围、取舍或待确认项 |
| [🎻 skill-violin · 首席琴师](skills/skill-violin/SKILL.md) | 只读整理技能库的重叠与分工 | 冲突说明、互补关系与治理建议 |

```text
$skill-piano 比较当前会话中适合这次前端页面任务的技能，说明评分和取舍。
$skill-violin 只读检查我的技能库，说明哪些可以互补、哪些容易重叠。
```

Claude Code 将上述 `$` 换为 `/`。单独比较结束于比较结果；通过总入口交办实际任务，选择后继续完成。明确指定某个技能时，直接遵从，不用评分要求你重新选择。

<a id="output"></a>

## 你会看到什么

下面是**合成示例**，展示表达方式，分数与可运行的 [`comparison.json`](examples/comparison.json) 一致，不是已安装技能的实测排名。

> 🎼 这次要制作可编辑的品牌演示文稿，需要兼顾内容制作和品牌排版。我会比较适合这个阶段的技能，再选择更合适的一项继续。
>
> 🎹 两个候选都满足示例设定的交付条件，差别主要在任务覆盖、约束适配与流程安排。

| 候选 | 适配分 | 本次适合点 | 本次取舍 |
| --- | ---: | --- | --- |
| Synthetic deck-b | **88 / 100** | 约束与流程更贴合 | 任务覆盖存在部分缺口 |
| Synthetic deck-a | 87 / 100 | 本阶段任务覆盖完整 | 约束与流程各有已知缺口 |

> B 只领先 1 分。按照这次统一标准，优先使用 B；它在约束和流程上的适配，略微抵消了 A 的覆盖优势。

真实比较会用已核实的具体事实代替示例中的抽象描述，并说明已读指令、已查实现、已试运行或已验收的范围。详见[完整表达示例](examples/experience.md)。

**最高分相同**时，先解释差异，再等待你的回答：

> 🎹 A 和 B 的适配分相同，差别主要在制作方式：A 沿用模板，版式更统一；B 支持定制布局，自由度更高。两者都能完成这次交付，你更看重哪一点？

界面预选和沉默不算选择。证据不足时保留“待核实”，没有合适候选时说明原因，不勉强推荐。

<a id="how-it-works"></a>

## 分数如何产生

```text
明确交付要求 → 发现同阶段候选 → 阅读指令与相关实现
             → 核实必要能力 → 比较适配 → 解释选择 → 执行与验收
```

自动选择先核实必要交付能力：明确缺失的候选不参选，未知先补证据。核实后只有一个明确可行候选时直接使用，无需强制排名；你已指定技能时直接遵从。

| 维度 | 权重 | 比较什么 |
| --- | ---: | --- |
| 交付吻合 | 30 | 格式、内容和可编辑程度 |
| 任务覆盖 | 24 | 本阶段动作、输入和规模 |
| 环境适配 | 20 | 工具、宿主能力和执行方式 |
| 约束符合 | 16 | 语言、品牌、隐私等已确认条件 |
| 流程合宜 | 10 | 必要步骤与任务复杂度是否相称 |

每项按证据取 0、1、2 档，未知保留区间。**分数表示本次任务适配度，不是成功概率或技能质量榜。** 不凭描述中的“专业”“高质量”“必须调用”加分。

Agent 负责阅读、核实与解释；Python 工具校验输入、算分、检查来源快照和决策状态。工具不证明证据真实或模型理解正确，最终质量仍须验收本次产物。选择失败时说明事实、重新评估，不悄悄替换技能掩盖失败。详见[评分规则](skills/skill-piano/references/scoring.md)与[来源协议](skills/skill-piano/references/protocol.md)。

## 怎样让普通任务也经过乐团

显式调用最直接。希望在普通对话中协调时，可将[可选路由约定](docs/integration.md)合并到生效的 **AGENTS.md**（Codex）或 **CLAUDE.md**（Claude Code）：用户未指定，且多个技能可能独立完成同一阶段时，再读取总入口。

安装不会修改这些文件。约定仍由模型执行，技能无法强制自己先加载，也不能移除已进入上下文的其他指令。不同阶段的互补技能可以配合，清楚的单技能任务无需额外比较。

<a id="runtime"></a>

## 运行依赖与开发

| 依赖 | 用途 |
| --- | --- |
| 可读取技能和本地文件的 Harness | 阅读候选、判断证据、执行并验收任务 |
| Python 3.10+ | 评分、只读来源核对和项目检查，仅使用标准库 |
| Node.js / npm 和 Git | 仅 Skills CLI 安装方式需要 |

无需额外 API 密钥或新增付费服务。没有 Python 时可以手算，但须说明未经过程序校验；不自动安装依赖。总入口由 Agent 编排，没有独立接管全部技能的常驻进程。

<details>
<summary>运行合成示例、检查与草案打包</summary>

在仓库根目录执行：

```bash
python3 skills/skill-piano/scripts/score.py examples/comparison.json
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 tools/package.py --output /tmp/skill-orchestra-draft
```

示例返回 `ready` 并选择 `deck-b`。草案打包需使用新的空输出目录，生成 ZIP 与 SHA-256，拒绝已有同名路径；不会创建 GitHub Release。正式发布附件从对应 Git 标签构建。

</details>

## 常见问题

**它只看技能描述吗？** 描述用于发现候选；评分需读取完整入口及影响判断的引用，必要时核实实现和工具。来源快照证明读取对象与版本一致，不证明语义理解或实际质量。

**装好就能自动管理所有技能吗？** 不能保证。显式调用与可选宿主约定提供入口，调度和权限仍由 Harness 决定。

**会记录使用次数，或自动禁用其他技能吗？** 当前没有使用计数、台账或新增日志系统。技能库治理默认只读，安装、禁用和配置修改遵循用户授权。

**验证到了什么程度？** 当前有 50 项程序测试和六个跨平台 CI 组合；有限 Codex CLI 样本验证了项目级入口、产物验收与同分等待。本次对照样本中，有无乐团均完成交付，不能宣称总体质量已提升。Claude Code、裸安装自动触发和广泛任务覆盖仍待验证。

## 支持范围与隐私

评分与来源工具在本地运行，不联网或上传记录；Agent 推理是否经过云端取决于宿主。私有任务、真实技能路径、库存与评估记录不随公共包分发。

当前采用 `score-2` 协议，旧输入须重新核实证据后迁移，不能只改版本字符串。相同名称的不同实例分别识别，同一实例的路径别名去重；只对已说明的收集范围负责。具体限制见[验证记录](docs/validation.md)。

<a id="docs"></a>

## 文档与许可

| 想了解什么 | 从这里开始 |
| --- | --- |
| 比较时怎样解释选择 | [表达示例](examples/experience.md) · [表达约定](skills/skill-orchestra/references/voice.md) |
| 如何评分与核对来源 | [评分规则](skills/skill-piano/references/scoring.md) · [计算与来源协议](skills/skill-piano/references/protocol.md) |
| 如何接入与验收 | [宿主入口](docs/integration.md) · [交付与纠偏](skills/skill-orchestra/references/delivery.md) |
| 实际测试了什么 | [验证记录](docs/validation.md) · [行为评测](docs/evaluation.md) |
| 版本怎样演进 | [更新记录](CHANGELOG.md) · [真实迭代与快照](docs/history.md) |
| 如何参与 | [贡献指南](CONTRIBUTING.md) · [发布流程](docs/releasing.md) · [提交问题](https://github.com/somkanel/skill-orchestra/issues/new/choose) |

代码与技能指引采用 [MIT](LICENSE)。命名和角色分工参考同作者的 [🎪 Video Circus](https://github.com/somkanel/video-circus)，未引入其视频处理代码或依赖；详见[第三方说明](THIRD_PARTY_NOTICES.md)。
