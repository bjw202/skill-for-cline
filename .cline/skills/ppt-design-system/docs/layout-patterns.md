# 레이아웃 패턴 & 슬라이드 구성 가이드

SKILL.md의 오버플로우 방지 상수(`SAFE`, `SAFE_TEXT`, `COLORS`, `FONTS`, `addTitleBar`, `addStyledTable`, `addStyledChart`)가 이미 선언되어 있다고 가정한다.

> **필수 전제**: 아래 모든 코드 예시는 `pptx.layout = 'LAYOUT_WIDE'`가 설정된 상태를 전제한다.
> 이 설정 없이는 모든 좌표가 틀어진다. (기본값 `LAYOUT_16x9`는 10"x5.625"로 이 스킬과 호환 안 됨)
>
> ```javascript
> const pptx = new PptxGenJS();
> pptx.layout = 'LAYOUT_WIDE';  // 13.33" x 7.5" — 필수!
> ```

---

## 8개 핵심 레이아웃 패턴

### 패턴 1: 표지 (Title Slide)

```
[전체 다크 배경]
  중앙: 과정명 (44pt ExtraBold, 흰색)
  중앙 아래: 부제목 (20pt Regular, 70% 흰색)
  하단: 발표자/날짜 (14pt, 50% 흰색)
```

```javascript
function createTitleSlide(pptx, title, subtitle, presenter, date) {
  // ★★★★ 최초 슬라이드 생성 전 반드시 확인
  // pptx.layout = 'LAYOUT_WIDE'; // 13.33" x 7.5" (PptxGenJS 인스턴스 생성 직후 1회 설정)
  const slide = pptx.addSlide();
  // 전체 다크 배경
  slide.addShape('rect', { x: 0, y: 0, w: '100%', h: '100%',
    fill: { color: COLORS.bg_dark } });
  // accent 라인
  slide.addShape('rect', { x: 0.6, y: 3.2, w: 1.5, h: 0.06,
    fill: { color: COLORS.accent_cyan } });
  // 메인 제목
  slide.addText(title, {
    x: 0.6, y: 2.2, w: 12.13, h: 1.2,
    fontSize: 44, ...FONTS.title, color: 'FFFFFF',
    charSpacing: -0.5, align: 'left', ...SAFE_TEXT
  });
  // 부제목
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.6, y: 3.5, w: 12.13, h: 0.7,
      fontSize: 20, ...FONTS.body, color: 'FFFFFFB3', // 70% 흰색
      align: 'left', ...SAFE_TEXT
    });
  }
  // 발표자 / 날짜
  slide.addText(`${presenter}  |  ${date}`, {
    x: 0.6, y: 6.5, w: 12.13, h: 0.4,
    // ★ 확인: 6.5+0.4=6.9 < 7.0 ✓
    fontSize: 14, ...FONTS.caption, color: 'FFFFFF80', // 50% 흰색
    align: 'left', ...SAFE_TEXT
  });
  return slide;
}
```

---

### 패턴 2: 섹션 구분 (Section Divider)

```
[좌측 40% 다크 배경 | 우측 60% 밝은 배경]
  좌측: 섹션 번호 (72pt Black, accent_cyan)
  우측: 섹션 제목 (36pt Bold) + 설명 (16pt Regular)
```

```javascript
function createSectionSlide(pptx, number, sectionTitle, description) {
  const slide = pptx.addSlide();
  // 좌측 다크 패널 (40% = 5.33")
  slide.addShape('rect', { x: 0, y: 0, w: 5.33, h: '100%',
    fill: { color: COLORS.bg_dark } });
  // 섹션 번호
  slide.addText(`${String(number).padStart(2, '0')}`, {
    x: 0.6, y: 2.5, w: 4.0, h: 2.0,
    fontSize: 72, ...FONTS.kpi, color: COLORS.accent_cyan,
    align: 'center', valign: 'middle', ...SAFE_TEXT
  });
  // 구분선
  slide.addShape('rect', { x: 5.33, y: 1.5, w: 0.06, h: 4.5,
    fill: { color: COLORS.accent_blue } });
  // 섹션 제목
  slide.addText(sectionTitle, {
    x: 5.7, y: 2.3, w: 7.0, h: 1.2,
    // ★ 확인: 5.7+7.0=12.7 < 12.73 ✓
    fontSize: 36, ...FONTS.title, color: COLORS.text_primary,
    charSpacing: -0.3, ...SAFE_TEXT
  });
  // 설명
  slide.addText(description, {
    x: 5.7, y: 3.8, w: 7.0, h: 2.5,
    fontSize: 16, ...FONTS.body, color: COLORS.text_secondary,
    lineSpacingMultiple: 1.5, ...SAFE_TEXT
  });
  return slide;
}
```

