#!/usr/bin/env python3
"""Nachbearbeitung der von pandoc erzeugten Word-Datei.

* Felder (Inhaltsverzeichnis, Seitenzahlen) werden beim Öffnen automatisch aktualisiert.
* Kindelemente werden in die vom OOXML-Schema verlangte Reihenfolge gebracht; pandoc hält
  diese an einigen Stellen nicht ein.
* Der Inhaltstyp für PNG-Bilder wird ergänzt.
"""
import shutil
import sys
import tempfile
import zipfile

from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

ORDERS = {
    "pPr": "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers "
           "pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE "
           "autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents "
           "suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle "
           "rPr sectPr pPrChange",
    "rPr": "rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint "
           "noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u "
           "effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath",
    "tblPr": "tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc "
             "tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription",
    "abstractNum": "nsid multiLevelType tmpl name styleLink numStyleLink lvl",
    "style": "name aliases basedOn next link autoRedraw hidden uiPriority semiHidden unhideWhenUsed "
             "qFormat locked personal personalCompose personalReply rsid pPr rPr tblPr trPr tcPr tblStylePr",
    "settings": "writeProtection view zoom removePersonalInformation removeDateAndTime "
                "doNotDisplayPageBoundaries displayBackgroundShape printPostScriptOverText "
                "printFractionalCharacterWidth printFormsData embedTrueTypeFonts embedSystemFonts "
                "saveSubsetFonts saveFormsData mirrorMargins alignBordersAndEdges "
                "bordersDoNotSurroundHeader bordersDoNotSurroundFooter gutterAtTop hideSpellingErrors "
                "hideGrammaticalErrors activeWritingStyle proofState formsDesign attachedTemplate "
                "linkStyles stylePaneFormatFilter stylePaneSortMethod documentType mailMerge "
                "revisionView trackRevisions doNotTrackMoves doNotTrackFormatting documentProtection "
                "autoFormatOverride styleLockTheme styleLockQFSet defaultTabStop autoHyphenation "
                "consecutiveHyphenLimit hyphenationZone doNotHyphenateCaps showEnvelope summaryLength "
                "clickAndTypeStyle defaultTableStyle evenAndOddHeaders bookFoldRevPrinting "
                "bookFoldPrinting bookFoldPrintingSheets drawingGridHorizontalSpacing "
                "drawingGridVerticalSpacing displayHorizontalDrawingGridEvery "
                "displayVerticalDrawingGridEvery doNotUseMarginsForDrawingGridOrigin "
                "drawingGridHorizontalOrigin drawingGridVerticalOrigin doNotShadeFormData "
                "noPunctuationKerning characterSpacingControl printTwoOnOne strictFirstAndLastChars "
                "noLineBreaksAfter noLineBreaksBefore savePreviewPicture doNotValidateAgainstSchema "
                "saveInvalidXml ignoreMixedContent alwaysShowPlaceholderText doNotDemarcateInvalidXml "
                "saveXmlDataOnly useXSLTWhenSaving saveThroughXslt showXMLTags "
                "alwaysMergeEmptyNamespace updateFields hdrShapeDefaults footnotePr endnotePr compat "
                "docVars rsids mathPr attachedSchema themeFontLang clrSchemeMapping "
                "doNotIncludeSubdocsInStats doNotAutoCompressPictures forceUpgrade captions "
                "readModeInkLockDown smartTagType schemaLibrary shapeDefaults doNotEmbedSmartTags "
                "decimalSymbol listSeparator",
}
ORDERS = {k: v.split() for k, v in ORDERS.items()}


def local(el):
    return etree.QName(el).localname if isinstance(el.tag, str) else ""


def reorder(root):
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        name = local(el)
        if name not in ORDERS or etree.QName(el).namespace != W:
            continue
        order = ORDERS[name]
        kids = [c for c in el if isinstance(c.tag, str)]
        kids.sort(key=lambda c: order.index(local(c)) if local(c) in order else len(order))
        for c in kids:
            el.remove(c)
            el.append(c)


def fix_xml(name, data):
    root = etree.fromstring(data)
    if name == "word/settings.xml" and root.find(f"{{{W}}}updateFields") is None:
        uf = etree.SubElement(root, f"{{{W}}}updateFields")
        uf.set(f"{{{W}}}val", "true")
    # nsid muss laut Schema genau 8 Hexadezimalziffern haben
    for nsid in root.iter(f"{{{W}}}nsid"):
        val = nsid.get(f"{{{W}}}val", "")
        nsid.set(f"{{{W}}}val", val.upper().zfill(8)[-8:])
    reorder(root)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


path = sys.argv[1]
tmp = tempfile.mktemp(suffix=".docx")
with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
    for item in src.infolist():
        data = src.read(item.filename)
        if item.filename.startswith("word/") and item.filename.endswith(".xml"):
            data = fix_xml(item.filename, data)
        if item.filename == "[Content_Types].xml" and b'Extension="png"' not in data:
            data = data.replace(b"<Default ", b'<Default Extension="png" ContentType="image/png"/><Default ', 1)
        dst.writestr(item, data)
shutil.move(tmp, path)
