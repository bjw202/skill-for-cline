---
name: doc-generator
description: |
  JSON 템플릿 기반으로 서식이 적용된 Word 문서(.docx)를 python-docx로 생성한다.
  doc-template-analyzer가 추출한 template.json을 사용하여 동일한 서식의 새 문서를 만든다.
  두 가지 모드: (A) 템플릿 원본 재현, (B) 템플릿 서식 + 새 콘텐츠 결합.
  다음 키워드에서 활성화: 문서 생성, docx 생성, Word 생성, 템플릿 기반 문서,
  doc generator, generate docx, create word, word document, 양식 적용,
  python-docx, 문서 만들기, 보고서 생성, template to docx
---

# Word 문서 생성기

JSON 템플릿을 기반으로 서식이 적용된 .docx 파일을 python-docx로 생성한다.
5단계 파이프라인으로 입력 검증부터 최종 저장까지 일원화한다.

```
[전체 흐름]
template.json + [content.json] → ① 입력 검증 → ② 문서 설정 → ③ 스타일 등록 → ④ 콘텐츠 생성 → ⑤ 최종 저장
```

**생성 모드:**
- **Mode A (Reproduce)**: template.json의 content를 그대로 재현
- **Mode B (Template + New Content)**: template.json의 서식 + content.json의 새 내용

---

## 1단계: 입력 검증 (Input Validation)

JSON 템플릿을 파싱하고 필수 필드를 검증한다.

**필수 환경:**
- Python 3.8+
- `python-docx` 패키지 (`pip install python-docx`)
- `lxml` 패키지 (python-docx 의존성, 자동 설치)

**확인 명령어:**

```bash
python -c "import docx; print('python-docx OK, version:', docx.__version__)"
```

**사용자에게 확인할 사항:**
- Q1. 템플릿 JSON 파일 경로
- Q2. 생성 모드 선택 (A: 원본 재현 / B: 새 콘텐츠 적용)
- Q3. (Mode B) 새 콘텐츠 데이터 또는 content.json 경로
- Q4. 출력 파일명 (기본: output.docx)

**필수 필드 검증:**

```python
required_fields = ["meta", "page_setup", "styles"]
# content는 Mode A에서만 필수
```

---

## 2단계: 문서 설정 (Document Setup)

python-docx로 새 문서를 생성하고 페이지 레이아웃을 설정한다.

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.section import WD_ORIENT

doc = Document()
section = doc.sections[0]

# 페이지 설정 적용
section.page_width = Cm(page_setup["page_width_cm"])
section.page_height = Cm(page_setup["page_height_cm"])
section.top_margin = Cm(page_setup["margin_top_cm"])
section.bottom_margin = Cm(page_setup["margin_bottom_cm"])
section.left_margin = Cm(page_setup["margin_left_cm"])
section.right_margin = Cm(page_setup["margin_right_cm"])

# 방향
if page_setup["orientation"] == "landscape":
    section.orientation = WD_ORIENT.LANDSCAPE
```

**다중 섹션 처리:**
- `sections` 배열의 각 항목에 대해 `doc.add_section()`으로 새 섹션 추가
- 섹션별 page_setup 개별 적용

---

## 3단계: 스타일 등록 (Style Configuration)

템플릿의 스타일 정의를 문서에 등록한다.

**기본 스타일 등록:**

```python
from docx.oxml.ns import qn

style = doc.styles.add_style("본문", WD_STYLE_TYPE.PARAGRAPH)
font = style.font
font.name = style_def["font"]["name_ascii"]
font.size = Pt(style_def["font"]["size_pt"])
font.bold = style_def["font"]["bold"]
```

**동아시아 글꼴 설정 (XML 직접 조작 필수):**

python-docx는 `w:eastAsia` 글꼴을 네이티브로 지원하지 않는다.

```python
rPr = style.element.get_or_add_rPr()
rFonts = rPr.find(qn('w:rFonts'))
if rFonts is None:
    rFonts = OxmlElement('w:rFonts')
    rPr.insert(0, rFonts)
rFonts.set(qn('w:eastAsia'), style_def["font"]["name_east_asia"])
```

**정렬 매핑:**

| JSON 값 | python-docx 상수 |
|---------|-----------------|
| "left" | WD_ALIGN_PARAGRAPH.LEFT |
| "center" | WD_ALIGN_PARAGRAPH.CENTER |
| "right" | WD_ALIGN_PARAGRAPH.RIGHT |
| "justify" | WD_ALIGN_PARAGRAPH.JUSTIFY |
| "distribute" | WD_ALIGN_PARAGRAPH.DISTRIBUTE |

상세 API 레퍼런스 및 XML 우회 패턴 → `docs/python-docx-api-reference.md` 참조

---

## 4단계: 콘텐츠 생성 (Content Generation)

### Mode A: 원본 재현

template.json의 `content` 배열을 순서대로 재현한다.

```python
for item in template["content"]:
    if item["type"] == "paragraph":
        add_paragraph(doc, item)
    elif item["type"] == "table":
        add_table(doc, item)
    elif item["type"] == "image":
        add_image(doc, item)
    elif item["type"] == "page_break":
        doc.add_page_break()
