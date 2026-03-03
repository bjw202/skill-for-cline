# skill-for-cline

Cline-compatible skills for the "슬기로운 코워크 생활" (Smart Co-work Life) project.

## Overview

This repository contains custom Cline skills designed for Korean business AI workflows.
These skills follow Cline's official skill specification (docs.cline.bot).

## Skills

### Builder Tools (`.cline/skills/`)

| Skill | Description | Purpose |
|-------|-------------|---------|
| `skill-builder` | Design and create Cline skills | Create new custom Cline skills following official standards |
| `skill-converter` | Convert Claude Code/MoAI skills to Cline | Migrate existing Claude Code skills to Cline format |
| `agent-builder` | Build agentic skill packages | Create multi-phase autonomous workflows |

### Sample Skills (`samples-claude-skills/`)

| Sample | Purpose |
|--------|---------|
| biz-email-writer | Korean business email writing |
| data-report-generator | Data report generation |
| excel-automation | Excel automation workflows |
| korean-biz-docs | Korean business document creation |
| korean-translator | Korean translation assistant |
| meeting-minutes | Meeting minutes generation |
| portfolio-builder | Portfolio creation |
| ppt-design-system | PowerPoint design system |
| project-tracker | Project tracking |
| prompt-engineer | Prompt engineering |
| proposal-maker | Business proposal creation |
| svg-diagram | SVG diagram creation |

## Cline Skill Standards

Skills follow the official Cline specification:
- Frontmatter: `name` (kebab-case) + `description` (max 1024 chars, action verb start)
- Docs references: Markdown link format `[file.md](docs/file.md)`
- SKILL.md size: ~5K tokens / 200-300 lines recommended
- Scripts: Only output enters context (token-efficient automation)

## Validation

Use the built-in validation script:

```bash
.cline/skills/skill-builder/scripts/validate-skill.sh <path/to/SKILL.md>
```

## Project Info

- Platform: Cline (VS Code Extension)
- Standards: [docs.cline.bot](https://docs.cline.bot)
- Language: Korean / English (bilingual)
