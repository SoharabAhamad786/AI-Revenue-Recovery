# RecoverAI — 5-Minute Manual Video Recording Guide
**Project Owner:** Soharab Ahamad  
**Track:** Track 3: AI Revenue Recovery  
**Tagline:** Intelligent Invoice and Payment Recovery Assistant  

This guide provides step-by-step visual cue directions for recording the 5-minute pitch video manually using OBS Studio, Loom, Camtasia, or Windows Game Bar (Win + Alt + R).

---

## 🛠️ Recording Setup & Preparation

1. **Resolution & Scaling:**
   - Set browser display to **1920x1080** (1080p).
   - Ensure browser zoom is at **100%**.
   - Press **F11** for full-screen borderless recording if desired.

2. **Launch Application:**
   ```bash
   python run_server.py
   ```
   *(Opens `http://localhost:5173/`)*

3. **Audio Preparation:**
   - You can either speak live using [`demo_video_script.md`](../demo_video_script.md) OR play the generated neural voiceover file: [`demo_video/demo_voiceover.mp3`](./demo_voiceover.mp3).

---

## 🎬 Step-by-Step Recording Timeline

### Segment 1: [0:00 – 0:40] Problem Statement & Login
* **Starting Page:** `http://localhost:5173/login`
* **Actions:**
  1. Hover cursor smoothly over the **RecoverAI** 3D logo and background particle constellation.
  2. Click **⚡ 1-Click Demo: Finance Manager** (`manager@recoverai.demo`).
  3. Notice the instant toast notification: *"Authentication successful! Welcome to RecoverAI."*
  4. System redirects to the Executive Dashboard.
* **Narration Cue:**
  > *"Welcome. In every B2B and SaaS business, accounts receivable is one of the most critical yet inefficient financial workflows..."*

---

### Segment 2: [0:40 – 1:30] Executive Dashboard & 3D Revenue Galaxy
* **Target Page:** `http://localhost:5173/` (Dashboard)
* **Actions:**
  1. Hover over the top KPI cards:
     - **$315,420** Total Outstanding
     - **$281,420** Total Overdue (red highlight)
     - **6 Accounts** Requiring Attention
     - **24.2%** Real-time Recovery Rate
  2. Scroll down to the **3D Revenue Galaxy**:
     - Click and gently drag the galaxy to rotate the 3D financial celestial orbit.
     - Hover over high-risk crimson nodes and healthy emerald nodes.
  3. Briefly scroll to view **Recovery Velocity Trends** and **Segment Health**.
* **Narration Cue:**
  > *"Enter RecoverAI. RecoverAI is built by Soharab Ahamad as an internship project for Track 3: AI Revenue Recovery..."*

---

### Segment 3: [1:30 – 2:40] Recovery Queue & AI Strategy Copilot
* **Target Page:** Click **Recovery Queue** in sidebar (`http://localhost:5173/recovery-queue`)
* **Actions:**
  1. Click the **"⭐ 5-Min Demo Scenarios"** toggle button at the top right.
     - Notice the queue filters instantly to show the 3 key scenarios.
  2. Click on the **Recommended for Demo** invoice row:
     - **INV-2024-024** | Customer: Jennifer Lee (Apex Solutions) | Amount: **$4,850** | 12 Days Overdue.
  3. System opens **Invoice Details** (`/invoices/24`):
     - Scroll down to the **3D Holographic AI Neural Core**.
     - Click the prominent **"Analyze with AI"** button.
     - Observe the AI Neural Orb pulsing as it synthesizes parameters.
     - Review the **85% Recovery Probability**, reasoning, and **Evidence Citations** from prior payments.
* **Narration Cue:**
  > *"Let's see RecoverAI in action. Navigating to the Recovery Queue, our system prioritizes overdue invoices dynamically..."*

---

### Segment 4: [2:40 – 3:35] Human Approval & Dispute Guardrail Block
* **Target Page:** Invoice Details (`/invoices/24`) -> (`/invoices/4`)
* **Actions:**
  1. Scroll down to the **Suggested Customer Message** card.
  2. Click the green **"Approve & Send Reminder"** button.
  3. In the confirmation modal, review the message and click **"Confirm & Dispatch"**.
  4. Notice the success toast and updated **Recovery Action History** timeline.
  5. Now navigate back to Recovery Queue and click on Disputed invoice **INV-2024-004** (Acme Corp - $14,500):
     - Scroll down to the action center.
     - Point out the red guardrail notice:
       *"Sending reminders is disabled for disputed invoices — Escalate to Human review required."*
     - Show that the **"Approve & Send Reminder"** button is disabled to protect customer relations.
* **Narration Cue:**
  > *"Notice that RecoverAI drafts a tailored, respectful reminder message ready for review. As a finance analyst, I can edit the wording directly..."*

---

### Segment 5: [3:35 – 4:25] Immutable Audit Trail & System Settings
* **Target Page:** Click **Audit Log** in sidebar (`http://localhost:5173/audit-log`)
* **Actions:**
  1. Scroll through the immutable audit table showing every login, analysis inference, reminder dispatch, and operator action with exact timestamps.
  2. Click on **Settings** (`/settings`):
     - Highlight the **About RecoverAI** card showing:
       - **Project Owner:** Soharab Ahamad
       - **Track:** Track 3 AI Revenue Recovery
       - **Architecture:** React + Flask + Three.js 3D
     - Point out the configurable **High-Value Threshold ($10,000)** and recovery cooldown policies.
* **Narration Cue:**
  > *"Under the hood, RecoverAI is built with a modern, production-grade full-stack architecture..."*

---

### Segment 6: [4:25 – 5:00] Analytics Suite, Pitch Mode & Closing
* **Target Page:** Click **Analytics** in sidebar (`http://localhost:5173/analytics`)
* **Actions:**
  1. Highlight the recovery metrics:
     - **35% reduction in days-to-payment**
     - **Aging Bucket distribution (1-30d, 31-60d, 61-90d, 90d+)**
     - **Customer Segment recovery performance**
  2. Click **"Pitch Mode"** in the top header to showcase the high-contrast presentation banner:
     *"🎬 Pitch Video Recording Mode • Built by Soharab Ahamad"*
  3. Conclude the video.
* **Narration Cue:**
  > *"Finally, looking at our Analytics suite, the business impact is undeniable... Thank you for watching. RecoverAI is built by Soharab Ahamad for Track 3: AI Revenue Recovery."*

---

## 🎞️ Combining Audio, Video, and Subtitles with FFmpeg

If you record a raw video `my_screen_recording.mp4`:

```bash
# 1. Combine screen recording with TTS audio:
ffmpeg -i my_screen_recording.mp4 -i demo_voiceover.mp3 -c:v libx264 -c:a aac -shortest recoverai_demo_with_audio.mp4

# 2. Burn in subtitles:
ffmpeg -i recoverai_demo_with_audio.mp4 -vf "subtitles=recoverai_demo_subtitles.srt:force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=25'" -c:a copy recoverai_demo_final.mp4
```
