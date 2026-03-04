# win32com Word COM API 레퍼런스

doc-template-analyzer 스킬의 COM 속성 매핑 및 변환 규칙.

---

## Word Application 초기화

```python
import win32com.client

word = win32com.client.Dispatch("Word.Application")
word.Visible = False  # 백그라운드 실행
word.DisplayAlerts = 0  # 경고 표시 안 함 (wdAlertsNone)

doc = word.Documents.Open(
    FileName=abs_path,
    ReadOnly=True,         # DRM 잠금 회피
    AddToRecentFiles=False,
    Visible=False
)
```

**DRM 문서 주의사항:**
- 사내 DRM 시스템 로그인 상태에서만 Open 가능
- `ReadOnly=True`로 열어야 DRM 쓰기 잠금 회피
- Open 후 최대 60초 대기 (DRM 복호화 지연)

---

## 단위 변환

COM API는 모든 치수를 포인트(pt) 단위로 반환한다.

```python
def pt_to_cm(pt):
    """포인트 → 센티미터 (한국 문서는 cm 사용)"""
    return round(pt / 28.3465, 2)

def cm_to_pt(cm):
    """센티미터 → 포인트"""
    return round(cm * 28.3465, 2)

def pt_to_inches(pt):
    """포인트 → 인치"""
    return round(pt / 72.0, 2)

def emu_to_cm(emu):
    """EMU → 센티미터 (InlineShape 크기용)"""
    return round(emu / 360000.0, 2)
```

---

## WdColor 변환

Word COM의 색상은 WdColor 정수형으로 반환된다. RGB와 바이트 순서가 다르다.

```python
def wd_color_to_hex(wd_color):
    """WdColor 정수 → #RRGGBB 문자열"""
    if wd_color is None or wd_color < 0:
        return None  # wdColorAutomatic
    if wd_color == 0xFF000000 or wd_color == -16777216:
        return None  # 자동 색상
    r = wd_color & 0xFF
    g = (wd_color >> 8) & 0xFF
    b = (wd_color >> 16) & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"

def hex_to_wd_color(hex_str):
    """#RRGGBB → WdColor 정수"""
    hex_str = hex_str.lstrip('#')
    r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    return r + (g << 8) + (b << 16)
```

**주의:** WdColor는 BGR 순서 (R이 하위 바이트)

---

## PageSetup 속성

```python
ps = section.PageSetup

page_setup = {
    "orientation": "landscape" if ps.Orientation == 1 else "portrait",
    "page_width_cm": pt_to_cm(ps.PageWidth),
    "page_height_cm": pt_to_cm(ps.PageHeight),
    "margin_top_cm": pt_to_cm(ps.TopMargin),
    "margin_bottom_cm": pt_to_cm(ps.BottomMargin),
    "margin_left_cm": pt_to_cm(ps.LeftMargin),
    "margin_right_cm": pt_to_cm(ps.RightMargin),
    "header_distance_cm": pt_to_cm(ps.HeaderDistance),
    "footer_distance_cm": pt_to_cm(ps.FooterDistance),
    "gutter_cm": pt_to_cm(ps.Gutter),
}
```

**Orientation 상수:**
- `0` = wdOrientPortrait (세로)
- `1` = wdOrientLandscape (가로)

---

## 스타일 속성

```python
for style in doc.Styles:
    if style.InUse:  # 사용 중인 스타일만
        style_info = {
            "name": style.NameLocal,  # 로컬라이즈된 이름
            "name_en": style.NameLocal,  # 영문 이름 (가능하면)
            "type": get_style_type(style.Type),
            "base_style": style.BaseStyle.NameLocal if style.BaseStyle else None,
            "font": extract_font(style.Font),
            "paragraph_format": extract_paragraph_format(style.ParagraphFormat),
        }
```

**Style.Type 상수:**
- `1` = wdStyleTypeParagraph (단락 스타일)
- `2` = wdStyleTypeCharacter (문자 스타일)
- `3` = wdStyleTypeTable (표 스타일)
- `4` = wdStyleTypeList (목록 스타일)

---

## Font 속성

```python
def extract_font(font):
    return {
        "name_ascii": font.Name,               # 영문/기본 글꼴
        "name_east_asia": font.NameFarEast,     # 한글/동아시아 글꼴
        "size_pt": font.Size,                   # 글꼴 크기 (pt)
        "bold": bool(font.Bold),
        "italic": bool(font.Italic),
        "underline": get_underline_type(font.Underline),
        "strikethrough": bool(font.StrikeThrough),
        "color": wd_color_to_hex(font.Color),
        "highlight_color": get_highlight(font.HighlightColorIndex),
        "superscript": bool(font.Superscript),
        "subscript": bool(font.Subscript),
        "all_caps": bool(font.AllCaps),
        "spacing_pt": font.Spacing,             # 자간 (pt)
    }
```

**Underline 상수 (주요):**
- `0` = wdUnderlineNone
- `1` = wdUnderlineSingle
- `2` = wdUnderlineWords
- `3` = wdUnderlineDouble

**HighlightColorIndex 상수 (주요):**
- `0` = wdNoHighlight
- `4` = wdBrightGreen
- `6` = wdYellow
- `7` = wdWhite

---

## ParagraphFormat 속성

