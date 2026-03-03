# 프로젝트 구조 (Project Structure)

> 슬기로운 코워크 생활 디렉토리 구조 및 아키텍처 설명

---

## 전체 디렉토리 트리

```
skill-for-cline/                           # 프로젝트 루트
├── CLAUDE.md                              # MoAI 오케스트레이터 설정 (필수)
│
├── smart-cowork-life/                     # Claude Code 플러그인 패키지
│   ├── README.md                          # 마켓플레이스 설치 가이드
│   ├── docs/                              # 설치 스크린샷 이미지
│   └── smart-cowork-life/                 # 실제 플러그인 콘텐츠
│       ├── README.md                      # 스킬·커맨드 전체 목록
│       ├── CHANGELOG.md                   # 버전별 변경 이력
│       ├── smart-office-life.plugin       # 플러그인 번들 파일
│       ├── skills/                        # 12종 업무 스킬
│       │   ├── biz-email-writer/          # 비즈니스 이메일 작성
│       │   ├── meeting-minutes/           # 회의록 자동 생성
│       │   ├── korean-biz-docs/           # 한국형 비즈니스 문서
│       │   ├── proposal-maker/            # 제안서/견적서
│       │   ├── excel-automation/          # 엑셀 업무 자동화
│       │   ├── prompt-engineer/           # 프롬프트 엔지니어링
│       │   ├── project-tracker/           # 프로젝트 관리
│       │   ├── portfolio-builder/         # 이력서·포트폴리오
│       │   ├── data-report-generator/     # 데이터 보고서
│       │   ├── korean-translator/         # 한영 번역
│       │   ├── ppt-design-system/         # PPT 디자인 시스템
│       │   └── svg-diagram/               # SVG 도식화
│       ├── commands/                      # 5종 슬래시 커맨드
│       │   ├── daily-report.md            # /daily-report
│       │   ├── weekly-report.md           # /weekly-report
│       │   ├── quick-email.md             # /quick-email
│       │   ├── meeting-note.md            # /meeting-note
│       │   └── resume-check.md            # /resume-check
│       ├── fonts/                         # 내장 폰트 리소스
│       │   ├── Pretendard/                # Pretendard 9종 웨이트
│       │   └── ChosunilboMyongjo/         # 조선일보명조
│       └── data/                          # 참조 데이터
│           └── (업종별 전문용어, 요율표 등)
│
├── .clinerules/                           # Cline 전용 변환본
│   ├── README.md                          # Cline 사용 가이드
│   ├── biz-email-knowledge.md             # [항시 로드] 이메일 도메인 지식
│   ├── data-report-knowledge.md           # [항시 로드] 데이터 보고서 지식
│   ├── excel-automation-knowledge.md      # [항시 로드] 엑셀 자동화 지식
│   ├── korean-biz-docs-knowledge.md       # [항시 로드] 한국형 문서 지식
│   ├── korean-translator-knowledge.md     # [항시 로드] 번역 도메인 지식
│   ├── meeting-minutes-knowledge.md       # [항시 로드] 회의록 지식
│   ├── ppt-design-system-knowledge.md     # [항시 로드] PPT 디자인 지식
│   ├── project-tracker-knowledge.md       # [항시 로드] 프로젝트 관리 지식
│   ├── proposal-maker-knowledge.md        # [항시 로드] 제안서 지식
│   ├── svg-diagram-knowledge.md           # [항시 로드] SVG 도식화 지식
│   └── workflows/                         # 명시적 워크플로우 (13종)
│       ├── biz-doc.md                     # 비즈니스 문서 워크플로우
│       ├── daily-report.md                # 일일보고서 워크플로우
│       ├── data-report.md                 # 데이터 보고서 워크플로우
│       ├── excel-helper.md                # 엑셀 도우미 워크플로우
│       ├── make-ppt.md                    # PPT 제작 워크플로우
│       ├── make-proposal.md               # 제안서 제작 워크플로우
│       ├── meeting-note.md                # 회의록 워크플로우
│       ├── project-tracker.md             # 프로젝트 추적 워크플로우
│       ├── quick-email.md                 # 빠른 이메일 워크플로우
│       ├── resume-check.md                # 이력서 검토 워크플로우
│       ├── svg-diagram.md                 # SVG 다이어그램 워크플로우
│       ├── translate-biz.md               # 비즈니스 번역 워크플로우
│       └── weekly-report.md               # 주간보고서 워크플로우
│
├── .cline/                                # Cline 스킬 (사내 Cline 개발 도구)
│   └── skills/                           # Cline 전용 스킬 정의
│       ├── skill-builder/                # Cline 스킬 생성 전문가
│       │   ├── SKILL.md                  # 스킬 생성 워크플로우 및 표준
│       │   └── docs/
│       │       └── cline-skill-standards.md  # Cline 스킬 표준 상세 가이드
│       └── skill-converter/              # 범용 스킬 → Cline 변환 전문가
│           ├── SKILL.md                  # 변환 워크플로우 및 매핑 규칙
│           └── docs/
│               └── conversion-mapping.md # 상세 변환 매핑 가이드
│
├── .moai/                                 # MoAI-ADK 설정
│   ├── config/                            # 프로젝트 설정 파일
│   │   └── sections/
│   │       ├── quality.yaml               # TDD/DDD 품질 게이트 설정
│   │       ├── language.yaml              # 언어 설정 (ko)
│   │       └── user.yaml                  # 사용자 설정
│   ├── project/                           # 프로젝트 문서 (이 디렉토리)
│   │   ├── product.md                     # 제품 설명서
│   │   ├── structure.md                   # 프로젝트 구조 (현재 파일)
│   │   └── tech.md                        # 기술 스택 문서
│   ├── specs/                             # SPEC 문서
│   ├── docs/                              # 생성된 문서
│   ├── memory/                            # 에이전트 메모리
│   ├── reports/                           # 품질 리포트
│   └── logs/                              # 실행 로그
│
└── .claude/                               # Claude Code 규칙·스킬
    ├── rules/moai/                        # MoAI 규칙 파일
    │   ├── core/                          # 핵심 원칙 (moai-constitution.md 등)
    │   ├── workflow/                      # 워크플로우 규칙
    │   └── development/                   # 개발 표준
    ├── skills/                            # 로컬 스킬 정의
    └── agent-memory/                      # 에이전트 영구 메모리
        └── manager-docs/                  # 문서 에이전트 메모리
```

