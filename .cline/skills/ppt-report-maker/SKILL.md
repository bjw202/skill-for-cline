---
name: ppt-report-maker
description: |
  보고용 raw text를 분석하여 PptxGenJS 코드로 변환하는 통합 PPT 제작 스킬.
  5단계 파이프라인: 원문 분석 → 맥락 확인 → 콘텐츠 구조화 → 기획안 출력 → PptxGenJS 코드 생성.
  한국형 비즈니스 디자인 시스템(Pretendard 타이포그래피, 6:3:1 색상 법칙, 8개 레이아웃 패턴)을 적용하여
  오버플로우 없는 최적 품질의 PPTX를 생성한다.
  Activate on: PPT, 보고서, 보고자료, 발표자료, 슬라이드, 프레젠테이션, 피치덱, pitch deck,
  PptxGenJS, PPT 디자인, PPT 기획, 슬라이드 기획, 보고서 구조화, PPT 만들기, PPT 생성,
  report to slides, presentation planning, slide design, slide planning
---

# PPT 보고자료 통합 제작 스킬

보고용 텍스트를 분석하여 한국형 비즈니스 PPT를 제작하는 통합 파이프라인.
5단계로 원문 분석부터 PptxGenJS 코드 생성까지 일원화한다.

```
[전체 흐름]
원문(raw text) → ① 분석 → ② 맥락확인 → ③ 구조화 → ④ 기획안 → ⑤ PptxGenJS 코드 → .pptx
```

---

## 1단계: 원문 분석 (Analyze)

사용자가 제공한 raw text를 다음 관점에서 분석한다.

**구조 분석:**
- 핵심 주제(Main Topic)와 하위 주제(Sub-topics) 식별
- 논리적 흐름 파악 (시간순, 인과관계, 비교, 문제-해결)

**콘텐츠 유형 분류 (6가지):**

| 유형 | 식별 기준 | 슬라이드 매핑 |
|------|----------|-------------|
| A. 정량 데이터 | 숫자, 비율, 증감률 | KPI Dashboard / Chart |
| B. 비교 데이터 | A vs B, 전후 비교 | Data Table / Two Column |
| C. 프로세스 | 단계, 절차, 타임라인 | Timeline |
| D. 핵심 메시지 | 결론, 제안, 액션 아이템 | Key Takeaway |
| E. 서술 텍스트 | 배경, 설명, 근거 | Body Text / Card Grid |
| F. 참조/부록 | 출처, 각주, 상세 데이터 | 부록 또는 제외 |

**데이터 포인트 추출:**
- 핵심 지표(KPI) 식별 및 목록화
- 비교 가능한 수치 쌍 식별
- 추이/변화 데이터 식별

분석 완료 후 사용자에게 **분석 요약 리포트**를 먼저 제시한다.

상세 분석 체크리스트 → `docs/analysis-guide.md` 참조

---

## 2단계: 맥락 확인 (Clarify)

원문 분석 후 `ask_followup_question`으로 확인한다. 한 번에 최대 3개씩 질문.

**필수 질문:**

Q1. 발표 목적과 대상 (경영진/팀 내부/고객/투자자/교육)
Q2. 발표 시간 및 슬라이드 규모 (5분/15분/30분/자유)
Q3. 강조하고 싶은 핵심 메시지 1~3가지 (원문에서 추출한 후보 제시)

**선택 질문 (필요 시):**
- 톤앤매너, 브랜드 색상, 특정 슬라이드 유형 요청, 제외할 내용, 첨부 데이터

---

## 3단계: 콘텐츠 구조화 (Structure)

질문 응답을 반영하여 원문을 슬라이드 단위로 재구성한다.

**핵심 원칙:**
1. **한 슬라이드 = 한 메시지**
2. **피라미드 구조**: 결론 → 근거 → 세부사항
3. **6x6 규칙**: 슬라이드당 최대 6개 글머리, 글머리당 한글 18자 이내
4. **데이터 우선**: 수치가 있으면 시각화 우선

**슬라이드 유형 배정:**

