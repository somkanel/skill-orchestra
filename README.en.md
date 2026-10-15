# 🎼 Skill Orchestra

**Give each task the skills it needs.**

[中文](README.md) · English

A skill suite for Codex and similar agent harnesses: **understand the task → compare fit → explain the choice → continue the work.**

When installed skills overlap, explain what kind of capability the task needs, identify relevant skills visible in the current session, and compare them using one rubric. A top-score tie belongs to the user, with concrete tradeoffs explained first.

Version **0.1.0 is a local development build**. It has not been published on GitHub or behaviorally accepted in a fresh harness session. See [validation](docs/validation.md) for the actual evidence.

## Why Orchestra?

Not every instrument needs to play at once. 🎼 The **conductor** coordinates the work. 🎹 The **pianist** compares skills through a task-specific audition. 🎻 The **first violin** clarifies roles and coordination across the library. Each skill works independently, or through the conductor.

Commands use familiar instrument names with a shared `skill-` prefix: orchestra, piano, violin. Musical imagery marks roles; explanations stay plain and specific.

## Install and update

Copy the three complete directories under `skills/` from this project or extracted draft ZIP to a Codex discovery location:

| Scope | Location |
| --- | --- |
| User | `~/.agents/skills/` |
| Project | `<project>/.agents/skills/` |

Keep references, scripts, agent metadata and licenses intact. Start a fresh session and verify all three entries before explicit invocation. Check the actual harness discovery list if its version uses different paths. No public repository URL or online installation command is provided yet.

Before updating, back up existing folders and preserve custom preferences and voice changes. Avoid installing the same instance into multiple discovery locations. Full installation shares voice guidance; individual skills retain their core workflow without the conductor. Installation does not change harness settings.

## Use

```text
$skill-orchestra Choose suitable skills, explain why, then complete this task: <task>
$skill-piano Compare the current session's skills for this task and explain their scores: <task>
$skill-violin Read-only audit my skill library and explain overlap and useful coordination.
```

Standalone comparison ends with the comparison; a task given to the conductor continues after selection. Top-score ties wait for the user's actual answer. A preselected UI option or silence is not an answer.

| Skill | Role |
| --- | --- |
| [🎼 skill-orchestra](skills/skill-orchestra/SKILL.md) | Explain, coordinate selection and continue execution |
| [🎹 skill-piano](skills/skill-piano/SKILL.md) | Score same-stage alternatives and explain tradeoffs |
| [🎻 skill-violin](skills/skill-violin/SKILL.md) | Audit identities, overlapping triggers and workflow conflicts |

## Fit scores

Check mandatory requirements first. Then score delivery fit (30), task coverage (24), environment (20), constraints (16) and workflow suitability (10). Three evidence-backed grades per dimension produce a 100-point score. Unknowns retain ranges; ineligible candidates do not rank. Scores describe task fit, not success probabilities or general quality.

The agent reads skills, assesses evidence and explains grades. A standard-library Python tool validates records, computes scores and identifies ties or missing evidence. It does not invoke skills or verify the truth of evidence. See the [protocol](skills/skill-piano/references/protocol.md).

## Run and develop

The scoring helper needs Python 3.10+ with no third-party dependencies, keys or added paid services. Without Python, manual calculation is possible with an explicit note that programmatic validation was unavailable. Other workflows are agent instructions rather than an autonomous daemon.

```bash
python3 skills/skill-piano/scripts/score.py examples/comparison.json
python3 tools/check.py
python3 -m unittest discover -s tests -v
python3 tools/package.py --output /tmp/skill-orchestra-draft
```

Example candidates are synthetic, not real skill rankings. The package tool produces a draft ZIP and checksum, refuses existing outputs, and does not publish releases.

## Boundaries and privacy

Skills cannot guarantee loading order or remove previously injected instructions. Clear tasks need no selection ceremony. Compare each necessary stage separately. Respect explicit user choices; do not modify configurations or disable skills without appropriate authorization.

The scoring helper works locally without network access. Agent inference depends on the harness. Private task records, local skill paths and evaluation transcripts belong in task directories, not public packages. Current tests do not establish cross-harness behavior or semantic routing quality.

## Documentation and license

[Voice](skills/skill-orchestra/references/voice.md) · [Scoring](skills/skill-piano/references/scoring.md) · [Evaluation](docs/evaluation.md) · [Validation](docs/validation.md) · [Contributing](CONTRIBUTING.md) · [Releasing](docs/releasing.md) · [Changelog](CHANGELOG.md)

[MIT](LICENSE). Naming and modular role design were inspired by [Video Circus](https://github.com/somkanel/video-circus). No video-processing code, dependencies, private records or third-party binaries are bundled.