---

## 주요 디렉토리 역할

### `smart-cowork-life/` — Claude Code 플러그인 패키지

Claude Code의 공식 플러그인 마켓플레이스를 통해 배포되는 원본 패키지입니다.

- **`skills/`**: 각 스킬은 독립 디렉토리로 구성되며, SKILL.md 파일에 Progressive Disclosure(3단계) 형식으로 지식이 정의됩니다. Claude가 대화 중 트리거 키워드를 감지하면 해당 스킬을 자동으로 로드합니다.
- **`commands/`**: 사용자가 `/` 슬래시로 직접 호출하는 커맨드 정의 파일입니다. 각 .md 파일이 하나의 커맨드에 대응합니다.
- **`fonts/`**: PPT 디자인 시스템에서 사용하는 Pretendard(9종 웨이트)와 조선일보명조 폰트 리소스입니다.
- **`data/`**: 업종별 전문용어 사전, 4대보험 요율표 등 스킬이 참조하는 정적 데이터입니다.

### `.cline/skills/` — Cline 개발 도구 스킬

사내 Cline 환경에서 사용하는 개발 지원 스킬입니다.

- **`skill-builder/`**: 새로운 Cline 스킬을 체계적으로 설계하고 제작하는 스킬. YAML 프론트매터 설계, 프로그레시브 디스클로저 구조, 5,000 토큰 제한 준수를 가이드합니다.
- **`skill-converter/`**: 기존 스킬(Claude Code, 일반 마크다운 등)을 분석하여 사내 Cline 환경에 최적화된 형식으로 변환하는 스킬. 도구명 매핑, 프론트매터 변환, 사내 제약 사항 반영을 자동화합니다.

### `.clinerules/` — Cline 전용 변환본

Claude Code 플러그인을 Cline 환경에 맞게 재구성한 버전입니다.

