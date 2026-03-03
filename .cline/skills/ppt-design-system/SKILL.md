---
name: ppt-design-system
description: |
  한국형 비즈니스 PPT 디자인 시스템. Pretendard + 명조체 타이포그래피,
  6:3:1 색상 법칙, PptxGenJS 네이티브 요소 매핑(테이블·차트·이미지·도형),
  슬라이드 레이아웃 가이드라인을 적용하여 최적 품질의 PPTX를 생성한다.
  콘텐츠 오버플로우 방지 시스템을 통해 모든 요소가 용지 범위 내에 배치됨을 보장한다.
  Activate on: PPT, 슬라이드, 프레젠테이션, 발표자료, 피치덱, pitch deck,
  PptxGenJS, PPT 디자인, 슬라이드 디자인, PPT 템플릿, PPT 폰트
---

# PPT 한국형 디자인 시스템

한국 비즈니스 환경에 최적화된 PPT 디자인 시스템.
Pretendard(고딕) + 조선일보명조(명조) 조합으로 전문적이고 가독성 높은 슬라이드를 생성한다.

---

## ★★★ 오버플로우 방지 시스템 (절대 원칙)

> **이 섹션은 가장 먼저 읽어야 한다. 슬라이드 생성 전 반드시 아래 상수와 규칙을 코드에 포함시킬 것.**

### 안전 영역 상수 (Safe Area Constants)

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
슬라이드 안전 영역 다이어그램 (16:9 / 13.33" × 7.5")
┌─────────────────────────────────────────┐ ← y=0
│←0.6"→                           ←0.6"→ │
│       ┌─────────────────────────┐       │ ← y=0.5"
│       │  콘텐츠 안전 영역        │       │
│       │  w=12.13"  h=6.5"      │       │
│       │                         │       │
│       │  제목 바 아래: y=1.6"   │       │
│       │  사용 가능 h=5.4"       │       │
│       └─────────────────────────┘       │ ← y=7.0"
│                                         │
└─────────────────────────────────────────┘ ← y=7.5"
  x+w 절대 한계: 12.73"  y+h 절대 한계: 7.0"
```

**절대 금지**: x + w > 12.73" 또는 y + h > 7.0" 인 요소 배치

### 텍스트 오버플로우 방지 규칙

```javascript
// ★ 모든 addText에 반드시 적용할 안전 옵션
const SAFE_TEXT = { wrap: true, shrinkText: true };

// ★ 텍스트 높이 계산 함수 (배치 전 반드시 계산)
function calcTextHeight(text, fontSize, lineSpacing = 1.4, maxWidthInch = 12.13) {
  // 한글 기준: 1인치당 약 72pt, 한글 1자 = 약 1em
  const ptPerInch = 72;
  const charsPerLine = Math.floor((maxWidthInch * ptPerInch) / fontSize * 1.8);
  const lineCount = Math.ceil(text.length / charsPerLine);
  return lineCount * (fontSize * lineSpacing / ptPerInch);
}

// 사용 예시: 배치 전 높이 확인
const textH = calcTextHeight(myText, 16, 1.4, 12.13);
if (SAFE.titleY + textH > SAFE.maxY) {
  // 슬라이드 분할 필요!
  console.warn('텍스트가 슬라이드를 초과합니다. 슬라이드를 분할하세요.');
}
```

**텍스트 글자 수 제한**:
- 16pt 기준 한 줄 최대: 한글 약 45자 / 영문 약 70자
- 반드시 `wrap: true` 설정
- 반드시 `shrinkText: true` 설정 (폴백)

### 테이블 오버플로우 방지 규칙

```javascript
// ★ 테이블 최대 행 수 계산
function maxTableRows(availableH = SAFE.contentH, rowH = 0.4, headerH = 0.45) {
  return Math.floor((availableH - headerH) / rowH);
  // 기본값: Math.floor((5.4 - 0.45) / 0.4) = 12행
  // 안전 권장: 8~10행 (여백 확보)
}

