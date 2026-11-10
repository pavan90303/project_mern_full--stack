"""
Generate comprehensive documentation PDFs for Edu-Track:
1. docs/Project_PPT.pdf
2. docs/Project_Documentation.pdf
3. docs/Database_Design.pdf
4. docs/API_Documentation.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

os.makedirs("docs", exist_ok=True)

# Custom NumberedCanvas for professional "Page X of Y" and running headers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header/footer on title page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header
        doc_title = getattr(self, "doc_title", "Edu Track – Student Academic Management System")
        self.drawString(54, 800, doc_title)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 558, 792)

        # Footer
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential & Proprietary – Edu Track Academic Suite")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


class SlideNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress on title slide

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(40, 570, "EDU TRACK ACADEMIC PLATFORM  |  SYSTEM PRESENTATION")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(1)
        self.line(40, 562, 752, 562)

        self.setFont("Helvetica", 8)
        self.line(40, 35, 752, 35)
        self.drawString(40, 24, "Edu Track – Full-Stack MERN Academic Management & Proctoring System")
        self.drawRightString(752, 24, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def get_custom_styles():
    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")   # Deep Blue
    accent = colors.HexColor("#4338CA")    # Indigo
    dark = colors.HexColor("#0F172A")      # Slate 900
    body = colors.HexColor("#334155")      # Slate 700

    styles.add(ParagraphStyle(
        name='DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary,
        alignment=1, # Center
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='DocSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='SubSectionHeading',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='BulletItem',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name='CodeSnippet',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=5,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        backColor=colors.HexColor("#EFF6FF"),
        borderColor=colors.HexColor("#93C5FD"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark
    ))
    styles.add(ParagraphStyle(
        name='TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=dark
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))
    return styles

print("Base setup configured successfully.")
