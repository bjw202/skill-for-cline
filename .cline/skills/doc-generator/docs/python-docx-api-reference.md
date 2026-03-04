# python-docx API 레퍼런스

doc-generator 스킬의 python-docx API 매핑 및 XML 우회 패턴.

---

## 기본 임포트

```python
from docx import Document
from docx.shared import Cm, Pt, Inches, Emu, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
```

---

## 단위 변환

JSON 템플릿은 cm 단위를 사용한다. python-docx로 변환 시:

```python
from docx.shared import Cm, Pt

# cm → python-docx 단위
width = Cm(21.0)        # 21cm
margin = Cm(2.54)       # 2.54cm

# pt → python-docx 단위
font_size = Pt(11.0)    # 11pt

# hex → RGBColor
def hex_to_rgb_color(hex_str):
    """#RRGGBB → RGBColor 객체"""
    if not hex_str:
        return None
    hex_str = hex_str.lstrip('#')
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return RGBColor(r, g, b)
```

---

## 페이지 설정

```python
doc = Document()
section = doc.sections[0]

# 용지 크기
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)

# 여백
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(3.17)
section.right_margin = Cm(3.17)

# 머리글/바닥글 거리
section.header_distance = Cm(1.27)
section.footer_distance = Cm(1.27)

# 제본 여백
section.gutter = Cm(0.0)

# 방향
section.orientation = WD_ORIENT.PORTRAIT  # 또는 WD_ORIENT.LANDSCAPE
# 가로 방향 시 width/height도 교환 필요
if orientation == "landscape":
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width, section.page_height = section.page_height, section.page_width
```

**다중 섹션 추가:**

```python
from docx.enum.section import WD_SECTION_START

new_section = doc.add_section(WD_SECTION_START.NEW_PAGE)
# 새 섹션에 개별 페이지 설정 적용
```

---

## 스타일 등록

### 단락 스타일

```python
from docx.enum.style import WD_STYLE_TYPE

# 새 스타일 생성 (이름 충돌 시 기존 스타일 사용)
try:
    style = doc.styles.add_style('본문', WD_STYLE_TYPE.PARAGRAPH)
except ValueError:
    style = doc.styles['본문']

# 기본 폰트 설정
font = style.font
font.name = 'Times New Roman'  # ASCII 글꼴
font.size = Pt(11)
font.bold = False
font.italic = False
font.color.rgb = hex_to_rgb_color('#000000')

# 단락 서식
pf = style.paragraph_format
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
pf.space_before = Pt(0)
pf.space_after = Pt(6)
pf.first_line_indent = Cm(0)
pf.left_indent = Cm(0)
```

### 동아시아 글꼴 (XML 필수)

python-docx는 `w:eastAsia` 글꼴 속성을 네이티브 API로 지원하지 않는다.

```python
def set_east_asia_font(style_or_run, font_name):
    """동아시아 글꼴 설정 (w:eastAsia)"""
    element = style_or_run.element if hasattr(style_or_run, 'element') else style_or_run
    rPr = element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)

# 사용 예시
set_east_asia_font(style, '맑은 고딕')

# run 레벨에서도 동일하게 적용 가능
run = paragraph.add_run('한글 텍스트')
set_east_asia_font(run, '맑은 고딕')
```

### 문자 스타일

```python
char_style = doc.styles.add_style('강조', WD_STYLE_TYPE.CHARACTER)
char_style.font.bold = True
char_style.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

---

## 정렬 매핑

### 단락 정렬

```python
ALIGNMENT_MAP = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
    "distribute": WD_ALIGN_PARAGRAPH.DISTRIBUTE,
}

def str_to_alignment(alignment_str):
    return ALIGNMENT_MAP.get(alignment_str, WD_ALIGN_PARAGRAPH.LEFT)
```

### 줄 간격

```python
LINE_SPACING_MAP = {
    "single": WD_LINE_SPACING.SINGLE,
    "1.5lines": WD_LINE_SPACING.ONE_POINT_FIVE,
    "double": WD_LINE_SPACING.DOUBLE,
    "exactly": WD_LINE_SPACING.EXACTLY,
    "atLeast": WD_LINE_SPACING.AT_LEAST,
    "multiple": WD_LINE_SPACING.MULTIPLE,
}

def apply_line_spacing(pf, rule_str, value):
    rule = LINE_SPACING_MAP.get(rule_str, WD_LINE_SPACING.SINGLE)
    pf.line_spacing_rule = rule
    if rule == WD_LINE_SPACING.MULTIPLE:
        pf.line_spacing = value  # 배수 값 (예: 1.6)
    elif rule in (WD_LINE_SPACING.EXACTLY, WD_LINE_SPACING.AT_LEAST):
        pf.line_spacing = Pt(value)  # 포인트 값