// ★ 테이블 배치 전 높이 확인
function checkTableBounds(rowCount, rowH = 0.4, headerH = 0.45, startY = SAFE.titleY) {
  const totalH = headerH + rowCount * rowH;
  const endY = startY + totalH;
  if (endY > SAFE.maxY) {
    const safe = maxTableRows(SAFE.maxY - startY, rowH, headerH);
    throw new Error(`테이블이 슬라이드를 초과합니다. 최대 ${safe}행 또는 슬라이드를 분할하세요.`);
  }
  return totalH;
}
```

**테이블 필수 규칙**:
- 슬라이드당 최대 **8~10행** (헤더 포함, 여백 확보)
- 행이 초과하면 → 슬라이드 분할 + "(계속)" 접미사 추가
- 셀 폰트 크기: **10~11pt** (절대 12pt 초과 금지)
- `autoPage: true` 설정 권장 (자동 페이지 분할)

### 글머리 목록 오버플로우 방지 규칙

**6x6 규칙 (절대 준수)**:
- 슬라이드당 최대 **6개 글머리** 기호
- 글머리당 최대 **한글 18자** / **영문 6단어**
- 항목이 6개를 초과하면 → 슬라이드 분할 필수

### 차트 오버플로우 방지 규칙

```javascript
// ★ 차트 안전 크기 (제목 바 이후 영역 기준)
const CHART_SAFE = {
  maxW: 12.13,   // 최대 너비
  maxH: 5.0,     // 최대 높이 (레전드 공간 확보)
  minY: 1.6,     // 최소 y (제목 바 아래)
};

