# Cline Skill Conversion: Detailed Mapping Reference

Comprehensive mapping tables for converting Claude Code / MoAI-ADK skills to Cline format.
This document is referenced by SKILL.md for extended conversion details.

---

## 1. Frontmatter Field Mapping

### Complete Field Reference

| Claude Code Field | Cline Action | Reason |
|------------------|--------------|--------|
| `name` | Keep | Required; verify kebab-case and directory match |
| `description: >` | Keep, change to `\|` | Cline requires literal block scalar for multi-line trigger keywords |
| `allowed-tools` | Remove | All Cline tools available by default; no permission system |
| `model` | Remove | Cline does not support model selection in frontmatter |
| `context: fork` | Remove | No sub-agent context isolation in Cline |
| `agent` | Remove | No agent type selection in Cline |
| `hooks` | Remove | Hooks not available (사내 제약) |
| `user-invocable` | Remove | All skills are always user-invocable in Cline |
| `disable-model-invocation` | Remove | Not supported |
| `argument-hint` | Remove | Not supported |
| `license` | Remove | Not in Cline spec |
| `compatibility` | Remove | Not in Cline spec |
| `metadata` block | Remove | Not supported; all metadata fields drop |
| `progressive_disclosure` | Remove | Progressive disclosure is implicit in Cline |
| `triggers` block | Embed in description | Move keywords into description "Activate on:" section |

### YAML Scalar Type: Critical Change

Claude Code uses folded scalar (`>`): newlines collapse to spaces.
Cline requires literal block (`|`): newlines preserved, enabling multi-line trigger keywords.

```yaml
# Claude Code (WRONG for Cline)
description: >
  Analyzes Python code quality.
  Use when reviewing Python files.

# Cline (CORRECT)
description: |
  Analyzes Python code quality.
  Use when reviewing Python files.
  Activate on: 파이썬 코드 리뷰, code analysis, Python quality
```

---

## 2. Tool Name Mapping

### File Operations

| Claude Code | Cline | Behavior Difference |
|-------------|-------|---------------------|
| `Read` | `read_file` | Identical |
| `Write` | `write_to_file` | Identical; creates or overwrites |
| `Edit` | `replace_in_file` | Both do search-and-replace, different syntax |
| `Grep` | `search_files` | Both regex-based; Cline adds `file_pattern` filter |
| `Glob` | `list_files` | Cline returns directory listing; less glob flexibility |

### Execution and Search

| Claude Code | Cline | Notes |
|-------------|-------|-------|
| `Bash` | `execute_command` | Functionally equivalent |
| `WebFetch` | `browser_action` or `use_mcp_tool` | `browser_action` uses Puppeteer; MCP = internal only |
| `WebSearch` | Not available | Remove; no external search |

### Interaction and Control

| Claude Code | Cline | Notes |
|-------------|-------|-------|
| `AskUserQuestion` | `ask_followup_question` | Functionally equivalent |
| `Task` | Not available | No sub-agent delegation in Cline |
| `Agent` (subagent_type) | Not available | No agent system |
| `TodoWrite` | Not available | No task list management |
| `NotebookEdit` | `write_to_file` | Write directly to notebook file |

### MCP Tools

| Claude Code | Cline | Constraint |
|-------------|-------|-----------|
| `mcp__context7__*` | Not available | External MCP; blocked on external network |
| `mcp__sequential-thinking__*` | Not available | External MCP; blocked |
| Custom MCP tools | `use_mcp_tool` | Internal network MCP only |

---

## 3. Directory Structure Mapping

### Path Transformation

