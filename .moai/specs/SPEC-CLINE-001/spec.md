---
id: SPEC-CLINE-001
title: "Cline Skills Quality Improvement"
version: "1.0.0"
status: completed
created: "2026-02-27"
updated: "2026-02-27"
author: jw
priority: high
tags: [cline, skills, quality, docs-reference, scripts, description]
---

# SPEC-CLINE-001: Cline 스킬 품질 개선

## 1. 환경 (Environment)

### 1.1 프로젝트 컨텍스트

- **프로젝트명**: 슬기로운 코워크 생활
- **목적**: Claude Code와 Cline 양쪽에서 동작하는 한국어 비즈니스 AI 어시스턴트 플러그인
- **대상 디렉토리**: `.cline/skills/` (3개 빌더/컨버터 스킬)
- **영향 받는 스킬**:
  - `skill-builder` - 새로운 Cline 스킬 생성 도구
  - `skill-converter` - Claude Code/MoAI 스킬을 Cline 형식으로 변환하는 도구
  - `agent-builder` - 에이전틱 스킬 패키지 제작 도구

### 1.2 기술 환경

- **플랫폼**: Cline (VS Code 확장)
- **스킬 표준**: Cline 공식 스킬 스펙 (docs.cline.bot)
- **프론트매터 필드**: `name` (kebab-case), `description` (최대 1024자)
- **SKILL.md 권장 크기**: ~5K 토큰 / 200-300줄
- **docs/ 참조 형식**: 마크다운 링크 `[file.md](docs/file.md)`
- **scripts/ 특성**: 출력만 컨텍스트에 진입 (소스 코드는 제외되어 토큰 효율적)

### 1.3 공식 Cline 규칙 (docs.cline.bot 기준)

1. 디렉토리 이름은 `name` 필드와 정확히 일치해야 함 (kebab-case)
2. 프론트매터 필드는 `name`과 `description` 두 개만 허용
3. `description`은 최대 1024자
4. SKILL.md 본문은 ~5K 토큰 / 200-300줄 권장
5. docs/ 파일 참조는 마크다운 링크 형식: `[file.md](docs/file.md)`
6. scripts/ 출력만 컨텍스트에 진입 (소스 코드가 아닌 실행 결과만 포함되어 토큰 효율적)
7. 저장 경로: `.cline/skills/`, `.clinerules/skills/`, `.claude/skills/`
8. 동일 이름의 글로벌 스킬이 프로젝트 스킬보다 우선

---

## 2. 가정 (Assumptions)

### 2.1 기술적 가정

- **A1**: Cline은 SKILL.md에서 마크다운 링크 형식(`[file.md](docs/file.md)`)을 감지하여 docs/ 파일을 자동 로드한다
  - 신뢰도: Medium
  - 근거: 공식 문서에서 "Referencing docs/ files from SKILL.md" 예시가 마크다운 링크 형식을 사용
  - 틀릴 경우의 위험: 백틱 형식도 동작한다면 수정 불필요, 하지만 공식 표준을 따르는 것이 안전
  - 검증 방법: 양쪽 형식으로 테스트하여 docs/ 파일 로딩 여부 확인

- **A2**: scripts/ 디렉토리의 스크립트 실행 시 소스 코드가 아닌 stdout 출력만 컨텍스트에 포함된다
  - 신뢰도: High
  - 근거: 공식 문서 명시 ("only output enters context, not source code")
  - 틀릴 경우의 위험: 토큰 효율성 주장이 무효화
  - 검증 방법: scripts/ 디렉토리에 테스트 스크립트 추가 후 컨텍스트 크기 비교

- **A3**: description 필드에서 액션 동사로 시작하면 스킬 트리거 효과가 향상된다
  - 신뢰도: Medium
  - 근거: 공식 문서 "Start with action verbs" 권장 및 예시 (Deploy, Generate 등)
  - 틀릴 경우의 위험: 트리거 효과 무관하더라도 공식 표준 준수는 가치 있음

