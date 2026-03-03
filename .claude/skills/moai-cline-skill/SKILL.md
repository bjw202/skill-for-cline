---
name: moai-cline-skill
description: >
  Creates new Cline-specific skills from scratch and converts existing Claude Code or
  MoAI-ADK skills to Cline format. Use when building a Cline skill, designing a new
  skill for Cline, converting a Claude Code skill to Cline, porting a MoAI skill to
  Cline, or migrating skills between AI platforms.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
user-invocable: true
metadata:
  version: "1.0.0"
  category: "workflow"
  status: "active"
  updated: "2026-03-03"
  modularized: "false"
  tags: "cline, skill-builder, skill-converter, migration, cline-format"
  argument-hint: "[build|convert] [skill-name-or-path]"

# MoAI Extension: Triggers
triggers:
  keywords:
    - cline skill
    - cline 스킬
    - skill builder
    - skill converter
    - cline format
    - convert skill
    - port skill
    - cline migration
    - SKILL.md
    - .cline/skills
---

# Cline Skill Builder & Converter

Builds new Cline skills from scratch and converts Claude Code/MoAI-ADK skills to Cline format.

Two modes:
- **BUILD**: Guide creating a brand-new Cline skill
- **CONVERT**: Transform an existing Claude Code or MoAI-ADK skill into Cline format

---

## Quick Reference

### Cline Skill Format (Minimal Valid Skill)

```yaml
---
name: my-skill          # matches directory name, kebab-case
description: |          # MUST use literal block `|`, NOT folded `>`
  What this skill does in 1-2 sentences.
  Activate on: keyword1, keyword2, keyword3
---
```

Only TWO frontmatter fields are supported: `name` and `description`.
All other Claude Code fields (`allowed-tools`, `model`, `hooks`, `metadata`, etc.) must be removed.

### File Structure

```
.cline/skills/{skill-name}/
  SKILL.md              # Required, under ~400 lines / 5K tokens
  docs/                 # Optional: advanced guides, references
  templates/            # Optional: reusable templates
  scripts/              # Optional: utility scripts (output enters context)
```

### Cline Constraints (Internal Network Policy)

- **MCP servers**: Internal network only (사내망 전용)
- **Hooks**: NOT available (사내 제약)
- **Agent delegation**: No Task()/Agent subagent concepts in Cline
- All Cline tools are available by default — no permission config needed

---

## BUILD Mode: Creating a New Cline Skill

### Step 1: Gather Requirements

Ask the user (or infer from context):
- Skill name (kebab-case, max 64 chars, must match directory)
- Core purpose: what problem does this skill solve?
- Target domain and key workflows
- Whether supporting files are needed (docs/, templates/, scripts/)

Suggest 2-3 name options based on the purpose.

### Step 2: Design the Description

The description is the ONLY activation mechanism. Write it to maximize discoverability:

```yaml
description: |
  [Action verb] [target domain]. [1-2 sentences of what it does.]
  Activate on: [Korean trigger], [English trigger], [specific terms]
```

Rules:
- Use literal block `|` (never folded `>`)
- Third person: "Generates..." not "I generate..."
- Include both Korean and English trigger keywords
- Be specific: "React component design" beats "frontend development"
- Max 1024 characters

Good example:
```yaml
description: |
  데이터베이스 마이그레이션을 안전하게 설계하고 실행한다.
  스키마 변경, 데이터 이전, 롤백 전략을 포함한다.
  Activate on: DB 마이그레이션, 스키마 변경, migration, database schema
```

### Step 3: Write SKILL.md Content

Recommended structure for the SKILL.md body:

```
# [Skill Title]

## Core Mission
[1-2 sentences: purpose and scope]

## Internal Network Constraints
[If skill mentions MCP or hooks, note: MCP = internal only, hooks = unavailable]

## Quick Reference
[Most-used patterns, essential rules]

## Implementation Guide
[Step-by-step workflows]

## Advanced Patterns
[Edge cases, troubleshooting — or link to docs/advanced.md]

## Related Skills
[Other Cline skills that pair well]
```

Token budget: ~5,000 tokens (roughly 300-400 lines). Move overflow content to `docs/`.

### Step 4: Cline Tools to Reference in Skill Content

When writing skill instructions that reference Cline tools, use these names:

| Category | Tool | Purpose |
|----------|------|---------|
| File read | `read_file` | Read file contents |
| File write | `write_to_file` | Create or overwrite file |
| File edit | `replace_in_file` | Partial file replacement |
| Search | `search_files` | Regex search in files |
| Directory | `list_files` | List directory contents |
| Code scan | `list_code_definition_names` | List code definitions |
| Terminal | `execute_command` | Run CLI commands |
| Browser | `browser_action` | Web automation (Puppeteer) |
| MCP | `use_mcp_tool` | MCP tool (internal network only) |
| MCP | `access_mcp_resource` | MCP resource (internal network only) |
| Interaction | `ask_followup_question` | Ask user for clarification |
| Completion | `attempt_completion` | Report final result |
| Context | `new_task` | Switch context window |

### Step 5: Create the Files

```
.cline/skills/{name}/SKILL.md   # main file
.cline/skills/{name}/docs/      # if advanced content needed
```

---

