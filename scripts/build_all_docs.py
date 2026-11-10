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
            return
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 800, "EDU TRACK ACADEMIC MANAGEMENT SUITE  |  OFFICIAL TECHNICAL DOCUMENTATION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 792, 558, 792)

        self.setFont("Helvetica", 8)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential – Edu Track System Engineering Specification")
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
            return
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#334155"))
        self.drawString(45, 570, "EDU TRACK: STUDENT ACADEMIC MANAGEMENT SYSTEM  |  EXECUTIVE PRESENTATION")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(1)
        self.line(45, 562, 747, 562)

        self.setFont("Helvetica", 8)
        self.line(45, 36, 747, 36)
        self.drawString(45, 24, "Full-Stack MERN Architecture | High-Availability Dual-Store Persistence")
        self.drawRightString(747, 24, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")
    secondary = colors.HexColor("#0284C7")
    accent = colors.HexColor("#4338CA")
    dark = colors.HexColor("#0F172A")
    body = colors.HexColor("#334155")

    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=29,
        textColor=primary,
        alignment=1,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#64748B"),
        alignment=1,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        name='SecHeading',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='SubSecHeading',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        name='Body',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='BodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=dark,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='Bullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=body,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name='Code',
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=dark,
        backColor=colors.HexColor("#F8FAFC"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=4,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name='Callout',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1E293B"),
        backColor=colors.HexColor("#EFF6FF"),
        borderColor=colors.HexColor("#93C5FD"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=7
    ))
    styles.add(ParagraphStyle(
        name='TCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=dark
    ))
    styles.add(ParagraphStyle(
        name='TCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=dark
    ))
    styles.add(ParagraphStyle(
        name='THeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    ))
    
    # Presentation specific styles
    styles.add(ParagraphStyle(
        name='SlideTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='SlideSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=secondary,
        spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        name='SlideCardHeader',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=accent,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name='SlideBody',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name='SlideBullet',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=body,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    ))
    return styles

print("Base styles configured.")