| 콘텐츠 유형 | 권장 슬라이드 유형 |
|-------------|-------------------|
| 도입/표지 | Title Slide |
| 섹션 전환 | Section Divider |
| 핵심 KPI | KPI Dashboard |
| 데이터 비교 | Data Table |
| 수치 추이 | Chart + Insight |
| 프로세스/일정 | Timeline |
| 다중 항목 | Card Grid |
| 비교 분석 | Two Column |
| 결론/제안 | Key Takeaway |

**슬라이드 수 산정:** `발표시간(분) × 0.8 ~ 1.2`장

청중별 슬라이드 구성 템플릿 → `docs/slide-templates.md` 참조

---

## 4단계: 기획안 출력 (Design Plan)

각 슬라이드별로 다음 요소를 포함한 markdown 기획안을 출력한다:

```markdown
# [발표 제목] — 슬라이드 기획안

## 기획 개요
- 대상 / 목적 / 슬라이드 수 / 예상 발표 시간 / 색상 팔레트

## 슬라이드 N: [제목]
- **유형**: [8개 패턴 중 택 1]
- **레이아웃**: [배치 설명]
- **콘텐츠**: [구체적 텍스트/데이터/차트 내용]
- **디자인 노트**: [색상, 폰트, 강조 요소]
```

각 슬라이드에 레이아웃 유형, 색상(hex), 타이포그래피, 시각화 유형, 배치를 명시한다.

**사용자에게 기획안을 보여주고 승인/수정 확인 후 5단계로 진행한다.**

---

## 5단계: PptxGenJS 코드 생성 (Generate)

승인된 기획안을 기반으로 PptxGenJS 코드를 생성한다.

### ★★★★ 필수 초기화 (이것을 빠뜨리면 모든 좌표가 틀어짐)

> **이 스킬의 모든 좌표는 13.33" x 7.5" (`LAYOUT_WIDE`) 기준이다.**
> **아래 초기화 코드가 없으면 모든 요소가 우측/하단으로 넘친다.**

```javascript
// ★★★★ 최초 1회 필수 — 이 코드 없이는 슬라이드가 깨진다!
const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';  // 13.33" x 7.5" (필수!)
```

| Layout 이름 | 크기 | 이 스킬과 호환 |
|-------------|------|---------------|
| `LAYOUT_16x9` (기본값) | 10" x 5.625" | **호환 안 됨** |
| **`LAYOUT_WIDE`** | **13.33" x 7.5"** | **이것만 사용** |

**절대 금지**: `pptx.layout = 'LAYOUT_WIDE'` 없이 슬라이드를 생성하는 것

---

### ★★★ 오버플로우 방지 시스템 (절대 원칙)

```javascript
// ★ 오버플로우 방지 상수 — 모든 슬라이드 생성 코드에 반드시 포함
const SAFE = {
  x: 0.6,        // 좌측 여백
  y: 0.5,        // 상단 여백
  w: 12.13,      // 콘텐츠 너비 (13.33 - 0.6 - 0.6)
  h: 6.5,        // 콘텐츠 높이 (7.5 - 0.5 - 0.5)
  maxX: 12.73,   // 우측 절대 한계 (0.6 + 12.13)
  maxY: 7.0,     // 하단 절대 한계 (0.5 + 6.5)
  titleY: 1.6,   // 제목 바 아래 콘텐츠 시작점
  contentH: 5.4, // 제목 바 제외 사용 가능 높이 (7.0 - 1.6)
};
```

```
슬라이드 안전 영역 (13.33" × 7.5")
┌─────────────────────────────────────────┐ ← y=0
│←0.6"→                           ←0.6"→ │
│       ┌─────────────────────────┐       │ ← y=0.5"
│       │  콘텐츠 안전 영역        │       │
│       │  w=12.13"  h=6.5"      │       │
│       │  제목 바 아래: y=1.6"   │       │
│       │  사용 가능 h=5.4"       │       │
│       └─────────────────────────┘       │ ← y=7.0"
└─────────────────────────────────────────┘ ← y=7.5"
  x+w 절대 한계: 12.73"  y+h 절대 한계: 7.0"
```

**모든 요소 배치 전 필수 검증:**
1. `x + w <= 12.73` (우측 초과 금지)
2. `y + h <= 7.0` (하단 초과 금지)
3. `x >= 0.6` (좌측 여백 확보)
4. `y >= 0.5` (상단 여백 확보)

