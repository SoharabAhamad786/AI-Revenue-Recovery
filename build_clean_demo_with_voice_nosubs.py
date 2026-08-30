"""
RecoverAI - 100% Clean 5-Minute Demo Video with Voiceover Only (ABSOLUTELY NO SUBTITLES)
Author & Developer: Soharab Ahamad
Track: Track 3: AI Revenue Recovery

Pipeline:
1. Generate master neural voiceover narration
2. Record live 1080p browser walkthrough (~297-300s) directly from browser
3. Mux clean video + voiceover audio with NO subtitle filters
4. Overwrite all demo mp4 files in project root
"""

import os
import sys
import time
import socket
import shutil
import asyncio
import subprocess
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
FINAL_OUTPUT = os.path.join(ROOT, "RecoverAI_5Min_Demo.mp4")
SYNC_FINAL = os.path.join(ROOT, "RecoverAI_5Min_Demo_Final.mp4")
SYNC_COMPLETE = os.path.join(ROOT, "RecoverAI_Complete_Demo.mp4")

TEMP_AUDIO = os.path.join(ROOT, "_clean_voice.mp3")
TEMP_RAW_DIR = os.path.join(ROOT, "_raw_clean_recording")
TEMP_CLEAN_VIDEO = os.path.join(ROOT, "_clean_screen_only.mp4")

SECTIONS = [
    {
        "start": 0.0, "end": 40.0,
        "text": (
            "Hello, I am Soharab Ahamad, and welcome to RecoverAI: "
            "an Intelligent Invoice and Payment Recovery Assistant. "
            "RecoverAI is my internship project for Track 3: AI Revenue Recovery. "
            "This platform helps accounts receivable teams identify overdue invoices, "
            "understand why customers haven't paid, and take the right recovery action. "
            "Here you can see our secure login screen with one-click demo access."
        )
    },
    {
        "start": 40.0, "end": 55.0,
        "text": (
            "Let me sign in as a Finance Manager using our one-click demo authentication. "
            "This gives us full approval access to the entire recovery platform."
        )
    },
    {
        "start": 55.0, "end": 130.0,
        "text": (
            "Welcome to the Executive Command Center. At the top, real-time KPI cards show "
            "$315,420 in total outstanding receivables, with $281,420 overdue. "
            "My AI engine identifies $189,200 as recoverable capital, while tracking "
            "3 open customer disputes, 4 failed payment webhooks, and a 24.2% recovery rate. "
            "Below, our interactive 3D Revenue Recovery Galaxy visualizes every open invoice "
            "as an orb clustered by risk level and recovery velocity. "
            "Scrolling down, we see historical recovery trend charts, "
            "aging distribution analysis across 30, 60, and 90-plus day buckets, "
            "and a real-time activity feed tracking all recovery actions taken by the team."
        )
    },
    {
        "start": 130.0, "end": 170.0,
        "text": (
            "The Recovery Queue presents a smart, prioritized worklist for the AR team. "
            "Unlike simple date sorting, my system calculates composite priority scores "
            "using payment behavior history, invoice age, and AI risk signals. "
            "Invoices are categorized into Low, Medium, and High risk tiers. "
            "The 5-Minute Demo Scenarios filter isolates our key demonstration profiles: "
            "a standard overdue invoice, a disputed account, and a high-value case."
        )
    },
    {
        "start": 170.0, "end": 220.0,
        "text": (
            "Opening invoice INV-2024-024 for Jennifer Lee at Apex Solutions. "
            "The invoice detail view shows the complete customer profile with "
            "a $42,000 lifetime value and an 85% reliability score. "
            "Clicking 'Analyze with AI' triggers my backend inference engine. "
            "In real-time, the AI computes an 85% recovery probability "
            "and recommends a courteous reminder with an installment option. "
            "Under Evidence Citations, the platform provides full transparency, "
            "citing 12 months of clean payment history, absence of support tickets, "
            "and corporate policy allowing installment flexibility."
        )
    },
    {
        "start": 220.0, "end": 235.0,
        "text": (
            "RecoverAI drafts a tailored customer reminder. "
            "As a finance analyst, I can customize this draft "
            "and click 'Approve and Send Reminder'. "
            "A confirmation modal verifies the payload before mock dispatch."
        )
    },
    {
        "start": 235.0, "end": 255.0,
        "text": (
            "Now, inspecting disputed invoice INV-2024-004 for Acme Corp. "
            "Here, my deterministic safety rules automatically take over. "
            "The send button is strictly disabled, and a compliance alert "
            "mandates escalation to Senior Human Review, "
            "preventing premature collection notices on disputed accounts."
        )
    },
    {
        "start": 255.0, "end": 270.0,
        "text": (
            "The Customers section aggregates portfolio-level debtor intelligence, "
            "allowing AR teams to tailor outreach strategies "
            "for enterprise Net-60 accounts versus seasonal clients."
        )
    },
    {
        "start": 270.0, "end": 290.0,
        "text": (
            "Analytics demonstrates proven business impact: "
            "reducing average days-to-payment by over 35 percent, "
            "cutting manual collections effort by 80 percent, "
            "and visualizing recovery trends across aging buckets."
        )
    },
    {
        "start": 290.0, "end": 300.0,
        "text": (
            "Finally, the Audit Log provides an immutable compliance ledger. "
            "Thank you for watching. RecoverAI was built by Soharab Ahamad "
            "for Track 3: AI Revenue Recovery."
        )
    }
]


