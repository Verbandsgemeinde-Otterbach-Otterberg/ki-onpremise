#!/usr/bin/env python3
"""Erzeugt tools/docx/reference.docx: Formatvorlage für die Word-Fassung des Berichts.

Grundlage ist die Standardvorlage von pandoc; angepasst werden Schriften, Farben,
Überschriften, Codeblöcke, Tabellen, Seitenformat (A4) und Fußzeile mit Seitenzahl.
Benötigt: pandoc, python-docx.
"""
import pathlib
import subprocess

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = pathlib.Path(__file__).parent
OUT = HERE / "reference.docx"
FONT, MONO = "Arial", "Consolas"
NAVY, BLUE, GREEN, INK, MUTED = "27506E", "34678C", "8DB23E", "1B2C39", "5A6B76"

OUT.write_bytes(subprocess.run(
    ["pandoc", "--print-default-data-file", "reference.docx"],
    check=True, capture_output=True).stdout)
doc = Document(OUT)
styles = doc.styles
# Die Standardvorlage enthält ein verirrtes Zeichen in einem rPr-Element; bereinigen.
for rpr in styles.element.iter(qn("w:rPr")):
    rpr.text = None
    for child in rpr:
        child.tail = None


def style(name, kind=WD_STYLE_TYPE.PARAGRAPH, base=None):
    """Sucht eine Formatvorlage über ID oder Namen; legt sie nur an, wenn sie fehlt."""
    wanted_id = name.replace(" ", "")
    for s in styles:
        if s.style_id == wanted_id or (s.name or "").lower() == name.lower():
            return s
    s = styles.add_style(name, kind)
    if base:
        s.base_style = style(base)
    return s


def font(s, size=None, bold=None, italic=None, color=None, name=FONT):
    s.font.name = name
    rpr = s.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        rfonts.attrib.pop(qn(attr), None)
    if size:
        s.font.size = Pt(size)
    if bold is not None:
        s.font.bold = bold
    if italic is not None:
        s.font.italic = italic
    if color:
        s.font.color.rgb = RGBColor.from_string(color)


def spacing(s, before=None, after=None, line=None):
    pf = s.paragraph_format
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing = line


def ppr_child(s, tag):
    ppr = s.element.get_or_add_pPr()
    el = ppr.find(qn(tag))
    if el is None:
        el = OxmlElement(tag)
        ppr.append(el)
    return el


def border(s, side, color, size=8, space=4):
    pbdr = ppr_child(s, "w:pBdr")
    el = OxmlElement(f"w:{side}")
    for k, v in (("w:val", "single"), ("w:sz", str(size)), ("w:space", str(space)), ("w:color", color)):
        el.set(qn(k), v)
    pbdr.append(el)