**우측 배치 시 최대 w:** x=5.0→7.73 / x=8.0→4.73 / x=10.0→2.73
**하단 배치 시 최대 h:** y=1.6→5.4 / y=3.0→4.0 / y=5.0→2.0

```javascript
// ★ 제목/라벨/KPI용 — shrinkText 없음 (지정 폰트 크기 유지)
const SAFE_TITLE = { wrap: true };
// ★ 본문/긴 텍스트용 — shrinkText 있음 (오버플로우 방지 폴백)
const SAFE_TEXT = { wrap: true, shrinkText: true };
```

**텍스트**: 16pt 기준 한 줄 최대 한글 약 45자, 반드시 `wrap: true`
**테이블**: 슬라이드당 최대 8~10행, 초과 시 슬라이드 분할 + "(계속)"
**차트**: h ≤ 5.0", legendPos: 'b' (하단)
**글머리**: 최대 6개, 글머리당 한글 18자 이내

---

### 색상 시스템 (6:3:1 법칙)

```javascript
const COLORS = {
  // 메인 60% — 배경/여백
  bg_primary:   'FFFFFF',  bg_secondary: 'F5F7FA',  bg_dark: '1A1F36',
  // 보조 30% — 본문/구조
  text_primary: '1A1F36',  text_secondary: '4A5568',
  text_tertiary: '718096', text_on_dark: 'FFFFFF',
  // 강조 10% — 포인트
  accent_blue: '4A7BF7',   accent_cyan: '00D4AA',
  accent_yellow: 'FFB020', accent_red: 'FF6B6B',  accent_purple: '8B5CF6',
};
```

---

### 폰트 시스템

```javascript
const FONTS = {
  title:    { fontFace: 'Pretendard', bold: true },   // ExtraBold/Black 36~44pt
  subtitle: { fontFace: 'Pretendard', bold: true },   // SemiBold/Bold 24~28pt
  body:     { fontFace: 'Pretendard', bold: false },  // Regular/Medium 16~20pt
  caption:  { fontFace: 'Pretendard', bold: false },  // Light/Regular 12~14pt
  serif:    { fontFace: 'ChosunilboNM', bold: false },// 조선일보명조 (인용구)
  kpi:      { fontFace: 'Pretendard', bold: true },   // Black 48~72pt
};
```

자간: 제목 `charSpacing: -0.5`, 본문 `charSpacing: 0.5`
줄간격: 제목 `lineSpacingMultiple: 1.1`, 본문 `lineSpacingMultiple: 1.4`

---

### PPT 네이티브 요소 매핑

> **절대 원칙**: 표 데이터 → `addTable()`, 수치 비교/추이 → `addChart()`.
> 도형/텍스트로 표·차트를 시뮬레이션하지 않는다.

```
콘텐츠 유형 판별
├─ 행×열 구조 데이터 ────────→ addTable()
├─ 수치 추이/비교/비율 ──────→ addChart()
├─ 외부 이미지/로고 ─────────→ addImage()
├─ 단순 텍스트 블록 ─────────→ addText()
├─ 장식/배경/구분선 ─────────→ addShape()
└─ 오디오/비디오 ────────────→ addMedia()
```

---

### 핵심 헬퍼 함수

```javascript
// ★ 표준 제목 바
function addTitleBar(slide, title, subtitle = '') {
  slide.addShape('rect', { x: 0.6, y: 0.5, w: 1.2, h: 0.06,
    fill: { color: COLORS.accent_blue } });
  slide.addText(title, { x: 0.6, y: 0.65, w: 10, h: 0.6,
    fontSize: 32, ...FONTS.title, color: COLORS.text_primary,
    charSpacing: -0.3, ...SAFE_TITLE });
  if (subtitle) {
    slide.addText(subtitle, { x: 0.6, y: 1.25, w: 10, h: 0.4,
      fontSize: 18, ...FONTS.body, color: COLORS.text_tertiary, ...SAFE_TITLE });
  }
}
```

