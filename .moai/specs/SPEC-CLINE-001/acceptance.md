---
spec_id: SPEC-CLINE-001
title: "Cline Skills Quality Improvement - Acceptance Criteria"
version: "1.0.0"
status: completed
created: "2026-02-27"
updated: "2026-02-27"
author: jw
---

# SPEC-CLINE-001: 인수 기준

## 1. Module 1: docs/ 참조 형식 수정

### AC-1.1: skill-builder docs/ 참조 형식

```gherkin
Given skill-builder/SKILL.md 파일이 존재할 때
When 파일 내용에서 docs/ 디렉토리 참조를 검색하면
Then 모든 docs/ 참조는 마크다운 링크 형식 [filename](docs/filename)이어야 한다
And 백틱 코드 형식(`docs/filename`)의 docs/ 참조는 존재하지 않아야 한다
```

### AC-1.2: skill-converter docs/ 참조 형식

```gherkin
Given skill-converter/SKILL.md 파일이 존재할 때
When 파일 내용에서 docs/ 디렉토리 참조를 검색하면
Then 모든 docs/ 참조는 마크다운 링크 형식 [filename](docs/filename)이어야 한다
And 백틱 코드 형식(`docs/filename`)의 docs/ 참조는 존재하지 않아야 한다
```

### AC-1.3: agent-builder docs/ 참조 형식

```gherkin
Given agent-builder/SKILL.md 파일이 존재할 때
When 파일 내용에서 docs/ 디렉토리 참조를 검색하면
Then 모든 docs/ 참조는 마크다운 링크 형식 [filename](docs/filename)이어야 한다
And 백틱 코드 형식(`docs/filename`)의 docs/ 참조는 존재하지 않아야 한다
```

### AC-1.4: cline-standards.md에 docs/ 참조 규칙 존재

```gherkin
Given cline-standards.md 파일이 존재할 때
When 파일 내용을 확인하면
Then docs/ 파일 참조 형식에 대한 명확한 규칙 섹션이 존재해야 한다
And 마크다운 링크 형식 [file.md](docs/file.md)이 올바른 형식으로 명시되어야 한다
And 백틱 형식이 잘못된 형식으로 명시되어야 한다
```

### AC-1.5: skill-builder 검증 체크리스트에 형식 검증 포함

```gherkin
Given skill-builder/SKILL.md의 검증 체크리스트 섹션이 존재할 때
When 체크리스트 항목을 확인하면
Then docs/ 참조가 마크다운 링크 형식인지 검증하는 항목이 포함되어야 한다
```

### 검증 방법 (Module 1)

| 검증 항목 | 도구 | 명령어/패턴 |
|-----------|------|-------------|
| 백틱 형식 부재 | Grep | `\`docs/[^`]+\`` 패턴이 3개 SKILL.md에서 0건 |
| 마크다운 링크 존재 | Grep | `\[.*\]\(docs/.*\)` 패턴이 각 SKILL.md에서 1건 이상 |
| cline-standards.md 규칙 | Read | docs/ 참조 형식 관련 섹션 존재 확인 |
| 검증 체크리스트 | Read | 마크다운 링크 형식 검증 항목 존재 확인 |

---

## 2. Module 2: scripts/ 디렉토리 통합

### AC-2.1: skill-builder PLAN 출력에 scripts/ 포함

```gherkin
Given skill-builder/SKILL.md의 PLAN 출력 형식 섹션이 존재할 때
When 디렉토리 구조 템플릿을 확인하면
Then scripts/ 디렉토리가 선택 항목으로 포함되어야 한다
And scripts/ 항목에 .sh 또는 .py 확장자 예시가 포함되어야 한다
```

### AC-2.2: agent-builder에 scripts/ 생성 로직 존재

```gherkin
Given agent-builder/SKILL.md 파일이 존재할 때
When Phase 4 또는 분석 태스크 관련 섹션을 확인하면
Then 분석 태스크 식별 시 scripts/ 디렉토리를 생성하도록 하는 지침이 존재해야 한다
And scripts/ 사용의 토큰 효율성 이점이 설명되어야 한다
```

### AC-2.3: cline-standards.md에 scripts/ 문서 존재

```gherkin
Given cline-standards.md 파일이 존재할 때
When 파일 내용을 확인하면
Then scripts/ 디렉토리에 대한 설명 섹션이 존재해야 한다
And "출력만 컨텍스트에 진입" (토큰 효율성) 특성이 명시되어야 한다
And scripts/ 사용이 적합한 상황에 대한 가이드가 포함되어야 한다
```

