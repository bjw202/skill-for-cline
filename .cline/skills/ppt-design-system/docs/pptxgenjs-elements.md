# PptxGenJS 요소별 상세 가이드

SKILL.md의 오버플로우 방지 상수(`SAFE`, `SAFE_TEXT`, `COLORS`, `FONTS`)가 이미 선언되어 있다고 가정한다.

> **필수 전제**: 아래 모든 코드 예시는 `pptx.layout = 'LAYOUT_WIDE'`가 설정된 상태를 전제한다.
> 이 설정 없이는 모든 좌표가 틀어진다. (기본값 `LAYOUT_16x9`는 10"x5.625"로 이 스킬과 호환 안 됨)
>
> ```javascript
> const pptx = new PptxGenJS();
> pptx.layout = 'LAYOUT_WIDE';  // 13.33" x 7.5" — 필수!
> ```

---

## 1. addTable() — 테이블 상세 가이드

표 형식 데이터는 **반드시** `addTable()`을 사용한다.

### 테이블 스타일 상수

```javascript
const TABLE_STYLE = {
  header: {
    bold: true,
    fill: { color: COLORS.bg_dark },
    color: COLORS.text_on_dark,
    fontFace: 'Pretendard',
    fontSize: 11,   // ★ 테이블 셀은 최대 11pt (오버플로우 방지)
    align: 'center',
    valign: 'middle'
  },
  cell: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    valign: 'middle'
  },
  cellRight: {  // 숫자 셀 (우측 정렬)
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    align: 'right',
    valign: 'middle'
  },
  cellAlt: {  // zebra stripe (짝수행)
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    fill: { color: COLORS.bg_secondary },
    valign: 'middle'
  },
  cellTotal: {  // 합계/소계 행
    bold: true,
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_primary,
    border: [{ type: 'solid', pt: 1.5, color: COLORS.text_primary }, null, null, null],
    valign: 'middle'
  }
};

const TABLE_OPTIONS = {
  x: SAFE.x,     // 0.6"
  y: 1.8,        // 제목 바(~1.6") 아래 0.2" 간격
  w: SAFE.w,     // 12.13"
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
  autoPage: false,
  margin: [5, 8, 5, 8]  // [top, right, bottom, left] pt
};
```

### 헬퍼 함수: addTitledTable (colspan 제목 행 포함)

```javascript
/**
 * 테이블 제목 행(colspan 병합) + 헤더 + 데이터 행을 가진 테이블 추가
 * ★ 오버플로우 가드 내장
 */
function addTitledTable(slide, tableTitle, headers, dataRows, opts = {}) {
  const colCount = headers.length;
  const rowH = opts.rowH?.[1] || 0.4;
  const startY = opts.y || TABLE_OPTIONS.y || 1.8;
  const availH = SAFE.maxY - startY;  // ★ 실제 남은 높이 기준 계산
  const headerTotalH = 0.55 + 0.45; // 제목행 + 컬럼헤더행
  const maxRows = Math.floor((availH - headerTotalH) / rowH);

  if (dataRows.length > maxRows) {
    console.warn(`★ addTitledTable: ${dataRows.length}행 > 최대 ${maxRows}행. 분할 권장.`);
    dataRows = dataRows.slice(0, maxRows);
  }

  const rows = [];

  // 테이블 제목 행 (colspan 병합)
  rows.push([{
    text: tableTitle,
    options: {
      colspan: colCount, bold: true,
      fill: { color: COLORS.bg_dark }, color: COLORS.text_on_dark,
      fontFace: 'Pretendard', fontSize: 13,
      align: 'center', valign: 'middle'
    }
  }]);

  // 컬럼 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: {
      bold: true, fill: { color: COLORS.bg_secondary },
      color: COLORS.text_primary, fontFace: 'Pretendard',
      fontSize: 11, align: 'center', valign: 'middle'
    }
  })));

  // 데이터 행 (zebra stripe)
  dataRows.forEach((row, i) => {
    const base = i % 2 === 1 ? TABLE_STYLE.cellAlt : TABLE_STYLE.cell;
    rows.push(row.map(cell =>
      typeof cell === 'string'
        ? { text: cell, options: { ...base } }
        : { text: cell.text, options: { ...base, ...cell.options } }
    ));
  });

  slide.addTable(rows, { ...TABLE_OPTIONS, ...opts });
}
```