```javascript
// ★ 테이블 스타일 단축
const TS = {
  hdr: { bold: true, fill: { color: COLORS.bg_dark }, color: COLORS.text_on_dark,
         fontFace: 'Pretendard', fontSize: 12, align: 'center', valign: 'middle' },
  cel: { fontFace: 'Pretendard', fontSize: 12, color: COLORS.text_secondary, valign: 'middle' },
  alt: { fontFace: 'Pretendard', fontSize: 12, color: COLORS.text_secondary,
         fill: { color: COLORS.bg_secondary }, valign: 'middle' }
};

// ★ 테이블 최대 행 수 계산
function maxTableRows(availableH = SAFE.contentH, rowH = 0.4, headerH = 0.45) {
  return Math.floor((availableH - headerH) / rowH);
}

// ★ 오버플로우 가드 포함 테이블
function addStyledTable(slide, headers, dataRows, opts = {}) {
  const startY = opts.y || 1.8;
  const rowH = opts.rowH?.[1] || 0.4;
  const availH = SAFE.maxY - startY;
  const max = maxTableRows(availH, rowH, 0.45);
  if (dataRows.length > max) dataRows = dataRows.slice(0, max);

  const rows = [ headers.map(h => ({ text: h, options: { ...TS.hdr } })) ];
  dataRows.forEach((row, i) => {
    const base = i % 2 === 1 ? TS.alt : TS.cel;
    rows.push(row.map(c => typeof c === 'string'
      ? { text: c, options: { ...base } }
      : { text: c.text, options: { ...base, ...c.options } }));
  });
  slide.addTable(rows, { x: 0.6, y: startY, w: 12.13,
    border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
    autoPage: false, margin: [5, 8, 5, 8], ...opts });
}
```

```javascript
// ★ 차트 스타일
const CHART_STYLE = {
  base: {
    showTitle: true, titleFontFace: 'Pretendard', titleFontSize: 16,
    showLegend: true, legendFontFace: 'Pretendard', legendFontSize: 10,
    legendPos: 'b',
    catAxisLabelFontFace: 'Pretendard', catAxisLabelFontSize: 11,
    valAxisLabelFontFace: 'Pretendard', valAxisLabelFontSize: 11,
  },
  colors: ['4A7BF7','00D4AA','FFB020','FF6B6B','8B5CF6','38BDF8']
};

// ★ 오버플로우 가드 포함 차트
function addStyledChart(slide, pptx, type, chartData, opts = {}) {
  const o = { x: 0.6, y: 1.8, w: 12.13, h: 5.0, ...opts };
  if (o.x + o.w > SAFE.maxX) { o.w = SAFE.maxX - o.x; }
  if (o.y + o.h > SAFE.maxY) { o.h = SAFE.maxY - o.y; }
  const typeMap = {
    BAR: pptx.charts.BAR, LINE: pptx.charts.LINE, PIE: pptx.charts.PIE,
    DOUGHNUT: pptx.charts.DOUGHNUT, AREA: pptx.charts.AREA,
    RADAR: pptx.charts.RADAR, SCATTER: pptx.charts.SCATTER
  };
  slide.addChart(typeMap[type], chartData, {
    ...CHART_STYLE.base,
    chartColors: CHART_STYLE.colors.slice(0, chartData.length || 6),
    ...o
  });
}
```

