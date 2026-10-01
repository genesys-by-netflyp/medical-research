#!/usr/bin/env python3
"""Render manuscript_v01.docx to a clean A4 PDF (fpdf2). Pulls paragraphs/tables/images
in document order from the docx (single source of truth)."""
import os
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph as DocxPara
from fpdf import FPDF

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doc = Document(os.path.join(BASE, "manuscript", "manuscript_v01.docx"))

pdf = FPDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=20)
pdf.set_margins(20, 18, 20)
pdf.add_page()
fig_n = 0
# fonts with unicode coverage
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
if os.path.exists(FONT):
    pdf.add_font("dv", "", FONT)
    pdf.add_font("dvb", "", FONT.replace("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"))
    BODY, BOLD = "dv", "dvb"
else:
    BODY, BOLD = "helvetica", "helvetica"

def style_of(p):
    s = (p.style.name or "").lower()
    if s.startswith("heading 1"): return 1
    if s.startswith("heading 2"): return 2
    if s.startswith("title"): return 0
    return None

def emit_table(tb):
    data = [[c.text.strip() for c in row.cells] for row in tb.rows]
    if not data: return
    ncols = len(data[0])
    w = (pdf.w - 2 * pdf.l_margin) / ncols
    pdf.set_font(BODY, size=7.5)
    for ri, row in enumerate(data):
        for ci, cell in enumerate(row):
            pdf.cell(w, 5, cell[:60], border=1)
        pdf.ln(5)
    pdf.ln(2)

for item in doc.iter_inner_content():
    if isinstance(item, DocxPara):
        txt = item.text.strip()
        if not txt:
            continue
        st = style_of(item)
        if st == 0:
            pdf.set_font(BOLD, size=15); pdf.multi_cell(0, 7, txt); pdf.ln(2)
        elif st == 1:
            pdf.set_font(BOLD, size=12.5); pdf.ln(2); pdf.multi_cell(0, 6, txt); pdf.ln(1)
        elif st == 2:
            pdf.set_font(BOLD, size=11); pdf.ln(1.5); pdf.multi_cell(0, 5.5, txt); pdf.ln(0.8)
        else:
            # images embedded via relationship
            if "graphic" in item._p.xml:
                figs = ["prisma_flow.png", "agent_outcome.png", "exposure_context.png"]
                img = os.path.join(BASE, "figures", figs[min(fig_n, 2)])
                fig_n += 1
                pdf.image(img, w=150)
                pdf.ln(2)
                continue
            pdf.set_font(BODY, size=9.5); pdf.multi_cell(0, 4.6, txt); pdf.ln(1)
    elif isinstance(item, Table):
        emit_table(item)

out = os.path.join(BASE, "manuscript", "manuscript_v01.pdf")
pdf.output(out)
print("PDF written:", out, os.path.getsize(out), "bytes")
