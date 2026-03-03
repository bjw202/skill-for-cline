# Cline 스킬 표준 상세 가이드

이 문서는 Cline 스킬 제작 시 참고하는 상세 표준 레퍼런스이다.

---

## 1. YAML 프론트매터 상세

### 필수 필드

```yaml
---
name: 스킬-이름
description: |
  스킬 설명 (최대 1024자)
---
```

#### name 필드 규칙

- 디렉토리명과 정확히 일치해야 함
- kebab-case만 허용: 소문자, 숫자, 하이픈
- 최대 64자
- 예약어 금지: `cline`, `anthropic`, `claude`

#### description 필드 규칙

- 최대 1024자
- Cline이 스킬 활성화 시점을 판단하는 유일한 기준
- 3인칭 서술: "~한다", "~를 수행한다"
- 반드시 포함할 내용:
  - 스킬이 하는 일 (WHAT)
  - 언제 사용하는지 (WHEN)
  - 활성화 트리거 키워드 (TRIGGER)

### description 작성 패턴

```yaml
# 패턴: [기능 동사] [대상 도메인]. [트리거 조건 나열]
description: |
  [무엇을 하는지 1~2문장].
  다음 키워드에서 활성화: [한국어 키워드], [영어 키워드]
```

**우수 사례:**

```yaml
description: |
  React 컴포넌트를 체계적으로 설계하고 구현한다. JSX 구조, 상태 관리,
  이벤트 처리, 성능 최적화에 대한 모범 사례를 제공한다.
  다음 키워드에서 활성화: React 컴포넌트, 리액트, useState, useEffect,
  component design, React hooks
```

```yaml
description: |
  데이터베이스 마이그레이션을 안전하게 설계하고 실행한다. 스키마 변경,
  데이터 이전, 롤백 전략을 포함한다.
  다음 키워드에서 활성화: DB 마이그레이션, 스키마 변경, migration,
  database schema, 테이블 변경
```

---

## 2. 디렉토리 구조 상세

### 기본 구조

```
.cline/skills/{스킬이름}/
  SKILL.md              # 필수 (5,000 토큰 이내)
  docs/                 # 선택: 상세 문서, 트러블슈팅, 레퍼런스
  templates/            # 선택: 설정 파일, 코드 스캐폴딩, 보일러플레이트
  scripts/              # 선택: 검증, 데이터 처리, API 스크립트
```

### 저장 위치

| 위치 | 경로 | 용도 |
|------|------|------|
| 프로젝트 | `.cline/skills/` | 팀 공유, 버전 관리 |
| 글로벌 | `~/.cline/skills/` | 개인 설정, 프로젝트 공통 |

이름 충돌 시 글로벌 스킬이 우선한다.

### 지원 파일 가이드

**docs/ 디렉토리:**
- 고급 가이드, 트러블슈팅, API 레퍼런스
- SKILL.md에서 "상세 내용은 docs/파일명.md 참조"로 연결
- 참조 깊이 1단계 유지 (SKILL.md → docs/file.md)

**templates/ 디렉토리:**
- 설정 파일 템플릿 (.json, .yaml, .toml 등)
- 코드 스캐폴딩 (컴포넌트 템플릿, 모듈 템플릿 등)
- 보일러플레이트 코드

**scripts/ 디렉토리:**
- 검증 스크립트 (린트, 타입 체크 등)
- 데이터 처리 스크립트
- API 호출 스크립트

---

## 3. 프로그레시브 디스클로저 상세

### Level 1: 메타데이터 (~100 토큰)

- 시작 시 자동 로드
- name + description만 포함
- Cline이 활성화 판단에 사용
- 토큰 소비 최소화

### Level 2: 지침 (~5,000 토큰)

- 요청이 description 트리거와 매칭될 때 로드
- SKILL.md 전체 본문
- 핵심 정보를 앞에 배치 (중요도 순)
- Cline이 이미 아는 내용은 제외

### Level 3: 리소스 (무제한)

- 필요 시에만 파일시스템으로 접근
- docs/, templates/, scripts/ 내 파일
- SKILL.md에서 명시적 참조 시 로드
- 토큰 소비 없이 대기

### 효과적인 Level 2 작성

