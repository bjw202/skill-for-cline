---
spec_id: SPEC-CLINE-001
title: "Cline Skills Quality Improvement - Implementation Plan"
version: "1.0.0"
status: completed
created: "2026-02-27"
updated: "2026-02-27"
author: jw
---

# SPEC-CLINE-001: 구현 계획

## 1. 마일스톤 개요

### Primary Goal: docs/ 참조 형식 수정 (Module 1)

**우선순위**: HIGH - 핵심 기능에 직접적 영향
**영향 범위**: 3개 스킬 SKILL.md + cline-standards.md
**의존성**: 없음 (독립적으로 먼저 수행 가능)

수행 항목:
1. skill-builder/SKILL.md의 모든 docs/ 참조를 백틱에서 마크다운 링크로 변환
2. skill-converter/SKILL.md의 모든 docs/ 참조를 백틱에서 마크다운 링크로 변환
3. agent-builder/SKILL.md의 모든 docs/ 참조를 백틱에서 마크다운 링크로 변환
4. cline-standards.md에 docs/ 참조 형식 규칙 섹션 추가
5. skill-builder 검증 체크리스트에 마크다운 링크 형식 검증 항목 추가/수정

### Secondary Goal: scripts/ 디렉토리 통합 (Module 2 + Module 3)

**우선순위**: HIGH - 토큰 효율성 및 기능 완성도에 영향
**영향 범위**: skill-builder, agent-builder, cline-standards.md
**의존성**: Module 1 완료 권장 (cline-standards.md 동시 수정 방지)

수행 항목:
1. skill-builder/SKILL.md의 PLAN 출력 구조에 scripts/ 추가
2. skill-builder/SKILL.md의 검증 체크리스트에 scripts/ 확인 항목 추가
3. scripts/ vs 인라인 명령어 사용 가이드 추가
4. agent-builder/SKILL.md에 scripts/ 실제 생성 로직 추가
5. cline-standards.md에 scripts/ 토큰 효율성 문서화
6. (Optional) skill-builder/scripts/ 디렉토리에 유틸리티 스크립트 생성

### Final Goal: description 필드 준수 (Module 4)

**우선순위**: MEDIUM - 표준 준수 및 트리거 효과 개선
**영향 범위**: 3개 스킬 프론트매터
**의존성**: 없음 (독립적 수행 가능, 하지만 다른 모듈과 함께 커밋 권장)

수행 항목:
1. skill-builder/SKILL.md의 description을 액션 동사로 시작하도록 수정
2. skill-converter/SKILL.md의 description을 액션 동사로 시작하도록 수정
3. agent-builder/SKILL.md의 description을 액션 동사로 시작하도록 수정
4. description-writing.md에 액션 동사 시작 요구사항 강화 및 예시 추가
5. skill-builder 검증 체크리스트에 description 형식 확인 항목 추가

---

## 2. 기술적 접근

### 2.1 Module 1: docs/ 참조 형식 수정

**전략**: Search-and-Replace 패턴

각 SKILL.md에서 다음 패턴을 검색하여 변환:

| 검색 패턴 | 변환 결과 |
|-----------|-----------|
| `` `docs/interview-guide.md` `` | `[interview-guide.md](docs/interview-guide.md)` |
| `` `docs/naming-guide.md` `` | `[naming-guide.md](docs/naming-guide.md)` |
| `` `docs/cline-standards.md` `` | `[cline-standards.md](docs/cline-standards.md)` |
| `` `docs/description-writing.md` `` | `[description-writing.md](docs/description-writing.md)` |

**cline-standards.md 추가 섹션**:

docs/ 파일 참조 규칙을 명시하는 새 섹션을 추가하여, 마크다운 링크 형식이 공식 표준임을 명확히 문서화.

**검증 체크리스트 수정**:

skill-builder의 기존 체크리스트 항목 중 "인라인 docs/ 참조 확인" 관련 항목을 마크다운 링크 형식 검증으로 강화.

### 2.2 Module 2: scripts/ 디렉토리 통합

**전략**: 점진적 통합

Phase A - 문서화:
- cline-standards.md에 scripts/ 토큰 효율성 특성 문서화
- scripts/ 사용 시기와 장점 설명

Phase B - 템플릿 업데이트:
- skill-builder의 PLAN 출력 형식에 scripts/ 선택 항목 추가
- agent-builder에 분석 태스크 식별 시 scripts/ 생성 로직 추가

Phase C - (Optional) 유틸리티 스크립트 생성:
- `scan-skills.sh`: 기존 스킬 디렉토리 구조 스캔
- `validate-skill.sh`: SKILL.md 형식 검증 (줄 수, 프론트매터, docs/ 참조 형식)

### 2.3 Module 3: skill-builder 템플릿 개선

**전략**: 기존 구조 확장

PLAN 출력의 디렉토리 구조 템플릿을 확장하고, scripts/ 사용 가이드를 인라인 지침으로 추가. 검증 체크리스트에 scripts/ 관련 항목을 포함.

### 2.4 Module 4: description 필드 수정

**전략**: 직접 수정 + 가이드 강화

각 스킬의 description을 공식 표준에 맞게 액션 동사로 시작하도록 수정. 이중 언어 (한국어/영어) 지원 유지.

**description 수정안**:

