# -*- coding: utf-8 -*-
"""
Word 문서 템플릿 분석기 (analyze_doc.py)

DRM 암호화된 사내 Word 문서를 win32com COM 자동화로 열어
서식 구조를 JSON 템플릿으로 추출한다.

사용법:
    python analyze_doc.py <입력.docx> [출력.json]

필수 환경:
    - Windows OS
    - Python 3.8+
    - pywin32 (pip install pywin32)
    - DRM 로그인 상태
"""

import json
import os
import sys
import datetime
from pathlib import Path

try:
    import win32com.client
    from win32com.client import constants as wc
except ImportError:
    print("오류: pywin32가 설치되지 않았습니다. pip install pywin32")
    sys.exit(1)

VERSION = "1.0.0"


# ─── 유틸리티 함수 ──────────────────────────────────────

def pt_to_cm(pt):
    """포인트 → 센티미터"""
    if pt is None:
        return 0.0
    return round(float(pt) / 28.3465, 2)


def emu_to_cm(emu):
    """EMU → 센티미터"""
    return round(float(emu) / 360000.0, 2)


def wd_color_to_hex(wd_color):
    """WdColor 정수 → #RRGGBB 문자열"""
    try:
        wd_color = int(wd_color)
    except (TypeError, ValueError):
        return None
    if wd_color < 0 or wd_color == 0xFF000000:
        return None
    r = wd_color & 0xFF
    g = (wd_color >> 8) & 0xFF
    b = (wd_color >> 16) & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"


def alignment_to_str(alignment_val):
    """WdParagraphAlignment → 문자열"""
    mapping = {
        0: "left",
        1: "center",
        2: "right",
        3: "justify",
        4: "distribute",
    }
    return mapping.get(alignment_val, "left")


def line_spacing_rule_to_str(rule_val):
    """WdLineSpacing → 문자열"""
    mapping = {
        0: "single",
        1: "1.5lines",
        2: "double",
        3: "exactly",
        4: "atLeast",
        5: "multiple",
    }
    return mapping.get(rule_val, "single")


def underline_to_str(underline_val):
    """WdUnderline → 문자열"""
    mapping = {0: "none", 1: "single", 2: "words", 3: "double"}
    return mapping.get(underline_val, "none")


def style_type_to_str(type_val):
    """WdStyleType → 문자열"""
    mapping = {1: "paragraph", 2: "character", 3: "table", 4: "list"}
    return mapping.get(type_val, "unknown")


def v_alignment_to_str(val):
    """WdCellVerticalAlignment → 문자열"""
    mapping = {0: "top", 1: "center", 3: "bottom"}
    return mapping.get(val, "top")


def number_style_to_format(style_val):
    """WdListNumberStyle → format 문자열"""
    mapping = {
        0: "decimal",
        22: "upper_alpha",
        23: "lower_alpha",
        1: "upper_roman",
        2: "lower_roman",
        41: "korean",
        42: "korean_digit",
        45: "ganada",
        46: "chosung",
        23: "bullet",
    }
    return mapping.get(style_val, "decimal")


def safe_str(val):
    """COM 객체를 안전하게 문자열로 변환"""
    try:
        if val is None:
            return None
        return str(val)
    except Exception:
        return None


def safe_float(val):
    """COM 객체를 안전하게 float로 변환"""
    try:
        if val is None:
            return 0.0
        return float(val)
    except Exception:
        return 0.0


def safe_bool(val):
    """COM 객체를 안전하게 bool로 변환 (-1=True in COM)"""
    try:
        if val is None:
            return False
        return bool(int(val))
    except Exception:
        return False


# ─── DocAnalyzer 클래스 ─────────────────────────────────

