"""
Generates docs/Project_Documentation.pdf
Comprehensive Software Requirements Specification (SRS) & System Architecture Report.
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
            return  # Suppress on title page

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 805, "EDU TRACK: STUDENT ACADEMIC MANAGEMENT SYSTEM  |  SRS & SYSTEM SPECIFICATION")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 797, 541, 797)

        self.setFont("Helvetica", 8)
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Confidential – Full-Stack MERN Academic Management & Proctoring System")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()


def build_documentation():
    pdf_path = os.path.join("docs", "Project_Documentation.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    primary = colors.HexColor("#1E3A8A")   # Blue 900
    secondary = colors.HexColor("#0284C7") # Sky 600
    accent = colors.HexColor("#4338CA")    # Indigo 700
    dark = colors.HexColor("#0F172A")      # Slate 900
    body_color = colors.HexColor("#334155")# Slate 700

    title_style = ParagraphStyle(
        'DocTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=primary, alignment=1, spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=20
    )
    h1 = ParagraphStyle(
        'H1', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=primary, spaceBefore=14, spaceAfter=6, keepWithNext=True
    )
    h2 = ParagraphStyle(
        'H2', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=accent, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    p = ParagraphStyle(
        'P', fontName='Helvetica', fontSize=9, leading=13, textColor=body_color, spaceAfter=5
    )
    p_bold = ParagraphStyle(
        'PBold', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=dark, spaceAfter=4
    )
    bullet = ParagraphStyle(
        'Bullet', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=body_color, leftIndent=14, firstLineIndent=-9, spaceAfter=3
    )
    callout = ParagraphStyle(
        'Callout', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor("#1E293B"),
        backColor=colors.HexColor("#EFF6FF"), borderColor=colors.HexColor("#93C5FD"), borderWidth=0.8, borderPadding=6, spaceAfter=6
    )
    code = ParagraphStyle(
        'Code', fontName='Courier', fontSize=7.5, leading=10, textColor=dark,
        backColor=colors.HexColor("#F8FAFC"), borderColor=colors.HexColor("#E2E8F0"), borderWidth=0.5, borderPadding=5, spaceAfter=5
    )
    th = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white)
    td = ParagraphStyle('TD', fontName='Helvetica', fontSize=8, leading=10.5, textColor=dark)
    td_b = ParagraphStyle('TDB', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=dark)

    story = []

    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</b>", ParagraphStyle('Dept', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=secondary, alignment=1, spaceAfter=15)))
    story.append(Paragraph("<b>PROJECT SPECIFICATION & ARCHITECTURE REPORT</b>", ParagraphStyle('ReportBadge', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=accent, alignment=1, spaceAfter=20)))
    story.append(HRFlowable(width="60%", thickness=2, color=primary, spaceAfter=25, spaceBefore=5))
    story.append(Paragraph("Edu Track – Student Academic Management System", title_style))
    story.append(Paragraph("A Robust, Role-Governed Full-Stack University Operating Suite with Real-Time Timetable Conflict Engines, Anti-Tamper Attendance, Section-Scoped Coursework, and Automated Proctoring", subtitle_style))
    story.append(Spacer(1, 30))

    meta_table = Table([
        [Paragraph("<b>Project Title:</b>", td_b), Paragraph("Edu Track Academic Management System", td)],
        [Paragraph("<b>Architecture Pattern:</b>", td_b), Paragraph("Multi-Tier MERN Architecture + Dual-Store High-Availability Engine", td)],
        [Paragraph("<b>Client Technology:</b>", td_b), Paragraph("React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts", td)],
        [Paragraph("<b>Server Technology:</b>", td_b), Paragraph("Node.js, Express, Socket.IO, JWT Security, Multer", td)],
        [Paragraph("<b>Persistence Layer:</b>", td_b), Paragraph("MongoDB Atlas Cloud Database + Autonomous Local JSON Store Engine", td)],
        [Paragraph("<b>Deployment Topology:</b>", td_b), Paragraph("Vercel Global Edge Network (Frontend) + Dedicated Node Service (Backend)", td)],
        [Paragraph("<b>Security Model:</b>", td_b), Paragraph("Role-Based Access Control (Admin, Faculty, Student) with Stateless JWT", td)],
        [Paragraph("<b>Document Release:</b>", td_b), Paragraph("Production Engineering Version 2.4.0 (November 2026)", td)],
    ], colWidths=[160, 327], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(meta_table)
    story.append(Spacer(1, 40))

    abstract_text = (
        "<b>Abstract:</b> Higher education institutions face mounting challenges when operating across disconnected software "
        "utilities for course scheduling, daily attendance verification, learning asset distribution, and student examination proctoring. "
        "Edu Track establishes a singular, integrated, role-governed platform uniting Institutional Administrators, Teaching Faculty, "
        "and Enrolled Students into an event-driven operating environment. Built upon modern web primitives, the system introduces: "
        "(1) an automated scheduling conflict detection engine preventing room, instructor, and student cohort overlaps; "
        "(2) an anti-tamper single-day attendance logging workflow; (3) strict section-level isolation for coursework and study materials; "
        "(4) an online examination suite featuring tab-switch proctoring and immediate auto-evaluation; and "
        "(5) an autonomous dual-store persistence engine ensuring zero operational interruption if cloud databases become unreachable. "
        "This document presents the definitive Software Requirements Specification (SRS), system architecture, detailed algorithms, "
        "and test validations of the platform."
    )
    story.append(Paragraph(abstract_text, callout))
    story.append(PageBreak())

    # ------------------ CHAPTER 1: INTRODUCTION ------------------
    story.append(Paragraph("1. Introduction & Project Scope", h1))
    story.append(Paragraph(
        "Modern university governance requires rigorous record-keeping, conflict-free instructional scheduling, dependable attendance "
        "metrics, and transparent academic evaluation pipelines. Traditional setups typically rely on disparate legacy software packages "
        "or paper-driven rosters, leading to administrative bottlenecks, scheduling clashes, data synchronization latency, and security vulnerabilities.",
        p
    ))
    story.append(Paragraph("1.1 Core Objectives", h2))
    story.append(Paragraph("• <b>Unified Academic Operating Environment:</b> Eliminate operational silos by centralizing user management, timetable planning, attendance records, coursework sharing, examinations, and grade point calculations.", bullet))
    story.append(Paragraph("• <b>Proactive Conflict Prevention:</b> Validate multi-dimensional constraints (classroom capacity, instructor allocation, student cohort schedule) at time of timetable entry rather than discovering clashes in production.", bullet))
    story.append(Paragraph("• <b>Continuous High Availability:</b> Guarantee uninterrupted campus workflows through an autonomous dual-store engine that falls back to local structured JSON persistence if cloud databases drop offline.", bullet))
    story.append(Paragraph("• <b>Integrity in Daily Attendance:</b> Lock session marking strictly to the active calendar date, preventing backdated attendance fraud and unverified historic record updates.", bullet))
    story.append(Paragraph("• <b>Fair & Monitored Online Testing:</b> Provide web-based assessments with strict time-window enforcement, automatic tab-switch detection, automated objective evaluation, and faculty-governed score releases.", bullet))

    story.append(Paragraph("1.2 System Stakeholders & User Classes", h2))
    story.append(Paragraph("The platform defines three strictly segregated user classes with distinct operational responsibilities:", p))
    story.append(Paragraph("• <b>Institutional Administrator:</b> Full governance over academic departments, course subjects, instructional cohorts, student rosters, faculty appointments, semester examination schedules, and institutional audit trails.", bullet))
    story.append(Paragraph("• <b>Teaching Faculty:</b> Confined strictly to assigned instructional sections and courses. Marks daily student attendance, uploads section-scoped study materials, publishes coursework, authors online quizzes, and releases scores.", bullet))
    story.append(Paragraph("• <b>Enrolled Student:</b> Accesses personalized weekly schedules, department semester exam dates, personal attendance percentages, section study materials, online assessments, and official cumulative academic transcripts.", bullet))
    story.append(Spacer(1, 6))

    # ------------------ CHAPTER 2: SOFTWARE REQUIREMENTS SPECIFICATION ------------------
    story.append(Paragraph("2. Software Requirements Specification (SRS)", h1))
    story.append(Paragraph("2.1 Functional Requirements Matrix", h2))

    fr_data = [
        [Paragraph("<b>Req ID</b>", th), Paragraph("<b>Module</b>", th), Paragraph("<b>Functional Specification</b>", th), Paragraph("<b>Priority</b>", th)],
        [Paragraph("FR-01", td_b), Paragraph("Authentication", td), Paragraph("Stateless JWT authentication with encrypted credential verification and role claim validation.", td), Paragraph("CRITICAL", td_b)],
        [Paragraph("FR-02", td_b), Paragraph("Administration", td), Paragraph("Creation and persistent storage of academic departments, subjects, student and faculty accounts.", td), Paragraph("CRITICAL", td_b)],
        [Paragraph("FR-03", td_b), Paragraph("Class Timetable", td), Paragraph("Weekly instructional schedule matrix with automated multi-variable collision detection engine.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-04", td_b), Paragraph("Exam Timetable", td), Paragraph("Schedule semester exams with department-filtered subject dropdown and universal student visibility.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-05", td_b), Paragraph("Attendance", td), Paragraph("Lock session marking to current calendar date; provide binary Present/Absent batch toggles.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-06", td_b), Paragraph("Section Scoping", td), Paragraph("Restrict faculty visibility strictly to allocated sections and assigned departmental courses.", td), Paragraph("CRITICAL", td_b)],
        [Paragraph("FR-07", td_b), Paragraph("Study Materials", td), Paragraph("Upload instructional documents with section-scoped distribution and student download access.", td), Paragraph("MEDIUM", td_b)],
        [Paragraph("FR-08", td_b), Paragraph("Coursework Tasks", td), Paragraph("Publish assignments; capture student file/text submissions in a faculty review ledger.", td), Paragraph("MEDIUM", td_b)],
        [Paragraph("FR-09", td_b), Paragraph("Online Exams", td), Paragraph("Create time-bounded MCQ assessments with passing cutoffs, timer, and tab-switch proctoring.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-10", td_b), Paragraph("Auto-Grading", td), Paragraph("Deterministically evaluate student answers against correct keys upon submission.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-11", td_b), Paragraph("Result Release", td), Paragraph("Faculty-governed release trigger unlocking student scorecards and review breakdown.", td), Paragraph("HIGH", td_b)],
        [Paragraph("FR-12", td_b), Paragraph("Dual-Store Sync", td), Paragraph("Seamless failover between MongoDB Atlas and atomic JSON persistence engine.", td), Paragraph("CRITICAL", td_b)],
    ]
    t_fr = Table(fr_data, colWidths=[45, 80, 312, 50], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(t_fr)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Non-Functional Requirements (NFR)", h2))
    story.append(Paragraph("• <b>NFR-01 Performance:</b> REST API response latency under 60 milliseconds for cached and index-backed read operations.", bullet))
    story.append(Paragraph("• <b>NFR-02 High Availability:</b> 99.95% system availability maintained through autonomous dual-store failover engine.", bullet))
    story.append(Paragraph("• <b>NFR-03 Data Integrity:</b> Complete foreign key referential consistency across rosters, timetables, and exam submissions.", bullet))
    story.append(Paragraph("• <b>NFR-04 Security & Privacy:</b> Passwords hashed with bcrypt (salt rounds = 10); strict section-level isolation prevents cross-cohort data leakage.", bullet))
    story.append(Paragraph("• <b>NFR-05 Usability:</b> Mobile-responsive interface adhering to WCAG 2.1 accessibility standards with intuitive dark/light theme switching.", bullet))
    story.append(PageBreak())

    # ------------------ CHAPTER 3: SYSTEM ARCHITECTURE & DUAL STORE ------------------
    story.append(Paragraph("3. System Architecture & Dual-Store Resilience", h1))
    story.append(Paragraph(
        "The system employs a decomposed multi-tier architecture dividing responsibilities between the Presentation Layer, "
        "the Application Gateway, and a Resilient Persistence Subsystem.",
        p
    ))

    arch_box = (
        "<b>Architectural Flow Overview:</b><br/>"
        "[Client Browser: React 18 SPA] <--- HTTPS / WSS ---> [Express API Gateway & Socket.IO Bus]<br/>"
        "                                                      |<br/>"
        "                     +--------------------------------+--------------------------------+<br/>"
        "                     |                                                                 |<br/>"
        "       [Primary Database: MongoDB Atlas]                             [Fallback Store: Local JSON Engine]<br/>"
        "       - Cloud Replica Set (M0/M10)                                 - Structured JSON Collections<br/>"
        "       - Mongoose Document ODM                                       - Atomic FS Rename Writes<br/>"
        "       - High-concurrency indexing                                   - Zero Cloud Dependency"
    )
    story.append(Paragraph(arch_box, code))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.1 Dual-Store Failover & Reconnect Algorithm", h2))
    story.append(Paragraph(
        "To insulate academic operations against internet outages or cloud database connection drops, the backend implements an autonomous "
        "persistence abstraction layer (<font face='Courier'>server/store/dualStore.ts</font>).",
        p
    ))
    story.append(Paragraph("• <b>Heartbeat Monitor:</b> A lightweight background timer regularly pings MongoDB Atlas with a 2000ms timeout threshold.", bullet))
    story.append(Paragraph("• <b>Autonomous Degraded Mode:</b> If MongoDB pings fail, the active driver automatically switches internal write/read pointers to local JSON files stored under <font face='Courier'>server/data/</font>.", bullet))
    story.append(Paragraph("• <b>Atomic Disk Commits:</b> Local updates are written first to temporary buffer files and committed using atomic file replacement (<font face='Courier'>fs.renameSync</font>), guaranteeing zero file corruption during power failures.", bullet))
    story.append(Paragraph("• <b>Transparent DTO Contract:</b> Client endpoints receive identical response payloads regardless of active store, accompanied by diagnostic header <font face='Courier'>X-Data-Source: mongo | json</font>.", bullet))
    story.append(Paragraph("• <b>Self-Healing Reconnection:</b> When Atlas connectivity is re-established, the backend triggers reconciliation routines synchronizing local mutations back to cloud collections.", bullet))
    story.append(Spacer(1, 8))

    # ------------------ CHAPTER 4: CORE BUSINESS ALGORITHMS ------------------
    story.append(Paragraph("4. Core Business Algorithms & Engines", h1))
    
    story.append(Paragraph("4.1 Timetable Conflict Detection Algorithm", h2))
    story.append(Paragraph(
        "When an administrator schedules a class period (<font face='Courier'>POST /api/timetable/class</font>), the system validates three mutually exclusive constraints before persisting the record:",
        p
    ))

    algo_text = (
        "<b>Algorithm: ValidateTimetablePeriod(NewPeriod P)</b><br/>"
        "1. Let <i>R</i> = P.room, <i>F</i> = P.facultyId, <i>C</i> = {P.department, P.semester, P.section}, <i>T</i> = {P.day, P.periodSlot}<br/>"
        "2. Query existing periods matching slot <i>T</i>:<br/>"
        "   a. <b>Room Clash Check:</b> If any period has <font face='Courier'>period.room == R</font>, throw <i>'Classroom R is already reserved for cohort ' + period.section</i><br/>"
        "   b. <b>Faculty Clash Check:</b> If any period has <font face='Courier'>period.facultyId == F</font>, throw <i>'Faculty member is already scheduled in room ' + period.room</i><br/>"
        "   c. <b>Cohort Clash Check:</b> If any period matches cohort <i>C</i>, throw <i>'Section ' + C.section + ' already has a scheduled class during this period'</i><br/>"
        "3. If all checks evaluate false, commit <i>P</i> to database.<br/>"
        "4. Broadcast event <font face='Courier'>timetable_updated</font> with payload <i>{ department, semester, section }</i> via Socket.IO."
    )
    story.append(Paragraph(algo_text, code))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Anti-Tamper Attendance Single-Day Enforcement", h2))
    story.append(Paragraph(
        "Attendance fraud frequently occurs when instructors backdate records. Edu Track resolves this at both UI and API layers: "
        "The date picker is strictly locked to the current system date (<font face='Courier'>new Date().toISOString().split('T')[0]</font>). "
        "On server receipt, the backend verifies that the submitted session date matches the server's current calendar day (within a 12-hour timezone tolerance), "
        "rejecting historic or future timestamps.",
        p
    ))

    story.append(Paragraph("4.3 Online Exam Lifecycle & Proctoring State Machine", h2))
    story.append(Paragraph(
        "Online exams progress through an immutable state machine:",
        p
    ))
    story.append(Paragraph("• <b>DRAFT:</b> Exam created by instructor; questions and timings editable.", bullet))
    story.append(Paragraph("• <b>SCHEDULED:</b> Exam published; students see start date and preparation guidelines.", bullet))
    story.append(Paragraph("• <b>ACTIVE (AVAILABLE):</b> Active examination window. Single-attempt rule enforced. Countdown timer active. Tab switches monitored via browser <font face='Courier'>window.onblur</font> and <font face='Courier'>document.visibilitychange</font>.", bullet))
    story.append(Paragraph("• <b>CLOSED:</b> Examination deadline passed; no new attempts permitted.", bullet))
    story.append(Paragraph("• <b>RESULTS RELEASED:</b> Faculty clicks 'Release Results'. Written attempts unlock student scorecards, percentage calculation, pass/fail status, and question answer keys.", bullet))
    story.append(PageBreak())

    # ------------------ CHAPTER 5: VERIFICATION & TESTING ------------------
    story.append(Paragraph("5. Verification, Testing & Quality Assurance", h1))
    story.append(Paragraph(
        "The platform underwent systematic test procedures covering unit components, integration bridges, network fault injection, and user role boundaries.",
        p
    ))

    test_table = [
        [Paragraph("<b>Test Case ID</b>", th), Paragraph("<b>Test Scope / Condition</b>", th), Paragraph("<b>Expected Behavior</b>", th), Paragraph("<b>Result</b>", th)],
        [Paragraph("TC-SEC-01", td_b), Paragraph("Access admin routes with student JWT token", td), Paragraph("HTTP 403 Forbidden returned; unauthorized route blocked.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-TIME-01", td_b), Paragraph("Schedule 2 classes in Room 301 at Monday 10:00 AM", td), Paragraph("Collision engine intercepts conflict; outputs descriptive alert.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-ATT-01", td_b), Paragraph("Attempt to submit attendance for yesterday's date", td), Paragraph("Date picker locked to today; API rejects out-of-bounds date.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-FAIL-01", td_b), Paragraph("Simulate MongoDB network disconnection", td), Paragraph("Store switches to local JSON; write succeeds with zero errors.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-EXAM-01", td_b), Paragraph("Student completes exam; attempts second submission", td), Paragraph("System flags attempt as already submitted; access barred.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-EXAM-02", td_b), Paragraph("Student switches browser tabs during exam", td), Paragraph("Proctoring alert modal displays; tab switch count logged.", td), Paragraph("PASSED", td_b)],
        [Paragraph("TC-EXAM-03", td_b), Paragraph("Faculty clicks 'Release Results' for closed exam", td), Paragraph("Student portal reveals scores and question review solutions.", td), Paragraph("PASSED", td_b)],
    ]
    t_test = Table(test_table, colWidths=[65, 150, 222, 50], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(t_test)
    story.append(Spacer(1, 10))

    # ------------------ CHAPTER 6: REPOSITORY LAYOUT & DEPLOYMENT ------------------
    story.append(Paragraph("6. Repository Structure & Deployment Topology", h1))
    story.append(Paragraph(
        "To satisfy industry modularity standards and simplify CI/CD pipelines, the codebase is arranged in a clean tripartite layout:",
        p
    ))

    repo_tree = (
        "Edu-Track-Student-Academic-Management-System/<br/>"
        "├── frontend/                 # React 18 + Vite + TypeScript frontend source code<br/>"
        "│   ├── src/                  # Components, portals, hooks, and services<br/>"
        "│   ├── public/               # Static assets, branding, and icons<br/>"
        "│   ├── package.json          # Frontend dependencies & Vite scripts<br/>"
        "│   └── vite.config.ts        # Optimized bundler configuration<br/>"
        "├── backend/                  # Node.js + Express backend service<br/>"
        "│   ├── routes/               # Modular REST endpoints (auth, timetable, exam, etc.)<br/>"
        "│   ├── store/                # DualStore engine & JSON fallback persistence<br/>"
        "│   ├── data/                 # Atomic local JSON database files<br/>"
        "│   ├── server.ts             # Gateway entrypoint & Socket.IO initialization<br/>"
        "│   └── package.json          # Server dependencies & scripts<br/>"
        "└── docs/                     # Official project engineering documents<br/>"
        "    ├── Project_PPT.pdf<br/>"
        "    ├── Project_Documentation.pdf<br/>"
        "    ├── Database_Design.pdf<br/>"
        "    └── API_Documentation.pdf"
    )
    story.append(Paragraph(repo_tree, code))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.1 Production Hosting Configuration", h2))
    story.append(Paragraph(
        "• <b>Frontend Hosting:</b> Deployed on Vercel Edge Network with automatic Brotli/Gzip compression, HTTP/2 multiplexing, and SPA client routing rewrites configured via <font face='Courier'>vercel.json</font>.",
        bullet
    ))
    story.append(Paragraph(
        "• <b>Backend Hosting:</b> Node.js process managed via PM2 on scalable cloud compute, binding to port 5000 with CORS authorization allowing the live Vercel domain.",
        bullet
    ))
    story.append(Paragraph(
        "• <b>Database Hosting:</b> MongoDB Atlas cloud replica cluster with automated volume backups and TLS encryption in transit.",
        bullet
    ))
    story.append(Spacer(1, 10))

    # ------------------ CHAPTER 7: CONCLUSION ------------------
    story.append(Paragraph("7. Conclusion & Future Roadmap", h1))
    story.append(Paragraph(
        "Edu Track demonstrates how modern full-stack web engineering solves longstanding university administrative challenges. "
        "By enforcing strict role-based access control, validating timetable collisions proactively, preventing attendance backdating, "
        "providing a secure online examination environment, and guaranteeing high availability via dual-store resilience, "
        "the system delivers a dependable, scalable, and intuitive digital foundation for academic institutions.",
        p
    ))
    story.append(Paragraph(
        "Planned enhancements include cross-platform mobile apps using React Native, automated AI student performance diagnostics, "
        "biometric attendance integration, and automated institutional accreditation report generation.",
        p
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    build_documentation()
