# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.1.0] - 2026-02-27

### Changed (SPEC-CLINE-001: Cline Skills Quality Improvement)

#### Module 1: docs/ Reference Format Fix
- Fixed all `docs/` file references from backtick format to markdown link format in 3 SKILL.md files
- Fixed template files: advanced-skill.md, agentic-skill-template.md, converted-skill.md
- Added "Referencing docs/ Files from SKILL.md" section to cline-standards.md documenting the correct format
- Added docs/ reference format validation to skill-builder checklist (item 11)

#### Module 2: scripts/ Directory Integration
- Added scripts/ directory option to skill-builder PLAN output template
- Strengthened agent-builder Phase 4 scripts/ creation guidance with token efficiency explanation
- Added "When to Use scripts/" subsection to cline-standards.md
- Created validate-skill.sh utility script in skill-builder/scripts/

#### Module 3: skill-builder Template Improvements
- Updated PLAN output directory structure to include `[scripts/[script].sh|.py <- 반복 작업 자동화 시]`
- Added scripts/ existence check to validation checklist (item 12)
- Updated validation report from 9/9 to 12/12 items

#### Module 4: description Field Compliance
- Updated skill-builder description: now starts with "Design and create..."
- Updated skill-converter description: now starts with "Convert Claude Code..."
- Updated agent-builder description: now starts with "Build agentic..."
- Added "액션 동사 시작 요구사항" section to description-writing.md with examples
- Added description action verb validation to skill-builder checklist

### Added
- `.cline/skills/skill-builder/scripts/validate-skill.sh` - SKILL.md format validation script
- SPEC-CLINE-001 documents in `.moai/specs/SPEC-CLINE-001/`

### Known Limitations
- skill-converter/SKILL.md is 304 lines (4 over 300-line limit) - deferred to next SPEC

## [1.0.0] - 2026-02-27

### Added
- Initial Cline skills: skill-builder, skill-converter, agent-builder
- Sample skills in samples-claude-skills/
- MoAI project configuration (.moai/)
