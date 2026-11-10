# Edu Track – Student Academic Management System

<div align="center">

![Edu Track Academic Management System](frontend/public/assets/edu_institution_seal_1791517510992.jpg)

**A Unified, Role-Governed University Operating Environment for Students, Teaching Faculty, and Institutional Administrators**

[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20TypeScript-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Bundler-Vite%208-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styles-Tailwind%20CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Node.js](https://img.shields.io/badge/Backend-Node.js%20%2B%20Express-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Socket.IO](https://img.shields.io/badge/Real--Time-Socket.IO-010101?logo=socket.io&logoColor=white)](https://socket.io/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas%20%2B%20Dual--Store-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel&logoColor=white)](https://projectmernfull-stack-roan.vercel.app/)

</div>

---

## 📁 Repository Structure

The repository is organized cleanly into modular, isolated domains following industry best practices:

```text
Edu-Track-Student-Academic-Management-System/
│
├── frontend/                 # React frontend source code
│   ├── src/                  # Components, portals, state, hooks, and services
│   │   ├── components/       # Admin, Faculty, and Student workspaces
│   │   ├── config/           # Firebase and environment runtime configurations
│   │   ├── services/         # REST API clients and WebSocket synchronization
│   │   └── types/            # TypeScript interfaces and domain schemas
│   ├── public/               # Public assets, institutional branding, and icons
│   ├── index.html            # Single Page Application HTML entrypoint
│   ├── vite.config.ts        # Bundler configuration and styling plugins
│   ├── tsconfig.json         # TypeScript compiler configurations
│   └── package.json          # Frontend-specific dependencies and scripts
│
├── backend/                  # Node.js + Express backend
│   ├── data/                 # High-availability autonomous JSON database store
│   ├── db/                   # MongoDB Atlas Mongoose connection lifecycle
│   ├── middleware/           # Stateless JWT authentication & RBAC role guards
│   ├── models/               # Mongoose schema definitions (16 collections)
│   ├── routes/               # Modular REST endpoints (auth, timetable, exam, etc.)
│   ├── store/                # DualStore persistence engine & failover sync
│   ├── tests/                # Automated auth and integration verification suites
│   ├── firebaseAdmin.ts      # Firebase Admin SDK server initialization
│   ├── server.ts             # Gateway entrypoint & Socket.IO server setup
│   ├── socket.ts             # WebSocket broadcast handlers and room managers
│   └── package.json          # Backend dependencies and standalone scripts
│
└── docs/                     # Official project engineering documents
    ├── Project_PPT.pdf               # Executive presentation slide deck (12 Slides)
    ├── Project_Documentation.pdf     # Academic SRS & System Architecture specification
    ├── Database_Design.pdf           # Entity-Relationship models & 16-collection schemas
    └── API_Documentation.pdf         # REST endpoints & Socket.IO event reference
```

---

## 📚 Official Engineering Documentation

Complete, publication-grade academic and technical documents are provided in [`docs/`](./docs/):

| Document | Description | Format | Direct Link |
|:---|:---|:---:|:---|
| **Project Presentation Deck** | 12-slide executive presentation covering problem landscape, MERN architecture, role governance matrix, conflict detection, anti-tamper attendance, and proctoring. | Landscape PDF | [docs/Project_PPT.pdf](./docs/Project_PPT.pdf) |
| **Project Documentation (SRS)** | Formal academic Software Requirements Specification (SRS), system architecture, functional modules, core algorithms, and testing matrices. | A4 Report PDF | [docs/Project_Documentation.pdf](./docs/Project_Documentation.pdf) |
| **Database Design Specification** | Comprehensive data modeling guide, entity-relationship cardinality, 16 collection schemas with types, indexing strategies, and dual-store sync protocols. | A4 Reference PDF | [docs/Database_Design.pdf](./docs/Database_Design.pdf) |
| **API Documentation** | Full REST endpoint reference, HTTP methods, headers, payloads, error schemas, status codes, and Socket.IO real-time event definitions. | A4 Reference PDF | [docs/API_Documentation.pdf](./docs/API_Documentation.pdf) |

---

## 🌟 Key Platform Features

### 1. Unified 3-Role Academic Governance
- **Institutional Administrator:** Department setup, course subjects, instructional cohorts, student/faculty rosters, weekly class timetables with collision validation, semester examination schedules, and audit trails.
- **Teaching Faculty:** Section-restricted rosters, anti-tamper daily attendance tracking (locked strictly to current calendar date), section-scoped study material uploads, coursework management, online quiz creation, and result release governance.
- **Enrolled Student:** Personalized weekly timetables, department semester exam dates, live attendance gauges, section study material downloads, proctored online examinations, and official semester academic transcripts.

### 2. Autonomous Timetable Conflict Engine
- Validates room bookings, instructor assignments, and student cohort schedules proactively before database commit.
- Prevents classroom double-booking and faculty scheduling overlaps.
- Dispatches instant WebSocket events (`timetable_updated`) to refresh client screens in real time.

### 3. Anti-Tamper Attendance Workflow
- Single-day session locking prevents instructors from backdating attendance records.
- Streamlined binary controls (`Present` / `Absent`) with rapid batch commits.
- Automatic aggregation calculates cumulative attendance percentages and triggers low-attendance warnings (< 75%).

### 4. Section-Scoped Coursework & Study Materials
- Instructors upload lecture notes, lab sheets, and assignment briefs scoped strictly to designated sections (e.g. `CSE-B`).
- Students view only materials and tasks relevant to their enrolled cohort.
- Dedicated submission review ledger enables grading and feedback entry.

### 5. Online Examination & Proctoring Pipeline
- Multiple-choice assessment authoring with custom time windows, question weights, pass cutoffs, and negative marking.
- Anti-cheat proctoring: monitors browser focus (`window.onblur`, `visibilitychange`), displays warning dialogs upon tab switching, and logs infractions.
- Automated instant grading compares choices against answer keys.
- Faculty-governed result release reveals scorecards, percentage calculations, pass/fail status, and question solutions to test takers.

### 6. High-Availability Dual-Store Persistence
- Primary persistence: **MongoDB Atlas Cloud Replica Set**.
- Fallback persistence: **Autonomous Atomic JSON Store** (`backend/data/edutrack_db.json`).
- If cloud database connectivity drops, the system seamlessly continues handling reads and writes with zero downtime.
- Automatic self-healing reconciliation synchronizes pending records upon reconnection.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js:** v18.0.0 or higher
- **npm:** v9.0.0 or higher
- **MongoDB:** Cloud Atlas URI or local instance (Optional: system runs autonomously on fallback store if omitted)

### 1. Installation
Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/pavan90303/project_mern_full--stack.git
cd project_mern_full--stack

# Install root dependencies
npm install

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install backend dependencies
cd backend && npm install && cd ..
```

### 2. Environment Configuration
Copy the provided `.env.example` templates to `.env`:

```bash
# Root & backend environment
cp .env.example .env
cp .env.example backend/.env
cp .env.example frontend/.env
```

Configure key variables:
```env
PORT=3000
NODE_ENV=development
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.ofrm69q.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=your_secure_jwt_secret_key_here
CLIENT_URL=http://localhost:5173
```

### 3. Running Locally

#### Option A: Run Full Application (Monorepo)
```bash
# Start frontend development server
npm run dev

# In a separate terminal, start backend server
npm start
```

#### Option B: Run Services Individually
```bash
# Start frontend only (port 5173)
npm run dev:frontend

# Start backend only (port 3000)
npm run dev:backend
```

### 4. Production Build
```bash
# Compiles frontend with Vite and syncs artifacts to dist/
npm run build
```

---

## 🌐 Production Deployment

- **Live Frontend (Vercel):** [https://projectmernfull-stack-roan.vercel.app/](https://projectmernfull-stack-roan.vercel.app/)
- **API Server:** Node.js + Express cluster with Socket.IO real-time gateway.
- **Database:** MongoDB Atlas cloud cluster with automated daily snapshots and TLS 1.3 encryption.

---

## 📄 License
This project is proprietary academic software developed for university operational management. All rights reserved.
