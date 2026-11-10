"""
Generates docs/Project_PPT.pdf
Executive presentation slide deck (12 Slides) in landscape orientation.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

os.makedirs("docs", exist_ok=True)

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
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(45, 570, "EDU TRACK ACADEMIC PLATFORM  |  EXECUTIVE ARCHITECTURE PRESENTATION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.8)
        self.line(45, 562, 747, 562)

        self.setFont("Helvetica", 7.5)
        self.line(45, 34, 747, 34)
        self.drawString(45, 23, "Full-Stack MERN Architecture | High-Availability Dual-Store Resilience | Socket.IO Sync")
        self.drawRightString(747, 23, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def build_ppt():
    pdf_path = os.path.join("docs", "Project_PPT.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=45,
        rightMargin=45,
        topMargin=50,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")   # Blue 900
    secondary = colors.HexColor("#0284C7") # Sky 600
    accent = colors.HexColor("#4338CA")    # Indigo 700
    dark = colors.HexColor("#0F172A")      # Slate 900
    body_color = colors.HexColor("#334155")# Slate 700

    s_title = ParagraphStyle(
        'STitle', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=primary, spaceAfter=4
    )
    s_sub = ParagraphStyle(
        'SSub', fontName='Helvetica', fontSize=10, leading=13, textColor=secondary, spaceAfter=12
    )
    card_h = ParagraphStyle(
        'CardH', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=accent, spaceAfter=4
    )
    card_p = ParagraphStyle(
        'CardP', fontName='Helvetica', fontSize=8.5, leading=12, textColor=body_color, spaceAfter=4
    )
    card_b = ParagraphStyle(
        'CardB', fontName='Helvetica', fontSize=8.5, leading=12, textColor=body_color, leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )
    code_p = ParagraphStyle(
        'CodeP', fontName='Courier', fontSize=7.5, leading=10, textColor=dark
    )

    def make_card(title, items, width=340, bg="#F8FAFC", border="#CBD5E1"):
        flowables = [Paragraph(f"<b>{title}</b>", card_h), Spacer(1, 3)]
        for it in items:
            if isinstance(it, str):
                flowables.append(Paragraph(f"• {it}", card_b))
            else:
                flowables.append(it)
        
        t = Table([[flowables]], colWidths=[width])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg)),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border)),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        return t

    story = []

    # ------------------ SLIDE 1: TITLE SLIDE ------------------
    cover_data = [
        [Paragraph("<font color='#0284C7' size='11'><b>ENTERPRISE ACADEMIC GOVERNANCE SUITE</b></font>", ParagraphStyle('CSub', alignment=1))],
        [Spacer(1, 10)],
        [Paragraph("<b>Edu Track – Student Academic Management System</b>", ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=primary, alignment=1))],
        [Paragraph("A Unified, Role-Governed Full-Stack University Operating Environment with Real-Time Timetable Conflict Engines, Section-Scoped Coursework, and Automated Online Examination Proctoring", ParagraphStyle('CDesc', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#475569'), alignment=1))],
        [Spacer(1, 16)],
        [Paragraph("<b>Technical Architecture & Executive Implementation Deck</b>", ParagraphStyle('CDeck', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=accent, alignment=1))],
        [Spacer(1, 20)],
        [Table([
            [
                Paragraph("<b>Technology Stack:</b><br/>React 18 • TypeScript • Tailwind CSS • Vite", card_p),
                Paragraph("<b>Backend Engine:</b><br/>Node.js • Express • Socket.IO • JWT Auth", card_p),
                Paragraph("<b>Persistence Layer:</b><br/>MongoDB Atlas + Dual-Store JSON Sync Engine", card_p)
            ]
        ], colWidths=[230, 230, 230], style=[
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ])]
    ]
    t_cover = Table(cover_data, colWidths=[702])
    t_cover.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 35)
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # ------------------ SLIDE 2: PROBLEM STATEMENT & MOTIVATION ------------------
    story.append(Paragraph("01. Executive Summary & Problem Landscape", s_title))
    story.append(Paragraph("Critical deficiencies in traditional higher-education academic administration software.", s_sub))
    
    col1 = make_card("Legacy Academic ERP Challenges", [
        "<b>Fragmented Portals:</b> Attendance, LMS, examination grading, and scheduling operate in disconnected silos, requiring duplicate manual data entry.",
        "<b>Timetable Scheduling Clashes:</b> Room, faculty, and cohort conflicts are caught retroactively rather than prevented at creation time.",
        "<b>Single Point of Failure:</b> Cloud database outages freeze campus administrative operations without a local fallback mechanism.",
        "<b>Attendance Fraud & Date Tampering:</b> Instructors backdating attendance or marking rosters outside scheduled operational windows.",
        "<b>Unregulated Online Examinations:</b> Lack of browser focus monitoring, lack of auto-evaluation, and insecure result release workflows."
    ], width=342, bg="#FEF2F2", border="#FECACA")

    col2 = make_card("The Edu-Track Modern Solution", [
        "<b>Unified 3-Role Architecture:</b> Zero-friction role segregation across Institutional Administrators, Teaching Faculty, and Enrolled Students.",
        "<b>Autonomous Conflict Engine:</b> Proactive pre-commit validation of room, instructor, and student cohort overlaps for weekly timetables.",
        "<b>High-Availability Dual-Store Resilience:</b> Seamless automated fallback to local atomic JSON persistence if MongoDB Atlas drops offline.",
        "<b>Anti-Tamper Single-Day Attendance:</b> Hardware/server enforced restriction locking attendance exclusively to the current active date.",
        "<b>End-to-End Online Exam Pipeline:</b> Integrated proctoring (tab-switch detection), instant auto-grading, and faculty-governed result releases."
    ], width=342, bg="#F0FDF4", border="#BBF7D0")

    story.append(Table([[col1, col2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 3: SYSTEM ARCHITECTURE ------------------
    story.append(Paragraph("02. Full-Stack System Architecture & Dual-Store Engine", s_title))
    story.append(Paragraph("Multi-tier reactive architecture ensuring continuous availability and bi-directional synchronization.", s_sub))

    arch_table = Table([
        [
            Paragraph("<b>CLIENT TIER (Frontend SPA)</b><br/>• React 18 with TypeScript<br/>• Tailwind CSS + Lucide Icons<br/>• Responsive Grid & Flex Layout<br/>• Role-Governed Routing & State<br/>• Recharts Academic Visualizer", card_p),
            Paragraph("<b>GATEWAY TIER (API & Realtime)</b><br/>• Node.js & Express REST Engine<br/>• JWT Bearer Authentication<br/>• Role Guard Middleware<br/>• Socket.IO WebSocket Broadcasts<br/>• Multer Course Material Uploads", card_p),
            Paragraph("<b>PERSISTENCE TIER (Dual-Store)</b><br/>• Primary: MongoDB Atlas Cloud<br/>• Fallback: Atomic JSON File Store<br/>• Auto-Switch on Network Failure<br/>• Self-Healing Dual-Store Reconciler<br/>• Zero Client Operation Interruptions", card_p)
        ]
    ], colWidths=[228, 228, 228], style=[
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#EFF6FF')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#EEF2FF')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ])
    story.append(arch_table)
    story.append(Spacer(1, 10))

    callout_arch = make_card("High-Availability Dual-Store Resilience Mechanism", [
        "<b>1. Detection:</b> Backend monitors MongoDB ping heartbeat. If unreachable (ECONNREFUSED / Network Timeout), state shifts to <i>Autonomous Local Store</i>.",
        "<b>2. Seamless Writes:</b> All CRUD operations route to structured JSON collections with ACID-like atomic rename file writes in <font face='Courier'>server/data/</font>.",
        "<b>3. Client Transparency:</b> REST endpoints return identical DTOs with <font face='Courier'>source: 'mongo' | 'json'</font>. The frontend displays live sync status pills without crashing.",
        "<b>4. Self-Healing:</b> Upon MongoDB reconnection, pending offline mutations synchronize back to cloud collections."
    ], width=696, bg="#F8FAFC", border="#93C5FD")
    story.append(callout_arch)
    story.append(PageBreak())

    # ------------------ SLIDE 4: ROLE GOVERNANCE & ACCESS CONTROL ------------------
    story.append(Paragraph("03. Role-Based Access Control (RBAC) Matrix", s_title))
    story.append(Paragraph("Strict enterprise permission boundaries isolating administrative, instructional, and student operations.", s_sub))

    rbac_data = [
        [
            Paragraph("<b>Capability / Operational Domain</b>", ParagraphStyle('RBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Admin Portal</b>", ParagraphStyle('RBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Faculty Portal</b>", ParagraphStyle('RBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Student Portal</b>", ParagraphStyle('RBH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
        ],
        [Paragraph("Manage Students, Faculty & Departments", card_p), Paragraph("Full Access (CRUD)", card_p), Paragraph("No Access (Hidden)", card_p), Paragraph("No Access (Hidden)", card_p)],
        [Paragraph("Weekly Timetable & Conflict Engine", card_p), Paragraph("Full Authoring & Schedule Publish", card_p), Paragraph("View Personal Faculty Schedule", card_p), Paragraph("View Enrolled Section Timetable", card_p)],
        [Paragraph("Semester Examination Timetable", card_p), Paragraph("Schedule & Publish All Depts", card_p), Paragraph("View Dept Exam Schedules", card_p), Paragraph("View Department Exam Timetable", card_p)],
        [Paragraph("Student Attendance Recording", card_p), Paragraph("View Institutional Analytics", card_p), Paragraph("Mark Session Attendance (Today Only)", card_p), Paragraph("View Personal Attendance %", card_p)],
        [Paragraph("Course Materials Distribution", card_p), Paragraph("System Storage Oversight", card_p), Paragraph("Upload Files (Section Scoped)", card_p), Paragraph("Download Section Materials", card_p)],
        [Paragraph("Online Exams & Proctoring", card_p), Paragraph("Audit Overall Assessments", card_p), Paragraph("Create Exams, Release Results", card_p), Paragraph("Attempt Once, View Results & Review", card_p)],
        [Paragraph("Official Grade Points & Transcripts", card_p), Paragraph("Publish Semester Grade Cards", card_p), Paragraph("Input Internal Assessment Marks", card_p), Paragraph("View Semester CGPA/SGPA Card", card_p)],
    ]
    t_rbac = Table(rbac_data, colWidths=[200, 164, 164, 164], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6)
    ])
    story.append(t_rbac)
    story.append(PageBreak())

    # ------------------ SLIDE 5: TIMETABLE & CONFLICT VALIDATION ------------------
    story.append(Paragraph("04. Class & Semester Exam Timetable Engine", s_title))
    story.append(Paragraph("Automated validation preventing cohort overlapping, room double-booking, and faculty collisions.", s_sub))

    c1 = make_card("Weekly Class Timetable Architecture", [
        "<b>Cohort Isolation:</b> Filtered dynamically by Department, Semester, and Section (e.g. CSE, Sem 6, Section A).",
        "<b>Persistent Matrix:</b> Stores periods across Monday through Saturday with Start/End times, Subject Code, Faculty ID, and Room.",
        "<b>Autonomous Conflict Detection:</b>",
        "  • <i>Room Conflict:</i> Ensures no two classes occupy the same Room at the identical Day/Period.",
        "  • <i>Faculty Clash:</i> Verifies the designated instructor is not assigned to another cohort simultaneously.",
        "  • <i>Cohort Collision:</i> Guarantees student section cannot have simultaneous overlapping periods.",
        "<b>Immediate Broadcast:</b> Dispatches WebSocket notification <font face='Courier'>timetable_updated</font> to all connected student screens."
    ], width=342, bg="#EFF6FF", border="#93C5FD")

    c2 = make_card("Semester Examination Timetable System", [
        "<b>Institutional Scope:</b> University-wide schedule management for mid-term and end-semester examinations.",
        "<b>Department-Filtered Subject Dropdown:</b>",
        "  • Eliminates manual code entry errors by reading registered departmental subjects directly from database.",
        "  • Auto-populates official Course Title and Subject Code upon selection.",
        "<b>Universal Student Visibility:</b>",
        "  • Once published by Admin, every enrolled student in that department immediately accesses the complete schedule.",
        "  • Displays Examination Date, Time Window, Hall/Venue, and Official Conduct Instructions.",
        "  • PDF export capability for student hall tickets and revision planning."
    ], width=342, bg="#F5F3FF", border="#C4B5FD")

    story.append(Table([[c1, c2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 6: FACULTY SECTION SCOPING & ATTENDANCE ------------------
    story.append(Paragraph("05. Faculty Section Isolation & Anti-Tamper Attendance", s_title))
    story.append(Paragraph("Enforcing assigned instructional boundaries and time-locked compliance in attendance tracking.", s_sub))

    c_f1 = make_card("Faculty Section & Subject Scoping", [
        "<b>Zero Cross-Section Leakage:</b> Instructors only see cohorts specifically allocated to them by the University Administrator.",
        "<b>Enrolled Students Directory:</b> Displays section-wise student rosters with register number, roll code, email, and live attendance %.",
        "<b>Assigned Subject Filtering:</b> Dropdown displays only subjects taught by the logged-in faculty, preventing unauthorized modifications.",
        "<b>Section Switcher Tabs:</b> Seamless navigation between assigned sections (e.g. CSE-A, CSE-B) with instant student counter badges."
    ], width=342, bg="#F0FDF4", border="#86EFAC")

    c_f2 = make_card("Anti-Tamper Attendance Workflow", [
        "<b>Today-Only Date Lock:</b> The attendance session date input is strictly locked to the current calendar date (disabling historical backdating and premature logging).",
        "<b>Streamlined Status Controls:</b> Binary <font color='#16A34A'><b>Present</b></font> and <font color='#DC2626'><b>Absent</b></font> toggles with 'Mark All Present' convenience accelerator.",
        "<b>Instant Batch Commit:</b> Saves session array with student IDs, attendance state, faculty signature, and server timestamp.",
        "<b>Automatic Aggregate Update:</b> Dynamically recalculates student total attended sessions, cumulative attendance %, and triggers low attendance warnings (< 75%)."
    ], width=342, bg="#FEFCE8", border="#FDE047")

    story.append(Table([[c_f1, c_f2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 7: COURSEWORK & STUDY MATERIALS ------------------
    story.append(Paragraph("06. Section-Scoped Coursework & Study Materials", s_title))
    story.append(Paragraph("Cloud document distribution and assignment submission tracking with granular section privacy.", s_sub))

    c_m1 = make_card("Course Materials Upload & Distribution", [
        "<b>File Upload Integration:</b> Instructors upload syllabus notes, lab sheets, and lecture slides via native file picker.",
        "<b>Section-Scoped Visibility:</b> Materials tagged to specific sections (e.g., CSE-B) appear exclusively in that section's student portal.",
        "<b>Persistent Metadata:</b> Stores document title, subject code, file size, MIME type, upload timestamp, and download URL.",
        "<b>Student Repository:</b> One-click secure asset retrieval with inline preview for PDFs and documents."
    ], width=342, bg="#F8FAFC", border="#CBD5E1")

    c_m2 = make_card("Assignments & Student Submission Ledger", [
        "<b>Task Creation:</b> Faculty define assignment prompt, deadline, maximum marks, and submission format requirements.",
        "<b>Student Submission Vault:</b> Dedicated faculty review page showing exactly which students submitted, submission text, attached file links, and submission timestamps.",
        "<b>Grading & Evaluation:</b> Instructors award marks, enter feedback comments, and synchronize grades directly to student progress cards.",
        "<b>Real-time Sync:</b> Students receive instant alerts when coursework is assigned or graded."
    ], width=342, bg="#EFF6FF", border="#93C5FD")

    story.append(Table([[c_m1, c_m2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 8: ONLINE EXAMINATION ENGINE ------------------
    story.append(Paragraph("07. Online Examination & Proctoring Pipeline", s_title))
    story.append(Paragraph("Secure, time-bounded multiple-choice examination system with real-time browser integrity proctoring.", s_sub))

    c_e1 = make_card("Exam Authoring & Operational Lifecycle", [
        "<b>Comprehensive Setup:</b> Title, Department, Semester, Section, Subject, Exam Date, Time Window, and Duration (mins).",
        "<b>Scoring Parameters:</b> Total marks, Passing cutoff, and configurable negative marking per question.",
        "<b>Dynamic MCQ Builder:</b> Instructors add questions, 4 option choices, designate correct key, and assign question weights.",
        "<b>State Machine Lifecycle:</b>",
        "  • <font color='#D97706'><b>UPCOMING:</b></font> Scheduled before start time.",
        "  • <font color='#2563EB'><b>AVAILABLE:</b></font> Active exam window open for student attempts.",
        "  • <font color='#DC2626'><b>EXPIRED:</b></font> Window closed; attempts barred.",
        "  • <font color='#16A34A'><b>RESULTS RELEASED:</b></font> Scores and answer keys visible."
    ], width=342, bg="#FEF3C7", border="#FCD34D")

    c_e2 = make_card("Student Exam Interface & Anti-Cheat Proctoring", [
        "<b>Single-Attempt Enforcer:</b> Students who have already written the exam cannot re-attempt under any circumstance.",
        "<b>Live Countdown Timer:</b> Synchronized with server clock; auto-submits responses upon expiration.",
        "<b>Tab-Switch & Blur Monitoring:</b>",
        "  • Detects when student unfocuses window or navigates to another browser tab.",
        "  • Displays alert warning modal and increments proctoring infraction counter.",
        "  • Logs total tab switches in final attempt payload for faculty integrity review.",
        "<b>Deterministic Auto-Evaluation:</b> Immediately compares student choices against answer keys on server submit."
    ], width=342, bg="#F0FDF4", border="#86EFAC")

    story.append(Table([[c_e1, c_e2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 9: RESULTS RELEASE & STUDENT VISIBILITY ------------------
    story.append(Paragraph("08. Result Release Governance & Student Review", s_title))
    story.append(Paragraph("Faculty-controlled result publication guaranteeing transparent evaluation and perpetual access.", s_sub))

    c_r1 = make_card("Faculty Result Release Workflow", [
        "<b>Controlled Release Button:</b> Faculty review submission analytics, score distribution, and pass rate before hitting 'Release Results'.",
        "<b>Instant Status Transition:</b> Sets <font face='Courier'>resultsReleased = true</font> and shifts exam status to <font color='#16A34A'><b>RESULTS RELEASED (CLOSED)</b></font>.",
        "<b>Lockout of Future Attempts:</b> Automatically closes exam window to any unattempted students, safeguarding exam integrity.",
        "<b>Instant Broadcast:</b> Dispatches WebSocket notification triggering real-time UI refresh on all student dashboards."
    ], width=342, bg="#F5F3FF", border="#C4B5FD")

    c_r2 = make_card("Student Scorecard & Question Review", [
        "<b>Unbroken Visibility:</b> Written exams remain permanently visible in student portal under 'Completed & Results' tab even after window expiration.",
        "<b>Detailed Scorecard:</b>",
        "  • Marks Obtained vs. Total Marks (e.g. 20 / 20 M).",
        "  • Percentage and Official <font color='#16A34A'><b>PASSED</b></font> / <font color='#DC2626'><b>NEEDS IMPROVEMENT</b></font> badge.",
        "  • Submission timestamp and Recorded tab-switch count.",
        "<b>Interactive Question Breakdown:</b> Shows student choice, correct answer, and explanation for post-exam review."
    ], width=342, bg="#EFF6FF", border="#93C5FD")

    story.append(Table([[c_r1, c_r2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 10: REAL-TIME SYNC & WEBSOCKET ENGINE ------------------
    story.append(Paragraph("09. Real-Time WebSocket Infrastructure & Event Bus", s_title))
    story.append(Paragraph("Socket.IO bi-directional communication ensuring instant collaboration across all academic stakeholders.", s_sub))

    ws_data = [
        [
            Paragraph("<b>Socket Event Channel</b>", ParagraphStyle('WH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Emitter Role</b>", ParagraphStyle('WH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Target Audience</b>", ParagraphStyle('WH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Operational Impact / UI Reaction</b>", ParagraphStyle('WH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
        ],
        [Paragraph("<font face='Courier'>timetable_updated</font>", code_p), Paragraph("Administrator", card_p), Paragraph("Dept Students & Faculty", card_p), Paragraph("Refreshes weekly timetable grid and room allocations without manual page reload.", card_p)],
        [Paragraph("<font face='Courier'>attendance_marked</font>", code_p), Paragraph("Teaching Faculty", card_p), Paragraph("Section Students", card_p), Paragraph("Updates live attendance counters, percentage gauge, and low attendance alerts.", card_p)],
        [Paragraph("<font face='Courier'>material_published</font>", code_p), Paragraph("Teaching Faculty", card_p), Paragraph("Cohort Section", card_p), Paragraph("Surfaces newly shared study PDF/link in Student Study Materials tab instantly.", card_p)],
        [Paragraph("<font face='Courier'>exam_results_released</font>", code_p), Paragraph("Teaching Faculty", card_p), Paragraph("Exam Students", card_p), Paragraph("Reveals final scores, pass/fail status, and question solutions to test takers.", card_p)],
        [Paragraph("<font face='Courier'>exam_scheduled</font>", code_p), Paragraph("Admin / Faculty", card_p), Paragraph("Target Students", card_p), Paragraph("Injects upcoming test card into student calendar and assessment notifications.", card_p)],
    ]
    t_ws = Table(ws_data, colWidths=[140, 100, 130, 326], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 5),
    ])
    story.append(t_ws)
    story.append(PageBreak())

    # ------------------ SLIDE 11: SECURITY & DEVOPS PIPELINE ------------------
    story.append(Paragraph("10. Security Architecture & Deployment Topology", s_title))
    story.append(Paragraph("Enterprise-grade security controls, input sanitization, and production cloud orchestration.", s_sub))

    c_s1 = make_card("Application & Data Security Safeguards", [
        "<b>Stateless JWT Bearer Auth:</b> Cryptographically signed tokens carrying user ID, role, department, and section claims.",
        "<b>RBAC Route Gateways:</b> Express middleware verifying roles before invoking controller logic (<font face='Courier'>verifyToken, checkRole</font>).",
        "<b>CORS & Payload Limits:</b> Whitelisted origins, parameterized queries preventing NoSQL injection, and sanitized file uploads.",
        "<b>Credential Protection:</b> Passwords hashed with BCrypt (10 salt rounds); secrets stored in strictly isolated environment variables."
    ], width=342, bg="#F8FAFC", border="#CBD5E1")

    c_s2 = make_card("Cloud Deployment & Continuous Delivery", [
        "<b>Frontend CDN (Vercel):</b> React SPA deployed on global Edge Network with client-side routing rewrites and asset caching.",
        "<b>Backend Host:</b> Node.js + Express cluster on Linux server container with automated process management (PM2).",
        "<b>Database Hosting:</b> MongoDB Atlas M0/M10 replica set with TLS 1.3 encryption-in-transit and automated snapshots.",
        "<b>Repository Layout:</b> Monorepo structure separating <font face='Courier'>frontend/</font>, <font face='Courier'>backend/</font>, and <font face='Courier'>docs/</font> for streamlined maintenance."
    ], width=342, bg="#EEF2FF", border="#C7D2FE")

    story.append(Table([[c_s1, c_s2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(PageBreak())

    # ------------------ SLIDE 12: CONCLUSION & FUTURE ROADMAP ------------------
    story.append(Paragraph("11. Summary of Achievements & Future Roadmap", s_title))
    story.append(Paragraph("Transforming university academic operations through robust software engineering.", s_sub))

    c_c1 = make_card("Key Project Achievements", [
        "<b>100% Operational Cohesion:</b> Eliminated cross-system data synchronization gaps by uniting timetables, attendance, coursework, and exams.",
        "<b>Zero-Downtime Architecture:</b> Proven dual-store resilience guarantees 24/7 administrative continuity even during network partitioning.",
        "<b>Academic Anti-Fraud Guarantees:</b> Date-locked attendance sessions and tab-switch monitored examinations eliminate common malpractice vectors.",
        "<b>Exceptional User Experience:</b> Sub-100ms UI interactions, responsive modern design, and dark/light ambient theme support."
    ], width=342, bg="#F0FDF4", border="#BBF7D0")

    c_c2 = make_card("Future Expansion Roadmap", [
        "<b>Mobile Applications:</b> Native iOS & Android portals built via React Native / Capacitor with push notifications.",
        "<b>AI Performance Diagnostics:</b> Predictive machine learning models identifying academically at-risk students for early intervention.",
        "<b>Biometric Attendance Hardware:</b> IoT fingerprint / facial recognition gateways syncing directly via REST API.",
        "<b>Automated University Accreditation:</b> One-click generation of NAAC / NBA compliance audits and outcome-based education (OBE) metrics."
    ], width=342, bg="#F5F3FF", border="#DDD6FE")

    story.append(Table([[c_c1, c_c2]], colWidths=[348, 348], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))

    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    build_ppt()