// 차트 배치 시: x=0.6, y=1.6, w≤12.13, h≤5.0
// 레전드: legendPos: 'b' (하단) — 좌우 오버플로우 방지
```

### 경계 검증 함수 (필수 포함)

```javascript
// ★ 모든 슬라이드 생성 완료 후 반드시 호출
function validateBounds(elements) {
  const errors = [];
  elements.forEach((el, i) => {
    const rightEdge = (el.x || 0) + (el.w || 0);
    const bottomEdge = (el.y || 0) + (el.h || 0);
    if (rightEdge > SAFE.maxX + 0.01) {
      errors.push(`요소[${i}] 우측 초과: ${rightEdge.toFixed(2)}" (한계: ${SAFE.maxX}")`);
    }
    if (bottomEdge > SAFE.maxY + 0.01) {
      errors.push(`요소[${i}] 하단 초과: ${bottomEdge.toFixed(2)}" (한계: ${SAFE.maxY}")`);
    }
  });
  if (errors.length > 0) {
    console.error('★ 오버플로우 경고:\n' + errors.join('\n'));
  }
  return errors.length === 0;
}
```

---

## PPT 네이티브 요소 매핑 (핵심 원칙)

> **절대 원칙**: 표 형식 데이터는 반드시 `addTable()`을, 수치 비교/추이는 반드시 `addChart()`를 사용한다.
> 도형(`addShape`)과 텍스트(`addText`)로 표/차트를 시뮬레이션하지 않는다.

### 요소 선택 의사결정 트리

```
콘텐츠 유형 판별
├─ 행×열 구조의 데이터인가? ──────────→ addTable()
│   예: 매출표, 일정표, 비교표, 가격표, 스펙표, 예산표
│
├─ 수치의 추이/비교/비율인가? ─────────→ addChart()
│   예: 매출 추이, 점유율, KPI 변화, 분기 비교
│
├─ 외부 이미지/로고/사진인가? ─────────→ addImage()
│   예: 제품 사진, 회사 로고, 스크린샷, 아이콘
│
├─ 단순 텍스트 블록인가? ──────────────→ addText()
│   예: 제목, 본문 단락, 글머리 기호 목록, 인용문
│
├─ 장식/배경/구분선/도형인가? ─────────→ addShape()
│   예: 배경 사각형, 구분선, 강조 바, 아이콘 원형
│
└─ 오디오/비디오인가? ─────────────────→ addMedia()
```

**절대 금지**:
- `addShape()`로 격자 그려 표 시뮬레이션 → `addTable()` 사용
- `addShape()`로 막대/원 그려 차트 시뮬레이션 → `addChart()` 사용

---

## 폰트 시스템

```
제목(Title):     Pretendard ExtraBold/Black    36~44pt
소제목:          Pretendard SemiBold/Bold       24~28pt
본문(Body):      Pretendard Regular/Medium      16~20pt
캡션:            Pretendard Light/Regular       12~14pt
인용구:          조선일보명조 Regular            18~22pt
숫자강조(KPI):   Pretendard Black               48~72pt
장식텍스트:      Pretendard Thin/ExtraLight     60~120pt
```

```javascript
const FONTS = {
  title:    { fontFace: 'Pretendard', bold: true },   // ExtraBold/Black
  subtitle: { fontFace: 'Pretendard', bold: true },   // SemiBold/Bold
  body:     { fontFace: 'Pretendard', bold: false },  // Regular/Medium
  caption:  { fontFace: 'Pretendard', bold: false },  // Light/Regular
  serif:    { fontFace: 'ChosunilboNM', bold: false },// 조선일보명조
  kpi:      { fontFace: 'Pretendard', bold: true },   // Black
};
```

**자간 & 줄간격**:
- 제목: `charSpacing: -0.5, lineSpacingMultiple: 1.1`
- 본문: `charSpacing: 0.5, lineSpacingMultiple: 1.4`
- 캡션: `charSpacing: 0.5, lineSpacingMultiple: 1.3`

---

## 색상 시스템 (6:3:1 법칙)

```javascript
const COLORS = {
  // 메인 60% — 배경/여백
  bg_primary:   'FFFFFF',  // 흰 배경
  bg_secondary: 'F5F7FA',  // 연한 회색 배경
  bg_dark:      '1A1F36',  // 다크 네이비 (표지/구분)

  // 보조 30% — 본문/구조
  text_primary:   '1A1F36', // 제목 텍스트
  text_secondary: '4A5568', // 본문 텍스트
  text_tertiary:  '718096', // 캡션/보조
  text_on_dark:   'FFFFFF', // 다크 배경 위 텍스트

  // 강조 10% — 포인트/CTA
  accent_blue:   '4A7BF7',  // 메인 블루
  accent_cyan:   '00D4AA',  // 시안 그린
  accent_yellow: 'FFB020',  // 골드 옐로우
  accent_red:    'FF6B6B',  // 경고 레드
  accent_purple: '8B5CF6',  // 보조 퍼플
};
```

---

## 레이아웃 시스템

슬라이드: 16:9 기준 **13.33" × 7.5"**

```javascript
// 표준 제목 바 추가 (모든 슬라이드에 사용)
function addTitleBar(slide, title, subtitle = '') {
  slide.addShape('rect', { x: 0.6, y: 0.5, w: 1.2, h: 0.06,
    fill: { color: COLORS.accent_blue } });
  slide.addText(title, { x: 0.6, y: 0.65, w: 10, h: 0.6,
    fontSize: 28, ...FONTS.title, color: COLORS.text_primary,
    charSpacing: -0.3, ...SAFE_TEXT });
  if (subtitle) {
    slide.addText(subtitle, { x: 0.6, y: 1.25, w: 10, h: 0.4,
      fontSize: 16, ...FONTS.body, color: COLORS.text_tertiary, ...SAFE_TEXT });
  }
}
```

---

## 핵심 레이아웃 패턴

전체 8개 패턴 상세 내용 → `docs/layout-patterns.md` 참조

### 패턴 1: 표지 (Title Slide)
- 전체 다크 배경 (`addShape` 전체 크기)
- 중앙: 과정명 44pt ExtraBold 흰색
- 하단: 발표자/날짜 14pt 50% 흰색

### 패턴 2: 섹션 구분 (Section Divider)
- 좌측 40% 다크 배경 / 우측 60% 밝은 배경
- 좌측: 섹션 번호 72pt Black, accent_cyan
- 우측: 섹션 제목 36pt Bold + 설명 16pt

### 패턴 3: 데이터 테이블 (★ 오버플로우 주의)
- 반드시 `addTable()` 사용
- 최대 8~10행 (헤더 포함)
- 초과 시 슬라이드 분할 + "(계속)" 표기

### 패턴 4: 차트+인사이트
- 좌측 60%: `addChart()` / 우측 40%: 핵심 인사이트
- 차트 크기: w≤12.13", h≤5.0" 준수

---

## 스타일 헬퍼 함수

### addStyledTable (오버플로우 가드 포함)

```javascript
const TS = {  // TABLE_STYLE 단축
  hdr: { bold: true, fill: { color: COLORS.bg_dark }, color: COLORS.text_on_dark,
         fontFace: 'Pretendard', fontSize: 11, align: 'center', valign: 'middle' },
  cel: { fontFace: 'Pretendard', fontSize: 11, color: COLORS.text_secondary, valign: 'middle' },
  alt: { fontFace: 'Pretendard', fontSize: 11, color: COLORS.text_secondary,
         fill: { color: COLORS.bg_secondary }, valign: 'middle' }
};