---

### 패턴 3: 2단 콘텐츠 (Two Column)

```
[상단: 제목 바]
[좌측 50% | 우측 50%] — 간격 0.4"
  각 컬럼: 소제목 (24pt Bold) + 본문 (16pt Regular)
```

```javascript
function createTwoColumnSlide(pptx, title, leftContent, rightContent) {
  const slide = pptx.addSlide();
  addTitleBar(slide, title);

  const colW = (SAFE.w - 0.4) / 2; // (12.13 - 0.4) / 2 = 5.865"
  const colY = SAFE.titleY;         // 1.6"
  const colH = SAFE.maxY - colY;    // 5.4"

  // 좌측 컬럼
  slide.addText(leftContent.title, {
    x: SAFE.x, y: colY, w: colW, h: 0.5,
    fontSize: 20, ...FONTS.subtitle, color: COLORS.text_primary, ...SAFE_TEXT
  });
  slide.addText(leftContent.body, {
    x: SAFE.x, y: colY + 0.6, w: colW, h: colH - 0.7,
    fontSize: 16, ...FONTS.body, color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, ...SAFE_TEXT
  });

  // 구분선
  const divX = SAFE.x + colW + 0.2;
  slide.addShape('line', { x: divX, y: colY, w: 0, h: colH - 0.2,
    line: { color: 'E2E8F0', width: 0.5 } });

  // 우측 컬럼
  const rightX = divX + 0.2;
  slide.addText(rightContent.title, {
    x: rightX, y: colY, w: colW, h: 0.5,
    fontSize: 20, ...FONTS.subtitle, color: COLORS.text_primary, ...SAFE_TEXT
  });
  slide.addText(rightContent.body, {
    x: rightX, y: colY + 0.6, w: colW, h: colH - 0.7,
    // ★ 확인: rightX+colW ≈ 6.26+5.865=12.12 < 12.73 ✓
    fontSize: 16, ...FONTS.body, color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, ...SAFE_TEXT
  });
  return slide;
}
```

---

### 패턴 4: 카드 그리드 (Card Grid)

```
[상단: 제목 바]
[2x2 또는 2x3 카드 그리드] — 카드 간격 0.3"
  각 카드: 둥근 모서리(rectRadius=0.1) + accent 색상 상단 바
```

```javascript
// 2x2 카드 그리드 예시 (4개 카드)
function createCardGridSlide(pptx, title, cards) {
  const slide = pptx.addSlide();
  addTitleBar(slide, title);

  const gap = 0.3;
  const cols = 2;
  const rows = Math.ceil(cards.length / cols);
  const cardW = (SAFE.w - gap * (cols - 1)) / cols; // (12.13 - 0.3) / 2 = 5.915"
  const availH = SAFE.contentH - 0.1;               // 5.4 - 0.1 = 5.3"
  const cardH = (availH - gap * (rows - 1)) / rows; // 2x2: (5.3-0.3)/2 = 2.5"

  cards.slice(0, cols * rows).forEach((card, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = SAFE.x + col * (cardW + gap);
    const y = SAFE.titleY + row * (cardH + gap);
    // ★ 확인: x+cardW ≤ 12.73, y+cardH ≤ 7.0
    addCard(slide, {
      x, y, w: cardW, h: cardH,
      title: card.title, body: card.body,
      accentColor: card.accentColor || COLORS.accent_blue
    });
  });
  return slide;
}
```

---

### 패턴 5: 타임라인 (Timeline)

```
[상단: 제목 바]
[좌측 색상 바 | 우측 항목 리스트]
  각 항목: 시간 (Bold) + 내용 (Regular) + 구분선
```

