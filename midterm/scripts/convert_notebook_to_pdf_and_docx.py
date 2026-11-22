import json
import base64
import io
import os
import re
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.units import inch
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def clean_markdown_for_reportlab(text):
    # Basic markdown to reportlab XML cleanup
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert bold **text** to <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert italic *text* to <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert code `text` to <font face="Courier">text</font>
    text = re.sub(r'`(.*?)`', r'<font face="Courier" color="#1D4ED8">\1</font>', text)
    return text

def convert_to_pdf(nb_path, output_pdf_path):
    print(f"Generating PDF from {nb_path} -> {output_pdf_path}...")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=10,
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        spaceAfter=2
    )

    code_title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E40AF'),
        fontName='Helvetica-Bold',
        spaceAfter=2
    )

    story = []

    # Cover / Header banner
    story.append(Paragraph("LearnCraft AI — Preprocessing & Exploratory Data Analysis (EDA)", title_style))
    story.append(Paragraph("<b>Course Evaluation:</b> Phase 2 Partial Implementation | <b>UN-SDG:</b> Goal 4 (Quality Education)", ParagraphStyle('Sub', parent=body_style, textColor=colors.HexColor('#2563EB'))))
    story.append(Paragraph("<b>Source Notebook:</b> <code>LearnCraft_AI_Preprocessing_and_EDA.ipynb</code>", ParagraphStyle('Note', parent=body_style, fontSize=8.5, textColor=colors.HexColor('#64748B'))))
    story.append(Spacer(1, 10))

    img_counter = 0

    for idx, cell in enumerate(nb.get("cells", [])):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            lines = source.split("\n")
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    story.append(Spacer(1, 4))
                    continue
                if line_str.startswith("# "):
                    pass # already covered by title
                elif line_str.startswith("### "):
                    cleaned = clean_markdown_for_reportlab(line_str.replace("### ", ""))
                    story.append(Paragraph(cleaned, h2_style))
                elif line_str.startswith("## "):
                    cleaned = clean_markdown_for_reportlab(line_str.replace("## ", ""))
                    story.append(Paragraph(cleaned, h2_style))
                elif line_str.startswith("- ") or line_str.startswith("* "):
                    cleaned = clean_markdown_for_reportlab(line_str[2:])
                    story.append(Paragraph(f"• {cleaned}", bullet_style))
                elif re.match(r'^\d+\.\s', line_str):
                    cleaned = clean_markdown_for_reportlab(line_str)
                    story.append(Paragraph(cleaned, bullet_style))
                else:
                    cleaned = clean_markdown_for_reportlab(line_str)
                    story.append(Paragraph(cleaned, body_style))

        elif cell_type == "code":
            # Code cell header
            exec_count = cell.get("execution_count", idx)
            story.append(Spacer(1, 4))
            story.append(Paragraph(f"<b>[Code Cell In[{exec_count}]]:</b>", code_title_style))

            # Code box (limit lines to fit cleanly)
            code_text = source.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            code_para = Paragraph(f"<font face='Courier' size='7.5' color='#0F172A'>{code_text.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", body_style)
            
            code_table = Table([[code_para]], colWidths=[530])
            code_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
                ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#CBD5E1')),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(code_table)
            story.append(Spacer(1, 4))

            # Outputs
            for out in cell.get("outputs", []):
                out_type = out.get("output_type")
                if out_type == "stream":
                    text_out = "".join(out.get("text", []))
                    clean_out = text_out.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    out_para = Paragraph(f"<font face='Courier' size='7' color='#047857'><b>[Output]:</b><br/>{clean_out.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", body_style)
                    out_table = Table([[out_para]], colWidths=[530])
                    out_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
                        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ]))
                    story.append(out_table)
                    story.append(Spacer(1, 4))

                elif out_type == "display_data":
                    data_dict = out.get("data", {})
                    if "image/png" in data_dict:
                        b64_img = data_dict["image/png"]
                        img_data = base64.b64decode(b64_img)
                        temp_img_path = f"temp_plot_{img_counter}.png"
                        img_counter += 1
                        with open(temp_img_path, "wb") as img_f:
                            img_f.write(img_data)
                        
                        # Add image with 510 width constraint
                        with PILImage.open(temp_img_path) as pil_img:
                            orig_w, orig_h = pil_img.size
                            ratio = orig_h / orig_w
                        target_w = 510
                        target_h = target_w * ratio
                        
                        story.append(Spacer(1, 4))
                        story.append(RLImage(temp_img_path, width=target_w, height=target_h))
                        story.append(Spacer(1, 8))

    doc.build(story)
    
    # Safe cleanup temp images on Windows
    for i in range(img_counter):
        p = f"temp_plot_{i}.png"
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

    print(f"PDF successfully created: {output_pdf_path} (Size: {os.path.getsize(output_pdf_path)} bytes)")