### 테이블 사용 예시

```javascript
// ===== 매출 계획표 =====
addTitledTable(slide, '2026년 매출 계획표',
  ['구분', 'Q1', 'Q2', 'Q3', 'Q4', '연간 합계'],
  [
    ['온라인',
     { text: '120M', options: { align: 'right' } },
     { text: '150M', options: { align: 'right' } },
     { text: '180M', options: { align: 'right' } },
     { text: '200M', options: { align: 'right' } },
     { text: '650M', options: { align: 'right', bold: true } }],
    ['오프라인',
     { text: '80M', options: { align: 'right' } },
     { text: '90M', options: { align: 'right' } },
     { text: '100M', options: { align: 'right' } },
     { text: '110M', options: { align: 'right' } },
     { text: '380M', options: { align: 'right', bold: true } }],
  ],
  { colW: [2, 1.8, 1.8, 1.8, 1.8, 2.5] }
);

// ===== 시간표/일정표 =====
addStyledTable(slide,
  ['교시', '시간', '과목', '내용', '비고'],
  [
    ['1', '09:00~09:50', 'Excel 기초', '데이터 정리 자동화', '이론'],
    ['2', '10:00~10:50', 'Excel 분석', 'KPI 대시보드 설계', '이론+실습'],
    ['3', '11:00~11:50', 'PPT 생성', '슬라이드 자동 변환', '이론'],
    // ★ 최대 8~10행 유지
  ],
  { colW: [1, 2.2, 2.5, 4, 1.8], rowH: [0.45, 0.4, 0.4, 0.4] }
);

// ===== 기능 비교표 =====
addStyledTable(slide,
  ['기능', 'Free', 'Pro', 'Enterprise'],
  [
    ['스킬 수', '12개', { text: '24개', options: { bold: true, color: COLORS.accent_blue } }, '무제한'],
    ['지원', '커뮤니티', '이메일', { text: '전담 매니저', options: { bold: true } }],
    ['가격', '무료', '월 9,900원', '문의'],
  ]
);
```

---

## 2. addChart() — 차트 상세 가이드

수치 데이터의 추이/비교/비율은 **반드시** `addChart()`를 사용한다.

### 차트 유형 선택 기준

| 데이터 유형 | 차트 유형 | PptxGenJS 상수 |
|------------|----------|---------------|
| 항목별 크기 비교 | 세로 막대 | `pptx.charts.BAR` |
| 시계열 추이/변화 | 꺾은선 | `pptx.charts.LINE` |
| 전체 대비 비율 (5개 이하) | 원형 | `pptx.charts.PIE` |
| 전체 대비 비율 (중앙 KPI) | 도넛 | `pptx.charts.DOUGHNUT` |
| 추이 + 누적량 | 영역 | `pptx.charts.AREA` |
| 다차원 항목 비교 | 방사형 | `pptx.charts.RADAR` |
| 두 변수 간 관계 | 산점도 | `pptx.charts.SCATTER` |
| 세 변수 관계 | 버블 | `pptx.charts.BUBBLE` |

### 차트 스타일 상수

```javascript
const CHART_STYLE = {
  base: {
    showTitle: true,
    titleFontFace: 'Pretendard', titleFontSize: 14,
    titleColor: COLORS.text_primary,
    showLegend: true,
    legendFontFace: 'Pretendard', legendFontSize: 9,
    legendColor: COLORS.text_secondary,
    legendPos: 'b',  // ★ 하단 레전드 — 좌우 오버플로우 방지
    catAxisLabelFontFace: 'Pretendard', catAxisLabelFontSize: 10,
    catAxisLabelColor: COLORS.text_tertiary,
    valAxisLabelFontFace: 'Pretendard', valAxisLabelFontSize: 10,
    valAxisLabelColor: COLORS.text_tertiary,
  },
  colors: [
    COLORS.accent_blue,   // 4A7BF7
    COLORS.accent_cyan,   // 00D4AA
    COLORS.accent_yellow, // FFB020
    COLORS.accent_red,    // FF6B6B
    COLORS.accent_purple, // 8B5CF6
    '38BDF8'              // 라이트 블루
  ]
};
```

