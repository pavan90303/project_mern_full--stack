"""
Generates docs/Database_Design.pdf
Exhaustive Database Design, Entity-Relationship Model & 16-Collection Schema Specification.
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
        self.drawString(54, 805, "EDU TRACK: DATABASE DESIGN & SCHEMA SPECIFICATION  |  MONGODB & DUAL-STORE")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 797, 541, 797)

        self.setFont("Helvetica", 8)
        self.line(54, 45, 541, 45)
        self.drawString(54, 32, "Confidential – Edu Track Persistence Architecture & Schema Reference")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(541, 32, page_str)
        self.restoreState()


def build_db_design():
    pdf_path = os.path.join("docs", "Database_Design.pdf")
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

    def make_schema_table(collection_name, description, fields):
        rows = [
            [Paragraph(f"<b>Collection: <font color='#4338CA'>{collection_name}</font></b> — {description}", ParagraphStyle('CT', fontName='Helvetica-Bold', fontSize=8, textColor=dark, backColor=colors.HexColor('#E0E7FF'), borderPadding=4)), "", "", "", ""]
        ]
        rows.append([
            Paragraph("<b>Field Name</b>", th),
            Paragraph("<b>BSON / JSON Type</b>", th),
            Paragraph("<b>Required</b>", th),
            Paragraph("<b>Default / Constraints</b>", th),
            Paragraph("<b>Description & Foreign Key</b>", th)
        ])
        for f in fields:
            rows.append([
                Paragraph(f[0], td_c),
                Paragraph(f[1], td),
                Paragraph(f[2], td_b),
                Paragraph(f[3], td),
                Paragraph(f[4], td)
            ])
        t = Table(rows, colWidths=[110, 80, 50, 100, 147], style=[
            ('SPAN', (0,0), (-1,0)),
            ('BACKGROUND', (0,1), (-1,1), primary),
            ('GRID', (0,1), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0,2), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
            ('PADDING', (0,0), (-1,-1), 3),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ])
        return t

    story = []

    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>ENTERPRISE PERSISTENCE ARCHITECTURE</b>", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=secondary, alignment=1, spaceAfter=15)))
    story.append(Paragraph("<b>DATABASE DESIGN & SCHEMA REFERENCE SPECIFICATION</b>", ParagraphStyle('Title2', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=accent, alignment=1, spaceAfter=18)))
    story.append(HRFlowable(width="60%", thickness=2, color=primary, spaceAfter=20, spaceBefore=5))
    story.append(Paragraph("Edu Track: Unified Data Architecture", title_style))
    story.append(Paragraph("High-Performance Document Modeling with Relational Integrity Constraints & Dual-Store Autonomous Synchronization", subtitle_style))
    story.append(Spacer(1, 20))

    meta = Table([
        [Paragraph("<b>Database Engine:</b>", td_b), Paragraph("MongoDB Atlas (M0/M10 Replica Set) + Local JSON Fallback Store", td)],
        [Paragraph("<b>Data Modeling Approach:</b>", td_b), Paragraph("Hybrid Document-Relational with Foreign Keys & In-Memory Indices", td)],
        [Paragraph("<b>Collection Count:</b>", td_b), Paragraph("16 Structured Production Collections", td)],
        [Paragraph("<b>ACID Atomicity:</b>", td_b), Paragraph("Document-level atomicity in MongoDB; Atomic fs.rename in JSON mode", td)],
        [Paragraph("<b>Index Strategy:</b>", td_b), Paragraph("Compound indices on {dept, sem, section}, {studentId, examId}, etc.", td)],
    ], colWidths=[150, 337], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(meta)
    story.append(Spacer(1, 25))

    intro_box = (
        "<b>Architectural Overview:</b> Edu Track utilizes a document-oriented persistence paradigm modeled to ensure "
        "ultra-fast read latency for academic rosters, timetables, and real-time assessments while enforcing relational constraints. "
        "Every entity is modeled as a primary collection with cross-collection referencing via foreign keys (<font face='Courier'>studentId, facultyId, subjectId, sectionId</font>). "
        "A dual-store persistence manager mirrors every transaction across MongoDB Atlas and atomic disk-backed JSON stores, "
        "guaranteeing zero data loss during network disconnects."
    )
    story.append(Paragraph(intro_box, callout))
    story.append(PageBreak())

    # ------------------ SECTION 1: ENTITY RELATIONSHIPS ------------------
    story.append(Paragraph("1. Entity Relationship & Cardinality Overview", h1))
    story.append(Paragraph(
        "The schema models the institutional hierarchy starting from Departments down to individual Student Exam Submissions:",
        p
    ))

    er_text = (
        "<b>Core Relational Cardinality:</b><br/>"
        "• <b>Department (1) ---> (N) Subjects:</b> Each department owns multiple curriculum subjects across semesters.<br/>"
        "• <b>Department (1) ---> (N) Sections:</b> A department contains multiple cohort sections (e.g. CSE-A, CSE-B).<br/>"
        "• <b>Section (1) ---> (N) Students:</b> Students belong to exactly one department, semester, and section.<br/>"
        "• <b>Faculty (1) ---> (N) Faculty Assignments:</b> Faculty are assigned specific subjects and sections.<br/>"
        "• <b>Section (1) ---> (N) Class Timetables:</b> Cohort timetable entries mapping day, period, room, subject, and instructor.<br/>"
        "• <b>Department (1) ---> (N) Exam Timetables:</b> Semester examination dates linking department subjects to halls.<br/>"
        "• <b>Faculty + Section (1) ---> (N) Attendance Records:</b> Daily sessions recording student presence.<br/>"
        "• <b>Faculty + Section (1) ---> (N) Course Materials:</b> Section-scoped documents and study notes.<br/>"
        "• <b>Faculty + Section (1) ---> (N) Online Exams:</b> MCQs with total/pass marks, timer, and state machine.<br/>"
        "• <b>Student + Online Exam (1) ---> (1) Exam Attempt:</b> Single-attempt record with score, tab switches, and answers."
    )
    story.append(Paragraph(er_text, code))
    story.append(Spacer(1, 6))

    # ------------------ SECTION 2: 16 PRODUCTION COLLECTIONS ------------------
    story.append(Paragraph("2. Complete Collection Schema Reference", h1))

    # 1. users
    story.append(make_schema_table("users", "Central user identities (Admins, Faculty, Students) with role credentials", [
        ("_id / id", "ObjectId / String", "YES", "UUID v4", "Primary key for authentication and cross-referencing"),
        ("email", "String", "YES", "Unique, Lowercase", "Unique login email address across the institution"),
        ("passwordHash", "String", "YES", "bcrypt(10)", "Securely hashed user password"),
        ("fullName", "String", "YES", "None", "Legal full name of user"),
        ("role", "String", "YES", "'ADMIN' | 'FACULTY' | 'STUDENT'", "RBAC authorization role"),
        ("department", "String", "OPTIONAL", "null for admin", "Department code (e.g., 'Computer Science & Engineering')"),
        ("semester", "Number", "OPTIONAL", "null for faculty", "Current academic semester (1 through 8)"),
        ("section", "String", "OPTIONAL", "null for admin", "Enrolled or assigned section (e.g. 'CSE-A', 'CSE-B')"),
        ("rollNumber", "String", "OPTIONAL", "Unique for students", "Official institutional roll / register number"),
        ("academicCgpa", "Number", "OPTIONAL", "0.00", "Cumulative Grade Point Average (Students only)"),
        ("createdAt", "Date / ISOString", "YES", "Date.now()", "Account provisioning timestamp")
    ]))
    story.append(Spacer(1, 8))

    # 2. departments
    story.append(make_schema_table("departments", "Academic institutional departments and administrative faculties", [
        ("id", "String", "YES", "Auto-generated", "Unique department identifier"),
        ("name", "String", "YES", "Unique", "Full department title (e.g., Computer Science & Engineering)"),
        ("code", "String", "YES", "Unique, Uppercase", "Short uppercase department code (e.g., 'CSE')"),
        ("hodName", "String", "YES", "None", "Name of Head of Department"),
        ("totalSemesters", "Number", "YES", "8", "Duration of academic curriculum in semesters"),
        ("activeSections", "Array<String>", "YES", "['A', 'B']", "List of recognized section letters"),
        ("createdAt", "Date / ISOString", "YES", "Date.now()", "Creation timestamp")
    ]))
    story.append(PageBreak())

    # 3. subjects
    story.append(make_schema_table("subjects", "Department curriculum subjects, course codes, and credit hours", [
        ("id", "String", "YES", "Auto-generated", "Primary subject key"),
        ("code", "String", "YES", "Unique per Dept", "Official course code (e.g., 'CS401', 'CS402')"),
        ("title", "String", "YES", "None", "Subject title (e.g., 'Database Internals & Storage Engines')"),
        ("department", "String", "YES", "FK -> departments.name", "Owning department"),
        ("semester", "Number", "YES", "1-8", "Academic semester level"),
        ("credits", "Number", "YES", "3", "Academic credit units"),
        ("type", "String", "YES", "'THEORY' | 'LAB'", "Instructional category")
    ]))
    story.append(Spacer(1, 8))

    # 4. sections
    story.append(make_schema_table("sections", "Instructional student cohorts and section allocations", [
        ("id", "String", "YES", "Auto-generated", "Unique section identifier"),
        ("name", "String", "YES", "None", "Section code name (e.g. 'CSE-A', 'CSE-B')"),
        ("department", "String", "YES", "FK -> departments.name", "Parent academic department"),
        ("semester", "Number", "YES", "1-8", "Associated semester level"),
        ("capacity", "Number", "YES", "60", "Maximum enrolled student capacity"),
        ("facultyAdvisor", "String", "OPTIONAL", "FK -> users.id", "Faculty coordinator assigned to this section")
    ]))
    story.append(Spacer(1, 8))

    # 5. faculty_assignments
    story.append(make_schema_table("faculty_assignments", "Mapping instructors to specific departmental subjects and cohorts", [
        ("id", "String", "YES", "Auto-generated", "Assignment record identifier"),
        ("facultyId", "String", "YES", "FK -> users.id", "Reference to the teaching faculty account"),
        ("facultyName", "String", "YES", "None", "Cached instructor name for fast lookup"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Assigned subject reference"),
        ("subjectCode", "String", "YES", "FK -> subjects.code", "Cached course code"),
        ("department", "String", "YES", "FK -> departments.name", "Target department"),
        ("semester", "Number", "YES", "1-8", "Target semester"),
        ("section", "String", "YES", "None", "Designated teaching section (e.g. 'CSE-B')")
    ]))
    story.append(Spacer(1, 8))

    # 6. class_timetables
    story.append(make_schema_table("class_timetables", "Weekly instructional timetable matrix with room & period allocations", [
        ("id", "String", "YES", "Auto-generated", "Unique period slot entry"),
        ("dayOfWeek", "String", "YES", "'Monday'..'Saturday'", "Instructional day"),
        ("periodNumber", "Number", "YES", "1 to 8", "Daily period index"),
        ("startTime", "String", "YES", "HH:MM format", "Period commencement time"),
        ("endTime", "String", "YES", "HH:MM format", "Period conclusion time"),
        ("department", "String", "YES", "FK -> departments.name", "Target cohort department"),
        ("semester", "Number", "YES", "1-8", "Target cohort semester"),
        ("section", "String", "YES", "None", "Target section (e.g., 'CSE-A')"),
        ("subjectCode", "String", "YES", "FK -> subjects.code", "Course subject code"),
        ("subjectName", "String", "YES", "None", "Full course name"),
        ("facultyId", "String", "YES", "FK -> users.id", "Assigned faculty member ID"),
        ("facultyName", "String", "YES", "None", "Assigned faculty member name"),
        ("room", "String", "YES", "None", "Physical or virtual lecture room / lab (e.g. 'Hall 101')")
    ]))
    story.append(PageBreak())

    # 7. exam_timetables
    story.append(make_schema_table("exam_timetables", "University semester examination schedules with room venues and timings", [
        ("id", "String", "YES", "Auto-generated", "Unique examination schedule entry"),
        ("department", "String", "YES", "FK -> departments.name", "Department subject to the examination"),
        ("semester", "Number", "YES", "1-8", "Semester level"),
        ("subjectCode", "String", "YES", "FK -> subjects.code", "Examined subject code"),
        ("courseTitle", "String", "YES", "FK -> subjects.title", "Official course title"),
        ("examDate", "String", "YES", "YYYY-MM-DD", "Date of scheduled examination"),
        ("startTime", "String", "YES", "HH:MM format", "Examination start time"),
        ("endTime", "String", "YES", "HH:MM format", "Examination end time"),
        ("room", "String", "YES", "None", "Examination venue / hall (e.g. 'Exam Hall 204')"),
        ("instructions", "String", "OPTIONAL", "University rules", "Candidate guidelines and required stationery"),
        ("createdBy", "String", "YES", "FK -> users.id", "Administrator ID who scheduled the exam")
    ]))
    story.append(Spacer(1, 8))

    # 8. attendance_records
    story.append(make_schema_table("attendance_records", "Daily session attendance tracking locked to calendar date", [
        ("id", "String", "YES", "Auto-generated", "Unique attendance session identifier"),
        ("sessionDate", "String", "YES", "Current Date (YYYY-MM-DD)", "Session date (locked strictly to current day)"),
        ("department", "String", "YES", "FK -> departments.name", "Cohort department"),
        ("semester", "Number", "YES", "1-8", "Cohort semester"),
        ("section", "String", "YES", "None", "Target instructional section"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Associated subject"),
        ("facultyId", "String", "YES", "FK -> users.id", "Instructor who logged attendance"),
        ("records", "Array<Object>", "YES", "[]", "Array of [{ studentId, rollNumber, status: 'present'|'absent' }]"),
        ("submittedAt", "Date / ISOString", "YES", "Date.now()", "Server commit timestamp")
    ]))
    story.append(Spacer(1, 8))

    # 9. course_materials
    story.append(make_schema_table("course_materials", "Section-scoped digital study materials, lecture slides and notes", [
        ("id", "String", "YES", "Auto-generated", "Unique document identifier"),
        ("title", "String", "YES", "None", "Document title / topic description"),
        ("description", "String", "OPTIONAL", "None", "Brief notes or instructions from faculty"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Related academic subject"),
        ("department", "String", "YES", "FK -> departments.name", "Associated department"),
        ("semester", "Number", "YES", "1-8", "Semester level"),
        ("section", "String", "YES", "None", "Section privacy scope (e.g. 'CSE-B')"),
        ("fileUrl", "String", "YES", "None", "Relative or cloud path to uploaded file"),
        ("fileName", "String", "YES", "None", "Original uploaded filename"),
        ("uploadedBy", "String", "YES", "FK -> users.id", "Faculty creator ID"),
        ("uploadedAt", "Date / ISOString", "YES", "Date.now()", "Publication timestamp")
    ]))
    story.append(Spacer(1, 8))

    # 10. assignments
    story.append(make_schema_table("assignments", "Coursework assignments, project tasks, and lab assignments", [
        ("id", "String", "YES", "Auto-generated", "Assignment identifier"),
        ("title", "String", "YES", "None", "Assignment title and task summary"),
        ("description", "String", "YES", "None", "Full coursework problem statement"),
        ("department", "String", "YES", "FK -> departments.name", "Target department"),
        ("semester", "Number", "YES", "1-8", "Target semester"),
        ("section", "String", "YES", "None", "Target section"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Curriculum course reference"),
        ("dueDate", "String", "YES", "YYYY-MM-DD", "Final submission cutoff date"),
        ("totalMarks", "Number", "YES", "20", "Maximum gradable marks")
    ]))
    story.append(PageBreak())

    # 11. student_submissions
    story.append(make_schema_table("student_submissions", "Student assignment uploads, submission text, and faculty grades", [
        ("id", "String", "YES", "Auto-generated", "Unique submission record"),
        ("assignmentId", "String", "YES", "FK -> assignments.id", "Associated coursework task"),
        ("studentId", "String", "YES", "FK -> users.id", "Submitting student account"),
        ("studentName", "String", "YES", "None", "Cached student full name"),
        ("rollNumber", "String", "YES", "None", "Student roll number"),
        ("submissionText", "String", "OPTIONAL", "None", "Student solution narrative or git repo link"),
        ("fileUrl", "String", "OPTIONAL", "None", "Attached solution document path"),
        ("submittedAt", "Date / ISOString", "YES", "Date.now()", "Actual timestamp of student upload"),
        ("status", "String", "YES", "'SUBMITTED' | 'GRADED'", "Workflow progression state"),
        ("marksAwarded", "Number", "OPTIONAL", "null until graded", "Evaluation score awarded by faculty"),
        ("feedback", "String", "OPTIONAL", "None", "Evaluator feedback notes")
    ]))
    story.append(Spacer(1, 8))

    # 12. online_exams
    story.append(make_schema_table("online_exams", "Time-bounded multiple-choice online examinations and quiz specifications", [
        ("id", "String", "YES", "Auto-generated", "Unique online examination key"),
        ("title", "String", "YES", "None", "Examination title (e.g. 'Lab Exam', 'Quiz 1')"),
        ("instructions", "String", "YES", "None", "Candidate rules and proctoring guidelines"),
        ("department", "String", "YES", "FK -> departments.name", "Cohort department"),
        ("semester", "Number", "YES", "1-8", "Semester level"),
        ("section", "String", "YES", "None", "Section scope ('All' or specific section)"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Associated subject"),
        ("subjectCode", "String", "YES", "None", "Cached course code (e.g. 'CS402')"),
        ("examDate", "String", "YES", "YYYY-MM-DD", "Scheduled examination date"),
        ("startTime", "String", "YES", "HH:MM format", "Window opening time"),
        ("endTime", "String", "YES", "HH:MM format", "Window closing time"),
        ("durationMinutes", "Number", "YES", "60", "Allowed test duration once student begins"),
        ("totalMarks", "Number", "YES", "20", "Total aggregate marks"),
        ("passMarks", "Number", "YES", "12", "Minimum threshold to pass"),
        ("negativeMarking", "String", "YES", "'None' | '0.25' | '0.5'", "Penalty deduction per wrong answer"),
        ("questions", "Array<Object>", "YES", "[]", "Array of [{ id, questionText, options: [4 strings], correctOptionIndex, marks }]"),
        ("status", "String", "YES", "'SCHEDULED'|'AVAILABLE'|'CLOSED'", "Active lifecycle status"),
        ("resultsReleased", "Boolean", "YES", "false", "Faculty flag granting student access to scores & answer key")
    ]))
    story.append(Spacer(1, 8))

    # 13. exam_attempts
    story.append(make_schema_table("exam_attempts", "Recorded student test attempts, tab-switch infractions, and scores", [
        ("id", "String", "YES", "Auto-generated", "Unique attempt identifier"),
        ("examId", "String", "YES", "FK -> online_exams.id", "Target online examination"),
        ("studentId", "String", "YES", "FK -> users.id", "Student who sat for the assessment"),
        ("studentName", "String", "YES", "None", "Cached student name"),
        ("rollNumber", "String", "YES", "None", "Cached student roll number"),
        ("answers", "Array<Object>", "YES", "[]", "Recorded selections: [{ questionId, selectedOptionIndex }]"),
        ("score", "Number", "YES", "0", "Evaluated marks scored"),
        ("totalMarks", "Number", "YES", "None", "Maximum attainable marks"),
        ("percentage", "Number", "YES", "None", "Score percentage (0.00% to 100.00%)"),
        ("isPassed", "Boolean", "YES", "false", "True if score >= passMarks"),
        ("startedAt", "Date / ISOString", "YES", "Date.now()", "Timestamp student clicked 'Attend Examination'"),
        ("submittedAt", "Date / ISOString", "YES", "Date.now()", "Timestamp student completed or timed out"),
        ("tabSwitchCount", "Number", "YES", "0", "Total proctoring window blur / tab-switch infractions"),
        ("status", "String", "YES", "'EVALUATED'", "Completion state")
    ]))
    story.append(PageBreak())

    # 14. marks_records
    story.append(make_schema_table("marks_records", "Official university semester marks, internal assessments, and grade points", [
        ("id", "String", "YES", "Auto-generated", "Unique academic grade record"),
        ("studentId", "String", "YES", "FK -> users.id", "Enrolled student account"),
        ("subjectId", "String", "YES", "FK -> subjects.id", "Target subject"),
        ("semester", "Number", "YES", "1-8", "Academic semester"),
        ("internalMarks", "Number", "YES", "Max 40", "Continuous internal assessment score"),
        ("externalMarks", "Number", "YES", "Max 60", "End-semester university theory/lab score"),
        ("totalMarks", "Number", "YES", "Max 100", "Composite final mark"),
        ("letterGrade", "String", "YES", "'O','A+','A','B+','B','RA'", "Institutional letter grade"),
        ("gradePoints", "Number", "YES", "10 to 0 scale", "Numerical grade points for CGPA computation")
    ]))
    story.append(Spacer(1, 8))

    # 15. notifications
    story.append(make_schema_table("notifications", "System alerts, timetable changes, exam announcements, and grade alerts", [
        ("id", "String", "YES", "Auto-generated", "Unique notification identifier"),
        ("recipientId", "String", "OPTIONAL", "FK -> users.id", "Direct user recipient (null if cohort broadcast)"),
        ("targetRole", "String", "OPTIONAL", "'STUDENT'|'FACULTY'|'ALL'", "Target role for wide announcements"),
        ("department", "String", "OPTIONAL", "None", "Department filter for broadcast"),
        ("section", "String", "OPTIONAL", "None", "Section filter for broadcast"),
        ("title", "String", "YES", "None", "Notification title banner"),
        ("message", "String", "YES", "None", "Full body text of alert"),
        ("isRead", "Boolean", "YES", "false", "Read status tracking for user inbox"),
        ("createdAt", "Date / ISOString", "YES", "Date.now()", "Dispatch timestamp")
    ]))
    story.append(Spacer(1, 8))

    # 16. audit_logs
    story.append(make_schema_table("audit_logs", "Security audit trail tracking administrative actions and system events", [
        ("id", "String", "YES", "Auto-generated", "Audit event log identifier"),
        ("userId", "String", "YES", "FK -> users.id", "Executing user ID"),
        ("userRole", "String", "YES", "Role claim", "Role of user at time of action"),
        ("action", "String", "YES", "Uppercase Verb", "Action type (e.g. 'CREATE_EXAM', 'RELEASE_RESULTS')"),
        ("entity", "String", "YES", "Collection name", "Affected domain entity"),
        ("entityId", "String", "OPTIONAL", "None", "Primary key of mutated entity"),
        ("ipAddress", "String", "YES", "Client IP", "Originating client network address"),
        ("details", "String", "OPTIONAL", "None", "JSON payload metadata describing the modification"),
        ("timestamp", "Date / ISOString", "YES", "Date.now()", "Immutable event timestamp")
    ]))
    story.append(Spacer(1, 10))

    # ------------------ SECTION 3: INDEXING STRATEGY ------------------
    story.append(Paragraph("3. Indexing Strategy & Performance Rules", h1))
    story.append(Paragraph(
        "To satisfy sub-50ms query latency, compound and unique indices are defined across high-frequency access paths:",
        p
    ))

    idx_table = Table([
        [Paragraph("<b>Collection</b>", th), Paragraph("<b>Index Key Specification</b>", th), Paragraph("<b>Type / Constraint</b>", th), Paragraph("<b>Query Optimization Objective</b>", th)],
        [Paragraph("users", td_c), Paragraph("{ email: 1 }", td_c), Paragraph("Unique Index", td_b), Paragraph("Ultra-fast credential lookup during authentication.", td)],
        [Paragraph("users", td_c), Paragraph("{ department: 1, section: 1 }", td_c), Paragraph("Compound Index", td_b), Paragraph("Fast retrieval of section student rosters.", td)],
        [Paragraph("class_timetables", td_c), Paragraph("{ department: 1, semester: 1, section: 1 }", td_c), Paragraph("Compound Index", td_b), Paragraph("Instant weekly timetable rendering.", td)],
        [Paragraph("class_timetables", td_c), Paragraph("{ dayOfWeek: 1, periodNumber: 1, room: 1 }", td_c), Paragraph("Compound Index", td_b), Paragraph("Conflict engine classroom collision checks.", td)],
        [Paragraph("online_exams", td_c), Paragraph("{ department: 1, semester: 1, section: 1 }", td_c), Paragraph("Compound Index", td_b), Paragraph("Listing assessments relevant to student cohort.", td)],
        [Paragraph("exam_attempts", td_c), Paragraph("{ examId: 1, studentId: 1 }", td_c), Paragraph("Unique Compound", td_b), Paragraph("Guarantees single attempt rule enforcement.", td)],
        [Paragraph("attendance_records", td_c), Paragraph("{ sessionDate: 1, section: 1, subjectId: 1 }", td_c), Paragraph("Compound Index", td_b), Paragraph("Retrieving daily section attendance logs.", td)],
    ], colWidths=[90, 160, 95, 142], style=[
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    story.append(idx_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_path}")

if __name__ == "__main__":
    build_db_design()