function addStyledTable(slide, headers, dataRows, opts = {}) {
  // ★ 오버플로우 가드: 최대 행 수 초과 시 잘라냄
  const rowH = opts.rowH?.[1] || 0.4;
  const max = maxTableRows(SAFE.contentH, rowH, 0.45);
  if (dataRows.length > max) dataRows = dataRows.slice(0, max);

  const rows = [ headers.map(h => ({ text: h, options: { ...TS.hdr } })) ];
  dataRows.forEach((row, i) => {
    const base = i % 2 === 1 ? TS.alt : TS.cel;
    rows.push(row.map(c => typeof c === 'string'
      ? { text: c, options: { ...base } }
      : { text: c.text, options: { ...base, ...c.options } }));
  });
  slide.addTable(rows, { x: 0.6, y: 1.8, w: 12.13,
    border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
    autoPage: false, margin: [5, 8, 5, 8], ...opts });
}
```

### addStyledChart (오버플로우 가드 포함)

```javascript
const CHART_STYLE = {
  base: {
    showTitle: true, titleFontFace: 'Pretendard', titleFontSize: 14,
    showLegend: true, legendFontFace: 'Pretendard', legendFontSize: 9,
    legendPos: 'b',  // ★ 하단 레전드 — 좌우 오버플로우 방지
    catAxisLabelFontFace: 'Pretendard', catAxisLabelFontSize: 10,
    valAxisLabelFontFace: 'Pretendard', valAxisLabelFontSize: 10,
  },
  colors: ['4A7BF7','00D4AA','FFB020','FF6B6B','8B5CF6','38BDF8']
};

function addStyledChart(slide, pptx, type, chartData, opts = {}) {
  // ★ 오버플로우 가드: x/y/w/h 클램핑
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

---

## QA 체크리스트

문서 생성 후 순서대로 확인:

**★★★ 오버플로우 검사 (최우선)**
- [ ] `validateBounds()` 함수 호출 및 오류 없음 확인
- [ ] 모든 요소의 x+w ≤ 12.73" 확인
- [ ] 모든 요소의 y+h ≤ 7.0" 확인
- [ ] 테이블 행 수 ≤ 10행 (초과 시 분할 완료 확인)
- [ ] 모든 `addText`에 `wrap: true, shrinkText: true` 적용 확인
- [ ] 차트 h ≤ 5.0" 및 legendPos: 'b' 확인
- [ ] 글머리 기호 ≤ 6개 / 줄당 한글 ≤ 18자 확인

**디자인 품질 검사**
- [ ] 제목 36~44pt / 소제목 24~28pt / 본문 16~20pt
- [ ] 색상 6:3:1 비율 준수
- [ ] 여백: 좌우 0.6" / 상하 0.5" 이상
- [ ] 한 슬라이드 1 메시지 원칙
- [ ] 폰트 2종 이내 (Pretendard + 명조)
- [ ] **표 데이터 → `addTable()` 사용 확인**
- [ ] **수치 비교/추이 → `addChart()` 사용 확인**
- [ ] **이미지/로고 → `addImage()` 사용 확인**

---

## 참고 문서

- `docs/pptxgenjs-elements.md` — PptxGenJS 요소별 상세 가이드 (addTable, addChart, addImage, addText, addShape, addNotes 전체 예시)
- `docs/layout-patterns.md` — 8개 레이아웃 패턴 전체, 슬라이드 구성 패턴 A/B/C, 2025-2026 디자인 트렌드, 추가 팔레트
