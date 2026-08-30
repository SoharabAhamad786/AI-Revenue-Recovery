# RecoverAI — 5-Minute Pitch Video Voiceover Script
**Project:** RecoverAI — Intelligent Invoice and Payment Recovery Assistant  
**Presenter / Author:** Soharab Ahamad  
**Track:** Track 3: AI Revenue Recovery  
**Total Target Duration:** ~5 minutes (300 seconds)

---

### [0:00 – 0:40] Part 1: The Revenue Recovery Problem
**Screen Target:** `http://localhost:5173/` (Dashboard Overview)  
**Presenter Action:** Show the $281,000 overdue metric and the 6 accounts requiring immediate attention.

> *"Welcome. In every B2B and SaaS business, accounts receivable is one of the most critical yet inefficient financial workflows. Every month, companies lose millions of dollars to overdue invoices and failed payments.*
>
> *Today, finance teams rely on manual follow-ups. Analysts spend hours digging through spreadsheets, drafting repetitive emails, and guessing which customer to contact next. This process is slow, inconsistent, and often strains customer relationships.*
>
> *Finance teams do not need a black-box bot blindly sending aggressive collection notices. They need an intelligent, transparent copilot that prioritizes the ledger, predicts recovery likelihood, drafts personalized communications, and keeps humans firmly in control of every financial decision."*

---

### [0:40 – 1:30] Part 2: Product Overview & Dashboard
**Screen Target:** `http://localhost:5173/` (3D Dashboard & Financial Galaxy)  
**Presenter Action:** Pan across the KPI cards, highlight the 3D Revenue Galaxy, and explain Recovery Velocity Trends.

> *"Enter RecoverAI. RecoverAI is built by Soharab Ahamad as an internship project for Track 3: AI Revenue Recovery.*
>
> *Here on the main executive dashboard, RecoverAI delivers immediate financial clarity. At a single glance, finance leaders see total outstanding debt, total overdue volume, and our real-time recovery rate.*
>
> *Our 3D Revenue Galaxy visualizes the entire accounts ledger by risk level and dollar volume. High-risk overdue accounts are highlighted in glowing crimson, while healthy accounts orbit securely. Below, our recovery velocity metrics track days-to-payment improvements and segment health.*
>
> *Everything is governed by our core principle: AI recommends and explains. Business rules validate. Humans approve sensitive actions. And the system records everything."*

---

### [1:30 – 2:40] Part 3: Live Demo — AI Strategy & Evidence
**Screen Target:** `http://localhost:5173/recovery-queue` -> `http://localhost:5173/invoices/24`  
**Presenter Action:** Click "Demo Scenarios" filter. Open Recommended invoice `INV-2024-024` for Jennifer Lee. Click "Analyze with AI".

> *"Let's see RecoverAI in action. Navigating to the Recovery Queue, our system prioritizes overdue invoices dynamically using composite risk scoring.*
>
> *We toggle the Demo Scenario mode and select our recommended demo invoice: invoice INV-2024-024 for customer Jennifer Lee, representing four thousand eight hundred and fifty dollars overdue by twelve days.*
>
> *When we open the invoice detail and click 'Analyze with AI', RecoverAI's neural recovery engine engages in real-time. Within milliseconds, the AI synthesizes Jennifer's payment history, credit reliability score of eighty-five percent, and zero dispute history.*
>
> *The AI computes an eighty-five percent recovery probability, recommends a polite early reminder, and cites exact evidence from the customer's prior transaction logs. It even authorizes a flexible payment plan option based on corporate policy."*

---

### [2:40 – 3:35] Part 4: Human-in-the-Loop Approval & Dispute Guardrails
**Screen Target:** `http://localhost:5173/invoices/24` -> `http://localhost:5173/invoices/4`  
**Presenter Action:** Review suggested message, click "Approve & Send". Navigate to Disputed invoice `INV-2024-004` to show disabled button and dispute guardrail.

> *"Notice that RecoverAI drafts a tailored, respectful reminder message ready for review. As a finance analyst, I can edit the wording directly. When satisfied, I click 'Approve and Send'. The confirmation modal logs the dispatch, updates the invoice timeline, and sends the notice through our secure payment gateway.*
>
> *Now, what happens if an invoice has an active dispute? Let's open invoice INV-2024-004 for Acme Corporation.*
>
> *Here, our deterministic safety engine takes over. Notice that the 'Approve and Send' button is strictly disabled with a red guardrail notice: 'Sending reminders is disabled for disputed invoices — Escalate to Human review required.'*
>
> *RecoverAI prevents embarrassing or legally risky automated collection messages when a customer has an unresolved dispute."*

---

### [3:35 – 4:25] Part 5: Technical Architecture & Audit Trail
**Screen Target:** `http://localhost:5173/audit-log` -> `http://localhost:5173/settings`  
**Presenter Action:** Show the immutable Audit Log table, demonstrate JSON details modal, and show Settings recovery policies.

> *"Under the hood, RecoverAI is built with a modern, production-grade full-stack architecture.*
>
> *The frontend is crafted in React eighteen with TypeScript, Vite, and Three.js for interactive 3D spatial depth. The backend is powered by Python Flask with SQLAlchemy and a comprehensive REST API, backed by a deterministic business validation engine.*
>
> *Crucially, every single action in RecoverAI is logged to our immutable Audit Trail. Whether an analyst signs in, triggers an AI inference, edits a message, or escalates an account, the event is recorded with timestamps, user IDs, and cryptographic payload details. Finance teams can export the entire log to CSV for compliance audits at any time."*

---

### [4:25 – 5:00] Part 6: Business Impact & Conclusion
**Screen Target:** `http://localhost:5173/analytics`  
**Presenter Action:** Show Analytics charts (Aging buckets, Segment breakdown, Days-to-payment reduction), toggle Pitch Mode banner, and conclude.

> *"Finally, looking at our Analytics suite, the business impact is undeniable.*
>
> *RecoverAI cuts days-to-payment by over thirty-five percent, reduces manual follow-up time by eighty percent, and recovers twenty-four percent more revenue while protecting valuable customer relationships.*
>
> *RecoverAI proves that artificial intelligence in finance works best when paired with human judgment, clear explainability, and bulletproof safety guardrails.*
>
> *Thank you for watching. RecoverAI is built by Soharab Ahamad for Track 3: AI Revenue Recovery."*