```javascript
function createTimelineSlide(pptx, title, items) {
  const slide = pptx.addSlide();
  addTitleBar(slide, title);

  const maxItems = 5; // ★ 5개 초과 시 슬라이드 분할
  const safeItems = items.slice(0, maxItems);
  const itemH = SAFE.contentH / safeItems.length;

  // 세로 타임라인 선
  slide.addShape('rect', { x: 1.8, y: SAFE.titleY, w: 0.06, h: SAFE.contentH,
    fill: { color: COLORS.accent_blue } });

  safeItems.forEach((item, i) => {
    const y = SAFE.titleY + i * itemH;
    // 타임라인 도트
    slide.addShape('ellipse', { x: 1.65, y: y + itemH / 2 - 0.12, w: 0.24, h: 0.24,
      fill: { color: COLORS.accent_blue } });
    // 시간 텍스트
    slide.addText(item.time, {
      x: SAFE.x, y: y + itemH / 2 - 0.2, w: 1.1, h: 0.4,
      fontSize: 13, ...FONTS.subtitle, color: COLORS.accent_blue,
      align: 'right', ...SAFE_TEXT
    });
    // 내용
    slide.addText(item.content, {
      x: 2.2, y: y + 0.1, w: SAFE.maxX - 2.2, h: itemH - 0.2,
      // ★ 확인: 2.2+(12.73-2.2)=12.73 ✓
      fontSize: 15, ...FONTS.body, color: COLORS.text_secondary,
      lineSpacingMultiple: 1.4, valign: 'middle', ...SAFE_TEXT
    });
    // 구분선 (마지막 항목 제외)
    if (i < safeItems.length - 1) {
      slide.addShape('line', { x: SAFE.x, y: y + itemH, w: SAFE.w, h: 0,
        line: { color: 'E2E8F0', width: 0.3 } });
    }
  });
  return slide;
}
```

---

### 패턴 6: KPI 대시보드 (Data Dashboard)

```
[상단: 제목 바]
[3~4열 KPI 카드] — Pretendard Black 48pt 숫자
[하단: addChart() 차트 영역]
```

```javascript
function createKPIDashboard(pptx, title, kpis, chartData) {
  const slide = pptx.addSlide();
  addTitleBar(slide, title);

  const kpiCount = Math.min(kpis.length, 4); // ★ 최대 4개
  const kpiW = SAFE.w / kpiCount;
  const kpiH = 1.5;
  const kpiY = SAFE.titleY;

  // KPI 카드들
  kpis.slice(0, kpiCount).forEach((kpi, i) => {
    const x = SAFE.x + i * kpiW;
    // KPI 숫자
    slide.addText(kpi.value, {
      x, y: kpiY, w: kpiW, h: 0.9,
      fontSize: 48, ...FONTS.kpi, color: COLORS.accent_blue,
      align: 'center', ...SAFE_TEXT
    });
    // KPI 라벨
    slide.addText(kpi.label, {
      x, y: kpiY + 0.9, w: kpiW, h: 0.4,
      fontSize: 13, ...FONTS.caption, color: COLORS.text_tertiary,
      align: 'center', ...SAFE_TEXT
    });
  });

  // 차트 (하단 영역)
  const chartY = kpiY + kpiH + 0.2;
  const chartH = Math.min(SAFE.maxY - chartY, 4.0); // ★ 오버플로우 방지
  if (chartData) {
    addStyledChart(slide, chartData.pptx, chartData.type, chartData.data, {
      x: SAFE.x, y: chartY, w: SAFE.w, h: chartH,
      showTitle: false
    });
  }
  return slide;
}
```

---

### 패턴 7: 데이터 테이블 (Data Table)

```
[상단: 제목 바]
[네이티브 테이블: addTable()]
  헤더: 다크 배경 + 흰색 텍스트
  짝수행: zebra stripe (bg_secondary)
  합계행: bold + 상단 border 강조
  ★ 최대 8~10행 (초과 시 슬라이드 분할)
```

```javascript
// 다중 슬라이드 테이블 분할 함수
function createDataTableSlides(pptx, title, headers, allRows, rowsPerSlide = 8) {
  const slides = [];
  const chunks = [];
  for (let i = 0; i < allRows.length; i += rowsPerSlide) {
    chunks.push(allRows.slice(i, i + rowsPerSlide));
  }

  chunks.forEach((chunk, pageIdx) => {
    const slide = pptx.addSlide();
    const slideTitle = chunks.length > 1
      ? `${title} (${pageIdx + 1}/${chunks.length})`
      : title;
    addTitleBar(slide, slideTitle);
    addStyledTable(slide, headers, chunk, {
      y: SAFE.titleY + 0.2,
      rowH: new Array(chunk.length + 1).fill(0.42)
    });
    slides.push(slide);
  });
  return slides;
}
```

---