| Claude Code | Cline | Notes |
|------------|-------|-------|
| `.claude/skills/{name}/` | `.cline/skills/{name}/` | Root path change |
| `SKILL.md` | `SKILL.md` | Keep name |
| `reference.md` | `docs/reference.md` | Move under docs/ |
| `examples.md` | `docs/examples.md` | Move under docs/ |
| `examples/` | `docs/examples/` | Move under docs/ |
| `modules/` | `docs/` | Flatten: each module file → docs/topic.md |
| `modules/INDEX.md` | Remove | Not needed in Cline |
| `references/` | `docs/` | Merge into docs/ |
| `scripts/` | `scripts/` | Keep as-is |
| `templates/` | `templates/` | Keep as-is |

### Module Flattening

Claude Code modules use a nested structure with an INDEX.md.
Cline docs/ is a flat reference directory.

```
# Claude Code (source)
SKILL.md → references modules/INDEX.md → modules/topic-a.md
                                        → modules/topic-b.md

# Cline (converted)
SKILL.md → docs/topic-a.md
         → docs/topic-b.md
```

Update SKILL.md references from `modules/INDEX.md` to direct `docs/topic-a.md` links.

---

## 4. Content Section Removal Guide

### Sections to Remove Completely

These MoAI-ADK/Claude Code-specific sections have no Cline equivalent:

- **TRUST 5 Framework**: Quality gates (Tested, Readable, Unified, Secured, Trackable)
- **SPEC Workflow**: /moai plan, /moai run, /moai sync references
- **@MX Tag Protocol**: @MX:NOTE, @MX:WARN, @MX:ANCHOR, @MX:TODO annotations
- **Agent Delegation**: Task(), subagent_type, TeamCreate, SendMessage patterns
- **Progressive Disclosure**: MoAI-specific token management explanations
- **Context7 Integration**: mcp__context7__resolve-library-id, get-library-docs
- **Hooks Configuration**: PreToolUse, PostToolUse, Stop event handlers
- **Model Selection**: model: claude-sonnet-4-6 or similar specifications
- **Works Well With (agents)**: manager-*, expert-*, builder-* agent references

### Sections to Keep and Adapt

| Section | Action |
|---------|--------|
| Core domain knowledge | Keep verbatim |
| Step-by-step workflows | Keep; replace agent delegation with direct instructions |
| Code examples | Keep; update tool names |
| Best practices | Keep |
| Constraints and rules | Keep; add Cline-specific constraints |
| External documentation links | Keep if links remain valid |

### Agent Delegation Rewrite Pattern

When a Claude Code skill delegates to an agent, rewrite as direct instructions:

```markdown
# Claude Code (remove this pattern)
Delegate to the expert-backend agent to:
- Analyze the API structure
- Generate FastAPI endpoints

# Cline (rewrite as direct steps)
To analyze and generate the API:
1. Use `read_file` to read existing route files
2. Use `search_files` to find endpoint patterns
3. Generate new endpoint code following the existing pattern
4. Use `write_to_file` to create the new route file
```

---

## 5. Description Writing Guide for Converted Skills

### Trigger Keyword Strategy

The description is the ONLY way Cline knows when to activate a skill.
Include keywords the user will actually type.

Structure template:
```
[Korean description of what the skill does.]
[English description or additional context.]
Activate on: [keyword1], [keyword2], [keyword3], [keyword4], [keyword5]
```

Keyword selection rules:
- Include 5-10 keywords minimum
- Mix Korean and English variants of the same concept
- Include specific technology names (FastAPI, PostgreSQL, etc.)
- Include action verbs users might type (생성, 분석, 변환, create, analyze, convert)

### Converting Claude Code Triggers

Claude Code uses a `triggers.keywords` YAML list. In Cline, embed these directly:

```yaml
# Claude Code source
triggers:
  keywords: ["Python", "FastAPI", "REST API", "backend"]
  agents: ["expert-backend"]
  phases: ["run"]

# Cline description (embed keywords, drop agent/phase info)
description: |
  FastAPI 기반 REST API를 설계하고 구현한다. 엔드포인트 생성,
  데이터 모델, 인증, 테스트를 포함한다.
  Activate on: FastAPI, Python API, REST API, 백엔드 개발, backend, endpoint
```