### 차트 사용 예시

```javascript
// ===== 매출 추이 (꺾은선) =====
addStyledChart(slide, pptx, 'LINE',
  [{ name: '매출(억)', labels: ['1월','2월','3월','4월','5월','6월'],
     values: [12, 15, 18, 22, 25, 30] }],
  { x: 0.6, y: 1.8, w: 7, h: 4.5, title: '2026 상반기 매출 추이' }
);

// ===== 부서별 비교 (막대) =====
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '목표', labels: ['영업','마케팅','개발','인사'], values: [100, 80, 120, 50] },
    { name: '실적', labels: ['영업','마케팅','개발','인사'], values: [95, 85, 110, 48] }
  ],
  { x: 0.6, y: 1.8, w: 12.13, h: 4.8, title: '부서별 목표 대비 실적' }
  // ★ h: 4.8 (5.0 이하 준수)
);

// ===== 구성비 (원형) =====
addStyledChart(slide, pptx, 'PIE',
  [{ name: '점유율', labels: ['제품A','제품B','제품C','기타'],
     values: [45, 25, 20, 10] }],
  { x: 3, y: 1.5, w: 7, h: 4.8, title: '제품별 매출 구성비' }
);

// ===== 진행률 (도넛) =====
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행률', labels: ['완료','잔여'], values: [75, 25] }],
  { x: 4, y: 2, w: 5, h: 4.0, title: '프로젝트 진행률',
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
  // ★ h: 4.0 (시작 y=2.0, 끝 y=6.0 < maxY=7.0 안전)
);
```

---

## 3. addImage() — 이미지 가이드

```javascript
// 파일 경로로 삽입
slide.addImage({
  path: '/path/to/image.png',
  x: 0.6, y: 1.8, w: 5, h: 3.5
  // ★ 확인: 0.6+5=5.6 < 12.73 ✓ / 1.8+3.5=5.3 < 7.0 ✓
});

// SVG → PNG 변환 후 삽입 (sharp 라이브러리)
const sharp = require('sharp');
const pngBuffer = await sharp(Buffer.from(svgString)).png().toBuffer();
const base64 = pngBuffer.toString('base64');
slide.addImage({
  data: 'image/png;base64,' + base64,
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// 로고 삽입 (우측 하단, 슬라이드 경계 내)
slide.addImage({
  path: '/path/to/logo.png',
  x: 11.5, y: 6.5, w: 1.2, h: 0.45
  // ★ 확인: 11.5+1.2=12.7 < 12.73 ✓ / 6.5+0.45=6.95 < 7.0 ✓
});
```

---

## 4. addText() — 텍스트 가이드

```javascript
// ★ 모든 addText에 SAFE_TEXT({ wrap: true, shrinkText: true }) 적용 필수

// 제목 (오버플로우 안전)
slide.addText('슬라이드 제목', {
  x: 0.6, y: 0.65, w: 10, h: 0.6,
  fontSize: 28, ...FONTS.title,
  color: COLORS.text_primary, charSpacing: -0.3,
  ...SAFE_TEXT
});

// 글머리 기호 목록 (★ 최대 6개 항목)
slide.addText([
  { text: '첫 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '두 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '하위 항목',   options: { bullet: true, indentLevel: 1 } },
  // ★ 6개 초과 금지 — 초과 시 슬라이드 분할
], {
  x: 0.6, y: 1.8, w: 12.13, h: 4.5,  // ★ 1.8+4.5=6.3 < 7.0 ✓
  fontSize: 16, ...FONTS.body,
  color: COLORS.text_secondary,
  lineSpacingMultiple: 1.5,
  paraSpaceAfter: 6,
  ...SAFE_TEXT
});

// 번호 목록
slide.addText([
  { text: '첫 번째 단계', options: { bullet: { type: 'number' } } },
  { text: '두 번째 단계', options: { bullet: { type: 'number' } } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 3,
  fontSize: 16, ...FONTS.body,
  color: COLORS.text_secondary,
  ...SAFE_TEXT
});

// 인용문 (명조체)
slide.addText('"변화를 두려워하지 마세요"', {
  x: 2, y: 3, w: 9, h: 1,
  fontSize: 22, ...FONTS.serif, italic: true,
  color: COLORS.text_tertiary, align: 'center',
  ...SAFE_TEXT
  // ★ 확인: 2+9=11 < 12.73 ✓ / 3+1=4 < 7.0 ✓
});
```