### 패턴 8: 차트+인사이트 (Chart & Insight)

```
[상단: 제목 바]
[좌측 60%: addChart() | 우측 40%: 핵심 인사이트]
  인사이트: KPI 스타일 숫자 + 짧은 설명
```

```javascript
function createChartInsightSlide(pptx, title, chartDef, insights) {
  const slide = pptx.addSlide();
  addTitleBar(slide, title);

  const chartW = SAFE.w * 0.6;  // 7.278"
  const insightW = SAFE.w * 0.4 - 0.3; // 4.552"
  const contentY = SAFE.titleY;
  const contentH = SAFE.contentH;

  // 좌측 차트
  addStyledChart(slide, chartDef.pptx, chartDef.type, chartDef.data, {
    x: SAFE.x, y: contentY,
    w: chartW, h: Math.min(contentH, 5.0) // ★ h ≤ 5.0"
  });

  // 우측 인사이트 패널
  const insightX = SAFE.x + chartW + 0.3;
  const insightPerH = contentH / Math.min(insights.length, 3);

  insights.slice(0, 3).forEach((insight, i) => {
    const y = contentY + i * insightPerH;
    // 숫자 강조
    slide.addText(insight.value, {
      x: insightX, y: y, w: insightW, h: insightPerH * 0.5,
      fontSize: 36, ...FONTS.kpi, color: COLORS.accent_blue,
      align: 'center', ...SAFE_TEXT
    });
    // 설명
    slide.addText(insight.description, {
      x: insightX, y: y + insightPerH * 0.5, w: insightW, h: insightPerH * 0.45,
      // ★ 확인: insightX+insightW ≈ 12.73 ✓
      fontSize: 14, ...FONTS.body, color: COLORS.text_secondary,
      align: 'center', lineSpacingMultiple: 1.3, ...SAFE_TEXT
    });
  });
  return slide;
}
```

---

## 실전 슬라이드 구성 패턴

### 패턴 A: 매출 보고 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '월별 매출 실적', '2026년 상반기');

// 상단: KPI 카드 3개 (addText + addShape)
const kpiData = [
  { label: '매출 합계', value: '₩3.2B' },
  { label: '전년 대비',  value: '+18%' },
  { label: '목표 달성률', value: '94%' }
];
const colors = [COLORS.accent_blue, COLORS.accent_cyan, COLORS.accent_yellow];
kpiData.forEach((kpi, i) => {
  addCard(slide, {
    x: SAFE.x + i * 4.1, y: 1.6, w: 3.8, h: 1.2,
    // ★ 확인: 0.6+(2*4.1)+3.8=12.6 < 12.73 ✓ / 1.6+1.2=2.8 < 7.0 ✓
    title: kpi.label, body: kpi.value, accentColor: colors[i]
  });
});

// 중단: 데이터 테이블 (addTable) — 최대 8행
addStyledTable(slide, ['월','매출','비용','영업이익','이익률'],
  monthlyData.slice(0, 8), // ★ 8행 이하로 제한
  { y: 3.0, rowH: new Array(9).fill(0.42) }
);
// ★ 검증: y=3.0, h=(0.45+8*0.42)=3.81 → 끝: 6.81 < 7.0 ✓
```

### 패턴 B: 비교 분석 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '경쟁사 비교 분석');

// 좌측 60%: 차트 (addChart)
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '자사',   labels: ['가격','품질','서비스','인지도'], values: [85, 92, 88, 70] },
    { name: '경쟁A', labels: ['가격','품질','서비스','인지도'], values: [90, 80, 75, 85] }
  ],
  { x: SAFE.x, y: SAFE.titleY, w: 7.0, h: 5.0, title: '' }
  // ★ 확인: 0.6+7.0=7.6 < 12.73 ✓ / 1.6+5.0=6.6 < 7.0 ✓
);

// 우측 40%: 비교표 (addTable) — 최대 6행
addStyledTable(slide, ['항목','자사','경쟁A'],
  [
    ['가격',    '85', '90'],
    ['품질',    '92', '80'],
    ['서비스',  '88', '75'],
    ['인지도',  '70', '85'],
  ],
  { x: 8.0, y: SAFE.titleY, w: 4.73 }
  // ★ 확인: 8.0+4.73=12.73 ✓ / 행수(4) ≤ 8 ✓
);
```

### 패턴 C: 프로젝트 현황 대시보드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '프로젝트 현황 대시보드', '2026년 2월 기준');

