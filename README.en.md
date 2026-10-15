<div align="center">
  <h1>🎼 Skill Orchestra</h1>
  <p><b>Give each task the skills it needs.</b></p>
  <p><a href="README.md">中文</a> · English</p>
  <p>
    <a href="https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1"><img src="https://img.shields.io/github/v/release/somkanel/skill-orchestra?include_prereleases&amp;label=preview" alt="Public preview"></a>
    <a href="https://github.com/somkanel/skill-orchestra/actions/workflows/checks.yml"><img src="https://github.com/somkanel/skill-orchestra/actions/workflows/checks.yml/badge.svg?branch=main" alt="Checks"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
    <a href="#runtime"><img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10 or newer"></a>
  </p>
  <p><a href="#install">Install</a> · <a href="#use">Use</a> · <a href="#output">See the output</a> · <a href="#how-it-works">Scoring</a> · <a href="#docs">Docs</a></p>
</div>

A skill suite for **Codex and similar Agent Harnesses**: **understand the task → check capabilities → explain the choice → deliver the work**.

Installed several similar skills but unsure which one fits? Orchestra helps the Agent find alternatives for the same stage, read their instructions and relevant implementation, and compare them against the actual deliverable.

- **Check delivery capability**: descriptions help discovery; necessary capabilities need evidence before recommendation.
- **Explain the tradeoffs**: show what the task needs, which skills match, and why one fits better; top-score ties belong to you.
- **Respect your choice**: explicit skill selection at the start or later in the conversation takes priority, with capability concerns kept advisory.
- **Continue the work**: the conductor proceeds to execution and acceptance checks; comparison and library governance can also run independently.

> **Current version: [v0.5.1 public preview](https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1).** Limited Codex CLI behavior checks exist. Claude Code invocation conventions are provided below, but behavior has not been tested there. Installation alone cannot guarantee activation. See [validation](docs/validation.md).

## Why Orchestra?

Not every instrument needs to play at once. 🎼 The **conductor** connects the workflow. 🎹 The **pianist** compares skills through a task-specific audition. 🎻 The **first violin** clarifies roles so skills can work together. Progress messages use these symbols, while explanations stay plain and specific.

Remember `orchestra`, `piano`, and `violin`, with a shared `skill-` prefix. Each role works independently or through the conductor.

<a id="install"></a>

## Install

