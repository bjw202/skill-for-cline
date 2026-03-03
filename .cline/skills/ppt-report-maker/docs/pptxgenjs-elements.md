# PptxGenJS 요소별 상세 가이드

SKILL.md의 오버플로우 방지 상수(`SAFE`, `SAFE_TITLE`, `SAFE_TEXT`, `COLORS`, `FONTS`)가 이미 선언되어 있다고 가정한다.

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
    bold: true, fill: { color: COLORS.bg_dark }, color: COLORS.text_on_dark,
    fontFace: 'Pretendard', fontSize: 12, align: 'center', valign: 'middle'
  },
  cell: {
    fontFace: 'Pretendard', fontSize: 12,
    color: COLORS.text_secondary, valign: 'middle'
  },
  cellRight: {
    fontFace: 'Pretendard', fontSize: 12,
    color: COLORS.text_secondary, align: 'right', valign: 'middle'
  },
  cellAlt: {
    fontFace: 'Pretendard', fontSize: 12,
    color: COLORS.text_secondary, fill: { color: COLORS.bg_secondary }, valign: 'middle'
  },
  cellTotal: {
    bold: true, fontFace: 'Pretendard', fontSize: 12,
    color: COLORS.text_primary,
    border: [{ type: 'solid', pt: 1.5, color: COLORS.text_primary }, null, null, null],
    valign: 'middle'
  }
};