```markdown
# 핵심 기능 (Level 2에 포함)
- 가장 자주 사용하는 패턴
- 필수 워크플로우 단계
- 핵심 규칙과 제약

# 상세 내용 (Level 3으로 분리)
- 엣지 케이스 처리 (→ docs/edge-cases.md)
- 전체 API 레퍼런스 (→ docs/api-reference.md)
- 코드 예제 모음 (→ docs/examples.md)
```

---

## 4. Cline 도구 상세 참조

### 파일 조작 도구

**read_file**: 파일 내용 읽기
- 파라미터: `path` (필수)
- 용도: 파일 분석, 코드 리뷰, 설정 확인

**write_to_file**: 파일 생성 또는 전체 덮어쓰기
- 파라미터: `path` (필수), `content` (필수)
- 주의: 기존 파일 전체 덮어씀, 부분 수정은 replace_in_file 사용

**replace_in_file**: 파일 내 특정 부분 교체
- 파라미터: `path` (필수), 검색/교체 내용
- 용도: 기존 파일의 특정 섹션만 수정

### 검색/탐색 도구

**search_files**: 정규식으로 파일 내용 검색
- 파라미터: `path` (필수), `regex` (필수), `file_pattern` (선택)
- 용도: 코드 패턴 탐색, 특정 문자열 찾기

**list_files**: 디렉토리 내용 나열
- 파라미터: `path` (필수)
- 용도: 프로젝트 구조 파악, 파일 존재 확인

**list_code_definition_names**: 코드 정의 목록 조회
- 파라미터: `path` (필수)
- 용도: 함수, 클래스, 변수 정의 탐색

### 실행 도구

**execute_command**: CLI 명령어 실행
- 파라미터: `command` (필수), `requires_approval` (선택)
- 용도: 빌드, 테스트, 린트, 패키지 설치 등

**browser_action**: 웹사이트 상호작용
- Puppeteer 기반 브라우저 자동화
- 용도: 웹 테스트, 스크린샷, UI 검증

### MCP 도구 (사내망 전용)

**use_mcp_tool**: MCP 서버 도구 사용
- 사내망 MCP 서버만 접속 가능
- 외부 MCP 서버 접근 불가

**access_mcp_resource**: MCP 서버 리소스 접근
- 사내망 MCP 리소스만 접근 가능

### 대화/완료 도구

**ask_followup_question**: 사용자에게 추가 질문
- 용도: 요구사항 명확화, 선택지 제시

**attempt_completion**: 최종 결과 제시
- 용도: 작업 완료 보고, 결과 요약

**new_task**: 새 작업으로 컨텍스트 전환
- 용도: 긴 작업 시 컨텍스트 윈도우 관리

---

## 5. 스킬 vs 규칙 vs 워크플로우 비교

| 항목 | 규칙 (Rules) | 스킬 (Skills) | 워크플로우 (Workflows) |
|------|-------------|--------------|---------------------|
| 위치 | `.clinerules/` | `.cline/skills/` | `.clinerules/workflows/` |
| 로딩 | 항상 활성 | 요청 매칭 시 | 수동 호출 (`/파일명`) |
| 용도 | 코딩 표준, 규칙 | 전문 지식, 절차 | 반복 프로세스 |
| 토큰 | 상시 소비 | 필요 시만 소비 | 호출 시만 소비 |
| 형식 | 마크다운 | YAML 프론트매터 + 마크다운 | 마크다운 (단계별) |
| 조건부 | paths 프론트매터 | description 기반 | N/A |

### 언제 무엇을 사용하나?

- **"항상 이 규칙을 따라라"** → 규칙 (Rules)
- **"이 상황에서 이 전문 지식을 적용해라"** → 스킬 (Skills)
- **"이 단계를 순서대로 실행해라"** → 워크플로우 (Workflows)

---

## 6. 체크리스트

### 스킬 생성 완료 체크리스트

- [ ] `.cline/skills/{name}/SKILL.md` 생성됨
- [ ] YAML 프론트매터에 `name`과 `description` 포함
- [ ] `name`이 디렉토리명과 일치
- [ ] `description`에 활성화 트리거 키워드 포함
- [ ] SKILL.md가 5,000 토큰 이내
- [ ] 중요 정보가 문서 앞부분에 배치
- [ ] 지원 파일 참조가 1단계 깊이
- [ ] 사내 제약 사항 위반 없음 (hooks 없음, 외부 MCP 없음)
- [ ] kebab-case 이름 규칙 준수
- [ ] 한국어/영어 트리거 키워드 병기