[Download v0.5.1](https://github.com/somkanel/skill-orchestra/releases/tag/v0.5.1) · [Changelog](CHANGELOG.md) · [Development history](docs/history.md)

Use the [Skills CLI](https://github.com/vercel-labs/skills), which requires Node.js / npm and Git. This command pins the recommended preview:

```bash
npx skills add https://github.com/somkanel/skill-orchestra/tree/v0.5.1 --skill '*' -a codex claude-code -g
```

This installs the conductor and both companion skills. For one Harness, keep only its name after `-a`. Omit `-g` for project installation. Start a fresh session and check that all three skills are visible.

**Or paste this into Codex or Claude Code:**

```text
Install Skill Orchestra from the v0.5.1 tag of https://github.com/somkanel/skill-orchestra.
Install all three complete directories, skill-orchestra, skill-piano and skill-violin,
in this Harness's user-level skill directory, preserving existing custom changes.
Check for Python 3.10 or newer and run the included synthetic scoring example.
Do not overwrite AGENTS.md or CLAUDE.md; explain the optional routing convention if I want automatic coordination.
```

<details>
<summary>Manual installation, updates, and other Harnesses</summary>

Download the [source ZIP](https://github.com/somkanel/skill-orchestra/releases/download/v0.5.1/skill-orchestra-0.5.1.zip) and [SHA-256 file](https://github.com/somkanel/skill-orchestra/releases/download/v0.5.1/skill-orchestra-0.5.1.sha256), verify the checksum, and extract. Or clone the same tag:

```bash
git clone --branch v0.5.1 --depth 1 https://github.com/somkanel/skill-orchestra.git
```

Copy all three complete directories under `skills/`, including scripts, references, metadata, and LICENSE:

| Harness | User-level installation | Project-level installation |
| --- | --- | --- |
| [Codex](https://developers.openai.com/codex/skills/) | `~/.agents/skills/` | `.agents/skills/` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/` | `.claude/skills/` |

For other Agent Skills hosts, check their actual discovery paths and skill lists. Do not copy `docs/` or historical archives as skills.

Back up existing folders before updating and preserve custom changes. Install each instance in one discovery location to avoid duplicates. A full installation shares voice guidance; individual companion skills retain their core workflow. Historical versions document development. Usage tracking from 0.2.0 was withdrawn and is absent from the current version.

</details>

<a id="use"></a>

## Use

**Codex**, invoke with `$`:

```text
$skill-orchestra Design a product homepage. Compare suitable skills, explain the choice, then complete the task.
```

**Claude Code**, for a regular skill installation, invoke with `/`:

```text
/skill-orchestra Design a product homepage. Compare suitable skills, explain the choice, then complete the task.
```

Include the deliverable, existing project, stack, and important constraints, such as "keep the existing React project," "must be editable," or "plan only, no code." Plugin installations may use namespaced commands; check the actual command list.

### Use a role independently

| Skill | When to use it | Output |
| --- | --- | --- |
| [🎼 skill-orchestra · Conductor](skills/skill-orchestra/SKILL.md) | Select skills for a real task and continue execution | Choice explanation, task deliverable, and acceptance results |
| [🎹 skill-piano · Pianist](skills/skill-piano/SKILL.md) | Compare alternatives for the same stage | Fit scores, evidence scope, tradeoffs, or unresolved questions |
| [🎻 skill-violin · First violin](skills/skill-violin/SKILL.md) | Read-only review of overlap and roles | Conflict explanations, complementary roles, and governance suggestions |

```text
$skill-piano Compare this session's skills for the frontend task and explain their scores and tradeoffs.
$skill-violin Read-only audit my skill library for overlap and useful coordination.
```

In Claude Code, replace `$` with `/`. Standalone comparison ends with its findings; the conductor continues the actual task after selection. Explicit user choice is followed directly without asking you to choose again through scoring.

<a id="output"></a>

## What you will see

This is a **synthetic example** illustrating the wording. Scores match the runnable [`comparison.json`](examples/comparison.json); they are not measured rankings of installed skills.

> 🎼 This task needs an editable brand deck, covering both content and brand layout. I will compare skills for this stage, then continue with the better fit.
>
> 🎹 Both candidates meet the example's delivery assumptions. Their differences are in coverage, constraints, and workflow.

| Candidate | Fit score | Strength for this task | Tradeoff |
| --- | ---: | --- | --- |
| Synthetic deck-b | **88 / 100** | Better fit for constraints and workflow | Partial task coverage |
| Synthetic deck-a | 87 / 100 | Full coverage of this stage | Known gaps in constraints and workflow |

> B leads by only one point. Under the same rubric, B takes priority: its constraint and workflow fit narrowly outweigh A's broader coverage.

Real comparisons replace these abstract labels with checked facts and state whether instructions, implementation, execution, or output acceptance were examined. See the [full wording example](examples/experience.md).

**If the highest scores tie**, explain the difference and wait for your answer:

> 🎹 A and B have the same fit score. A follows a template for consistent layouts; B supports custom layouts with more freedom. Both can deliver this task. Which matters more to you?

A preselected UI option or silence is not a choice. Insufficient evidence stays unresolved; no suitable candidate means an explanation rather than a forced recommendation.

<a id="how-it-works"></a>

## How scoring works

```text
Define the deliverable → Find same-stage candidates → Read instructions and relevant implementation
                      → Check capabilities → Compare fit → Explain → Execute and validate
```

Automatic selection checks necessary capabilities first: known gaps exclude a candidate; unknowns need evidence. If only one clearly viable candidate remains, use it without mandatory numerical ranking. Explicit user choice is followed directly.

| Dimension | Weight | What it compares |
| --- | ---: | --- |
| Delivery fit | 30 | Format, content, and editability |
| Task coverage | 24 | Actions, inputs, and scale for this stage |
| Environment | 20 | Tools, host capabilities, and execution approach |
| Constraints | 16 | Confirmed language, brand, privacy, and other conditions |
| Workflow suitability | 10 | Necessary steps relative to task complexity |

Each dimension receives an evidence-backed grade of 0, 1, or 2; unknowns retain ranges. **Scores describe fit for this task, not success probabilities or general skill quality.** Claims such as "professional," "high quality," or "must invoke" do not earn points.

The Agent reads, checks, and explains. Python helpers validate inputs, calculate scores, check source snapshots, and identify decision states. They do not prove evidence truthful or the model's understanding correct. Validate the actual deliverable; if selection fails, explain and reassess rather than silently switching skills. See the [rubric](skills/skill-piano/references/scoring.md) and [source protocol](skills/skill-piano/references/protocol.md).

## Route ordinary tasks through Orchestra

Explicit invocation is the most direct entry. For ordinary conversations, optionally merge the [routing convention](docs/integration.md) into the effective **AGENTS.md** for Codex or **CLAUDE.md** for Claude Code: read the conductor when the user has not chosen a skill and several skills could independently deliver the same stage.

Installation does not edit these files. The convention is model guidance. A skill cannot enforce loading order or remove other instructions already in context. Complementary stages can cooperate, and clear single-skill tasks need no extra comparison.

<a id="runtime"></a>

## Runtime dependencies and development

| Dependency | Purpose |
| --- | --- |
| Harness with skill and local file access | Read candidates, assess evidence, execute, and validate |
| Python 3.10+ | Scoring, read-only source checks, and project checks; standard library only |
| Node.js / npm and Git | Required only for the Skills CLI installation method |

No extra API key or added paid service is needed. Without Python, manual scoring is possible if the missing programmatic check is disclosed. Dependencies are not installed automatically. The Agent coordinates the entry workflow; there is no daemon taking over all skills.

<details>
<summary>Run the synthetic example, checks, and draft packaging</summary>

From the repository root:

```bash
python3 skills/skill-piano/scripts/score.py examples/comparison.json
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 tools/package.py --output /tmp/skill-orchestra-draft
```

The example returns `ready` and selects `deck-b`. Draft packaging needs a new empty output directory and writes a ZIP and SHA-256, refusing existing output paths. It does not create a GitHub Release. Published assets are built from their Git tags.

</details>

## Frequently asked questions

**Does it only read descriptions?** Descriptions discover candidates. Scoring requires full entrypoints and relevant references, with implementation and tool checks where decisive. Source snapshots establish file identity and consistency, not semantic understanding or quality.

**Does installation automatically manage every skill?** Activation is not guaranteed. Explicit invocation and optional host instructions provide entry routing; the Harness retains scheduling and permissions.

**Does it count uses or disable other skills?** There is no usage counter, ledger, or added logging system. Library governance is read-only by default. Installation, disabling, and configuration changes follow user authorization.

**What has been validated?** There are 50 program tests and six cross-platform CI combinations. Limited Codex CLI samples exercised project entry routing, deliverable checks, and waiting on a tie. Both the Orchestra and baseline samples completed the task, so general quality improvement cannot be claimed. Claude Code behavior, bare-install activation, and broad task coverage remain untested.

## Coverage and privacy

Scoring and source helpers run locally without network access or record uploads. Cloud inference depends on the host. Public packages exclude private tasks, actual skill paths, inventories, and evaluation transcripts.

The current input protocol is `score-2`. Legacy records require evidence reassessment rather than a schema-string change. Distinct instances with the same name remain distinct; path aliases for one instance are deduplicated. Scope claims apply only to the disclosed collection range. See [validation](docs/validation.md) for limits.

<a id="docs"></a>

## Docs and license

| What you want to know | Start here |
| --- | --- |
| How choices are explained | [Wording example](examples/experience.md) · [Voice guide](skills/skill-orchestra/references/voice.md) |
| How scoring and provenance work | [Rubric](skills/skill-piano/references/scoring.md) · [Calculation and source protocol](skills/skill-piano/references/protocol.md) |
| How to integrate and validate delivery | [Harness integration](docs/integration.md) · [Delivery and correction](skills/skill-orchestra/references/delivery.md) |
| What was actually tested | [Validation](docs/validation.md) · [Behavioral evaluation](docs/evaluation.md) |
| How the project evolved | [Changelog](CHANGELOG.md) · [Preserved development history](docs/history.md) |
| How to contribute | [Contributing](CONTRIBUTING.md) · [Releasing](docs/releasing.md) · [Report an issue](https://github.com/somkanel/skill-orchestra/issues/new/choose) |

Code and skill instructions use [MIT](LICENSE).