const TABLE_OPTIONS = {
  x: SAFE.x,     // 0.6"
  y: 1.8,        // 제목 바 아래
  w: SAFE.w,     // 12.13"
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
  autoPage: false,
  margin: [5, 8, 5, 8]
};
```

### 헬퍼 함수: addTitledTable (colspan 제목 행 포함)

```javascript
function addTitledTable(slide, tableTitle, headers, dataRows, opts = {}) {
  const colCount = headers.length;
  const rowH = opts.rowH?.[1] || 0.4;
  const startY = opts.y || TABLE_OPTIONS.y || 1.8;
  const availH = SAFE.maxY - startY;
  const headerTotalH = 0.55 + 0.45;
  const maxRows = Math.floor((availH - headerTotalH) / rowH);
  if (dataRows.length > maxRows) {
    console.warn(`addTitledTable: ${dataRows.length}행 > 최대 ${maxRows}행. 분할 권장.`);
    dataRows = dataRows.slice(0, maxRows);
  }
  const rows = [];
  // 테이블 제목 행 (colspan 병합)
  rows.push([{
    text: tableTitle,
    options: {
      colspan: colCount, bold: true,
      fill: { color: COLORS.bg_dark }, color: COLORS.text_on_dark,
      fontFace: 'Pretendard', fontSize: 14,
      align: 'center', valign: 'middle'
    }
  }]);
  // 컬럼 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: {
      bold: true, fill: { color: COLORS.bg_secondary },
      color: COLORS.text_primary, fontFace: 'Pretendard',
      fontSize: 12, align: 'center', valign: 'middle'
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
// 매출 계획표
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

// 시간표/일정표
addStyledTable(slide,
  ['교시', '시간', '과목', '내용', '비고'],
  [
    ['1', '09:00~09:50', 'Excel 기초', '데이터 정리 자동화', '이론'],
    ['2', '10:00~10:50', 'Excel 분석', 'KPI 대시보드 설계', '이론+실습'],
    ['3', '11:00~11:50', 'PPT 생성', '슬라이드 자동 변환', '이론'],
  ],
  { colW: [1, 2.2, 2.5, 4, 1.8], rowH: [0.45, 0.4, 0.4, 0.4] }
);

// 기능 비교표
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

### 차트 사용 예시

```javascript
// 매출 추이 (꺾은선)
addStyledChart(slide, pptx, 'LINE',
  [{ name: '매출(억)', labels: ['1월','2월','3월','4월','5월','6월'],
     values: [12, 15, 18, 22, 25, 30] }],
  { x: 0.6, y: 1.8, w: 7, h: 4.5, title: '2026 상반기 매출 추이' }
);

// 부서별 비교 (막대)
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '목표', labels: ['영업','마케팅','개발','인사'], values: [100, 80, 120, 50] },
    { name: '실적', labels: ['영업','마케팅','개발','인사'], values: [95, 85, 110, 48] }
  ],
  { x: 0.6, y: 1.8, w: 12.13, h: 4.8, title: '부서별 목표 대비 실적' }
);

// 구성비 (원형)
addStyledChart(slide, pptx, 'PIE',
  [{ name: '점유율', labels: ['제품A','제품B','제품C','기타'],
     values: [45, 25, 20, 10] }],
  { x: 3, y: 1.5, w: 7, h: 4.8, title: '제품별 매출 구성비' }
);

// 진행률 (도넛)
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행률', labels: ['완료','잔여'], values: [75, 25] }],
  { x: 4, y: 2, w: 5, h: 4.0, title: '프로젝트 진행률',
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
);
```

---

## 3. addImage() — 이미지 가이드

```javascript
// 파일 경로로 삽입
slide.addImage({
  path: '/path/to/image.png',
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// SVG -> PNG 변환 후 삽입 (sharp 라이브러리)
const sharp = require('sharp');
const pngBuffer = await sharp(Buffer.from(svgString)).png().toBuffer();
const base64 = pngBuffer.toString('base64');
slide.addImage({
  data: 'image/png;base64,' + base64,
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// 로고 삽입 (우측 하단)
slide.addImage({
  path: '/path/to/logo.png',
  x: 11.5, y: 6.5, w: 1.2, h: 0.45
  // 11.5+1.2=12.7 < 12.73, 6.5+0.45=6.95 < 7.0
});
```

---

## 4. addText() — 텍스트 가이드

```javascript
// 제목 (SAFE_TITLE — 폰트 크기 유지)
slide.addText('슬라이드 제목', {
  x: 0.6, y: 0.65, w: 10, h: 0.6,
  fontSize: 32, ...FONTS.title,
  color: COLORS.text_primary, charSpacing: -0.3,
  ...SAFE_TITLE
});

// 글머리 기호 목록 (최대 6개 항목)
slide.addText([
  { text: '첫 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '두 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '하위 항목',   options: { bullet: true, indentLevel: 1 } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 4.5,
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
});
```

---

## 5. addShape() — 장식/레이아웃 보조만

```javascript
// 전체 배경
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: { color: COLORS.bg_dark }
});

// 악센트 라인
slide.addShape('rect', {
  x: 0.6, y: 0.5, w: 1.2, h: 0.06,
  fill: { color: COLORS.accent_blue }
});

// 카드 배경 (둥근 모서리)
slide.addShape('roundRect', {
  x: 0.6, y: 1.8, w: 5.5, h: 3.0,
  rectRadius: 0.1,
  fill: { color: 'FFFFFF' },
  shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
});

// 구분선
slide.addShape('line', {
  x: 0.6, y: 4, w: 12.13, h: 0,
  line: { color: 'E2E8F0', width: 0.5 }
});

// 금지: 표 격자를 도형으로 그리기 -> addTable() 사용
// 금지: 막대 차트를 사각형으로 그리기 -> addChart() 사용
```

---

## 6. addNotes() — 발표자 노트

```javascript
slide.addNotes('이 슬라이드에서는 매출 추이를 설명합니다.\n핵심 포인트: Q3 성장률 40% 강조');
```

---

## 텍스트 높이 계산 함수

```javascript
function calcTextHeight(text, fontSize, lineSpacing = 1.4, maxWidthInch = 12.13) {
  const ptPerInch = 72;
  const charsPerLine = Math.floor((maxWidthInch * ptPerInch) / fontSize * 1.8);
  const lineCount = Math.ceil(text.length / charsPerLine);
  return lineCount * (fontSize * lineSpacing / ptPerInch);
}

// 사용 예시: 배치 전 높이 확인
const textH = calcTextHeight(myText, 16, 1.4, 12.13);
if (SAFE.titleY + textH > SAFE.maxY) {
  console.warn('텍스트가 슬라이드를 초과합니다. 분할 필요.');
}
```

---

## 코드 컨벤션

### 폰트 파일 참고

```javascript
// PptxGenJS는 폰트 파일 임베딩을 직접 지원하지 않음
// 시스템에 Pretendard 및 조선일보명조가 설치된 환경에서 사용
const FONT_DIR = path.join(__dirname, 'fonts'); // OTF 파일 경로
```

**포함 폰트 파일 (fonts/ 디렉토리):**
- Pretendard-Thin.otf ~ Pretendard-Black.otf (9종)
- ChosunNm.ttf (조선일보명조)
