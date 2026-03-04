# JSON 템플릿 스키마 명세

doc-template-analyzer와 doc-generator가 공유하는 JSON 템플릿의 전체 구조 명세.

---

## 최상위 구조

```json
{
  "meta": {},
  "page_setup": {},
  "sections": [],
  "styles": {},
  "numbering": {},
  "content": []
}
```

---

## meta (메타데이터)

```json
{
  "meta": {
    "source_file": "보고서양식.docx",
    "analyzed_at": "2026-03-04T10:00:00",
    "analyzer_version": "1.0.0",
    "page_count": 12,
    "word_count": 3500
  }
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| source_file | string | Y | 원본 파일명 |
| analyzed_at | string | Y | 분석 시각 (ISO 8601) |
| analyzer_version | string | Y | 분석기 버전 |
| page_count | integer | N | 페이지 수 |
| word_count | integer | N | 단어 수 |

---

## page_setup (기본 페이지 설정)

문서의 기본 페이지 설정. 섹션별 개별 설정은 `sections[].page_setup`에서 오버라이드.

```json
{
  "page_setup": {
    "orientation": "portrait",
    "page_width_cm": 21.0,
    "page_height_cm": 29.7,
    "margin_top_cm": 2.54,
    "margin_bottom_cm": 2.54,
    "margin_left_cm": 3.17,
    "margin_right_cm": 3.17,
    "header_distance_cm": 1.27,
    "footer_distance_cm": 1.27,
    "gutter_cm": 0.0
  }
}
```

| 필드 | 타입 | 필수 | 기본값 | 설명 |
|------|------|------|--------|------|
| orientation | string | Y | "portrait" | "portrait" 또는 "landscape" |
| page_width_cm | float | Y | 21.0 | 용지 너비 (cm) |
| page_height_cm | float | Y | 29.7 | 용지 높이 (cm) |
| margin_*_cm | float | Y | - | 상하좌우 여백 (cm) |
| header_distance_cm | float | N | 1.27 | 머리글 거리 (cm) |
| footer_distance_cm | float | N | 1.27 | 바닥글 거리 (cm) |
| gutter_cm | float | N | 0.0 | 제본 여백 (cm) |

---

## sections (섹션 목록)

```json
{
  "sections": [
    {
      "index": 0,
      "page_setup": { "...": "page_setup과 동일 구조" },
      "has_different_first_page": true,
      "headers": {
        "primary": { "paragraphs": [] },
        "first_page": { "paragraphs": [] },
        "even_pages": null
      },
      "footers": {
        "primary": { "paragraphs": [] },
        "first_page": { "paragraphs": [] },
        "even_pages": null
      }
    }
  ]
}
```

---

## styles (스타일 정의)

### paragraph_styles

```json
{
  "paragraph_styles": [
    {
      "name": "본문",
      "name_en": "Body Text",
      "base_style": "표준",
      "font": {
        "name_ascii": "Times New Roman",
        "name_east_asia": "맑은 고딕",
        "size_pt": 11.0,
        "bold": false,
        "italic": false,
        "underline": "none",
        "strikethrough": false,
        "color": "#000000",
        "superscript": false,
        "subscript": false,
        "all_caps": false,
        "spacing_pt": 0.0
      },
      "paragraph_format": {
        "alignment": "justify",
        "line_spacing_rule": "multiple",
        "line_spacing": 1.6,
        "space_before_pt": 0.0,
        "space_after_pt": 6.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
        "right_indent_cm": 0.0,
        "keep_with_next": false,
        "keep_together": false,
        "page_break_before": false,
        "outline_level": 10
      }
    }
  ]
}
```

### font 객체

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| name_ascii | string | Y | 영문/기본 글꼴 |
| name_east_asia | string | Y | 한글/동아시아 글꼴 |
| size_pt | float | Y | 글꼴 크기 (pt) |
| bold | boolean | Y | 굵게 |
| italic | boolean | Y | 기울임 |
| underline | string | N | "none", "single", "double", "words" |
| strikethrough | boolean | N | 취소선 |
| color | string | N | "#RRGGBB" 또는 null (자동) |
| spacing_pt | float | N | 자간 (pt) |

### paragraph_format 객체

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| alignment | string | Y | "left", "center", "right", "justify", "distribute" |
| line_spacing_rule | string | Y | "single", "1.5lines", "double", "exactly", "atLeast", "multiple" |
| line_spacing | float | Y | 줄 간격 값 |
| space_before_pt | float | N | 단락 앞 간격 (pt) |
| space_after_pt | float | N | 단락 뒤 간격 (pt) |
| first_line_indent_cm | float | N | 첫 줄 들여쓰기 (cm) |
| left_indent_cm | float | N | 왼쪽 들여쓰기 (cm) |
| right_indent_cm | float | N | 오른쪽 들여쓰기 (cm) |

### character_styles / table_styles

character_styles는 font 객체만 포함 (paragraph_format 없음).
table_styles는 name, font, borders 포함.

---

## numbering (번호 매기기)

```json
{
  "numbering": {
    "definitions": [
      {
        "id": 0,
        "name": "가나다 목록",
        "levels": [
          {
            "level": 1,
            "format": "korean",
            "text": "%1.",
            "start": 1,
            "indent_cm": 1.27,
            "tab_cm": 1.9
          },
          {
            "level": 2,
            "format": "decimal",
            "text": "%1.%2",
            "start": 1,
            "indent_cm": 2.54,
            "tab_cm": 3.17
          }
        ]
      }
    ]
  }
}
```

**format 값:**
- `"decimal"` — 1, 2, 3
- `"korean"` — 가, 나, 다
- `"korean_digit"` — 일, 이, 삼
- `"ganada"` — ㄱ, ㄴ, ㄷ
- `"upper_alpha"` — A, B, C
- `"lower_alpha"` — a, b, c
- `"upper_roman"` — I, II, III
- `"lower_roman"` — i, ii, iii
- `"bullet"` — 글머리 기호

---

## content (본문 콘텐츠)

### paragraph

```json
{
  "type": "paragraph",
  "style": "본문",
  "text": "전체 텍스트 내용",
  "runs": [
    {
      "text": "굵은 텍스트",
      "font": { "bold": true, "size_pt": 11.0 }
    },
    {
      "text": " 일반 텍스트",
      "font": { "bold": false, "size_pt": 11.0 }
    }
  ],
  "numbering": {
    "definition_id": 0,
    "level": 1
  },
  "paragraph_format": null
}
```

- `style`: 적용된 스타일 이름 (styles에 정의된 이름)
- `runs`: 서식이 다른 텍스트 조각 목록
- `numbering`: null이면 번호 없음
- `paragraph_format`: null이면 스타일 기본값 사용, 값이 있으면 오버라이드

### table

```json
{
  "type": "table",
  "rows": 3,
  "cols": 4,
  "col_widths_cm": [3.0, 5.0, 4.0, 3.0],
  "data": [
    [
      {
        "text": "헤더 1",
        "shading_color": "#1A1F36",
        "font": { "bold": true, "color": "#FFFFFF" },
        "merge": null,
        "vertical_alignment": "center"
      }
    ]
  ],
  "borders": {
    "top": { "style": "single", "width_pt": 1.0, "color": "#000000" },
    "bottom": { "style": "single", "width_pt": 1.0, "color": "#000000" },
    "left": { "style": "single", "width_pt": 0.5, "color": "#000000" },
    "right": { "style": "single", "width_pt": 0.5, "color": "#000000" },
    "inside_h": { "style": "single", "width_pt": 0.5, "color": "#CCCCCC" },
    "inside_v": { "style": "single", "width_pt": 0.5, "color": "#CCCCCC" }
  }
}
```

**cell.merge 객체:**
```json
{ "row_span": 2, "col_span": 1 }
```
null이면 병합 없음.

**borders.style 값:** "none", "single", "double", "dotted", "dashed", "thick"

### page_break

```json
{ "type": "page_break" }
```

### image

```json
{
  "type": "image",
  "width_cm": 10.0,
  "height_cm": 6.5,
  "image_file": "images/img_001.png",
  "alt_text": ""
}
```

---

## 전체 예시 (축약)

```json
{
  "meta": {
    "source_file": "보고서양식.docx",
    "analyzed_at": "2026-03-04T10:00:00",
    "analyzer_version": "1.0.0"
  },
  "page_setup": {
    "orientation": "portrait",
    "page_width_cm": 21.0,
    "page_height_cm": 29.7,
    "margin_top_cm": 2.54,
    "margin_bottom_cm": 2.54,
    "margin_left_cm": 3.17,
    "margin_right_cm": 3.17
  },
  "sections": [
    {
      "index": 0,
      "page_setup": null,
      "has_different_first_page": false,
      "headers": { "primary": null },
      "footers": { "primary": null }
    }
  ],
  "styles": {
    "paragraph_styles": [
      {
        "name": "표준",
        "font": {
          "name_ascii": "Times New Roman",
          "name_east_asia": "맑은 고딕",
          "size_pt": 11.0,
          "bold": false
        },
        "paragraph_format": {
          "alignment": "justify",
          "line_spacing_rule": "multiple",
          "line_spacing": 1.6
        }
      }
    ],
    "character_styles": [],
    "table_styles": []
  },
  "numbering": { "definitions": [] },
  "content": [
    {
      "type": "paragraph",
      "style": "표준",
      "text": "보고서 내용",
      "runs": [{ "text": "보고서 내용", "font": {} }]
    }
  ]
}
```