## CONVERT Mode: Claude Code/MoAI-ADK to Cline

### Step 1: Analyze the Source Skill

Read the source SKILL.md and identify:
- Core purpose (keep this)
- Frontmatter fields (most will be removed)
- Tool references (map to Cline equivalents)
- MoAI-specific content (remove or simplify)
- Convertibility: is the core functionality achievable in Cline?

### Step 2: Frontmatter Transformation

| Claude Code Field | Cline Action | Notes |
|------------------|--------------|-------|
| `name` | Keep | Verify kebab-case |
| `description: >` | Keep, change to `\|` | Change scalar type |
| `allowed-tools` | Remove | All tools available by default |
| `model` | Remove | Not supported |
| `context: fork` | Remove | No sub-agent isolation |
| `agent` | Remove | No agent types |
| `hooks` | Remove | Not available (사내 제약) |
| `license` | Remove | Not in Cline format |
| `compatibility` | Remove | Not in Cline format |
| `user-invocable` | Remove | Always invocable |
| `metadata` block | Remove | Not supported |
| `progressive_disclosure` | Remove | Implicit in Cline |
| `triggers` block | Move to description | Embed keywords in description |

Result: only `name` and `description` remain.

### Step 3: Description Rewrite

Claude Code uses `description: >` (folded scalar — newlines become spaces).
Cline requires `description: |` (literal block — preserves newlines for trigger keywords).

Rewrite the description to:
1. Change `>` to `|`
2. Keep the core "what/when" content
3. Add trigger keywords at the end: `Activate on: [keywords]`
4. If `triggers.keywords` existed, embed them into the description

### Step 4: Content Adaptation

Remove these MoAI/Claude Code-specific sections:
- `@MX` tag protocols and SPEC references
- TRUST 5 quality gates
- Agent delegation patterns (Task(), subagent_type, etc.)
- MoAI workflow phases (RED-GREEN-REFACTOR, etc.)
- Context7 MCP references (external MCP not available)
- Progressive disclosure implementation notes

Keep and adapt:
- Core domain knowledge and patterns
- Step-by-step workflows (rewrite as direct instructions)
- Code examples and templates
- Best practices and constraints

### Step 5: Tool Name Mapping

Replace Claude Code tool names with Cline equivalents in all prose:

| Claude Code | Cline |
|-------------|-------|
| `Read` | `read_file` |
| `Write` | `write_to_file` |
| `Edit` | `replace_in_file` |
| `Grep` | `search_files` |
| `Glob` | `list_files` |
| `Bash` | `execute_command` |
| `WebFetch` | `browser_action` or `use_mcp_tool` (internal only) |
| `WebSearch` | Remove (not available) |
| `Task` / `Agent` | Remove (no agent delegation) |
| `AskUserQuestion` | `ask_followup_question` |
| `TodoWrite` | Remove (not available) |

### Step 6: Directory Restructure

| Claude Code Path | Cline Path |
|-----------------|------------|
| `.claude/skills/{name}/` | `.cline/skills/{name}/` |
| `SKILL.md` | `SKILL.md` |
| `modules/*.md` | `docs/*.md` (flatten) |
| `references/` | `docs/` (merge) |
| `scripts/` | `scripts/` (keep) |
| `templates/` | `templates/` (keep) |

### Step 7: Validate

Use this checklist before finishing:

- [ ] `name` matches the directory name
- [ ] `description` uses `|` (literal block), not `>`
- [ ] Only `name` and `description` in frontmatter
- [ ] No Claude Code-specific tool names remain
- [ ] No agent delegation (`Task()`, `subagent_type`) patterns
- [ ] No `@MX` tags or SPEC references
- [ ] No external MCP references
- [ ] No hooks configuration
- [ ] SKILL.md under ~400 lines / 5K tokens
- [ ] File references are one level deep only

---

## Conversion Feasibility Guide

**Convert freely:**
- Knowledge-based skills (guides, patterns, standards)
- File manipulation workflows
- Code analysis and generation
- Terminal/CLI automation

**Convert with adaptation:**
- Skills with external MCP dependencies (internal-only MCP may substitute)
- Skills with heavy agent delegation (rewrite as direct step-by-step instructions)

**Do NOT convert:**
- Skills that fundamentally depend on Claude Code-exclusive features (Agent Teams, hooks automation)
- Skills where >50% of value is lost in conversion

When conversion is not recommended, explain why and suggest what portions can be adapted.

---

## Conversion Report Template

After converting, output a summary:

```markdown
## Skill Conversion Report

**Source**: [path and format]
**Output**: .cline/skills/{name}/

### Changes Made
- Frontmatter: removed [list fields], rewrote description
- Tools mapped: [list of tool name changes]
- Sections removed: [MoAI-specific content removed]
- Files created: [list of new files]

### Functionality Notes
- [Any features that changed behavior]
- [Any features that could not be converted]

### Action Required
- [Items needing user review]
```

---

## Works Well With

- `.cline/skills/skill-builder/` — Cline-native skill creation guide
- `.cline/skills/skill-converter/` — Cline-native conversion guide
- `docs/conversion-mapping.md` — Extended conversion mapping reference

For detailed Cline standards, see [docs/cline-skill-standards.md](docs/cline-skill-standards.md)