- **`*-knowledge.md` (10종)**: Cline이 세션 시작 시 자동으로 로드하는 도메인 지식 파일입니다. 항상 활성화되어 있어 해당 도메인의 맥락을 상시 제공합니다.
- **`workflows/` (13종)**: 사용자가 명시적으로 요청할 때만 실행되는 단계별 워크플로우 정의입니다. Claude Code의 슬래시 커맨드에 해당합니다.

### `.moai/` — MoAI-ADK 오케스트레이션 설정

MoAI(Claude Code용 전략 오케스트레이터) 프레임워크의 설정 및 산출물이 저장됩니다.

- **`config/`**: 개발 방법론(TDD/DDD), 언어, 품질 게이트 설정
- **`project/`**: 프로젝트 레벨 문서 (현재 문서 포함)
- **`specs/`**: SPEC-First 개발 방법론에 따른 요구사항 명세서
- **`reports/`**: 코드 품질 및 TRUST 5 검증 리포트

---

## 크로스 플랫폼 아키텍처

```
[원본 콘텐츠: smart-cowork-life/skills/]
            |
            | 변환
            v
[Claude Code: skills/ + commands/]    [Cline: .clinerules/ + workflows/]
     트리거 기반 자동 활성화               Knowledge(항시) + Workflow(명시)
     Progressive Disclosure (3단계)      2단계 Knowledge/Workflow 구조
     플러그인 마켓플레이스 배포             프로젝트 디렉토리 복사 설치
```

Claude Code 버전은 Level 1(메타데이터) → Level 2(본문) → Level 3(번들) 3단계 Progressive Disclosure 구조로 토큰을 효율적으로 사용합니다. Cline 버전은 더 단순한 2계층 구조로, Knowledge Rules(항상 로드)와 Workflows(요청 시 로드)로 나뉩니다.

---

## 모듈 조직 전략

### 스킬 디렉토리 구조

각 스킬은 다음 파일 구조를 따릅니다.

```
skills/[스킬명]/
├── SKILL.md              # 핵심 파일 (트리거, 설명, 레벨 1 콘텐츠)
├── level2-content.md     # 상세 지침 (레벨 2, 요청 시 로드)
└── reference/            # 참조 자료 (레벨 3, 필요 시 로드)
    ├── templates.md      # 문서 템플릿
    └── examples.md       # 실제 예시
```

### 파일 명명 규칙

- **스킬 디렉토리**: `kebab-case` (예: `biz-email-writer`, `ppt-design-system`)
- **Knowledge 파일**: `[스킬명]-knowledge.md` (예: `biz-email-knowledge.md`)
- **Workflow 파일**: `[동작]-[대상].md` (예: `make-ppt.md`, `quick-email.md`)
- **커맨드 파일**: `[커맨드명].md` (예: `daily-report.md`, `resume-check.md`)
- **설정 파일**: `[섹션명].yaml` (예: `quality.yaml`, `language.yaml`)

---

## 핵심 파일 위치 요약

| 파일/디렉토리 | 절대 경로 | 역할 |
|---------------|-----------|------|
| 프로젝트 루트 설정 | `/skill-for-cline/CLAUDE.md` | MoAI 오케스트레이터 설정 |
| 스킬 목록 | `/skill-for-cline/smart-cowork-life/smart-cowork-life/skills/` | 12종 업무 스킬 |
| 커맨드 목록 | `/skill-for-cline/smart-cowork-life/smart-cowork-life/commands/` | 5종 슬래시 커맨드 |
| Cline 스킬 | `/skill-for-cline/.cline/skills/` | 2종 개발 도구 스킬 (skill-builder, skill-converter) |
| Cline 지식 | `/skill-for-cline/.clinerules/` | 10종 항시 로드 지식 |
| Cline 워크플로우 | `/skill-for-cline/.clinerules/workflows/` | 13종 명시적 워크플로우 |
| 품질 설정 | `/skill-for-cline/.moai/config/sections/quality.yaml` | TDD 품질 게이트 |
| 언어 설정 | `/skill-for-cline/.moai/config/sections/language.yaml` | 한국어(ko) 설정 |
| 플러그인 번들 | `/skill-for-cline/smart-cowork-life/smart-cowork-life/smart-office-life.plugin` | 배포 패키지 |