```

---

## 표(Table)

### 기본 표 생성

```python
table = doc.add_table(rows=3, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# 열 너비 설정
for i, width_cm in enumerate(col_widths):
    table.columns[i].width = Cm(width_cm)
```

### 셀 음영 (XML 우회)

```python
def apply_cell_shading(cell, color_hex):
    """셀 배경색 적용"""
    if not color_hex:
        return
    color = color_hex.lstrip('#')
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    shading.set(qn('w:color'), 'auto')
    cell._tc.get_or_add_tcPr().append(shading)
```

### 표 테두리 (XML 우회)

```python
def apply_table_borders(table, borders_def):
    """표 테두리 설정"""
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    borders = OxmlElement('w:tblBorders')

    # JSON key → XML element name 매핑
    edge_map = {
        'top': 'top', 'bottom': 'bottom',
        'left': 'left', 'right': 'right',
        'inside_h': 'insideH', 'inside_v': 'insideV',
    }

    # style → w:val 매핑
    style_map = {
        'none': 'none', 'single': 'single', 'double': 'double',
        'dotted': 'dotted', 'dashed': 'dashed', 'thick': 'thick',
    }

    for json_key, xml_name in edge_map.items():
        edge_def = borders_def.get(json_key, {})
        if not edge_def or edge_def.get('style') == 'none':
            continue
        el = OxmlElement(f'w:{xml_name}')
        el.set(qn('w:val'), style_map.get(edge_def.get('style', 'single'), 'single'))
        el.set(qn('w:sz'), str(int(edge_def.get('width_pt', 1) * 8)))  # half-point
        el.set(qn('w:space'), '0')
        color = edge_def.get('color', '#000000')
        el.set(qn('w:color'), color.lstrip('#') if color else '000000')
        borders.append(el)

    tblPr.append(borders)
```

### 셀 병합

```python
# 세로 병합 (row span)
cell_a = table.cell(0, 0)
cell_b = table.cell(2, 0)  # 3행에 걸쳐 병합
cell_a.merge(cell_b)

# 가로 병합 (col span)
cell_a = table.cell(0, 0)
cell_b = table.cell(0, 2)  # 3열에 걸쳐 병합
cell_a.merge(cell_b)
```

### 셀 수직 정렬

```python
VERTICAL_ALIGNMENT_MAP = {
    "top": WD_CELL_VERTICAL_ALIGNMENT.TOP,
    "center": WD_CELL_VERTICAL_ALIGNMENT.CENTER,
    "bottom": WD_CELL_VERTICAL_ALIGNMENT.BOTTOM,
}

cell.vertical_alignment = VERTICAL_ALIGNMENT_MAP.get(v_align, WD_CELL_VERTICAL_ALIGNMENT.TOP)
```

---

## 머리글/바닥글

```python
# 첫 페이지 다른 머리글
section.different_first_page_header_footer = True

# 기본 머리글
header = section.header
header.is_linked_to_previous = False
p = header.paragraphs[0]  # 기존 빈 단락 사용
p.text = "머리글 텍스트"
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# 첫 페이지 머리글
first_header = section.first_page_header
first_p = first_header.paragraphs[0]
first_p.text = "첫 페이지 머리글"

# 바닥글도 동일 패턴
footer = section.footer
```

---

## 이미지 삽입

```python
from docx.shared import Cm

# 너비 지정 (높이는 자동 비율)
doc.add_picture('images/img_001.png', width=Cm(10))

# 너비 + 높이 지정
doc.add_picture('images/img_001.png', width=Cm(10), height=Cm(6.5))
```

---

## 번호 매기기 (XML 조작)

python-docx는 목록/번호 매기기를 제한적으로 지원한다.

```python
def add_list_paragraph(doc, text, level=0, num_id=1):
    """번호 매기기 단락 추가"""
    p = doc.add_paragraph(text)
    pPr = p._p.get_or_add_pPr()
    numPr = OxmlElement('w:numPr')
    ilvl = OxmlElement('w:ilvl')
    ilvl.set(qn('w:val'), str(level))
    numId = OxmlElement('w:numId')
    numId.set(qn('w:val'), str(num_id))
    numPr.append(ilvl)
    numPr.append(numId)
    pPr.append(numPr)
    return p
```

---

## Run 레벨 서식 적용

```python
def apply_font(font, font_def):
    """font_def 딕셔너리를 python-docx Font 객체에 적용"""
    if font_def.get("name_ascii"):
        font.name = font_def["name_ascii"]
    if font_def.get("size_pt"):
        font.size = Pt(font_def["size_pt"])
    if font_def.get("bold") is not None:
        font.bold = font_def["bold"]
    if font_def.get("italic") is not None:
        font.italic = font_def["italic"]
    if font_def.get("color"):
        font.color.rgb = hex_to_rgb_color(font_def["color"])
    if font_def.get("underline") and font_def["underline"] != "none":
        font.underline = True
    if font_def.get("strikethrough"):
        font.strike = font_def["strikethrough"]
    if font_def.get("superscript"):
        font.superscript = font_def["superscript"]
    if font_def.get("subscript"):
        font.subscript = font_def["subscript"]
    if font_def.get("all_caps"):
        font.all_caps = font_def["all_caps"]
```

---

## 자주 발생하는 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `KeyError: 'Normal'` | 스타일 이름 불일치 | 로컬라이즈된 이름 사용 (예: '표준') |
| `ValueError: style already exists` | 중복 스타일 등록 | try/except로 기존 스타일 가져오기 |
| `PackageNotFoundError` | 빈 문서 생성 실패 | `Document()` 대신 기본 템플릿 사용 |
| 한글 깨짐 | eastAsia 글꼴 미설정 | XML로 `w:eastAsia` 직접 설정 |
| 표 너비 무시 | autofit 활성화 | `table.autofit = False` 설정 |
