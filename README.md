<div align="center">

# 💎 RecoverAI
### *Intelligent Invoice and Payment Recovery Assistant*

**Developed by [Soharab Ahamad](https://github.com/SoharabAhamad786)**  
*Track 3: AI Revenue Recovery — Human-in-the-Loop Accounts Receivable Platform*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg?logo=react&logoColor=white)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF.svg?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-3D_Visuals-black.svg?logo=three.js&logoColor=white)](https://threejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-core-governance-philosophy">Governance</a> •
  <a href="#-key-features">Key Features</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-demo-credentials">Demo Access</a> •
  <a href="#-api-endpoints">API Reference</a>
</p>

---

</div>

## 📖 Overview

**RecoverAI** is an enterprise-grade, human-in-the-loop AI platform designed to transform how accounts receivable (AR) and finance teams recover overdue invoices and resolve failed payment events.

Traditional collections rely on brute-force reminder blasts and static spreadsheets that damage client relationships and fail on complex B2B disputes. **RecoverAI** pairs predictive machine learning with deterministic safety policies, allowing AR analysts to act with AI-assisted precision while retaining full human control over customer communications.

> **💡 The RecoverAI Operating Principle:**  
> *"AI recommends and explains. Business rules validate. Humans approve sensitive actions. The system records everything."*

---

## 🏛️ Core Governance Philosophy

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   1. AI Copilot │  ───► │  2. Policy Gate │  ───► │ 3. Human Review │  ───► │ 4. Audit Ledger │
│                 │       │                 │       │                 │       │                 │
│ Computes score, │       │ Validates rules,│       │ Analyst edits,  │       │ Cryptographic   │
│ risk band &     │       │ checks disputes,│       │ approves, or    │       │ timestamped log │
│ tailored draft  │       │ enforces limits │       │ rejects action  │       │ for compliance  │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

1. **Autonomous Inference with Explainability:** The AI calculates recovery probabilities, determines optimal escalation timing, and generates respectful payment reminders backed by verifiable *Evidence Citations*.
2. **Deterministic Safety Guardrails:** Code-level business rules enforce non-negotiable boundaries — immediately blocking automated reminders if an invoice is in dispute or marked as paid.
3. **Human-in-the-Loop Final Sign-Off:** No message is dispatched without explicit human analyst verification and one-click modal confirmation.
4. **Immutable Audit Trail:** Every recommendation, analyst revision, policy check, and mock dispatch is permanently logged for SOC2 and financial compliance.

---

## ✨ Key Features

### 🌌 Interactive 3D & 2D Financial Command Center
- **Three.js Financial Galaxy:** Real-time 3D orbital visualization mapping open receivables by risk tier, overdue velocity, and recovery score.
- **Instant 2D/3D Mode Switch:** Seamless toggle in top navigation allowing users to switch between futuristic 3D glassmorphism and clean enterprise 2D mode.
- **Executive Portfolio KPIs:** Live tracking of Total Outstanding ($315K+), Overdue Receivables ($281K+), Predictively Recoverable Capital ($189K+), Open Disputes, and Overall Recovery Rate (24.2%).

### 🎯 Multi-Signal Priority Recovery Queue
- **Composite Scoring Engine:** Sorts invoices using a multidimensional weighting algorithm factoring in customer payment history, invoice aging bucket, relationship health, and dispute signals.
- **Risk Segmentation:** Visual indicators for High, Medium, and Low risk bands with tailored action pathways.
- **Demo Scenario Filters:** One-click filter highlighting key validation personas:
  - 🌟 **Recommended Demo Invoice:** `INV-2024-024` (Jennifer Lee / Apex Solutions — $4,850, 85% Recovery Probability).
  - 🛑 **Dispute Guardrail Gate:** `INV-2024-004` (Acme Corp — $14,500, Disputed, Send Button Strictly Blocked).
  - 💼 **High-Value Escalation:** `INV-2024-012` (Global Logistics — $38,000, Requires Manager Sign-Off).

### 🤖 AI Neural Analysis & Evidence Citations
- **Holographic 3D AI Core:** Interactive canvas animating neural weights during strategy computation.
- **Evidence-Based Reasoning:** Cites discrete facts behind every recommendation (e.g., *12-month clean payment history*, *Zero unresolved support tickets*, *Installment policy flexibility*).
- **Tone-Adaptive Reminder Generator:** Auto-drafts courteous, firm, or installment-focused reminders tailored to the debtor's reliability profile.

### 👥 Customer Portfolio Intelligence & Analytics
- **Debtor Profiles:** Lifetime value (LTV), reliability scores, average days-to-payment, and communication history.
- **Recovery Analytics Suite:** Deep-dive charts showing recovery velocity across aging buckets (1–30d, 31–60d, 61–90d, 90+d) and segment performance.

### 🔒 Enterprise Security & Auditability
- **Role-Based Access Control (RBAC):** Distinct permissions for Finance Managers (full approval & policy configuration) and Finance Analysts (drafting & queue review).
- **Audit Ledger:** Chronological event feed with JSON payload inspection and one-click CSV export.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend UI** | **React 18, TypeScript, Vite** | Reactive, type-safe single-page application |
| **3D Graphics** | **Three.js, Canvas API** | Interactive 3D Financial Galaxy & Neural Orb visualizations |
| **Styling** | **Vanilla CSS + Glassmorphism Tokens** | Sleek dark-mode aesthetic with custom animations |
| **Icons & UI Components** | **Lucide Icons, Headless UI** | Accessible, modern interface components |
| **Backend API** | **Python 3.10+, Flask REST API** | High-throughput asynchronous backend service |
| **Database & ORM** | **SQLAlchemy 2.0, SQLite** | Relational persistence with foreign-key integrity |
| **AI Inference Engine** | **Modular Provider Interface** | Supports Gemini API, OpenAI GPT-4, and Local Heuristic Engine |
| **Testing** | **Pytest** | Comprehensive test coverage across all REST endpoints and business rules |

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and **npm**

### Unified 1-Command Launch (Recommended)
Clone the repository and run the unified server script:

```bash
# Clone repository
git clone https://github.com/SoharabAhamad786/AI-Revenue-Recovery.git
cd AI-Revenue-Recovery

# Launch both Backend & Frontend (Auto-opens browser at http://localhost:5173)
python run_server.py
```

*On Windows, you can also simply double-click `start.bat` or run `npm start`.*

---

### Manual Setup (Optional)

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
# Backend runs on http://127.0.0.1:5000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

---

## 🔐 Demo Credentials (1-Click Login Available)

RecoverAI includes pre-seeded demo accounts with preset role permissions:

| Role | Email | Password | Permissions |
|---|---|---|---|
| 👔 **Finance Manager** | `manager@recoverai.demo` | `manager123` | Full Approval, Policy Overrides, Settings |
| 📊 **Finance Analyst** | `analyst@recoverai.demo` | `analyst123` | Queue Review, AI Analysis, Reminder Drafting |

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/login` | Authenticate user & return session token |
| `GET` | `/api/dashboard/summary` | Retrieve executive KPIs and portfolio liquidity metrics |
| `GET` | `/api/dashboard/trends` | Fetch historical recovery velocity and aging distributions |
| `GET` | `/api/invoices` | List prioritized invoices with filter, search, and pagination |
| `GET` | `/api/invoices/<id>` | Fetch detailed invoice ledger, customer profile, and audit logs |
| `POST` | `/api/invoices/<id>/analyze` | Trigger AI strategy inference, score calculation & evidence citations |
| `POST` | `/api/invoices/<id>/actions/send-reminder` | Dispatch approved customer reminder (guarded by rule engine) |
| `GET` | `/api/customers` | Retrieve customer intelligence and payment reliability metrics |
| `GET` | `/api/analytics/overview` | Fetch portfolio-wide recovery trends and efficiency metrics |
| `GET` | `/api/audit-logs` | Retrieve chronological, immutable compliance audit log |

---

## 🧪 Running Automated Tests

```bash
cd backend
pytest tests/ -v
```

---

## 👨‍💻 Author & Acknowledgements

- **Project Lead & Developer:** [Soharab Ahamad](https://github.com/SoharabAhamad786)
- **Program:** Internship Project — *Track 3: AI Revenue Recovery*
- **License:** Open-source under the [MIT License](LICENSE).

<div align="center">

*Built with precision and governance by **Soharab Ahamad**.*

</div>