### 2.2 운영 가정

- **A4**: 3개 스킬 모두 동일한 패턴으로 수정 가능하며 각 스킬의 고유 구조는 보존해야 한다
- **A5**: 기존 스킬 사용자(이 도구로 스킬을 이미 만든 사용자)에게 호환성 영향 없음
- **A6**: cline-standards.md는 모든 빌더 스킬이 참조하는 공유 표준 문서이다

---

## 3. 요구사항 (Requirements)

### Module 1: docs/ 참조 형식 수정 [CRITICAL]

**REQ-1.1** (Ubiquitous)
시스템은 **항상** docs/ 파일 참조에 마크다운 링크 형식 `[filename.md](docs/filename.md)`을 사용해야 한다.

**REQ-1.2** (Event-Driven)
**WHEN** skill-builder가 새 스킬을 생성할 때, **THEN** 생성된 SKILL.md의 docs/ 참조는 반드시 마크다운 링크 형식이어야 한다.

**REQ-1.3** (Event-Driven)
**WHEN** skill-converter가 Claude Code 스킬을 변환할 때, **THEN** 변환된 SKILL.md의 docs/ 참조는 반드시 마크다운 링크 형식이어야 한다.

**REQ-1.4** (Unwanted)
시스템은 docs/ 파일 참조에 백틱 코드 형식(`` `docs/file.md` ``)을 **사용하지 않아야 한다**.

**REQ-1.5** (Event-Driven)
**WHEN** cline-standards.md가 참조될 때, **THEN** docs/ 파일 참조 형식에 대한 명확한 규칙이 마크다운 링크 형식으로 문서화되어 있어야 한다.

**REQ-1.6** (Event-Driven)
**WHEN** skill-builder의 검증 체크리스트가 실행될 때, **THEN** docs/ 참조가 마크다운 링크 형식인지 검증해야 한다.

### Module 2: scripts/ 디렉토리 통합 [IMPORTANT]

**REQ-2.1** (Event-Driven)
**WHEN** skill-builder가 PLAN 출력을 생성할 때, **THEN** 파일 구조에 scripts/ 디렉토리가 포함되어야 한다.

**REQ-2.2** (State-Driven)
**IF** 스킬이 반복적 분석 작업(스캔, 카운트, 검증 등)을 수행해야 하는 경우, **THEN** scripts/ 디렉토리에 자동화 스크립트를 생성해야 한다.

**REQ-2.3** (Event-Driven)
**WHEN** agent-builder가 분석 태스크를 식별할 때, **THEN** 해당 태스크를 위한 scripts/를 실제로 생성해야 한다.

**REQ-2.4** (Event-Driven)
**WHEN** cline-standards.md가 참조될 때, **THEN** scripts/ 디렉토리의 토큰 효율성 특성에 대한 문서가 포함되어 있어야 한다.

**REQ-2.5** (Optional)
**가능하면** skill-builder 자체에도 유틸리티 스크립트(예: scan-skills.sh, count-chars.py)를 제공해야 한다.

### Module 3: skill-builder 템플릿 개선 [IMPORTANT]

**REQ-3.1** (Event-Driven)
**WHEN** skill-builder가 PLAN 형식을 출력할 때, **THEN** 파일 구조에 `scripts/` 디렉토리가 선택 항목으로 포함되어야 한다.

**REQ-3.2** (Event-Driven)
**WHEN** skill-builder의 검증 체크리스트가 실행될 때, **THEN** 자동화가 관련된 경우 scripts/ 존재 여부를 확인해야 한다.

**REQ-3.3** (State-Driven)
**IF** 스킬이 인라인 명령어 대신 스크립트로 처리 가능한 작업을 포함하는 경우, **THEN** scripts/ 사용을 권장하는 가이드가 제공되어야 한다.

**REQ-3.4** (Event-Driven)
**WHEN** skill-builder의 PLAN 출력에 디렉토리 구조가 표시될 때, **THEN** 다음 형식이어야 한다:
```
.cline/skills/[name]/
  SKILL.md
  [docs/[guide].md]
  [templates/[tmpl].md]
  [scripts/[script].sh|.py]
```