```

### Mode B: 템플릿 서식 + 새 콘텐츠

content.json의 구조:
```json
{
  "content": [
    { "type": "paragraph", "style": "제목 1", "text": "새 보고서 제목" },
    { "type": "paragraph", "style": "본문", "text": "새 본문 내용..." },
    { "type": "table", "style": "표 스타일", "data": [[...]] }
  ]
}
```

스타일 이름으로 template.json의 스타일 정의를 찾아 적용한다.

**단락 생성:**

```python
def add_paragraph(doc, para_def):
    p = doc.add_paragraph(style=para_def.get("style"))
    for run_def in para_def.get("runs", []):
        run = p.add_run(run_def["text"])
        apply_font(run.font, run_def.get("font", {}))
    if "paragraph_format" in para_def and para_def["paragraph_format"]:
        apply_paragraph_format(p.paragraph_format, para_def["paragraph_format"])
```

**표 생성 (셀 음영 XML 우회):**

```python
def apply_cell_shading(cell, color_hex):
    """셀 배경색 적용 (python-docx 미지원 → XML 직접 조작)"""
    from docx.oxml import OxmlElement
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex.lstrip('#'))
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)
```

**표 테두리 XML 우회:**

```python
def apply_table_borders(table, borders_def):
    """표 테두리 설정 (XML 직접 조작)"""
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    borders = OxmlElement('w:tblBorders')
    for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        edge_def = borders_def.get(edge.lower().replace('inside', 'inside_'), {})
        if edge_def:
            el = OxmlElement(f'w:{edge}')
            el.set(qn('w:val'), edge_def.get('style', 'single'))
            el.set(qn('w:sz'), str(int(edge_def.get('width_pt', 1) * 8)))
            el.set(qn('w:color'), edge_def.get('color', '000000').lstrip('#'))
            borders.append(el)
    tblPr.append(borders)
```

**이미지 삽입:**

```python
def add_image(doc, image_def):
    img_path = image_def.get("image_file", "")
    if os.path.exists(img_path):
        width = Cm(image_def.get("width_cm", 10))
        doc.add_picture(img_path, width=width)
```

---

## 5단계: 최종 저장 (Finalize & Export)

머리글/바닥글을 적용하고 문서를 저장한다.

**머리글/바닥글 적용:**

```python
for section_def in template.get("sections", []):
    section = doc.sections[section_def["index"]]
    if section_def.get("has_different_first_page"):
        section.different_first_page_header_footer = True
    # 머리글 텍스트 추가
    header = section.header
    if section_def.get("headers", {}).get("primary"):
        for para_def in section_def["headers"]["primary"]["paragraphs"]:
            p = header.add_paragraph()
            p.text = para_def.get("text", "")
```

**최종 저장:**

```python
doc.save(output_path)
```

**스크립트 실행:**

```bash
# Mode A: 원본 재현
python scripts/generate_doc.py template.json output.docx

# Mode B: 새 콘텐츠 적용
python scripts/generate_doc.py template.json content.json output.docx
```

---

## python-docx 한계 및 XML 우회 요약

| 기능 | 문제 | 해결 방법 |
|------|------|----------|
| 동아시아 글꼴 | `w:eastAsia` API 없음 | `rFonts.set(qn('w:eastAsia'), ...)` |
| 셀 음영 | 셀 배경색 API 없음 | `w:shd` OxmlElement 직접 생성 |
| 표 테두리 | 제한적 API | `w:tblBorders` XML 구성 |
| 번호 매기기 | 목록 지원 제한적 | `numbering.xml` oxml 조작 |

상세 API 레퍼런스 → `docs/python-docx-api-reference.md` 참조
JSON 스키마 사양 → `docs/json-schema-spec.md` 참조

---

## 참고 문서

- `docs/python-docx-api-reference.md` — python-docx API 매핑 및 XML 우회 패턴
- `docs/json-schema-spec.md` — JSON 템플릿 스키마 전체 명세
- `scripts/generate_doc.py` — 독립 실행 가능한 생성 스크립트
- `templates/sample-template.json` — 최소 작동 템플릿 예시