// 좌측 상단: 진행률 도넛 (addChart)
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행', labels: ['완료','잔여'], values: [72, 28] }],
  { x: SAFE.x, y: SAFE.titleY, w: 4.0, h: 3.2,
    showTitle: false, chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
  // ★ 확인: 0.6+4.0=4.6 < 12.73 ✓ / 1.6+3.2=4.8 < 7.0 ✓
);

// 우측 상단: 주간 이슈 테이블 (addTable) — 최대 4행
addStyledTable(slide, ['이슈','담당','상태','기한'],
  [
    ['서버 지연', '김개발', '진행중', '2/20'],
    ['UI 버그',  '박디자', '완료',   '2/18'],
    // ★ 최대 4행 (헤더 포함 5행)
  ],
  { x: 5.0, y: SAFE.titleY, w: 7.73,
    rowH: [0.42, 0.38, 0.38] }
  // ★ 확인: 5.0+7.73=12.73 ✓ / 1.6+(0.42+0.38+0.38)=2.78 < 7.0 ✓
);

// 하단: 마일스톤 테이블 (addTable) — 최대 4행
addStyledTable(slide, ['마일스톤','시작일','종료일','진행률','상태'],
  [
    ['기획', '1/15', '2/10', '100%', '✅'],
    ['개발', '2/11', '4/30', '45%',  '🔧'],
    ['테스트', '5/1', '5/31', '0%',  '⏳'],
  ],
  { x: SAFE.x, y: 5.0, w: SAFE.w,
    rowH: [0.42, 0.38, 0.38, 0.38] }
  // ★ 확인: y=5.0, h=(0.42+3*0.38)=1.56 → 끝: 6.56 < 7.0 ✓
);
```

---

## 추가 팔레트 옵션

### Warm Corporate (따뜻한 기업 톤)

```javascript
const WARM = {
  bg_dark: '2D1B4E', accent_blue: 'E8725A',
  accent_cyan: '4ECDC4', accent_yellow: 'F9C74F', accent_purple: '7B68EE'
};
```

### Nature Green (친환경/ESG)

```javascript
const GREEN = {
  bg_dark: '1B3A2D', accent_blue: '2D9CDB',
  accent_cyan: '27AE60', accent_yellow: 'F2C94C', accent_red: 'EB5757'
};
```

### Minimal Mono (미니멀)

```javascript
const MONO = {
  bg_dark: '111111', accent_blue: '333333',
  accent_cyan: '666666', accent_yellow: 'AAAAAA', text_primary: '111111'
};
```

---

## 2025-2026 한국형 PPT 디자인 트렌드

### 기능적 미니멀리즘
- 불필요한 장식 요소 배제, 콘텐츠 중심 디자인
- 넓은 여백(White Space) 적극 활용
- 한 슬라이드 = 한 메시지 원칙 강화
- 배경: 순백(#FFFFFF) 또는 연한 회색(#F5F7FA~#F8FAFC)

### 모듈형 레이아웃
- 카드 기반 그리드 시스템 (2x2, 2x3, 1+2 변형)
- 모듈 간 일관된 간격(0.3"~0.4") 유지
- 반복 가능한 레이아웃으로 일관성 확보

### 포인트 컬러 전략
- 배경: 라이트 그레이 (#F5F7FA)
- 포인트: 네이비(#1A1F36) + 1~2가지 악센트 컬러
- 6:3:1 법칙 엄수
- 그라데이션보다 단색(Flat) 선호

### 타이포그래피
- **Pretendard**: 한국 비즈니스 PPT 표준 폰트
- 제목은 ExtraBold~Black, 본문은 Regular~Medium
- 자간: 제목 타이트(-0.5pt), 본문 약간 넓게(+0.5pt)
- 명조체(조선일보명조)는 인용구/강조에만 포인트 사용

### 데이터 시각화 강화
- 숫자 중심 KPI 카드 레이아웃
- 복잡한 3D 차트 대신 2D 플랫 차트 (`addChart()` 활용)
- 아이콘 + 숫자 조합의 인포그래픽 스타일
- SVG 도식화 연계 (svg-diagram 스킬 활용)

### 이미지 & 아이콘 가이드
- SVG 아이콘 → sharp로 PNG 변환 후 `addImage()` 삽입
- Hero Image: 슬라이드당 핵심 이미지 1개
- 이미지 선택 기준: 주제, 분위기, 해상도, 색상, 여백