| 스킬 | 현재 description | 수정안 |
|------|------------------|--------|
| skill-builder | "Cline 스킬 생성 전문가 / Cline skill creation specialist. Designs..." | "Design and create production-ready Cline skills following official standards. Cline 공식 표준에 맞춰 스킬을 설계하고 생성합니다." |
| skill-converter | "Claude Code / AntiGravity 스킬을 Cline 호환 형식으로 분석 및 변환합니다" | "Convert Claude Code and MoAI skills to Cline-compatible format with automatic structure analysis. Claude Code / MoAI 스킬을 Cline 호환 형식으로 변환합니다." |
| agent-builder | "에이전틱 스킬 패키지 제작 전문가 / Agentic skill package specialist. Cline에는..." | "Build agentic skill packages for Cline with multi-phase workflow automation. Cline용 에이전틱 스킬 패키지를 설계하고 제작합니다." |

**참고**: 최종 description은 구현 시 실제 SKILL.md 내용을 기반으로 조정 가능.

---

## 3. 아키텍처 설계 방향

### 3.1 변경 범위 분석

```
.cline/skills/
  skill-builder/
    SKILL.md              <- M1, M2, M3, M4 수정
    docs/
      cline-standards.md  <- M1, M2 수정
      description-writing.md <- M4 수정
    scripts/              <- M2 신규 생성 (Optional)
      scan-skills.sh      <- 신규
      validate-skill.sh   <- 신규
  skill-converter/
    SKILL.md              <- M1, M4 수정
  agent-builder/
    SKILL.md              <- M1, M2, M4 수정
```

### 3.2 수정 순서 전략

1. **cline-standards.md 먼저 수정** (M1 + M2 표준 문서화)
   - docs/ 참조 형식 규칙 추가
   - scripts/ 토큰 효율성 문서 추가
   - 이후 3개 SKILL.md 수정의 근거 문서 역할

2. **description-writing.md 수정** (M4 표준 문서화)
   - 액션 동사 시작 요구사항 강화

3. **skill-builder/SKILL.md 수정** (M1 + M2 + M3 + M4)
   - 가장 많은 변경이 필요한 파일
   - docs/ 참조 형식 변경
   - PLAN 출력 구조 업데이트
   - 검증 체크리스트 강화
   - description 필드 수정

4. **skill-converter/SKILL.md 수정** (M1 + M4)
   - docs/ 참조 형식 변경
   - description 필드 수정

5. **agent-builder/SKILL.md 수정** (M1 + M2 + M4)
   - docs/ 참조 형식 변경
   - scripts/ 생성 로직 추가
   - description 필드 수정

6. **(Optional) scripts/ 유틸리티 스크립트 생성** (M2)
   - scan-skills.sh 생성
   - validate-skill.sh 생성

---

## 4. 리스크 및 대응 방안

### R1: docs/ 파일 로딩 메커니즘 불확실성
- **리스크**: 마크다운 링크 형식이 아닌 다른 방식으로 docs/ 파일을 로드할 가능성
- **확률**: Low (공식 문서 예시가 마크다운 링크 사용)
- **대응**: 변경 후 실제 Cline에서 docs/ 파일 로딩 테스트 수행
- **완화**: 어떤 형식이든 공식 표준을 따르는 것이 안전한 선택

### R2: SKILL.md 줄 수 제한 초과
- **리스크**: scripts/ 관련 내용 추가로 200-300줄 권장 초과 가능
- **확률**: Medium
- **대응**: 추가 내용을 최소화하고, 상세 내용은 docs/ 파일로 분리
- **완화**: 수정 전후 줄 수 비교 검증 포함

### R3: description 변경으로 인한 트리거 불일치
- **리스크**: description 변경이 기존 트리거 패턴에 영향을 줄 수 있음
- **확률**: Low (핵심 키워드는 유지)
- **대응**: 변경 후 트리거 키워드 보존 여부 확인
- **완화**: 기존 핵심 키워드를 description에 포함하도록 설계

### R4: 기존 사용자 호환성
- **리스크**: 이 도구로 이미 만든 스킬이 있는 사용자에게 영향
- **확률**: Low (생성 도구의 변경이지 생성된 스킬은 영향 없음)
- **대응**: 변경 사항이 새로 생성되는 스킬에만 적용됨을 명시

---

## 5. 구현 후 검증

### 5.1 자동 검증

- Grep으로 3개 SKILL.md에서 백틱 형식 docs/ 참조 부재 확인
- Grep으로 3개 SKILL.md에서 마크다운 링크 형식 docs/ 참조 존재 확인
- 각 SKILL.md의 줄 수가 300줄 이내인지 확인
- description 필드가 액션 동사로 시작하는지 패턴 매칭

### 5.2 수동 검증

- Cline에서 수정된 스킬 로딩 후 docs/ 파일 접근 가능 여부 확인
- skill-builder로 새 스킬 생성 시 PLAN 출력에 scripts/ 포함 확인
- 각 스킬의 트리거 효과 확인

---

## 6. 다음 단계

구현 준비 완료 시:
1. `/moai run SPEC-CLINE-001`로 구현 시작
2. Module 순서대로 수정 진행
3. 각 Module 완료 후 검증 수행
4. 전체 완료 후 `/moai sync SPEC-CLINE-001`로 문서 동기화