### Module 4: description 필드 준수 [MEDIUM]

**REQ-4.1** (Ubiquitous)
시스템의 모든 스킬 description 필드는 **항상** 액션 동사로 시작해야 한다.

**REQ-4.2** (Event-Driven)
**WHEN** skill-builder가 새 스킬의 description을 생성할 때, **THEN** 해당 description은 액션 동사로 시작해야 한다.

**REQ-4.3** (Event-Driven)
**WHEN** description-writing.md가 참조될 때, **THEN** 액션 동사 시작 요구사항이 예시와 함께 명확히 문서화되어 있어야 한다.

**REQ-4.4** (Event-Driven)
**WHEN** skill-builder의 검증 체크리스트가 실행될 때, **THEN** description 필드의 액션 동사 시작 여부를 확인해야 한다.

---

## 4. 명세 (Specifications)

### 4.1 수정 대상 파일 목록

| Module | 파일 경로 | 수정 유형 |
|--------|-----------|-----------|
| M1 | `.cline/skills/skill-builder/SKILL.md` | docs/ 참조 형식 수정 |
| M1 | `.cline/skills/skill-converter/SKILL.md` | docs/ 참조 형식 수정 |
| M1 | `.cline/skills/agent-builder/SKILL.md` | docs/ 참조 형식 수정 |
| M1 | `.cline/skills/skill-builder/docs/cline-standards.md` | docs/ 참조 형식 규칙 추가 |
| M2 | `.cline/skills/skill-builder/SKILL.md` | PLAN 출력 구조에 scripts/ 추가 |
| M2 | `.cline/skills/agent-builder/SKILL.md` | scripts/ 실제 생성 로직 추가 |
| M2 | `.cline/skills/skill-builder/docs/cline-standards.md` | scripts/ 토큰 효율성 문서화 |
| M2 | `.cline/skills/skill-builder/scripts/` | (신규) 유틸리티 스크립트 생성 |
| M3 | `.cline/skills/skill-builder/SKILL.md` | PLAN 형식, 검증 체크리스트 업데이트 |
| M4 | `.cline/skills/skill-builder/SKILL.md` | description 필드 수정 |
| M4 | `.cline/skills/skill-converter/SKILL.md` | description 필드 수정 |
| M4 | `.cline/skills/agent-builder/SKILL.md` | description 필드 수정 |
| M4 | `.cline/skills/skill-builder/docs/description-writing.md` | 액션 동사 요구사항 강화 |

### 4.2 참조 형식 변경 예시

**Before (현재 - 잘못된 형식)**:
```
자세한 가이드는 `docs/interview-guide.md` 참조
```

**After (수정 후 - 올바른 형식)**:
```
자세한 가이드는 [interview-guide.md](docs/interview-guide.md) 참조
```

### 4.3 description 변경 예시

**Before (현재)**:
```yaml
description: "Cline 스킬 생성 전문가 / Cline skill creation specialist. Designs..."
```

**After (수정 후)**:
```yaml
description: "Design and create Cline skills with official standards compliance..."
```

또는 한국어:
```yaml
description: "Cline 공식 표준에 맞춰 스킬을 설계하고 생성합니다..."
```

### 4.4 PLAN 출력 디렉토리 구조 변경

**Before**:
```
.cline/skills/[name]/
  SKILL.md
  [docs/[guide].md  <- 복잡한 스킬만]
  [templates/[tmpl].md  <- 필요시]
```

**After**:
```
.cline/skills/[name]/
  SKILL.md
  [docs/[guide].md  <- 복잡한 스킬만]
  [templates/[tmpl].md  <- 필요시]
  [scripts/[script].sh|.py  <- 반복 작업 자동화시]
```

### 4.5 제약사항

