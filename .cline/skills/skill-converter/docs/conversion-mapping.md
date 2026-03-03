# 스킬 변환 상세 매핑 가이드

이 문서는 다양한 형식의 스킬을 Cline 스킬로 변환할 때 참고하는 상세 매핑 레퍼런스이다.

---

## 1. 프론트매터 필드 매핑

### Claude Code → Cline 프론트매터 변환표

| Claude Code 필드 | Cline 변환 | 처리 방법 |
|-----------------|-----------|----------|
| `name` | `name` | 그대로 유지, kebab-case 확인 |
| `description` | `description` | 한국어로 재작성, 트리거 키워드 추가 |
| `allowed-tools` | 제거 | Cline 프론트매터 미지원 |
| `model` | 제거 | Cline 프론트매터 미지원 |
| `context` | 제거 | Cline에 fork 컨텍스트 개념 없음 |
| `agent` | 제거 | Cline에 에이전트 타입 개념 없음 |
| `hooks` | 제거 | 사내 제약: hooks 미사용 |
| `user-invocable` | 제거 | Cline은 모든 스킬이 사용자/AI 호출 가능 |
| `disable-model-invocation` | 제거 | Cline 미지원 |
| `argument-hint` | 제거 | Cline 미지원 |

---

## 2. 도구(Tool) 변환 상세 매핑

### 파일 조작 도구

| Claude Code | Cline | 변환 시 주의사항 |
|------------|-------|---------------|
| `Read` | `read_file` | 파라미터명 변경: `file_path` → `path` |
| `Write` | `write_to_file` | 파라미터명 변경: `file_path` → `path`, `content` 동일 |
| `Edit` | `replace_in_file` | 동작 방식 차이: Claude는 old_string/new_string, Cline은 search/replace 블록 |
| `MultiEdit` | `replace_in_file` 반복 | Cline은 다중 편집 도구 없음, 순차 호출로 대체 |
| `NotebookEdit` | `write_to_file` | Jupyter 전용 편집 없음, 파일 직접 수정으로 대체 |

### 검색/탐색 도구

| Claude Code | Cline | 변환 시 주의사항 |
|------------|-------|---------------|
| `Grep` | `search_files` | 파라미터 차이: `pattern` → `regex`, `glob` → `file_pattern` |
| `Glob` | `list_files` | Cline은 glob 패턴 미지원, 경로 기반 나열만 가능 |
| `WebSearch` | 변환 불가 | 외부 웹 검색 미지원, 사내 MCP 대안 검토 |
| `WebFetch` | `use_mcp_tool` 또는 `browser_action` | 사내망 URL만 가능, 외부 URL 접근 불가 |

### 실행/제어 도구

| Claude Code | Cline | 변환 시 주의사항 |
|------------|-------|---------------|
| `Bash` | `execute_command` | 파라미터: `command` 동일, Cline은 `requires_approval` 추가 |
| `Agent` / `Task` | 변환 불가 | 에이전트 위임 없음, 직접 실행 지시로 재작성 |
| `TodoWrite` | 변환 불가 | 작업 목록 도구 없음, 본문에서 단계별 목록으로 대체 |
| `TaskCreate/Update/List/Get` | 변환 불가 | 작업 관리 도구 없음 |

### 대화/완료 도구

| Claude Code | Cline | 변환 시 주의사항 |
|------------|-------|---------------|
| `AskUserQuestion` | `ask_followup_question` | 유사 기능, 파라미터 구조 다름 |
| `EnterPlanMode` | 변환 불가 | 계획 모드 없음, 워크플로우로 대체 가능 |
| `ExitPlanMode` | 변환 불가 | 계획 모드 없음 |
| `Skill` | 변환 불가 | 스킬 호출 도구 없음 (description 기반 자동 활성화) |

### MCP 도구

| Claude Code | Cline | 변환 시 주의사항 |
|------------|-------|---------------|
| 외부 MCP 도구 | `use_mcp_tool` | 사내망에 해당 MCP 서버 있을 경우만 가능 |
| 기타 외부 MCP | 제거 | 사내망 전용 제약 |

---

## 3. 디렉토리 구조 변환 상세

### Claude Code 구조 → Cline 구조

```
# Claude Code 원본
.claude/skills/custom-example/
  SKILL.md                    # 메인 스킬 (500줄 제한)
  reference.md                # 상세 레퍼런스
  examples.md                 # 코드 예제
  modules/                    # 모듈화된 주제별 가이드
    topic-a.md
    topic-b.md
  scripts/
    validate.sh
  templates/
    config-template.json

# Cline 변환 후
.cline/skills/custom-example/
  SKILL.md                    # 메인 스킬 (5,000 토큰 제한)
  docs/                       # 모든 문서 통합
    reference.md              # 상세 레퍼런스
    examples.md               # 코드 예제
    topic-a.md                # modules/ 내용 이동
    topic-b.md
  scripts/
    validate.sh               # 그대로 유지
  templates/
    config-template.json       # 그대로 유지
```

### 변환 규칙

1. `reference.md`, `examples.md` → `docs/` 하위로 이동
2. `modules/` 디렉토리 → `docs/` 하위로 파일 이동
3. `scripts/`, `templates/` → 그대로 유지
4. SKILL.md 내 파일 참조 경로 업데이트

---

## 4. 콘텐츠 변환 패턴

### 에이전트 위임 → 직접 실행 변환

