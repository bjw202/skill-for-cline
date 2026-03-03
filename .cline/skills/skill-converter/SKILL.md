---
name: skill-converter
description: |
  범용 스킬을 사내 Cline 환경에 최적화된 형식으로 변환한다.
  Claude Code 스킬, 일반 마크다운 지침서, 외부 스킬을 검토하고 Cline 스킬로 변환한다.
  다음 키워드에서 활성화: 스킬 변환, 스킬 컨버팅, 스킬 포팅, 스킬 최적화,
  convert skill, port skill, migrate skill, skill conversion
---

# Cline 스킬 변환 전문가

## 핵심 임무

기존 스킬(Claude Code, 일반 마크다운 등)을 분석하고 사내 Cline 환경에 최적화된 스킬로 변환한다. 단순 포맷 변환이 아닌, Cline의 도구 체계와 사내 제약 사항을 반영한 실질적 최적화를 수행한다.

## 사내 제약 사항

- MCP 서버: 사내망 전용만 접속 가능
- Hooks: 사용 불가
- 외부 네트워크 MCP 도구 참조 제거 필요

---

## 변환 워크플로우

### 1단계: 원본 스킬 분석

원본 스킬을 읽고 다음을 파악한다:

- 스킬의 핵심 목적과 기능 범위
- 사용 중인 도구(Tool) 목록
- 프론트매터 필드 구성
- 외부 의존성 (MCP, hooks, 외부 API 등)
- Cline 비호환 요소 식별

### 2단계: 호환성 검토

Cline 호환 여부를 판단하고 변환 계획을 수립한다:

**자동 변환 가능 항목:**

- 프론트매터 필드 매핑
- 도구명 변환 (예: `Read` → `read_file`)
- 디렉토리 경로 변환 (예: `.claude/skills/` → `.cline/skills/`)
- 기본 구조 변환

**수동 검토 필요 항목:**

- 에이전트/서브에이전트 참조 (Cline에 없는 개념)
- 외부 MCP 서버 의존 기능
- Hooks 기반 자동화 로직
- 모델 지정 기능 (`model` 필드)
- 컨텍스트 포크 (`context: fork`)

**변환 불가 항목:**

- 외부 네트워크 MCP 도구 호출
- Hooks 자동화
- 에이전트 위임 체인

### 3단계: 변환 실행

**프론트매터 변환:**

```yaml
# 원본 (Claude Code)
---
name: example-skill
description: Example skill for code analysis
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
context: fork
agent: Explore
user-invocable: true
hooks:
  - event: PostToolUse
    script: validate.sh
---

# 변환 후 (Cline)
---
name: example-skill
description: |
  코드 분석을 수행한다. 파일 구조 탐색, 패턴 검색, 코드 리뷰를 지원한다.
  다음 키워드에서 활성화: 코드 분석, code analysis, 코드 리뷰
---
```

변환 규칙:
- `name`: 그대로 유지 (kebab-case 확인)
- `description`: 한국어로 재작성, 활성화 트리거 명시
- `allowed-tools`: 제거 (Cline은 프론트매터에서 도구 제한 미지원)
- `model`: 제거 (Cline은 프론트매터에서 모델 지정 미지원)
- `context`, `agent`: 제거 (Cline 미지원)
- `hooks`: 제거 (사내 제약)
- Cline 미지원 필드: 모두 제거

**도구명 변환 매핑:**

| Claude Code 도구 | Cline 도구 | 비고 |
|-----------------|-----------|------|
| `Read` | `read_file` | 동일 기능 |
| `Write` | `write_to_file` | 동일 기능 |
| `Edit` | `replace_in_file` | search/replace 방식 |
| `Grep` | `search_files` | 정규식 검색 |
| `Glob` | `list_files` | 파일 패턴 매칭 |
| `Bash` | `execute_command` | CLI 명령 실행 |
| `WebFetch` | `browser_action` 또는 `use_mcp_tool` | 사내망 MCP만 가능 |
| `WebSearch` | 변환 불가 | 외부 검색 미지원 |
| `Agent` / `Task` | 변환 불가 | 에이전트 개념 없음 |
| `AskUserQuestion` | `ask_followup_question` | 유사 기능 |
| `TodoWrite` | 변환 불가 | 해당 기능 없음 |
| `NotebookEdit` | `write_to_file` | 직접 파일 편집으로 대체 |

**디렉토리 구조 변환:**

| Claude Code | Cline |
|------------|-------|
| `.claude/skills/{name}/` | `.cline/skills/{name}/` |
| `SKILL.md` | `SKILL.md` (동일) |
| `reference.md` | `docs/reference.md` |
| `examples.md` / `examples/` | `docs/examples.md` |
| `modules/` | `docs/` (하위 파일로 이동) |
| `scripts/` | `scripts/` (동일) |
| `templates/` | `templates/` (동일) |

### 4단계: 최적화

변환 후 Cline 환경에 맞게 최적화한다:

**description 최적화:**
- 한국어로 재작성
- 구체적 활성화 트리거 키워드 추가
- 한국어 + 영어 키워드 병기

**콘텐츠 최적화:**
- 에이전트 위임 지시를 직접 실행 지시로 변환
- Claude Code 전용 개념 (프로그레시브 디스클로저, 에이전트 체계 등) 제거
- Cline 도구 체계에 맞는 지침으로 재작성
- 사내 제약 사항 반영

**토큰 최적화:**
- SKILL.md 5,000 토큰 이내 유지
- 과도한 설명 압축
- 필요 시 docs/로 분리

### 5단계: 검증

- YAML 프론트매터 유효성 확인
- name이 디렉토리명과 일치하는지 확인
- Cline 비호환 도구 참조가 남아있지 않은지 확인
- 사내 제약 위반 항목이 없는지 확인
- SKILL.md 토큰 제한 준수 확인

---

## 변환 판단 기준

모든 스킬을 무조건 변환하지 않는다. 다음 기준으로 판단한다:

**변환 권장:**
- 핵심 기능이 Cline 도구로 대체 가능한 경우
- 파일 조작, 코드 분석, 터미널 명령 중심 스킬
- 지식 기반 스킬 (가이드, 표준, 패턴)

**변환 주의:**
- 외부 MCP 의존도가 높은 경우 (기능 축소 필요)
- 에이전트 위임이 핵심 로직인 경우 (워크플로우 재설계 필요)
- Hooks 자동화가 필수인 경우 (대안 설계 필요)

**변환 비권장:**
- 핵심 기능이 Cline 미지원 기능에 전적으로 의존하는 경우
- 변환 시 원본 가치의 50% 이상이 손실되는 경우

변환 비권장으로 판단된 경우, 사용자에게 이유를 설명하고 대안을 제시한다.

---

## 변환 보고서 형식

변환 완료 후 다음 형식으로 보고한다:

```markdown
## 스킬 변환 보고서

### 원본 정보
- 원본 형식: [Claude Code / 일반 마크다운 / 기타]
- 원본 위치: [파일 경로]

### 변환 결과
- 변환 위치: .cline/skills/{name}/
- 파일 목록: [생성된 파일 나열]

### 변환 내역
- 프론트매터: [변환된 필드 목록]
- 도구 매핑: [변환된 도구 목록]
- 제거 항목: [Cline 미지원으로 제거된 기능]

### 최적화 사항
- [적용된 최적화 내역]

### 주의 사항
- [기능 축소/변경 사항]
- [사용자 확인 필요 항목]
```

---

## 상세 매핑 문서

프론트매터 필드별 상세 변환 규칙과 도구 매핑 가이드는 `docs/conversion-mapping.md`를 참조한다.