```python
def extract_paragraph_format(pf):
    return {
        "alignment": get_alignment(pf.Alignment),
        "line_spacing_rule": get_line_spacing_rule(pf.LineSpacingRule),
        "line_spacing": pf.LineSpacing,
        "space_before_pt": pf.SpaceBefore,
        "space_after_pt": pf.SpaceAfter,
        "first_line_indent_cm": pt_to_cm(pf.FirstLineIndent),
        "left_indent_cm": pt_to_cm(pf.LeftIndent),
        "right_indent_cm": pt_to_cm(pf.RightIndent),
        "keep_with_next": bool(pf.KeepWithNext),
        "keep_together": bool(pf.KeepTogether),
        "page_break_before": bool(pf.PageBreakBefore),
        "outline_level": pf.OutlineLevel,
    }
```

**Alignment 상수:**
- `0` = wdAlignParagraphLeft
- `1` = wdAlignParagraphCenter
- `2` = wdAlignParagraphRight
- `3` = wdAlignParagraphJustify
- `4` = wdAlignParagraphDistribute

**LineSpacingRule 상수:**
- `0` = wdLineSpaceSingle
- `1` = wdLineSpace1pt5
- `2` = wdLineSpaceDouble
- `3` = wdLineSpaceExactly (고정)
- `4` = wdLineSpaceAtLeast (최소)
- `5` = wdLineSpaceMultiple (배수)

---

## 표(Table) 속성

```python
for table in doc.Tables:
    table_info = {
        "rows": table.Rows.Count,
        "cols": table.Columns.Count,
        "col_widths_cm": [pt_to_cm(col.Width) for col in table.Columns],
        "data": [],
        "borders": extract_table_borders(table),
    }
    for row in table.Rows:
        row_data = []
        for cell in row.Cells:
            cell_info = {
                "text": cell.Range.Text.rstrip('\r\x07'),
                "row_span": cell.Range.Information(14),  # wdMaximumNumberOfRows
                "col_span": get_col_span(cell),
                "shading_color": wd_color_to_hex(cell.Shading.BackgroundPatternColor),
                "vertical_alignment": get_v_alignment(cell.VerticalAlignment),
                "font": extract_font(cell.Range.Font),
            }
            row_data.append(cell_info)
        table_info["data"].append(row_data)
```

**Cell.VerticalAlignment 상수:**
- `0` = wdCellAlignVerticalTop
- `1` = wdCellAlignVerticalCenter
- `3` = wdCellAlignVerticalBottom

**셀 병합 감지:**
- `cell.Range.Information(wdStartOfRangeRowNumber)` / `wdStartOfRangeColumnNumber`
- 이전 셀과 같은 위치면 병합된 셀

---

## 머리글/바닥글

```python
# 각 섹션별
for section in doc.Sections:
    headers = {}
    footers = {}

    # wdHeaderFooterPrimary = 1
    # wdHeaderFooterFirstPage = 2
    # wdHeaderFooterEvenPages = 3

    for hf_type in [1, 2, 3]:
        header = section.Headers(hf_type)
        if header.Exists:
            headers[hf_type] = {
                "text": header.Range.Text,
                "paragraphs": [extract_paragraph(p) for p in header.Range.Paragraphs],
            }
```

---

## InlineShape (이미지) 추출

```python
for i, shape in enumerate(doc.InlineShapes):
    if shape.Type == 3:  # wdInlineShapePicture
        img_info = {
            "width_cm": emu_to_cm(shape.Width * 914400 / 72),
            "height_cm": emu_to_cm(shape.Height * 914400 / 72),
            "image_file": f"images/img_{i+1:03d}.png",
        }
        # 이미지 저장: Range를 클립보드로 복사 후 PIL로 저장
        shape.Range.CopyAsPicture()
```

**InlineShape.Type 상수:**
- `3` = wdInlineShapePicture
- `5` = wdInlineShapeLinkedPicture
- `1` = wdInlineShapeEmbeddedOLEObject

---

## 번호 매기기 (ListTemplate)

```python
for lt in doc.ListTemplates:
    numbering_def = {
        "name": lt.Name if lt.Name else "unnamed",
        "levels": [],
    }
    for level_num in range(1, lt.ListLevels.Count + 1):
        level = lt.ListLevels(level_num)
        numbering_def["levels"].append({
            "level": level_num,
            "number_format": get_number_format(level.NumberFormat),
            "number_style": level.NumberStyle,  # wdListNumberStyleKorean 등
            "text_format": level.NumberFormat,
            "start_at": level.StartAt,
            "indent_cm": pt_to_cm(level.NumberPosition),
            "tab_cm": pt_to_cm(level.TabPosition),
        })
```

**한국어 번호 스타일 (NumberStyle):**
- `41` = wdListNumberStyleKorean (가, 나, 다)
- `42` = wdListNumberStyleKoreanDigit (일, 이, 삼)
- `45` = wdListNumberStyleGanada (ㄱ, ㄴ, ㄷ)
- `46` = wdListNumberStyleChosung (ㄱ, ㄴ, ㄷ — 초성)

---

## 안전한 정리 패턴

```python
word = None
doc = None
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(file_path, ReadOnly=True)
    # ... 분석 수행
    result = analyze(doc)
finally:
    try:
        if doc:
            doc.Close(False)  # SaveChanges=False
    except:
        pass
    try:
        if word:
            word.Quit()
    except:
        pass
```

**고아 프로세스 방지:**
- 반드시 `finally` 블록에서 `doc.Close()` → `word.Quit()` 순서 실행
- 예외 발생 시에도 Word 프로세스 정리 보장
- 작업 관리자에서 WINWORD.EXE 잔존 확인 습관