---

## 5. addShape() — 장식/레이아웃 보조만

```javascript
// ✅ 올바른 사용: 전체 배경
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: { color: COLORS.bg_dark }
});

// ✅ 올바른 사용: 악센트 라인
slide.addShape('rect', {
  x: 0.6, y: 0.5, w: 1.2, h: 0.06,
  fill: { color: COLORS.accent_blue }
});

// ✅ 올바른 사용: 카드 배경 (둥근 모서리)
slide.addShape('roundRect', {
  x: 0.6, y: 1.8, w: 5.5, h: 3.0,
  rectRadius: 0.1,
  fill: { color: 'FFFFFF' },
  shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
  // ★ 확인: 0.6+5.5=6.1 < 12.73 ✓ / 1.8+3.0=4.8 < 7.0 ✓
});

// ✅ 올바른 사용: 구분선
slide.addShape('line', {
  x: 0.6, y: 4, w: 12.13, h: 0,
  line: { color: 'E2E8F0', width: 0.5 }
  // ★ 확인: 0.6+12.13=12.73 ≤ 12.73 ✓ / y=4 < 7.0 ✓
});

// ❌ 금지: 표 격자를 도형으로 그리기 → addTable() 사용
// ❌ 금지: 막대 차트를 사각형으로 그리기 → addChart() 사용
```

---

## 6. addNotes() — 발표자 노트

```javascript
slide.addNotes('이 슬라이드에서는 매출 추이를 설명합니다.\n핵심 포인트: Q3 성장률 40% 강조');
```

---

## 코드 컨벤션

### 폰트 상수 정의

```javascript
// PptxGenJS는 폰트 파일 임베딩을 직접 지원하지 않음
// 시스템에 Pretendard 및 조선일보명조가 설치된 환경에서 사용
const FONTS = {
  title:    { fontFace: 'Pretendard', bold: true },
  subtitle: { fontFace: 'Pretendard', bold: true },
  body:     { fontFace: 'Pretendard', bold: false },
  caption:  { fontFace: 'Pretendard', bold: false },
  serif:    { fontFace: 'ChosunilboNM', bold: false }, // 조선일보명조
  kpi:      { fontFace: 'Pretendard', bold: true },
  deco:     { fontFace: 'Pretendard', bold: false },   // Thin/ExtraLight
};

const FONT_DIR = path.join(__dirname, 'fonts'); // OTF 파일 경로
```

### 페이지 번호 추가

```javascript
function addPageNumber(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 11.6, y: 6.6, w: 0.9, h: 0.3,
    // ★ 확인: 11.6+0.9=12.5 < 12.73 ✓ / 6.6+0.3=6.9 < 7.0 ✓
    fontSize: 9, ...FONTS.caption,
    color: COLORS.text_tertiary, align: 'right',
    ...SAFE_TEXT
  });
}
```

### 카드 생성 함수

```javascript
function addCard(slide, { x, y, w, h, title, body, accentColor }) {
  // ★ 오버플로우 가드
  const rightEdge = x + w;
  const bottomEdge = y + h;
  if (rightEdge > SAFE.maxX) console.warn(`카드 우측 초과: ${rightEdge}"`);
  if (bottomEdge > SAFE.maxY) console.warn(`카드 하단 초과: ${bottomEdge}"`);

  // 카드 배경
  slide.addShape('roundRect', {
    x, y, w, h, rectRadius: 0.1,
    fill: { color: 'FFFFFF' },
    shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
  });
  // 상단 accent 바
  slide.addShape('rect', {
    x: x + 0.02, y, w: w - 0.04, h: 0.06,
    fill: { color: accentColor || COLORS.accent_blue }
  });
  // 카드 제목
  slide.addText(title, {
    x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.35,
    fontSize: 16, ...FONTS.subtitle, color: COLORS.text_primary,
    ...SAFE_TEXT
  });
  // 카드 본문
  slide.addText(body, {
    x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.75,
    fontSize: 13, ...FONTS.body, color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, valign: 'top',
    ...SAFE_TEXT
  });
}
```