class DocAnalyzer:
    """Word 문서 분석기"""

    def __init__(self, file_path, output_dir=None):
        self.file_path = os.path.abspath(file_path)
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {self.file_path}")

        self.output_dir = output_dir or os.path.dirname(self.file_path)
        self.images_dir = os.path.join(self.output_dir, "images")
        self.word = None
        self.doc = None
        self.result = {
            "meta": {},
            "page_setup": {},
            "sections": [],
            "styles": {
                "paragraph_styles": [],
                "character_styles": [],
                "table_styles": [],
            },
            "numbering": {"definitions": []},
            "content": [],
        }

    def open(self):
        """Word COM 인스턴스 생성 및 문서 열기"""
        self.word = win32com.client.Dispatch("Word.Application")
        self.word.Visible = False
        self.word.DisplayAlerts = 0  # wdAlertsNone
        self.doc = self.word.Documents.Open(
            FileName=self.file_path,
            ReadOnly=True,
            AddToRecentFiles=False,
            Visible=False,
        )

    def close(self):
        """Word COM 정리 (고아 프로세스 방지)"""
        try:
            if self.doc:
                self.doc.Close(False)
        except Exception:
            pass
        try:
            if self.word:
                self.word.Quit()
        except Exception:
            pass

    def analyze(self):
        """전체 분석 수행"""
        self._analyze_meta()
        self._analyze_sections()
        self._analyze_styles()
        self._analyze_content()
        return self.result

    def export(self, output_path=None):
        """분석 결과를 JSON으로 저장"""
        if output_path is None:
            base = os.path.splitext(os.path.basename(self.file_path))[0]
            output_path = os.path.join(self.output_dir, f"{base}_template.json")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.result, f, ensure_ascii=False, indent=2)

        # 요약 마크다운 생성
        summary_path = output_path.replace("_template.json", "_summary.md")
        self._write_summary(summary_path)

        return output_path

    # ─── 내부 분석 메서드 ────────────────────────────────

    def _analyze_meta(self):
        """메타데이터 분석"""
        self.result["meta"] = {
            "source_file": os.path.basename(self.file_path),
            "analyzed_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "analyzer_version": VERSION,
            "page_count": self.doc.ComputeStatistics(2),  # wdStatisticPages
            "word_count": self.doc.ComputeStatistics(0),  # wdStatisticWords
        }

    def _analyze_sections(self):
        """섹션별 페이지 설정, 머리글/바닥글 분석"""
        for idx in range(1, self.doc.Sections.Count + 1):
            section = self.doc.Sections(idx)
            ps = section.PageSetup

            section_data = {
                "index": idx - 1,
                "page_setup": {
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
                },
                "has_different_first_page": safe_bool(ps.DifferentFirstPageHeaderFooter),
                "headers": self._extract_headers_footers(section, is_header=True),
                "footers": self._extract_headers_footers(section, is_header=False),
            }

            # 첫 번째 섹션을 기본 page_setup으로 사용
            if idx == 1:
                self.result["page_setup"] = section_data["page_setup"].copy()

            self.result["sections"].append(section_data)

    def _extract_headers_footers(self, section, is_header=True):
        """머리글 또는 바닥글 추출"""
        collection = section.Headers if is_header else section.Footers
        result = {}
        hf_types = {"primary": 1, "first_page": 2, "even_pages": 3}

        for name, hf_type in hf_types.items():
            try:
                hf = collection(hf_type)
                if hf.Exists:
                    text = hf.Range.Text.strip()
                    if text:
                        paragraphs = []
                        for para in hf.Range.Paragraphs:
                            paragraphs.append(self._analyze_paragraph(para))
                        result[name] = {"paragraphs": paragraphs}
                    else:
                        result[name] = None
                else:
                    result[name] = None
            except Exception:
                result[name] = None

        return result

    def _analyze_styles(self):
        """문서에서 사용 중인 모든 스타일 분석"""
        for style in self.doc.Styles:
            try:
                if not style.InUse:
                    continue

                style_type = style_type_to_str(style.Type)
                style_data = {
                    "name": safe_str(style.NameLocal),
                    "base_style": safe_str(style.BaseStyle.NameLocal) if style.BaseStyle else None,
                }

                if style_type == "paragraph":
                    style_data["font"] = self._extract_font(style.Font)
                    style_data["paragraph_format"] = self._extract_paragraph_format(
                        style.ParagraphFormat
                    )
                    self.result["styles"]["paragraph_styles"].append(style_data)

                elif style_type == "character":
                    style_data["font"] = self._extract_font(style.Font)
                    self.result["styles"]["character_styles"].append(style_data)

                elif style_type == "table":
                    style_data["font"] = self._extract_font(style.Font)
                    self.result["styles"]["table_styles"].append(style_data)

            except Exception:
                continue

    def _analyze_content(self):
        """본문 콘텐츠 순회 (단락, 표, 이미지)"""
        content = []
        table_ranges = set()

        # 표의 범위를 먼저 수집 (중복 방지)
        for i in range(1, self.doc.Tables.Count + 1):
            try:
                table = self.doc.Tables(i)
                table_ranges.add((table.Range.Start, table.Range.End))
            except Exception:
                continue

        # 본문 단락 순회
        for para in self.doc.Content.Paragraphs:
            try:
                para_start = para.Range.Start

                # 표 내부 단락인지 확인
                in_table = False
                for t_start, t_end in table_ranges:
                    if t_start <= para_start < t_end:
                        in_table = True
                        break

                if in_table:
                    continue

                # 페이지 나누기 확인
                if para.Range.Text.strip() == "" and safe_bool(
                    para.ParagraphFormat.PageBreakBefore
                ):
                    content.append({"type": "page_break"})
                    continue

                content.append(self._analyze_paragraph(para))

            except Exception:
                continue

        # 표 분석
        for i in range(1, self.doc.Tables.Count + 1):
            try:
                table = self.doc.Tables(i)
                table_data = self._analyze_table(table)
                # 표의 위치에 삽입 (간단히 순서대로 추가)
                content.append(table_data)
            except Exception:
                continue

        # 이미지 추출
        self._extract_images()

        self.result["content"] = content

        # 번호 매기기 분석
        self._analyze_numbering()

    def _analyze_paragraph(self, para):
        """단락 분석"""
        text = para.Range.Text.rstrip("\r\x07\x0b\x0c")
        style_name = safe_str(para.Style.NameLocal) if para.Style else None

        runs = self._extract_runs(para)

        result = {
            "type": "paragraph",
            "style": style_name,
            "text": text,
            "runs": runs,
        }

        # 번호 매기기 정보
        try:
            list_format = para.Range.ListFormat
            if list_format.ListType != 0:  # wdListNoNumbering
                result["numbering"] = {
                    "definition_id": None,
                    "level": list_format.ListLevelNumber,
                }
        except Exception:
            pass

        # 단락 서식 오버라이드 (스타일과 다를 경우)
        try:
            pf = para.ParagraphFormat
            if safe_bool(pf.PageBreakBefore):
                result.setdefault("paragraph_format", {})
                result["paragraph_format"]["page_break_before"] = True
        except Exception:
            pass

        return result

    def _extract_runs(self, para):
        """단락의 run(동일 서식 문자 그룹) 추출"""
        runs = []
        try:
            words = para.Range.Words
            if words.Count == 0:
                return runs

            current_text = ""
            current_font = None

            for i in range(1, words.Count + 1):
                try:
                    word = words(i)
                    font_info = self._extract_font(word.Font)
                    word_text = word.Text

                    if current_font is None:
                        current_font = font_info
                        current_text = word_text
                    elif self._fonts_equal(current_font, font_info):
                        current_text += word_text
                    else:
                        if current_text.rstrip("\r\x07"):
                            runs.append({"text": current_text.rstrip("\r\x07"), "font": current_font})
                        current_text = word_text
                        current_font = font_info
                except Exception:
                    continue

            if current_text.rstrip("\r\x07"):
                runs.append({"text": current_text.rstrip("\r\x07"), "font": current_font})

        except Exception:
            # 폴백: 전체 텍스트를 하나의 run으로
            text = para.Range.Text.rstrip("\r\x07")
            if text:
                runs.append({"text": text, "font": self._extract_font(para.Range.Font)})

        return runs

    def _fonts_equal(self, font1, font2):
        """두 폰트 정보가 동일한지 비교 (주요 속성만)"""
        keys = ["name_ascii", "name_east_asia", "size_pt", "bold", "italic", "color"]
        for key in keys:
            if font1.get(key) != font2.get(key):
                return False
        return True

    def _extract_font(self, font):
        """Font COM 객체에서 폰트 정보 추출"""
        return {
            "name_ascii": safe_str(font.Name),
            "name_east_asia": safe_str(font.NameFarEast),
            "size_pt": safe_float(font.Size),
            "bold": safe_bool(font.Bold),
            "italic": safe_bool(font.Italic),
            "underline": underline_to_str(font.Underline),
            "strikethrough": safe_bool(font.StrikeThrough),
            "color": wd_color_to_hex(font.Color),
            "spacing_pt": safe_float(font.Spacing),
        }

    def _extract_paragraph_format(self, pf):
        """ParagraphFormat COM 객체에서 단락 서식 추출"""
        return {
            "alignment": alignment_to_str(pf.Alignment),
            "line_spacing_rule": line_spacing_rule_to_str(pf.LineSpacingRule),
            "line_spacing": safe_float(pf.LineSpacing),
            "space_before_pt": safe_float(pf.SpaceBefore),
            "space_after_pt": safe_float(pf.SpaceAfter),
            "first_line_indent_cm": pt_to_cm(pf.FirstLineIndent),
            "left_indent_cm": pt_to_cm(pf.LeftIndent),
            "right_indent_cm": pt_to_cm(pf.RightIndent),
            "keep_with_next": safe_bool(pf.KeepWithNext),
            "keep_together": safe_bool(pf.KeepTogether),
            "page_break_before": safe_bool(pf.PageBreakBefore),
        }

    def _analyze_table(self, table):
        """표 분석"""
        rows_count = table.Rows.Count
        cols_count = table.Columns.Count

        # 열 너비 추출
        col_widths = []
        try:
            for col in table.Columns:
                col_widths.append(pt_to_cm(col.Width))
        except Exception:
            col_widths = [0.0] * cols_count

        # 셀 데이터 추출
        data = []
        for row in table.Rows:
            row_data = []
            for cell in row.Cells:
                try:
                    cell_text = cell.Range.Text.rstrip("\r\x07")
                    cell_info = {
                        "text": cell_text,
                        "shading_color": wd_color_to_hex(cell.Shading.BackgroundPatternColor),
                        "vertical_alignment": v_alignment_to_str(cell.VerticalAlignment),
                        "font": self._extract_font(cell.Range.Font),
                        "merge": None,
                    }
                    row_data.append(cell_info)
                except Exception:
                    row_data.append({"text": "", "merge": None})
            data.append(row_data)

        # 테두리 추출
        borders = self._extract_table_borders(table)

        return {
            "type": "table",
            "rows": rows_count,
            "cols": cols_count,
            "col_widths_cm": col_widths,
            "data": data,
            "borders": borders,
        }

    def _extract_table_borders(self, table):
        """표 테두리 정보 추출"""
        border_map = {
            "top": -1,       # wdBorderTop
            "bottom": -3,    # wdBorderBottom
            "left": -2,      # wdBorderLeft
            "right": -4,     # wdBorderRight
            "inside_h": -5,  # wdBorderHorizontal
            "inside_v": -6,  # wdBorderVertical
        }
        border_style_map = {
            0: "none", 1: "single", 3: "double",
            6: "dotted", 7: "dashed", 12: "thick",
        }

        borders = {}
        for name, border_id in border_map.items():
            try:
                border = table.Borders(border_id)
                borders[name] = {
                    "style": border_style_map.get(border.LineStyle, "single"),
                    "width_pt": safe_float(border.LineWidth),
                    "color": wd_color_to_hex(border.Color),
                }
            except Exception:
                borders[name] = {"style": "none", "width_pt": 0, "color": None}

        return borders

    def _extract_images(self):
        """인라인 이미지 추출"""
        os.makedirs(self.images_dir, exist_ok=True)

        for i in range(1, self.doc.InlineShapes.Count + 1):
            try:
                shape = self.doc.InlineShapes(i)
                if shape.Type == 3:  # wdInlineShapePicture
                    img_filename = f"img_{i:03d}.png"
                    img_info = {
                        "type": "image",
                        "width_cm": pt_to_cm(shape.Width),
                        "height_cm": pt_to_cm(shape.Height),
                        "image_file": f"images/{img_filename}",
                    }
                    self.result["content"].append(img_info)

                    # 이미지를 파일로 저장 시도
                    try:
                        shape.Range.CopyAsPicture()
                        # 클립보드에서 이미지를 저장하는 작업은
                        # PIL이나 추가 라이브러리가 필요하므로 경로만 기록
                    except Exception:
                        pass

            except Exception:
                continue

    def _analyze_numbering(self):
        """번호 매기기 정의 분석"""
        try:
            for i in range(1, self.doc.ListTemplates.Count + 1):
                lt = self.doc.ListTemplates(i)
                definition = {
                    "id": i - 1,
                    "name": safe_str(lt.Name) or f"list_{i}",
                    "levels": [],
                }

                for level_num in range(1, min(lt.ListLevels.Count + 1, 10)):
                    try:
                        level = lt.ListLevels(level_num)
                        definition["levels"].append({
                            "level": level_num,
                            "format": number_style_to_format(level.NumberStyle),
                            "text": safe_str(level.NumberFormat),
                            "start": level.StartAt,
                            "indent_cm": pt_to_cm(level.NumberPosition),
                            "tab_cm": pt_to_cm(level.TabPosition),
                        })
                    except Exception:
                        continue

                if definition["levels"]:
                    self.result["numbering"]["definitions"].append(definition)
        except Exception:
            pass

    def _write_summary(self, summary_path):
        """분석 요약 마크다운 생성"""
        meta = self.result["meta"]
        styles = self.result["styles"]
        sections = self.result["sections"]
        content = self.result["content"]

        para_count = sum(1 for c in content if c.get("type") == "paragraph")
        table_count = sum(1 for c in content if c.get("type") == "table")
        image_count = sum(1 for c in content if c.get("type") == "image")

        summary = f"""# 문서 분석 요약

## 기본 정보
- **파일명**: {meta.get('source_file', 'N/A')}
- **분석 시각**: {meta.get('analyzed_at', 'N/A')}
- **분석기 버전**: {meta.get('analyzer_version', 'N/A')}
- **페이지 수**: {meta.get('page_count', 'N/A')}
- **단어 수**: {meta.get('word_count', 'N/A')}

## 구조
- **섹션 수**: {len(sections)}
- **단락 스타일**: {len(styles['paragraph_styles'])}개
- **문자 스타일**: {len(styles['character_styles'])}개
- **표 스타일**: {len(styles['table_styles'])}개
- **번호 정의**: {len(self.result['numbering']['definitions'])}개

## 본문 요소
- **단락**: {para_count}개
- **표**: {table_count}개
- **이미지**: {image_count}개

## 페이지 설정
- **방향**: {self.result['page_setup'].get('orientation', 'N/A')}
- **용지 크기**: {self.result['page_setup'].get('page_width_cm', 0)}cm x {self.result['page_setup'].get('page_height_cm', 0)}cm
- **여백**: 상 {self.result['page_setup'].get('margin_top_cm', 0)}cm / 하 {self.result['page_setup'].get('margin_bottom_cm', 0)}cm / 좌 {self.result['page_setup'].get('margin_left_cm', 0)}cm / 우 {self.result['page_setup'].get('margin_right_cm', 0)}cm
"""

        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)


# ─── 메인 실행 ──────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("사용법: python analyze_doc.py <입력.docx> [출력.json]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"분석 시작: {input_file}")

    analyzer = DocAnalyzer(input_file)
    try:
        analyzer.open()
        print("문서 열기 완료")

        result = analyzer.analyze()
        print("분석 완료")

        output_path = analyzer.export(output_file)
        print(f"내보내기 완료: {output_path}")

        # 요약 출력
        meta = result["meta"]
        content = result["content"]
        print(f"\n=== 분석 요약 ===")
        print(f"페이지: {meta.get('page_count', 'N/A')}")
        print(f"섹션: {len(result['sections'])}")
        print(f"스타일: 단락 {len(result['styles']['paragraph_styles'])} / "
              f"문자 {len(result['styles']['character_styles'])} / "
              f"표 {len(result['styles']['table_styles'])}")
        print(f"본문: 단락 {sum(1 for c in content if c.get('type') == 'paragraph')} / "
              f"표 {sum(1 for c in content if c.get('type') == 'table')} / "
              f"이미지 {sum(1 for c in content if c.get('type') == 'image')}")

    finally:
        analyzer.close()
        print("Word 프로세스 정리 완료")


if __name__ == "__main__":
    main()