def log(msg):
    print(f"[RecoverAI Clean Demo] {msg}", flush=True)


def get_port():
    for p in [5173, 5174, 5175]:
        try:
            with socket.socket() as s:
                s.settimeout(0.5)
                if s.connect_ex(("127.0.0.1", p)) == 0:
                    return p
        except Exception:
            pass
    return 5173


def safe_click(page, selector, timeout=3000):
    try:
        page.locator(selector).first.click(timeout=timeout)
        return True
    except Exception:
        return False


def safe_goto(page, url):
    for _ in range(3):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            return
        except Exception:
            time.sleep(1)


async def generate_voice():
    import edge_tts
    log("Step 1: Generating neural voiceover narration...")
    voice = "en-US-ChristopherNeural"
    full_text = " ".join(s["text"] for s in SECTIONS)
    comm = edge_tts.Communicate(full_text, voice, rate="-2%")
    await comm.save(TEMP_AUDIO)
    log(f"Voiceover saved: {TEMP_AUDIO}")


def record_browser():
    port = get_port()
    base = f"http://localhost:{port}"
    log(f"Step 2: Recording fresh 1080p browser walkthrough on {base}...")

    shutil.rmtree(TEMP_RAW_DIR, ignore_errors=True)
    os.makedirs(TEMP_RAW_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=TEMP_RAW_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = ctx.new_page()

        # Login (0:00 - 0:40)
        log("[0:00] Login Screen")
        safe_goto(page, f"{base}/login")
        page.wait_for_timeout(10000)
        page.mouse.wheel(0, 200)
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, -200)
        page.wait_for_timeout(6000)
        page.mouse.move(960, 540)
        page.wait_for_timeout(6000)
        page.mouse.move(960, 600)
        page.wait_for_timeout(5000)

        # 1-Click Login (0:40 - 0:55)
        log("[0:40] One-Click Login as Finance Manager")
        safe_click(page, "button:has-text('Finance Manager')")
        page.wait_for_timeout(8000)

        # Dashboard (0:55 - 2:10)
        log("[0:55] Dashboard - KPI Cards")
        page.wait_for_timeout(15000)
        log("[1:10] Dashboard - 3D Galaxy")
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(15000)
        log("[1:25] Dashboard - Recovery Trends")
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(10000)
        log("[1:35] Dashboard - Aging Distribution")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(10000)
        log("[1:45] Dashboard - Recent Activity")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(10000)
        log("[1:55] Dashboard - Back to top")
        page.mouse.wheel(0, -1500)
        page.wait_for_timeout(8000)

        # Recovery Queue (2:10 - 2:50)
        log("[2:10] Recovery Queue")
        safe_goto(page, f"{base}/recovery-queue")
        page.wait_for_timeout(8000)
        safe_click(page, "button:has-text('Demo Scenarios')")
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, -600)
        page.wait_for_timeout(5000)

        # Invoice Detail INV-2024-024 (2:50 - 3:40)
        log("[2:50] Invoice Detail - INV-2024-024")
        safe_goto(page, f"{base}/invoices/24")
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 250)
        page.wait_for_timeout(6000)
        log("[3:05] AI Analysis")
        safe_click(page, "button:has-text('Analyze with AI')")
        page.wait_for_timeout(14000)
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(8000)

        # Approve & Send (3:40 - 3:55)
        log("[3:40] Approve & Send Reminder")
        try:
            btn = page.locator("button:has-text('Approve & Send Reminder')")
            if btn.first.is_enabled(timeout=2000):
                btn.first.click(timeout=2000)
                page.wait_for_timeout(4000)
                safe_click(page, "button:has-text('Confirm')")
                page.wait_for_timeout(5000)
        except Exception:
            pass
        page.wait_for_timeout(4000)

        # Dispute Guardrail INV-2024-004 (3:55 - 4:15)
        log("[3:55] Dispute Guardrail - INV-2024-004")
        safe_goto(page, f"{base}/invoices/4")
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(7000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(7000)

        # Customers (4:15 - 4:30)
        log("[4:15] Customers")
        safe_goto(page, f"{base}/customers")
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(8000)

        # Analytics (4:30 - 4:50)
        log("[4:30] Analytics")
        safe_goto(page, f"{base}/analytics")
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(7000)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(9000)

        # Audit Log (4:50 - 5:05)
        log("[4:50] Audit Log")
        safe_goto(page, f"{base}/audit-log")
        page.wait_for_timeout(8000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(8000)

        # Settings (5:05 - 5:20)
        log("[5:05] Settings")
        safe_goto(page, f"{base}/settings")
        page.wait_for_timeout(8000)
        safe_click(page, "button:has-text('Pitch Mode')")
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(6000)
        page.wait_for_timeout(5000)

        log("Browser walkthrough recording complete.")
        ctx.close()
        browser.close()

    webm_files = [os.path.join(TEMP_RAW_DIR, f) for f in os.listdir(TEMP_RAW_DIR) if f.endswith(".webm")]
    if not webm_files:
        raise RuntimeError("No recorded webm video found!")
    webm = webm_files[0]

    log(f"Transcoding raw webm to clean video: {TEMP_CLEAN_VIDEO}...")
    subprocess.run([
        "ffmpeg", "-y", "-i", webm,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an",
        TEMP_CLEAN_VIDEO
    ], check=True)
    shutil.rmtree(TEMP_RAW_DIR, ignore_errors=True)


def mux_clean():
    log("Step 3: Muxing clean video with voiceover audio (NO SUBTITLES)...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", TEMP_CLEAN_VIDEO,
        "-i", TEMP_AUDIO,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-af", "apad",
        "-shortest",
        FINAL_OUTPUT
    ], check=True)

    # Sync to all file names
    shutil.copy(FINAL_OUTPUT, SYNC_FINAL)
    shutil.copy(FINAL_OUTPUT, SYNC_COMPLETE)

    # Clean temporary files
    for tmp in [TEMP_AUDIO, TEMP_CLEAN_VIDEO]:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", FINAL_OUTPUT],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    dur = float(res.stdout.strip()) if res.stdout.strip() else 0

    print("\n" + "=" * 70, flush=True)
    print("[SUCCESS] 100% Clean 5-Minute Demo Video with Voiceover (NO Subtitles)!", flush=True)
    print(f"  Final File: {FINAL_OUTPUT}", flush=True)
    print(f"  Duration:   {dur:.1f}s ({dur/60:.1f} minutes)", flush=True)
    print(f"  Resolution: 1920x1080 Full HD", flush=True)
    print(f"  Voice:      Neural Voiceover (en-US-ChristopherNeural)", flush=True)
    print(f"  Subtitles:  ZERO / NONE (Completely clean screen)", flush=True)
    print("=" * 70 + "\n", flush=True)


def main():
    asyncio.run(generate_voice())
    record_browser()
    mux_clean()


if __name__ == "__main__":
    main()