def shade(s, fill):
    shd = ppr_child(s, "w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)


# Fließtext
for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
    s = style(name)
    font(s, size=10.5, color=INK)
spacing(style("Body Text"), before=0, after=7, line=1.15)
spacing(style("First Paragraph"), before=0, after=7, line=1.15)
spacing(style("Compact"), before=0, after=3, line=1.1)

# Überschriften
h1 = style("Heading 1")
font(h1, size=17, bold=True, color=NAVY)
spacing(h1, before=0, after=12)
h1.paragraph_format.page_break_before = True
h1.paragraph_format.keep_with_next = True
border(h1, "bottom", GREEN, size=10, space=6)
for name, size, color, before in (("Heading 2", 13.5, NAVY, 16), ("Heading 3", 11.5, BLUE, 12)):
    s = style(name)
    font(s, size=size, bold=True, color=color)
    spacing(s, before=before, after=5)
    s.paragraph_format.keep_with_next = True

# Titelblatt
from docx.enum.text import WD_ALIGN_PARAGRAPH
style("Title").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
style("Subtitle").paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
font(style("Title"), size=30, bold=True, color=NAVY)
spacing(style("Title"), before=36, after=6)
font(style("Subtitle"), size=14, color=INK, italic=False)
spacing(style("Subtitle"), before=0, after=24)
proj = style("Projektzeile", base="Normal")
font(proj, size=11, bold=True, color="5C7E4C")
spacing(proj, before=48, after=6)
meta = style("Metadaten", base="Normal")
font(meta, size=11, color=INK)
spacing(meta, before=0, after=12, line=1.3)
note = style("Hinweis", base="Normal")
font(note, size=9.5, italic=True, color=MUTED)
spacing(note, before=18, after=0, line=1.2)
toc_h = style("TOC Heading")
font(toc_h, size=17, bold=True, color=NAVY)
spacing(toc_h, before=0, after=12)

# Code
code = style("Source Code")
font(code, size=8, name=MONO, color=INK)
spacing(code, before=2, after=8, line=1.0)
shade(code, "F2F6F9")
for side in ("top", "left", "bottom", "right"):
    border(code, side, "D5E0E8", size=4, space=4)
font(style("Verbatim Char", WD_STYLE_TYPE.CHARACTER), size=9, name=MONO, color="2B4658")

# Hervorhebungen (Markdown-Zitate) als farbig hinterlegter Kasten
quote = style("Block Text")
font(quote, size=10.5, italic=False, color=INK)
spacing(quote, before=6, after=10, line=1.2)
shade(quote, "EDF3E6")
border(quote, "left", GREEN, size=24, space=8)
quote.paragraph_format.left_indent = Cm(0.3)
quote.paragraph_format.right_indent = Cm(0.3)

# Kasten auf dem Titelblatt
box = style("Kasten", base="Normal")
font(box, size=11, color=INK)
spacing(box, before=30, after=0, line=1.3)
shade(box, "EDF3E6")
for side in ("top", "left", "bottom", "right"):
    border(box, side, GREEN, size=12, space=8)

# Tabellen: Rahmen und farbige Kopfzeile
tbl = style("Table", WD_STYLE_TYPE.TABLE)
tblpr = tbl.element.find(qn("w:tblPr"))
if tblpr is None:
    tblpr = OxmlElement("w:tblPr")
    tbl.element.append(tblpr)
for old in tblpr.findall(qn("w:tblBorders")):
    tblpr.remove(old)
borders = OxmlElement("w:tblBorders")
for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
    el = OxmlElement(f"w:{side}")
    for k, v in (("w:val", "single"), ("w:sz", "4"), ("w:space", "0"), ("w:color", "C9D7E2")):
        el.set(qn(k), v)
    borders.append(el)
tblpr.append(borders)
for old in tblpr.findall(qn("w:tblCellMar")):
    tblpr.remove(old)
mar = OxmlElement("w:tblCellMar")
for side, w in (("top", 50), ("left", 90), ("bottom", 50), ("right", 90)):
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:w"), str(w))
    el.set(qn("w:type"), "dxa")
    mar.append(el)
tblpr.append(mar)
for old in tbl.element.findall(qn("w:tblStylePr")):
    tbl.element.remove(old)
first = OxmlElement("w:tblStylePr")
first.set(qn("w:type"), "firstRow")
rpr = OxmlElement("w:rPr")
b = OxmlElement("w:b")
rpr.append(b)
col = OxmlElement("w:color")
col.set(qn("w:val"), NAVY)
rpr.append(col)
first.append(rpr)
tcpr = OxmlElement("w:tcPr")
shd = OxmlElement("w:shd")
for k, v in (("w:val", "clear"), ("w:color", "auto"), ("w:fill", "DDE8F3")):
    shd.set(qn(k), v)
tcpr.append(shd)
first.append(tcpr)
tbl.element.append(first)

# Links
font(style("Hyperlink", WD_STYLE_TYPE.CHARACTER), color=BLUE)

# Seite: A4, Ränder, Fußzeile mit Seitenzahl, Titelseite ohne Fußzeile
section = doc.sections[0]
section.page_width, section.page_height = Cm(21), Cm(29.7)
section.left_margin = section.right_margin = Cm(2.2)
section.top_margin, section.bottom_margin = Cm(2.2), Cm(2.0)
section.header_distance, section.footer_distance, section.gutter = Cm(1.2), Cm(1.0), Cm(0)
section.different_first_page_header_footer = True
fp = section.footer.paragraphs[0]
fp.text = ""
run = fp.add_run("Zwischenbericht September 2026 · VG Otterbach-Otterberg · "
                 "Projekt „KI-Sprachmodelle in der kommunalen Verwaltung“ · Seite ")
run.font.size, run.font.color.rgb, run.font.name = Pt(8), RGBColor.from_string(MUTED), FONT
for kind, text in (("begin", None), ("instr", " PAGE "), ("end", None)):
    r = fp.add_run()
    r.font.size, r.font.color.rgb, r.font.name = Pt(8), RGBColor.from_string(MUTED), FONT
    if kind == "instr":
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = text
        r._r.append(it)
    else:
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        r._r.append(fc)

# Kindelemente von pPr in Schema-Reihenfolge bringen (Word ist hier strikt)
PPR_ORDER = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
             "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
             "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN",
             "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind", "contextualSpacing",
             "mirrorIndents", "suppressOverlap", "jc", "textDirection", "textAlignment",
             "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr", "pPrChange"]
for ppr in doc.styles.element.iter(qn("w:pPr")):
    children = list(ppr)
    children.sort(key=lambda c: PPR_ORDER.index(c.tag.split("}")[1])
                  if c.tag.split("}")[1] in PPR_ORDER else len(PPR_ORDER))
    for c in children:
        ppr.remove(c)
        ppr.append(c)

STYLE_ORDER = ["name", "aliases", "basedOn", "next", "link", "autoRedraw", "hidden", "uiPriority",
               "semiHidden", "unhideWhenUsed", "qFormat", "locked", "personal", "personalCompose",
               "personalReply", "rsid", "pPr", "rPr", "tblPr", "trPr", "tcPr", "tblStylePr"]
TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
               "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd",
               "tblLayout", "tblCellMar", "tblLook"]


def reorder(parent, order):
    kids = list(parent)
    kids.sort(key=lambda c: order.index(c.tag.split("}")[1]) if c.tag.split("}")[1] in order else len(order))
    for c in kids:
        parent.remove(c)
        parent.append(c)


for st in styles.element.iter(qn("w:style")):
    reorder(st, STYLE_ORDER)
for tp in styles.element.iter(qn("w:tblPr")):
    reorder(tp, TBLPR_ORDER)

doc.save(OUT)
print(f"erstellt: {OUT}")