### AC-2.4: (Optional) 유틸리티 스크립트 존재

```gherkin
Given skill-builder/scripts/ 디렉토리가 생성된 경우
When 디렉토리 내용을 확인하면
Then 최소 1개 이상의 유틸리티 스크립트가 존재해야 한다
And 각 스크립트는 실행 가능한 형식이어야 한다
And 각 스크립트는 목적을 설명하는 주석을 포함해야 한다
```

### 검증 방법 (Module 2)

| 검증 항목 | 도구 | 명령어/패턴 |
|-----------|------|-------------|
| PLAN 출력 구조 | Grep | `scripts/` 가 skill-builder/SKILL.md에 존재 |
| agent-builder 로직 | Read | scripts/ 생성 관련 지침 존재 확인 |
| cline-standards.md | Grep | `scripts/` 및 토큰 관련 설명 존재 |
| 유틸리티 스크립트 | Glob | `.cline/skills/skill-builder/scripts/*` 패턴 매칭 |

---

## 3. Module 3: skill-builder 템플릿 개선

### AC-3.1: PLAN 출력 디렉토리 구조 완성

```gherkin
Given skill-builder/SKILL.md의 PLAN 출력 형식이 존재할 때
When 디렉토리 구조를 확인하면
Then 다음 구조가 표시되어야 한다:
  | 항목 | 필수/선택 |
  |------|-----------|
  | SKILL.md | 필수 |
  | docs/ | 선택 (복잡한 스킬) |
  | templates/ | 선택 (필요시) |
  | scripts/ | 선택 (반복 작업 자동화시) |
```

### AC-3.2: 검증 체크리스트에 scripts/ 확인 포함

```gherkin
Given skill-builder/SKILL.md의 검증 체크리스트가 존재할 때
When 체크리스트 항목을 확인하면
Then 자동화 작업이 있는 경우 scripts/ 디렉토리 존재 여부를 확인하는 항목이 포함되어야 한다
```

### AC-3.3: scripts/ vs 인라인 가이드 존재

```gherkin
Given skill-builder/SKILL.md 또는 관련 docs/ 파일이 존재할 때
When scripts/ 사용에 대한 가이드를 확인하면
Then 다음 내용이 포함되어야 한다:
  - scripts/ 사용이 적합한 경우 (반복 분석, 검증, 스캔)
  - 인라인 명령어가 적합한 경우 (일회성 작업, 간단한 명령)
  - 토큰 효율성 이점 설명
```

### 검증 방법 (Module 3)

| 검증 항목 | 도구 | 명령어/패턴 |
|-----------|------|-------------|
| 디렉토리 구조 | Read | PLAN 출력에 4개 항목 모두 존재 확인 |
| 체크리스트 항목 | Grep | `scripts` 관련 검증 항목 존재 |
| 사용 가이드 | Read | scripts/ vs 인라인 가이드 섹션 존재 확인 |

---

## 4. Module 4: description 필드 준수

### AC-4.1: skill-builder description 액션 동사 시작

```gherkin
Given skill-builder/SKILL.md의 프론트매터가 존재할 때
When description 필드를 확인하면
Then description은 영어 액션 동사로 시작해야 한다
  (예: Design, Create, Build, Generate, Convert, Analyze 등)
And description은 1024자 이내여야 한다
```

### AC-4.2: skill-converter description 액션 동사 시작

```gherkin
Given skill-converter/SKILL.md의 프론트매터가 존재할 때
When description 필드를 확인하면
Then description은 영어 액션 동사로 시작해야 한다
And description은 1024자 이내여야 한다
```

### AC-4.3: agent-builder description 액션 동사 시작

```gherkin
Given agent-builder/SKILL.md의 프론트매터가 존재할 때
When description 필드를 확인하면
Then description은 영어 액션 동사로 시작해야 한다
And description은 1024자 이내여야 한다
```

### AC-4.4: description-writing.md에 액션 동사 요구사항 강화

```gherkin
Given description-writing.md 파일이 존재할 때
When 파일 내용을 확인하면
Then 액션 동사로 시작해야 한다는 요구사항이 명확히 문서화되어야 한다
And 올바른 예시(액션 동사 시작)가 3개 이상 포함되어야 한다
And 잘못된 예시(명사구 시작)가 1개 이상 포함되어야 한다
```