```markdown
# 원본 (Claude Code - 에이전트 위임)
복잡한 분석이 필요한 경우 expert-backend 에이전트에 위임한다.
보안 검토는 expert-security 에이전트에 위임한다.

# 변환 후 (Cline - 직접 실행)
복잡한 분석이 필요한 경우 다음 단계를 직접 수행한다:
1. search_files로 관련 코드 패턴 검색
2. read_file로 핵심 파일 분석
3. 분석 결과를 사용자에게 보고

보안 검토 시 다음을 직접 점검한다:
1. OWASP Top 10 체크리스트 기반 코드 검토
2. 입력 검증 로직 확인
3. 인증/인가 흐름 검증
```

### 프로그레시브 디스클로저 변환

```markdown
# 원본 (Claude Code - 3레벨 구조)
## Level 1 - Quick Reference
[즉각적 가치, 핵심 패턴]

## Level 2 - Implementation Guide
[단계별 가이드, 일반 워크플로우]

## Level 3 - Advanced Implementation
[전문가 지식, 엣지 케이스]

# 변환 후 (Cline - 동일 구조 유지, 명칭 변경)
## 빠른 참조
[즉각적 가치, 핵심 패턴]

## 구현 가이드
[단계별 가이드, 일반 워크플로우]

## 고급 패턴
[전문가 지식, 엣지 케이스]
(또는 docs/advanced.md로 분리)
```

---

## 5. description 최적화 패턴

### 영어 → 한국어 변환

```yaml
# 원본 (영어)
description: |
  Code analysis specialist. Analyzes codebase structure, dependencies,
  and code quality. Use when: code review, architecture analysis, refactoring.

# 변환 후 (한국어 + 영어 키워드)
description: |
  코드 분석 전문가. 코드베이스 구조, 의존성, 코드 품질을 분석한다.
  다음 키워드에서 활성화: 코드 분석, 코드 리뷰, 아키텍처 분석,
  리팩토링, code analysis, code review, architecture
```

### 트리거 키워드 보강

변환 시 다음을 확인하고 보강한다:

1. 한국어 키워드 추가 (원본이 영어만 있는 경우)
2. 영어 키워드 유지 (한국어만 있는 경우 영어 추가)
3. 동의어/유사어 포함 (예: DB → 데이터베이스 → database)
4. 축약어 포함 (예: API, REST, SQL)
5. 구체적 기술명 포함 (예: PostgreSQL, Redis, React)

---

## 6. 변환 불가 기능 대안

### Hooks 대안

| 원본 Hook | 대안 |
|----------|------|
| PreToolUse 검증 | 스킬 본문에 "실행 전 확인 사항" 섹션 추가 |
| PostToolUse 알림 | 스킬 본문에 "실행 후 검증" 단계 추가 |
| Stop 이벤트 | "완료 시 체크리스트" 섹션으로 대체 |

### 에이전트 위임 대안

| 원본 위임 | 대안 |
|----------|------|
| 전문 에이전트 호출 | 해당 전문 지식을 스킬 본문에 직접 포함 |
| 병렬 에이전트 실행 | 순차적 단계로 재구성 |
| 에이전트 간 통신 | 단일 워크플로우로 통합 |

### 외부 MCP 대안

| 원본 MCP | 대안 |
|---------|------|
| 외부 MCP 도구 호출 | 사내 MCP 서버에 동일 서비스가 있으면 use_mcp_tool로 대체 |
| 외부 API 호출 | 사내 MCP 서버 또는 execute_command로 대체 |
| 외부 문서 조회 | 필요한 문서를 docs/에 미리 저장 |

---

## 7. 일반 마크다운 → Cline 스킬 변환

일반 마크다운 문서(가이드, 표준 문서 등)를 Cline 스킬로 변환하는 방법:

### 변환 단계

1. **목적 식별**: 문서의 핵심 목적을 파악
2. **프론트매터 생성**: name과 description 작성
3. **구조 재편**: Cline 스킬 구조(빠른 참조/구현 가이드/고급 패턴)로 재편
4. **토큰 최적화**: 5,000 토큰 이내로 핵심 내용 압축
5. **오버플로우 분리**: 초과 내용을 docs/로 분리
6. **트리거 설정**: description에 활성화 키워드 추가

### 변환 예시

```markdown
# 원본: 코딩 컨벤션 가이드 (일반 마크다운)
# 코딩 컨벤션
## 변수 명명 규칙
- camelCase 사용
- 의미 있는 이름 ...

# 변환 후: Cline 스킬
---
name: coding-convention
description: |
  사내 코딩 컨벤션을 적용한다. 변수 명명, 함수 구조, 파일 구성 규칙을 안내한다.
  다음 키워드에서 활성화: 코딩 컨벤션, naming convention, 코딩 규칙, 코드 스타일
---

# 코딩 컨벤션 가이드
## 빠른 참조
[핵심 규칙 요약]

## 구현 가이드
[상세 규칙 설명]
```

---

## 8. 변환 체크리스트

### 변환 전 확인

- [ ] 원본 스킬의 핵심 기능 파악 완료
- [ ] Cline 비호환 요소 식별 완료
- [ ] 변환 가능 여부 판단 완료
- [ ] 대체 방안 수립 완료 (비호환 기능)

### 변환 중 확인

- [ ] 프론트매터가 name + description만 포함
- [ ] 도구명이 Cline 체계로 변환됨
- [ ] 에이전트 참조가 직접 실행으로 변환됨
- [ ] 외부 MCP 참조 제거됨
- [ ] Hooks 참조 제거됨
- [ ] 디렉토리 경로가 .cline/skills/로 변환됨

### 변환 후 확인

- [ ] SKILL.md 5,000 토큰 이내
- [ ] YAML 프론트매터 구문 유효
- [ ] name이 디렉토리명과 일치
- [ ] description에 한국어/영어 트리거 키워드 포함
- [ ] 사내 제약 사항 위반 없음
- [ ] 참조 파일 경로 유효
- [ ] 변환 보고서 작성 완료