```javascript
// ★ 카드 생성 함수
function addCard(slide, { x, y, w, h, title, body, accentColor }) {
  if (x + w > SAFE.maxX) console.warn(`카드 우측 초과: ${x+w}"`);
  if (y + h > SAFE.maxY) console.warn(`카드 하단 초과: ${y+h}"`);
  slide.addShape('roundRect', { x, y, w, h, rectRadius: 0.1,
    fill: { color: 'FFFFFF' },
    shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' } });
  slide.addShape('rect', { x: x+0.02, y, w: w-0.04, h: 0.06,
    fill: { color: accentColor || COLORS.accent_blue } });
  slide.addText(title, { x: x+0.2, y: y+0.2, w: w-0.4, h: 0.35,
    fontSize: 18, ...FONTS.subtitle, color: COLORS.text_primary, ...SAFE_TITLE });
  slide.addText(body, { x: x+0.2, y: y+0.55, w: w-0.4, h: h-0.75,
    fontSize: 14, ...FONTS.body, color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, valign: 'top', ...SAFE_TEXT });
}
```

```javascript
// ★ 페이지 번호
function addPageNumber(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 11.6, y: 6.6, w: 0.9, h: 0.3,
    fontSize: 10, ...FONTS.caption, color: COLORS.text_tertiary,
    align: 'right', ...SAFE_TITLE });
}
```

```javascript
// ★ 경계 검증 (모든 슬라이드 생성 완료 후 호출)
function validateBounds(elements) {
  const errors = [];
  elements.forEach((el, i) => {
    if ((el.x||0)+(el.w||0) > SAFE.maxX+0.01)
      errors.push(`요소[${i}] 우측 초과: ${((el.x||0)+(el.w||0)).toFixed(2)}"`);
    if ((el.y||0)+(el.h||0) > SAFE.maxY+0.01)
      errors.push(`요소[${i}] 하단 초과: ${((el.y||0)+(el.h||0)).toFixed(2)}"`);
  });
  if (errors.length > 0) console.error('★ 오버플로우 경고:\n' + errors.join('\n'));
  return errors.length === 0;
}
```

---

### 차트 유형 선택 기준

| 데이터 유형 | 차트 유형 | PptxGenJS 상수 |
|------------|----------|---------------|
| 항목별 크기 비교 | 세로 막대 | `pptx.charts.BAR` |
| 시계열 추이/변화 | 꺾은선 | `pptx.charts.LINE` |
| 전체 대비 비율 (5개 이하) | 원형 | `pptx.charts.PIE` |
| 전체 대비 비율 (중앙 KPI) | 도넛 | `pptx.charts.DOUGHNUT` |
| 추이 + 누적량 | 영역 | `pptx.charts.AREA` |
| 다차원 항목 비교 | 방사형 | `pptx.charts.RADAR` |

---

### QA 체크리스트

코드 생성 후 순서대로 확인:

**★★★★ 레이아웃 초기화 (최최우선)**
- [ ] `pptx.layout = 'LAYOUT_WIDE'` 설정 확인

**★★★ 오버플로우 검사 (최우선)**
- [ ] 모든 요소의 `x + w <= 12.73` 확인
- [ ] 모든 요소의 `y + h <= 7.0` 확인
- [ ] 우측 하단 배치 요소 특별 주의 (x >= 8.0 또는 y >= 5.0)
- [ ] 테이블 행 수 ≤ 10행 (초과 시 분할)
- [ ] 제목/라벨/KPI에 `...SAFE_TITLE`, 본문에 `...SAFE_TEXT` 적용
- [ ] 차트 y+h ≤ 7.0 및 legendPos: 'b' 확인
- [ ] 글머리 기호 ≤ 6개 / 줄당 한글 ≤ 18자

**디자인 품질 검사**
- [ ] 제목 36~44pt / 소제목 24~28pt / 본문 16~20pt
- [ ] 색상 6:3:1 비율 준수
- [ ] 여백: 좌우 0.6" / 상하 0.5" 이상
- [ ] 한 슬라이드 1 메시지 원칙
- [ ] 표 데이터 → `addTable()` / 수치 → `addChart()` / 이미지 → `addImage()`

---

## 추가 팔레트 옵션

```javascript
// Warm Corporate (따뜻한 기업 톤)
const WARM = { bg_dark: '2D1B4E', accent_blue: 'E8725A',
  accent_cyan: '4ECDC4', accent_yellow: 'F9C74F', accent_purple: '7B68EE' };

// Nature Green (친환경/ESG)
const GREEN = { bg_dark: '1B3A2D', accent_blue: '2D9CDB',
  accent_cyan: '27AE60', accent_yellow: 'F2C94C', accent_red: 'EB5757' };

// Minimal Mono (미니멀)
const MONO = { bg_dark: '111111', accent_blue: '333333',
  accent_cyan: '666666', accent_yellow: 'AAAAAA', text_primary: '111111' };
```

---

## 참고 문서

- `docs/analysis-guide.md` — 원문 분석 체크리스트 및 콘텐츠 분류 상세 기준
- `docs/slide-templates.md` — 청중별/목적별 슬라이드 구성 템플릿 모음
- `docs/layout-patterns.md` — 8개 레이아웃 패턴 전체 코드, 슬라이드 구성 패턴, 디자인 트렌드
- `docs/pptxgenjs-elements.md` — PptxGenJS 요소별 상세 가이드 (addTable, addChart, addImage, addText, addShape, addNotes)