- **C1**: SKILL.md는 200-300줄 (~5K 토큰) 제한을 초과하지 않아야 함
- **C2**: 프론트매터에는 `name`과 `description` 두 필드만 사용
- **C3**: description은 1024자를 초과하지 않아야 함
- **C4**: 기존 스킬 사용자의 호환성을 유지해야 함
- **C5**: 한국어와 영어 이중 언어 지원을 유지해야 함

### 4.6 추적성 (Traceability)

| 요구사항 | 대상 파일 | 검증 방법 |
|----------|-----------|-----------|
| REQ-1.1~1.4 | 3개 SKILL.md | Grep으로 백틱 참조 부재 확인 |
| REQ-1.5 | cline-standards.md | docs/ 참조 규칙 섹션 존재 확인 |
| REQ-1.6 | skill-builder/SKILL.md | 체크리스트에 형식 검증 항목 확인 |
| REQ-2.1~2.4 | 각 대상 파일 | scripts/ 관련 내용 존재 확인 |
| REQ-2.5 | skill-builder/scripts/ | 유틸리티 스크립트 파일 존재 확인 |
| REQ-3.1~3.4 | skill-builder/SKILL.md | PLAN 형식, 체크리스트 확인 |
| REQ-4.1~4.4 | 3개 SKILL.md, description-writing.md | description 시작 문자 패턴 확인 |

---

## 5. 전문가 협의 권장사항

이 SPEC의 요구사항은 주로 문서 및 설정 수정이므로 별도의 전문가 에이전트 협의 없이 구현 가능합니다. 단, 다음 경우 협의를 권장합니다:

- **expert-frontend**: Cline 확장 동작에 대한 심층 분석이 필요한 경우 (docs/ 파일 로딩 메커니즘 확인)
- **expert-testing**: scripts/ 디렉토리 유틸리티 스크립트의 테스트 전략 수립 시

---

## 6. Implementation Notes

**완료일**: 2026-02-27
**상태**: completed

### 실제 수정된 파일 목록

1. `.cline/skills/skill-builder/SKILL.md` - description 액션 동사 수정 + PLAN 템플릿 scripts/ 추가 + 체크리스트 항목 11, 12 추가
2. `.cline/skills/skill-converter/SKILL.md` - description 액션 동사 수정 + 8개 docs/ 백틱 참조 마크다운 링크로 변환
3. `.cline/skills/agent-builder/SKILL.md` - description 액션 동사 수정 + 6개 docs/ 백틱 참조 변환 + scripts/ 생성 로직 추가
4. `.cline/skills/skill-builder/docs/cline-standards.md` - "Referencing docs/ Files" 섹션 추가 + "When to Use scripts/" 섹션 추가
5. `.cline/skills/skill-builder/docs/description-writing.md` - "액션 동사 시작 요구사항" 섹션 추가
6. `.cline/skills/skill-builder/scripts/validate-skill.sh` - 신규 생성 (SKILL.md 검증 스크립트)
7. `.cline/skills/skill-builder/templates/advanced-skill.md` - 4개 백틱 참조 수정
8. `.cline/skills/agent-builder/templates/agentic-skill-template.md` - 2개 백틱 참조 수정
9. `.cline/skills/skill-converter/templates/converted-skill.md` - 1개 백틱 참조 수정

### 범위 변경 사항

원래 계획에 없던 템플릿 파일 수정이 추가 수행됨 (보너스 범위):
- `skill-builder/templates/advanced-skill.md`
- `agent-builder/templates/agentic-skill-template.md`
- `skill-converter/templates/converted-skill.md`

이 파일들에서도 동일한 백틱 참조 패턴이 발견되어 일관성을 위해 함께 수정.

### 이연된 항목

- **skill-converter/SKILL.md 줄 수 감소**: 304줄로 300줄 제한 4줄 초과
  - 원인: 상세한 변환 패턴 문서화로 인한 분량
  - 결정: 별도 SPEC으로 처리 예정 (콘텐츠 품질 유지 우선)
  - 다음 SPEC: skill-converter 최적화 (줄 수 감소)