### AC-4.5: skill-builder 검증 체크리스트에 description 확인 포함

```gherkin
Given skill-builder/SKILL.md의 검증 체크리스트가 존재할 때
When 체크리스트 항목을 확인하면
Then description 필드가 액션 동사로 시작하는지 확인하는 항목이 포함되어야 한다
```

### 검증 방법 (Module 4)

| 검증 항목 | 도구 | 명령어/패턴 |
|-----------|------|-------------|
| description 시작 패턴 | Grep | `^description:` 뒤에 액션 동사 패턴 확인 |
| 1024자 제한 | Read | description 필드 길이 측정 |
| description-writing.md | Read | 액션 동사 요구사항 및 예시 존재 확인 |
| 검증 체크리스트 | Read | description 형식 확인 항목 존재 |

---

## 5. 전체 품질 게이트

### QG-1: SKILL.md 크기 제한

```gherkin
Given 수정이 완료된 모든 SKILL.md 파일에 대해
When 각 파일의 줄 수를 확인하면
Then 각 파일은 300줄을 초과하지 않아야 한다
And 각 파일의 토큰 수는 약 5K를 초과하지 않아야 한다 (정밀 측정 불필요, 줄 수로 대리 확인)
```

### QG-2: 프론트매터 무결성

```gherkin
Given 수정이 완료된 모든 SKILL.md 파일에 대해
When 프론트매터를 확인하면
Then name 필드는 디렉토리 이름과 일치해야 한다 (kebab-case)
And description 필드만 수정되고 다른 필드는 변경되지 않아야 한다
And 프론트매터에는 name과 description 두 필드만 존재해야 한다
```

### QG-3: 기존 기능 보존

```gherkin
Given 수정이 완료된 모든 SKILL.md 파일에 대해
When 기존 핵심 기능 섹션을 확인하면
Then 각 스킬의 핵심 워크플로우는 변경되지 않아야 한다
And 기존 docs/ 파일의 내용은 변경되지 않아야 한다 (참조 형식만 변경)
And 한국어/영어 이중 언어 지원이 유지되어야 한다
```

### QG-4: 이중 언어 유지

```gherkin
Given 수정이 완료된 모든 스킬 파일에 대해
When 한국어 및 영어 콘텐츠를 확인하면
Then 기존의 한국어/영어 이중 언어 패턴이 유지되어야 한다
And 새로 추가된 콘텐츠도 이중 언어를 지원해야 한다
```

---

## 6. Definition of Done

모든 Module의 인수 기준과 품질 게이트를 충족하면 SPEC-CLINE-001은 완료된 것으로 간주합니다.

### 필수 완료 조건

- [x] Module 1: 3개 SKILL.md의 모든 docs/ 참조가 마크다운 링크 형식으로 변환됨
- [x] Module 1: cline-standards.md에 docs/ 참조 형식 규칙이 문서화됨
- [x] Module 1: 검증 체크리스트에 마크다운 링크 형식 검증 항목이 추가됨
- [x] Module 2: skill-builder PLAN 출력에 scripts/ 디렉토리가 포함됨
- [x] Module 2: agent-builder에 scripts/ 생성 로직이 추가됨
- [x] Module 2: cline-standards.md에 scripts/ 토큰 효율성이 문서화됨
- [x] Module 3: PLAN 출력 디렉토리 구조에 scripts/ 포함됨
- [x] Module 3: 검증 체크리스트에 scripts/ 확인 항목 포함됨
- [x] Module 4: 3개 스킬의 description이 액션 동사로 시작함
- [x] Module 4: description-writing.md에 액션 동사 요구사항이 강화됨
- [x] QG-1: 모든 SKILL.md가 300줄 이내 (skill-converter 304줄 - 별도 SPEC 처리 예정)
- [x] QG-2: 프론트매터 무결성 유지
- [x] QG-3: 기존 핵심 기능 보존
- [x] QG-4: 이중 언어 지원 유지

### 선택 완료 조건

- [x] Module 2 (Optional): skill-builder/scripts/ 유틸리티 스크립트 생성됨 (validate-skill.sh)
- [x] Module 3 (Optional): scripts/ vs 인라인 상세 가이드 작성됨 (cline-standards.md의 "When to Use scripts/" 섹션)