def convert_to_docx(nb_path, output_docx_path):
    print(f"Generating Word DOCX from {nb_path} -> {output_docx_path}...")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    doc = docx.Document()

    # Document Title
    title = doc.add_heading("LearnCraft AI — Preprocessing & Exploratory Data Analysis (EDA)", level=0)
    sub = doc.add_paragraph()
    r = sub.add_run("Phase 2 Partial Implementation Submission | UN-SDG Goal 4: Quality Education\nSource Notebook: LearnCraft_AI_Preprocessing_and_EDA.ipynb")
    r.font.italic = True
    r.font.color.rgb = RGBColor(75, 85, 99)

    img_counter = 0

    for idx, cell in enumerate(nb.get("cells", [])):
        cell_type = cell.get("cell_type")
        source = "".join(cell.get("source", []))

        if cell_type == "markdown":
            lines = source.split("\n")
            for line in lines:
                line_str = line.strip()
                if not line_str:
                    continue
                if line_str.startswith("# "):
                    pass
                elif line_str.startswith("### "):
                    doc.add_heading(line_str.replace("### ", ""), level=2)
                elif line_str.startswith("## "):
                    doc.add_heading(line_str.replace("## ", ""), level=1)
                elif line_str.startswith("- ") or line_str.startswith("* "):
                    p = doc.add_paragraph(style='List Bullet')
                    p.add_run(line_str[2:])
                elif re.match(r'^\d+\.\s', line_str):
                    p = doc.add_paragraph(style='List Number')
                    p.add_run(line_str)
                else:
                    p = doc.add_paragraph()
                    p.add_run(line_str)

        elif cell_type == "code":
            exec_count = cell.get("execution_count", idx)
            h = doc.add_paragraph()
            hr = h.add_run(f"In [{exec_count}]:")
            hr.bold = True
            hr.font.color.rgb = RGBColor(30, 64, 175)

            # Code
            cp = doc.add_paragraph()
            c_run = cp.add_run(source)
            c_run.font.name = 'Courier New'
            c_run.font.size = Pt(8.5)
            c_run.font.color.rgb = RGBColor(15, 23, 42)

            # Outputs
            for out in cell.get("outputs", []):
                out_type = out.get("output_type")
                if out_type == "stream":
                    text_out = "".join(out.get("text", []))
                    op = doc.add_paragraph()
                    opr = op.add_run(f"Output:\n{text_out}")
                    opr.font.name = 'Courier New'
                    opr.font.size = Pt(8)
                    opr.font.color.rgb = RGBColor(4, 120, 87)

                elif out_type == "display_data":
                    data_dict = out.get("data", {})
                    if "image/png" in data_dict:
                        b64_img = data_dict["image/png"]
                        img_data = base64.b64decode(b64_img)
                        temp_img_path = f"temp_docx_plot_{img_counter}.png"
                        img_counter += 1
                        with open(temp_img_path, "wb") as img_f:
                            img_f.write(img_data)
                        doc.add_picture(temp_img_path, width=Inches(6.2))
                        doc.add_paragraph()

    doc.save(output_docx_path)

    for i in range(img_counter):
        p = f"temp_docx_plot_{i}.png"
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

    print(f"DOCX successfully created: {output_docx_path} (Size: {os.path.getsize(output_docx_path)} bytes)")

if __name__ == "__main__":
    nb_file = "LearnCraft_AI_Preprocessing_and_EDA.ipynb"
    convert_to_pdf(nb_file, "LearnCraft_AI_Preprocessing_and_EDA.pdf")
    convert_to_docx(nb_file, "LearnCraft_AI_Preprocessing_and_EDA.docx")
