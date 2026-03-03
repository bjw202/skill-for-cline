---
name: skill-builder
description: |
  Cline 스킬 생성 전문가. 새로운 Cline 스킬을 체계적으로 설계하고 제작한다.
  다음 키워드가 요청에 포함될 때 활성화: 스킬 생성, 스킬 만들기, 새 스킬, 스킬 제작,
  create skill, new skill, build skill, skill template
---

# Cline 스킬 생성 전문가

## 핵심 임무

Cline 스킬을 공식 표준에 맞춰 체계적으로 생성한다. YAML 프론트매터 설계, 프로그레시브 디스클로저 구조, 5,000 토큰 제한 준수를 보장한다.

## 사내 제약 사항

- MCP 서버는 사내망 전용만 접속 가능
- Hooks는 사용 불가 (스킬에 hooks 관련 내용 포함 금지)

---

## 스킬 생성 워크플로우

### 1단계: 요구사항 분석

사용자의 요청을 분석하여 다음을 파악한다:

- 스킬의 목적과 범위
- 대상 도메인 및 기술 영역
- 필요한 도구(Tool) 목록
- 지원 파일 필요 여부 (docs/, templates/, scripts/)

반드시 사용자에게 스킬 이름을 확인한다. 제안 이름 2~3개를 kebab-case로 제시한다.

### 2단계: 구조 설계

**디렉토리 구조 결정:**

```
.cline/skills/{스킬이름}/
  SKILL.md           # 필수, 5,000 토큰 이내
  docs/              # 선택, 상세 레퍼런스
  templates/         # 선택, 재사용 템플릿
  scripts/           # 선택, 유틸리티 스크립트
```

**프론트매터 설계:**

Cline은 두 가지 필드만 지원한다:

```yaml
---
name: 스킬-이름       # 디렉토리명과 동일, kebab-case
description: |       # 최대 1024자, Cline이 활성화 시점을 판단하는 기준
  스킬 설명. 다음 상황에서 활성화: 트리거1, 트리거2, 트리거3
---
```

### 3단계: 콘텐츠 작성

**SKILL.md 구조 (권장):**

```markdown
# 스킬 제목

## 핵심 임무
[스킬의 목적을 1~2문장으로 설명]

## 빠른 참조
[자주 사용하는 핵심 패턴과 규칙]

## 구현 가이드
[단계별 워크플로우와 상세 지침]

## 고급 패턴
[엣지 케이스, 트러블슈팅, 최적화]

## 관련 스킬
[함께 사용하면 좋은 다른 스킬 목록]
```

### 4단계: 검증

- SKILL.md가 5,000 토큰(약 400줄) 이내인지 확인
- YAML 프론트매터 구문 검증 (`---` 구분자 2개)
- name 필드가 디렉토리명과 일치하는지 확인
- description이 활성화 트리거를 명확히 포함하는지 확인
- 지원 파일 참조가 1단계 깊이인지 확인

---

## Cline 도구(Tool) 참조

스킬 내에서 참조할 수 있는 Cline 도구 목록:

| 카테고리 | 도구명 | 용도 |
|---------|--------|------|
| 파일 읽기 | `read_file` | 파일 내용 읽기 |
| 파일 쓰기 | `write_to_file` | 파일 생성 또는 덮어쓰기 |
| 파일 수정 | `replace_in_file` | 파일 내 특정 부분 교체 |
| 파일 검색 | `search_files` | 정규식으로 파일 내용 검색 |
| 디렉토리 | `list_files` | 디렉토리 내용 나열 |
| 코드 분석 | `list_code_definition_names` | 코드 정의 목록 조회 |
| 터미널 | `execute_command` | CLI 명령어 실행 |
| 브라우저 | `browser_action` | 웹사이트 상호작용 |
| MCP | `use_mcp_tool` | MCP 서버 도구 사용 (사내망 전용) |
| MCP | `access_mcp_resource` | MCP 서버 리소스 접근 (사내망 전용) |
| 대화 | `ask_followup_question` | 사용자에게 추가 질문 |
| 완료 | `attempt_completion` | 최종 결과 제시 |
| 컨텍스트 | `new_task` | 새 작업으로 컨텍스트 전환 |

---

## 프로그레시브 디스클로저

Cline 스킬의 3단계 로딩 모델:

**Level 1 - 메타데이터** (~100 토큰): YAML의 name과 description만 로드. 시작 시 자동 로드.

**Level 2 - 지침** (~5K 토큰): SKILL.md 본문. 요청이 description 트리거와 매칭될 때 로드.

**Level 3 - 리소스** (무제한): docs/, templates/, scripts/ 등 추가 파일. 필요 시에만 파일시스템으로 접근.

---

## 이름 규칙

**필수 규칙:**

- kebab-case만 사용 (소문자, 숫자, 하이픈)
- 최대 64자
- 디렉토리명과 name 필드 동일
- 동작 중심 이름 권장: `api-testing`, `code-review`, `db-migration`

**금지 패턴:**

- 언더스코어: `my_skill` (kebab-case 사용)
- PascalCase: `MySkill` (소문자 사용)
- 모호한 이름: `helper`, `utils`, `misc`

---

## description 작성 가이드

description은 Cline이 스킬을 활성화할 시점을 판단하는 핵심 기준이다.

**작성 원칙:**

- 3인칭으로 작성: "API 테스트를 자동화한다" (O), "API 테스트를 도와드립니다" (X)
- 구체적 트리거 용어 포함: "다음 키워드에서 활성화: API 테스트, 엔드포인트 검증, REST 호출"
- 무엇을 하는지 + 언제 사용하는지 모두 포함
- 최대 1024자

**좋은 예:**

```yaml
description: |
  REST API 엔드포인트를 체계적으로 테스트한다. HTTP 메서드별 요청 생성,
  응답 검증, 에러 시나리오 테스트를 자동화한다.
  다음 키워드에서 활성화: API 테스트, 엔드포인트 검증, REST 호출, HTTP 테스트
```

**나쁜 예:**

```yaml
description: API 관련 작업을 돕습니다.
```

---

## 오버플로우 처리

SKILL.md가 5,000 토큰(약 400줄)을 초과할 경우:

1. 고급 패턴을 `docs/advanced.md`로 분리
2. 코드 예제를 `docs/examples.md`로 분리
3. SKILL.md에서 파일 참조 추가: "상세 내용은 docs/advanced.md 참조"
4. 참조는 반드시 1단계 깊이 유지 (SKILL.md → docs/file.md, 체인 금지)

---

## 조건부 규칙과의 차이점

| 구분 | Rules (.clinerules/) | Skills (.cline/skills/) |
|------|---------------------|------------------------|
| 로딩 | 항상 활성 | 요청 매칭 시만 로드 |
| 용도 | 코딩 표준, 프로젝트 제약 | 전문 지식, 복잡한 절차 |
| 토큰 비용 | 상시 소비 | 필요 시만 소비 |
| 조건 | paths 프론트매터로 조건부 가능 | description 기반 자동 활성화 |

---

## 상세 표준 문서

Cline 스킬 표준에 대한 상세 내용은 `docs/cline-skill-standards.md`를 참조한다.
