"""Updates the TOC fields in a .docx with Microsoft Word and exports a PDF.
Usage: python scripts/docx_to_pdf.py <file.docx>"""
import os, sys
import win32com.client

path = os.path.abspath(sys.argv[1])
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
try:
    doc = word.Documents.Open(path)
    # compact single-spaced TOC / list-of-figures entries (Word built-in styles)
    for sid in (-20, -21, -36):  # TOC 1, TOC 2, Table of Figures
        st = doc.Styles(sid)
        st.Font.Name = "Times New Roman"
        st.Font.Size = 12
        st.ParagraphFormat.LineSpacingRule = 0  # single
        st.ParagraphFormat.SpaceAfter = 0
        st.ParagraphFormat.SpaceBefore = 0
    for toc in doc.TablesOfContents:
        toc.Update()
    doc.Fields.Update()
    doc.Save()
    pages = doc.ComputeStatistics(2)  # wdStatisticPages
    doc.ExportAsFixedFormat(path[:-5] + ".pdf", 17)  # wdExportFormatPDF
    doc.Close(False)
    print("pages:", pages)
finally:
    word.Quit()
