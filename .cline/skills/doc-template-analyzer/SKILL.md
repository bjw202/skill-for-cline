---
name: doc-template-analyzer
description: |
  DRM 암호화된 사내 Word 문서(.doc/.docx)를 win32com으로 열어 서식 구조를 JSON 템플릿으로 추출한다.
  페이지 설정, 스타일, 머리글/바닥글, 번호 매기기, 본문(단락/표/이미지)을 분석하여
  재사용 가능한 template.json을 생성한다.
  다음 키워드에서 활성화: 문서 분석, 문서 양식, Word 분석, docx 분석, 템플릿 추출,
  doc template, document analysis, extract template, word format, 양식 추출,
  DRM 문서, 사내 문서 양식, win32com, COM 자동화
---

# Word 문서 템플릿 분석기

DRM 암호화된 사내 Word 문서를 win32com COM 자동화로 열어 서식 구조를 JSON 템플릿으로 추출한다.
4단계 파이프라인으로 환경 확인부터 JSON 내보내기까지 일원화한다.

```
[전체 흐름]
DRM 문서(.doc/.docx) → ① 환경 확인 → ② 문서 분석 → ③ 사용자 확인 → ④ JSON 내보내기
```

---

## 1단계: 환경 확인 (Environment Check)

사용자에게 소스 파일 경로를 받고 실행 환경을 검증한다.

**필수 조건:**
- Windows OS (win32com은 Windows 전용)
- Python 3.8+ 설치
- `pywin32` 패키지 설치 (`pip install pywin32`)
- DRM 로그인 상태 (사내 문서 보안 시스템에 로그인 필요)

**확인 명령어:**

```bash
# Python 및 pywin32 확인
python -c "import win32com.client; print('win32com OK')"

# 파일 존재 확인
python -c "import os; print(os.path.exists(r'<파일경로>'))"
```

**사용자에게 확인할 사항:**
- Q1. 분석할 문서 경로 (절대 경로 권장)
- Q2. 출력 디렉토리 (기본: 소스 파일과 같은 위치)
- Q3. 이미지 추출 여부 (기본: Yes)

---

## 2단계: 문서 분석 (Document Analysis)

`scripts/analyze_doc.py`를 실행하거나, 수동으로 COM 자동화 코드를 작성하여 분석한다.

**스크립트 실행:**

```bash
python scripts/analyze_doc.py "<입력파일.docx>" "<출력.json>"
```

**분석 항목:**

| 카테고리 | 추출 내용 | COM 속성 |
|---------|----------|---------|
| 메타데이터 | 페이지 수, 단어 수 | `doc.ComputeStatistics()` |
| 페이지 설정 | 여백, 방향, 용지 크기 | `section.PageSetup` |
| 스타일 | 단락/문자/표 스타일 | `doc.Styles` |
| 머리글/바닥글 | 섹션별 머리글/바닥글 | `section.Headers/Footers` |
| 번호 매기기 | 목록 정의 (가/나/다 등) | `doc.ListTemplates` |
| 본문 내용 | 단락, 표, 이미지 | `doc.Content`, `doc.Tables`, `doc.InlineShapes` |

**핵심 기술 포인트:**

단위 변환 (COM은 포인트 단위 반환):
```python
def pt_to_cm(pt):
    return round(pt / 28.3465, 2)
```

WdColor → RGB 변환:
```python
def wd_color_to_hex(wd_color):
    if wd_color < 0 or wd_color == 0xFF000000:
        return None  # 자동 색상
    r = wd_color & 0xFF
    g = (wd_color >> 8) & 0xFF
    b = (wd_color >> 16) & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"
```

이중 글꼴 처리 (한국어 문서 필수):
```python
font_info = {
    "name_ascii": font.Name,           # 영문 글꼴
    "name_east_asia": font.NameFarEast, # 한글 글꼴
    "size_pt": font.Size,
    "bold": font.Bold,
    "italic": font.Italic,
    "color": wd_color_to_hex(font.Color),
}
```

Run 감지 (동일 서식 문자 그룹화):
- `paragraph.Range`의 각 문자를 순회하며 Font 속성 비교
- 동일 속성이면 같은 run으로 묶어 텍스트 병합
- 속성 변경 시 새 run 시작

안전한 COM 정리:
```python
try:
    doc = word.Documents.Open(file_path)
    # ... 분석 수행
finally:
    if doc:
        doc.Close(False)
    word.Quit()
```

DRM 타임아웃:
- `word.Documents.Open()` 호출 시 DRM 복호화 지연 발생 가능
- `ReadOnly=True` 옵션으로 열기 (쓰기 잠금 회피)
- COM 타임아웃은 넉넉하게 설정 (60초 이상)

상세 COM API 레퍼런스 → `docs/win32com-api-reference.md` 참조

---

## 3단계: 사용자 확인 (User Confirmation)

분석 완료 후 `ask_followup_question`으로 요약을 제시하고 확인받는다.

**제시할 요약 정보:**

```markdown
## 문서 분석 요약

- 파일명: 보고서양식.docx
- 섹션 수: 3개
- 페이지 수: 12쪽
- 스타일 수: 단락 15개 / 문자 8개 / 표 3개
- 본문 요소: 단락 45개 / 표 5개 / 이미지 3개
- 머리글/바닥글: 있음 (첫 페이지 다름)
- 번호 매기기: 2개 정의 (가나다, 1.1.1)
- 추출 이미지: 3개

### 경고 사항
- [있을 경우] 일부 스타일에 NameFarEast 누락
- [있을 경우] 복잡한 셀 병합 감지 (정확도 저하 가능)
```

**사용자 선택지:**
- "전체 내보내기 진행" → 4단계로
- "특정 항목 제외 후 내보내기" → 제외 항목 지정 후 4단계
- "분석 중단" → 종료

---

## 4단계: JSON 내보내기 (Export)

승인된 분석 결과를 JSON 템플릿으로 저장한다.

**출력 파일:**

| 파일 | 설명 |
|-----|------|
| `{파일명}_template.json` | 전체 서식 템플릿 |
| `images/` | 추출된 인라인 이미지 |
| `{파일명}_summary.md` | 분석 요약 마크다운 |

**JSON 스키마 개요:**

```json
{
  "meta": {
    "source_file": "보고서양식.docx",
    "analyzed_at": "2026-03-04T10:00:00",
    "analyzer_version": "1.0.0"
  },
  "page_setup": { "orientation": "portrait", "page_width_cm": 21.0, "..." : "..." },
  "sections": [{ "page_setup": {}, "headers": {}, "footers": {} }],
  "styles": {
    "paragraph_styles": [{ "name": "...", "font": {}, "paragraph_format": {} }],
    "character_styles": [],
    "table_styles": []
  },
  "numbering": { "definitions": [] },
  "content": [
    { "type": "paragraph", "style": "...", "text": "...", "runs": [] },
    { "type": "table", "rows": 5, "cols": 3, "data": [[]] },
    { "type": "image", "width_cm": 10.0, "image_file": "images/img_001.png" }
  ]
}
```

상세 JSON 스키마 사양 → `docs/json-schema-spec.md` 참조

---

## 참고 문서

- `docs/win32com-api-reference.md` — COM 속성 매핑, WdColor 변환, 열거형 상수
- `docs/json-schema-spec.md` — JSON 템플릿 스키마 전체 명세
- `scripts/analyze_doc.py` — 독립 실행 가능한 분석 스크립트