---

## 6. Common Conversion Patterns

### Pattern: Knowledge/Guide Skill

Easiest conversion. Core content needs minimal changes.

1. Strip frontmatter to just `name` and `description`
2. Change `>` to `|` in description
3. Add trigger keywords to description
4. Remove any @MX or SPEC sections
5. Update tool names in prose

### Pattern: Workflow Skill

Moderate conversion. Agent delegation must be rewritten.

1. Identify each delegation point
2. Rewrite as step-by-step direct instructions using Cline tools
3. Replace TodoWrite with numbered checklists
4. Keep the logical sequence; just change the executor (agent → direct action)

### Pattern: Domain Expertise Skill

Moderate conversion. Context7 MCP references must be removed.

1. Remove all `mcp__context7__*` tool calls
2. Replace "look up latest docs via Context7" with "refer to official documentation"
3. Embed relevant documentation snippets directly in the skill if needed
4. Update tool names

### Pattern: Integration/Platform Skill

Hard conversion. May have significant capability loss.

1. Identify which features depend on external MCP or hooks
2. Assess whether internal-network MCP can substitute
3. Document what is lost in the conversion report
4. Provide manual alternatives for any automated workflows

---

## 7. Validation Checklist (Detailed)

### Frontmatter Validation

- [ ] Exactly 2 `---` delimiters (opening and closing)
- [ ] `name:` field present and matches directory name
- [ ] `name` value is kebab-case (lowercase, hyphens only, no underscores)
- [ ] `name` is 64 characters or fewer
- [ ] `description:` field present and uses `|` literal block
- [ ] Description is 1024 characters or fewer
- [ ] No other frontmatter fields present

### Content Validation

- [ ] No Claude Code tool names (Read, Write, Edit, Grep, Glob, Bash)
- [ ] No agent delegation patterns (Task, subagent_type, TeamCreate)
- [ ] No @MX tag references
- [ ] No TRUST 5 or SPEC workflow references
- [ ] No external MCP tool calls (context7, sequential-thinking)
- [ ] No hooks configuration or references
- [ ] No model selection references
- [ ] File references use `docs/` not `modules/` or `references/`
- [ ] File references are one level deep only (no chained references)

### Size Validation

- [ ] SKILL.md is under ~400 lines (approximately 5,000 tokens)
- [ ] If over limit, advanced content is split to docs/ files
- [ ] Each docs/ file is self-contained (no cross-file chaining)

### Cline Constraint Validation

- [ ] No hooks-based automation
- [ ] MCP references marked as "internal network only" (사내망 전용)
- [ ] No references to external AI services or APIs

---

## 8. Quick Reference: Before/After Examples

### Frontmatter: Before and After

Before (Claude Code):
```yaml
---
name: moai-lang-python
description: >
  Python development specialist covering FastAPI, Django,
  data science, and testing patterns.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python:*), mcp__context7__resolve-library-id
user-invocable: false
metadata:
  version: "1.0.0"
  category: "language"
  status: "active"
  tags: "python, fastapi, django"
triggers:
  keywords: ["Python", "FastAPI", "Django", "pytest"]
  agents: ["expert-backend"]
  phases: ["run"]
---
```

After (Cline):
```yaml
---
name: moai-lang-python
description: |
  Python 개발 전문가. FastAPI, Django, 데이터 과학, 테스트 패턴을 다룬다.
  Activate on: Python, FastAPI, Django, pytest, 파이썬, 파이썬 개발,
  data science, 데이터 분석, backend, 백엔드
---
```

### Tool Reference: Before and After

Before (Claude Code):
```markdown
Use `Grep` to search for the pattern, then use `Read` to load the file.
After editing, use `Edit` to apply the changes.
```

After (Cline):
```markdown
Use `search_files` to search for the pattern, then use `read_file` to load the file.
After editing, use `replace_in_file` to apply the changes.
```
