"""
Generates docs/API_Documentation.pdf
OpenAPI / REST & WebSocket Real-time API Reference Specification.
"""

import os
from reportlab.lib.pagesizes import A4
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
        self.drawString(54, 805, "EDU TRACK: REST & WEBSOCKET API SPECIFICATION  |  DEVELOPER REFERENCE")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 797, 541, 797)

        self.setFont("Helvetica", 8)
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Confidential – Edu Track System Integration & Interface Protocol")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()


def build_api_docs():
    pdf_path = os.path.join("docs", "API_Documentation.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")
    secondary = colors.HexColor("#0284C7")
    accent = colors.HexColor("#4338CA")
    dark = colors.HexColor("#0F172A")
    body_color = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=primary, alignment=1, spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=20
    )
    h1 = ParagraphStyle(
        'H1', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=primary, spaceBefore=12, spaceAfter=5, keepWithNext=True
    )
    h2 = ParagraphStyle(
        'H2', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=accent, spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    p = ParagraphStyle(
        'P', fontName='Helvetica', fontSize=8.5, leading=12, textColor=body_color, spaceAfter=4
    )
    bullet = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=8, leading=11.5, textColor=body_color, leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )
    code = ParagraphStyle(
        'Code', fontName='Courier', fontSize=7.5, leading=10, textColor=dark,
        backColor=colors.HexColor("#F8FAFC"), borderColor=colors.HexColor("#E2E8F0"), borderWidth=0.5, borderPadding=4, spaceAfter=5
    )
    callout = ParagraphStyle(
        'Callout', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E293B"),
        backColor=colors.HexColor("#EFF6FF"), borderColor=colors.HexColor("#93C5FD"), borderWidth=0.8, borderPadding=6, spaceAfter=6
    )
    th = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white)
    td = ParagraphStyle('TD', fontName='Helvetica', fontSize=7, leading=9, textColor=dark)
    td_b = ParagraphStyle('TDB', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=dark)
    td_c = ParagraphStyle('TDC', fontName='Courier', fontSize=7, leading=9, textColor=dark)

    def make_endpoint_box(method, path, summary, auth, role, req_body, res_body):
        method_colors = {
            'GET': '#0284C7',     # Sky
            'POST': '#16A34A',    # Green
            'PUT': '#D97706',     # Amber
            'DELETE': '#DC2626'   # Red
        }
        m_color = method_colors.get(method, '#475569')

        hdr = [
            Paragraph(f"<font color='white'><b>{method}</b></font>", ParagraphStyle('MB', fontName='Helvetica-Bold', fontSize=8, alignment=1, textColor=colors.white)),
            Paragraph(f"<b><font face='Courier' color='#0F172A'>{path}</font></b> — {summary}", ParagraphStyle('PH', fontName='Helvetica', fontSize=8, textColor=dark))
        ]
        meta = [
            Paragraph(f"<b>Auth:</b> {auth} | <b>Required Roles:</b> {role}", ParagraphStyle('AM', fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor('#475569'))),
            ""
        ]
        req_p = [Paragraph("<b>Request Payload / Query Params:</b>", td_b), ""]
        req_c = [Paragraph(f"<font face='Courier'>{req_body}</font>", td_c), ""]
        res_p = [Paragraph("<b>Response Payload (HTTP 200/201):</b>", td_b), ""]
        res_c = [Paragraph(f"<font face='Courier'>{res_body}</font>", td_c), ""]

        t = Table([
            hdr, meta, req_p, req_c, res_p, res_c
        ], colWidths=[55, 432])
        t.setStyle(TableStyle([
            ('SPAN', (0,1), (1,1)),
            ('SPAN', (0,2), (1,2)),
            ('SPAN', (0,3), (1,3)),
            ('SPAN', (0,4), (1,4)),
            ('SPAN', (0,5), (1,5)),
            ('BACKGROUND', (0,0), (0,0), colors.HexColor(m_color)),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor('#F1F5F9')),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#E2E8F0')),
            ('PADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        return t

    story = []

    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>APPLICATION PROGRAMMING INTERFACE SPECIFICATION</b>", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=secondary, alignment=1, spaceAfter=15)))
    story.append(Paragraph("<b>REST ENDPOINT & WEBSOCKET PROTOCOL REFERENCE</b>", ParagraphStyle('Title2', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=accent, alignment=1, spaceAfter=18)))
    story.append(HRFlowable(width="60%", thickness=2, color=primary, spaceAfter=20, spaceBefore=5))
    story.append(Paragraph("Edu Track API Reference Manual", title_style))
    story.append(Paragraph("Stateless JSON Web Token (JWT) Authentication, Role-Governed Gateways, and Real-Time Event Protocols", subtitle_style))
    story.append(Spacer(1, 20))

    meta = Table([
        [Paragraph("<b>Base URL:</b>", td_b), Paragraph("<font face='Courier'>/api/v1</font> or <font face='Courier'>/api</font> (Production Host: https://projectmernfull-stack-roan.vercel.app)", td)],
        [Paragraph("<b>Transport Security:</b>", td_b), Paragraph("HTTPS / TLS 1.3 (REST) and WSS (WebSocket)", td)],
        [Paragraph("<b>Authentication:</b>", td_b), Paragraph("HTTP Header: <font face='Courier'>Authorization: Bearer &lt;JWT_TOKEN&gt;</font>", td)],
        [Paragraph("<b>Payload Standard:</b>", td_b), Paragraph("JSON (application/json) and Multipart/form-data for uploads", td)],
        [Paragraph("<b>Standard Response:</b>", td_b), Paragraph("<font face='Courier'>{ success: boolean, data?: any, message?: string, error?: string }</font>", td)],
    ], colWidths=[150, 337], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(meta)
    story.append(Spacer(1, 25))

    overview_box = (
        "<b>API Overview:</b> The Edu Track API suite provides comprehensive access to academic administration, scheduling, "
        "attendance, study material distribution, and online examination workflows. All endpoints enforce strict Role-Based Access "
        "Control (RBAC). Requests to protected routes must supply a cryptographically signed Bearer JWT token issued upon login. "
        "The server transparently executes queries across the active persistence engine (MongoDB Atlas or Fallback JSON Store)."
    )
    story.append(Paragraph(overview_box, callout))
    story.append(PageBreak())

    # ------------------ SECTION 1: AUTHENTICATION APIS ------------------
    story.append(Paragraph("1. Authentication & Profile Management", h1))

    story.append(make_endpoint_box(
        "POST", "/api/auth/login", "Authenticate user and issue JWT token",
        "Public", "All",
        "{ email: \"student@edutrack.edu\", password: \"SecurePass123\" }",
        "{ success: true, token: \"eyJhbGciOi...\", user: { id: \"...\", name: \"Pavan\", role: \"STUDENT\", department: \"CSE\", section: \"CSE-B\" } }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/auth/register", "Provision a new administrative or departmental account",
        "Admin Only", "ADMIN",
        "{ fullName: \"Dr. Smith\", email: \"smith@edutrack.edu\", password: \"...\", role: \"FACULTY\", department: \"CSE\" }",
        "{ success: true, message: \"User account registered successfully\", userId: \"usr-9021\" }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "GET", "/api/auth/me", "Retrieve current authenticated user profile & session context",
        "Bearer JWT", "ADMIN, FACULTY, STUDENT",
        "None (Header: Authorization: Bearer <token>)",
        "{ success: true, user: { id: \"...\", email: \"...\", role: \"FACULTY\", department: \"CSE\", teachingSections: [\"CSE-A\", \"CSE-B\"] } }"
    ))
    story.append(PageBreak())

    # ------------------ SECTION 2: ROSTER & USER MANAGEMENT ------------------
    story.append(Paragraph("2. User Roster & Account Administration", h1))

    story.append(make_endpoint_box(
        "GET", "/api/users/students", "Retrieve list of students filtered by cohort",
        "Bearer JWT", "ADMIN, FACULTY",
        "Query: ?department=CSE&semester=6&section=CSE-B",
        "{ success: true, count: 60, students: [{ id: \"...\", rollNumber: \"990000001\", name: \"Pavan\", email: \"p@gmail.com\", attendance: 86.6 }] }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "GET", "/api/users/faculty", "Retrieve departmental teaching faculty directory",
        "Bearer JWT", "ADMIN, FACULTY",
        "Query: ?department=CSE",
        "{ success: true, faculty: [{ id: \"...\", name: \"Prof. Maruthi Kumar\", email: \"m@edutrack.edu\", assignedSubjects: [\"CS401\", \"CS402\"] }] }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/users", "Create single student or faculty account with persistent storage",
        "Bearer JWT", "ADMIN",
        "{ name: \"John Doe\", email: \"john@edutrack.edu\", role: \"STUDENT\", department: \"CSE\", semester: 6, section: \"CSE-A\", rollNumber: \"990000088\" }",
        "{ success: true, message: \"Student record stored permanently in database\", student: { id: \"...\", ... } }"
    ))
    story.append(PageBreak())

    # ------------------ SECTION 3: TIMETABLES & CONFLICT ENGINE ------------------
    story.append(Paragraph("3. Timetable Planning & Conflict Engine", h1))

    story.append(make_endpoint_box(
        "GET", "/api/timetable/class", "Retrieve weekly instructional class timetable for cohort",
        "Bearer JWT", "ADMIN, FACULTY, STUDENT",
        "Query: ?department=CSE&semester=6&section=CSE-A",
        "{ success: true, periods: [{ dayOfWeek: \"Monday\", periodNumber: 1, startTime: \"09:00\", endTime: \"10:00\", subjectCode: \"CS401\", facultyName: \"Maruthi\", room: \"101\" }] }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/timetable/class", "Schedule class period with proactive collision validation",
        "Bearer JWT", "ADMIN",
        "{ dayOfWeek: \"Monday\", periodNumber: 2, startTime: \"10:00\", endTime: \"11:00\", department: \"CSE\", semester: 6, section: \"CSE-A\", subjectCode: \"CS402\", facultyId: \"f-1\", room: \"Hall 101\" }",
        "Success (201): { success: true, message: \"Period scheduled\" } | Conflict (409): { success: false, error: \"Room Hall 101 is already booked during Monday Period 2\" }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "GET", "/api/timetable/exam", "Retrieve semester examination schedule for department",
        "Bearer JWT", "ADMIN, FACULTY, STUDENT",
        "Query: ?department=Computer Science & Engineering&semester=6",
        "{ success: true, examSchedule: [{ id: \"...\", examDate: \"2026-11-20\", startTime: \"10:00 AM\", endTime: \"01:00 PM\", subjectCode: \"CS401\", courseTitle: \"Distributed Systems\", room: \"Hall 101\" }] }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/timetable/exam", "Publish semester examination date and room venue",
        "Bearer JWT", "ADMIN",
        "{ department: \"Computer Science & Engineering\", semester: 6, subjectCode: \"CS401\", courseTitle: \"Distributed Systems\", examDate: \"2026-11-20\", startTime: \"10:00 AM\", endTime: \"01:00 PM\", room: \"Exam Hall 101\", instructions: \"University ID card mandatory.\" }",
        "{ success: true, message: \"Semester exam published successfully; visible to all department students\" }"
    ))
    story.append(PageBreak())

    # ------------------ SECTION 4: ATTENDANCE & MATERIALS ------------------
    story.append(Paragraph("4. Daily Attendance & Course Materials", h1))

    story.append(make_endpoint_box(
        "POST", "/api/attendance", "Submit section attendance session (locked to today's date)",
        "Bearer JWT", "FACULTY",
        "{ sessionDate: \"2026-11-10\", department: \"CSE\", semester: 6, section: \"CSE-B\", subjectId: \"sub-401\", records: [{ studentId: \"s-1\", status: \"present\" }, { studentId: \"s-2\", status: \"absent\" }] }",
        "{ success: true, message: \"Attendance logged for 60 students\", timestamp: \"2026-11-10T14:10:00Z\" }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/materials", "Upload course document scoped to teaching section",
        "Bearer JWT (Multipart)", "FACULTY",
        "FormData: file: <binary PDF>, title: \"Unit 3 Notes\", department: \"CSE\", semester: 6, section: \"CSE-B\", subjectId: \"sub-401\"",
        "{ success: true, message: \"Material uploaded successfully\", material: { id: \"m-91\", fileUrl: \"/uploads/unit3.pdf\", section: \"CSE-B\" } }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "GET", "/api/materials", "Retrieve study materials scoped to student's section",
        "Bearer JWT", "FACULTY, STUDENT",
        "Query: ?department=CSE&semester=6&section=CSE-B",
        "{ success: true, materials: [{ id: \"m-91\", title: \"Unit 3 Notes\", fileName: \"unit3.pdf\", fileUrl: \"/uploads/unit3.pdf\", uploadedAt: \"...\" }] }"
    ))
    story.append(PageBreak())

    # ------------------ SECTION 5: ONLINE EXAMINATIONS & PROCTORING ------------------
    story.append(Paragraph("5. Online Examinations & Proctoring Pipeline", h1))

    story.append(make_endpoint_box(
        "POST", "/api/online-exams", "Create time-bounded online assessment with MCQs",
        "Bearer JWT", "FACULTY",
        "{ title: \"Mid-Term Assessment\", department: \"CSE\", semester: 6, section: \"CSE-B\", subjectId: \"sub-402\", examDate: \"2026-11-15\", startTime: \"14:00\", endTime: \"15:30\", durationMinutes: 60, totalMarks: 20, passMarks: 12, negativeMarking: \"None\", questions: [{ questionText: \"...\", options: [\"A\",\"B\",\"C\",\"D\"], correctOptionIndex: 1, marks: 2 }] }",
        "{ success: true, message: \"Online exam created\", examId: \"ex-5501\" }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/online-exams/:id/start", "Student begins exam; validates window & single attempt rule",
        "Bearer JWT", "STUDENT",
        "Body: {} (ID in URL)",
        "{ success: true, attemptId: \"att-102\", durationMinutes: 60, questions: [{ id: \"q1\", text: \"...\", options: [...] }] }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/online-exams/:id/submit", "Submit exam responses, proctoring tab-switch count & auto-evaluate",
        "Bearer JWT", "STUDENT",
        "{ attemptId: \"att-102\", answers: [{ questionId: \"q1\", selectedOptionIndex: 1 }], tabSwitchCount: 0 }",
        "{ success: true, message: \"Exam submitted successfully\", score: 20, totalMarks: 20, isPassed: true }"
    ))
    story.append(Spacer(1, 8))

    story.append(make_endpoint_box(
        "POST", "/api/online-exams/:id/release-results", "Faculty releases scores and unlocks review to students",
        "Bearer JWT", "FACULTY",
        "Body: {} (ID in URL)",
        "{ success: true, message: \"Results released; exam closed for new attempts; students notified\" }"
    ))
    story.append(PageBreak())

    # ------------------ SECTION 6: WEBSOCKET REAL-TIME EVENTS ------------------
    story.append(Paragraph("6. WebSocket Real-Time Event Protocol (Socket.IO)", h1))
    story.append(Paragraph(
        "Edu Track establishes an active bi-directional WebSocket connection via Socket.IO upon user authentication.",
        p
    ))

    ws_table = Table([
        [Paragraph("<b>Event Identifier</b>", th), Paragraph("<b>Direction</b>", th), Paragraph("<b>Payload Specification</b>", th), Paragraph("<b>Functional Action</b>", th)],
        [Paragraph("join_cohort", td_c), Paragraph("Client -> Server", td_b), Paragraph("{ department: \"CSE\", semester: 6, section: \"CSE-B\" }", td_c), Paragraph("Subscribes socket to cohort room.", td)],
        [Paragraph("timetable_updated", td_c), Paragraph("Server -> Client", td_b), Paragraph("{ department: \"CSE\", semester: 6, section: \"CSE-A\" }", td_c), Paragraph("Triggers automatic class timetable reload.", td)],
        [Paragraph("attendance_marked", td_c), Paragraph("Server -> Client", td_b), Paragraph("{ section: \"CSE-B\", subjectId: \"sub-401\", date: \"...\" }", td_c), Paragraph("Updates live attendance gauge and alerts.", td)],
        [Paragraph("material_published", td_c), Paragraph("Server -> Client", td_b), Paragraph("{ section: \"CSE-B\", materialTitle: \"Unit 3 Notes\" }", td_c), Paragraph("Surfaces new study material pill in student portal.", td)],
        [Paragraph("exam_results_released", td_c), Paragraph("Server -> Client", td_b), Paragraph("{ examId: \"ex-5501\", title: \"Lab Exam\" }", td_c), Paragraph("Unlocks scorecards and review keys for test takers.", td)],
        [Paragraph("exam_scheduled", td_c), Paragraph("Server -> Client", td_b), Paragraph("{ examId: \"ex-5501\", examDate: \"2026-11-15\" }", td_c), Paragraph("Adds upcoming examination badge to student dashboard.", td)],
    ], colWidths=[110, 80, 160, 137], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(ws_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    build_api_docs()
