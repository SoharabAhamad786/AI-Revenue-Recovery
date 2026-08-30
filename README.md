# RecoverAI — Intelligent Invoice and Payment Recovery Assistant
**Project Owner:** Soharab Ahamad  
**Track:** Track 3 — AI Revenue Recovery Internship Project  
**Tagline:** *Intelligent Invoice and Payment Recovery Assistant*

---

## Overview

RecoverAI is a full-stack, production-style AI Accounts Receivable Copilot designed to help finance teams recover overdue revenue faster while enforcing strict human-in-the-loop governance. Built by **Soharab Ahamad**, it combines predictive recovery scoring, autonomous strategy generation, deterministic business validation rules, and an immutable audit trail.

> **Core Safety Principle:**  
> *"AI recommends and explains. Business rules validate. Humans approve sensitive actions. The system records everything."*

---

## Quick Start (One-Command Launch)

To start both the Flask backend and React/Vite 3D frontend, and automatically launch RecoverAI in your default web browser:

```bash
python run_server.py
```

*(Alternatively, you can run `npm start` or double-click `start.bat` on Windows)*

---

### Demo Accounts (1-Click Instant Sign-In)

| Role | Email | Password | Access Level |
|---|---|---|---|
| **Finance Manager** | `manager@recoverai.demo` | `manager123` | Full Approval & Policy Configuration |
| **Finance Analyst** | `analyst@recoverai.demo` | `analyst123` | Draft, AI Analysis, & Queue Review |

---

## Key Features

1. **5-Minute Pitch Mode & Presenter Helper:**
   - Dedicated Pitch Mode toggle providing high-contrast layout and simplified navigation for recording.
   - Built-in **Pitch Guide (Internal)** with timed section cues (0:00–5:00) and step-by-step click targets.
   - **Demo Scenarios Toggle** in Recovery Queue highlighting:
     - 🌟 **Recommended Demo Invoice** (`INV-2024-024` - Jennifer Lee, $4,850 Overdue, 85% Recovery Prob).
     - ⚠️ **Disputed Invoice Guardrail** (`INV-2024-004` - Acme Corp, $14,500, Send Button Blocked).
     - 💎 **High-Value Gate** (`INV-2024-012` - Global Logistics, $38,000, Requires Manager Sign-off).

2. **3D Holographic UI / UX & 2D Classic Toggle:**
   - Interactive Three.js particle constellation and financial galaxy.
   - 3D Holographic AI Neural Orb visualizing real-time strategy computation.
   - One-click instant 2D/3D mode switch in top navigation.

3. **Deterministic Business Rules Engine:**
   - Blocks automated reminders on disputed invoices and paid invoices.
   - Requires Finance Manager approval for high-value invoices (default >$10,000).
   - Prevents duplicate dispatches with idempotent tokens and cooldown periods.

4. **Immutable Audit Trail:**
   - Every login, AI strategy inference, human message edit, reminder dispatch, and escalation is cryptographically logged and exportable to CSV.

---

## Technology Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons, Three.js, React Router 6
- **Backend:** Python Flask REST API, SQLAlchemy 2.0 ORM, SQLite
- **AI Engine:** Structured output recovery copilot (Deterministic Rules Engine + OpenAI / Gemini / Offline Provider)
- **Testing:** Pytest (32/32 passing tests)

---

## Automated Demo Video & Voiceover

To generate or re-run the automated 5-minute video recording with voiceover and burned-in subtitles:

```bash
# 1. Generate TTS voiceover & subtitles
python demo_video/generate_audio.py

# 2. Run automated screen recording & composite final video
python demo_video/produce_video.py
```

*Final Video Output:* `demo_video/recoverai_demo_final.mp4`

---

## License & Credits

Developed by **Soharab Ahamad** for Track 3: AI Revenue Recovery. All rights reserved.
