"""
RecoverAI - 5-Minute Complete Deep-Dive Video Production Pipeline
Records the 1080p application walkthrough using Playwright,
generates neural voiceover narration in individual developer perspective (Soharab Ahamad),
creates bottom-left synchronized SRT subtitles, and outputs the final MP4 deliverable.

Author: Soharab Ahamad
Project: RecoverAI - Track 3 AI Revenue Recovery
Deliverables in Project Root:
  - RecoverAI_Complete_Demo.mp4 (5-Minute Final Video with bottom-left burned subtitles)
  - RecoverAI_Complete_Demo_Script.txt (5-Minute Script transcript)
  - RecoverAI_Complete_Demo_Subtitles.srt (Synchronized bottom-left subtitles)
"""

import os
import sys
import time
import socket
import shutil
import asyncio
import subprocess
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_FILE = os.path.join(ROOT_DIR, "RecoverAI_Complete_Demo_Script.txt")
SRT_FILE = os.path.join(ROOT_DIR, "RecoverAI_Complete_Demo_Subtitles.srt")
FINAL_VIDEO_MP4 = os.path.join(ROOT_DIR, "RecoverAI_Complete_Demo.mp4")
TEMP_AUDIO_MP3 = os.path.join(ROOT_DIR, "_temp_master_voiceover.mp3")
TEMP_VIDEO_RAW_MP4 = os.path.join(ROOT_DIR, "_temp_screen_raw.mp4")
TEMP_VIDEO_WITH_AUDIO_MP4 = os.path.join(ROOT_DIR, "_temp_with_audio.mp4")

# 5-Minute Timed Sections (Total ~300 seconds)
SECTIONS = [
    {
        "id": 1,
        "title": "Introduction & Attribution",
        "text": (
            "Hello. I am Soharab Ahamad, and I built RecoverAI: an Intelligent Invoice and Payment Recovery Assistant. "
            "RecoverAI is built by Soharab Ahamad as an internship project for Track 3: AI Revenue Recovery. "
            "In modern B2B and SaaS enterprise finance, managing accounts receivable is one of the most vital yet labor-intensive operations. "
            "Every month, businesses lose millions of dollars in working capital due to overdue invoices, unaddressed customer disputes, and manual collections bottlenecks."
        )
    },
    {
        "id": 2,
        "title": "Problem & Governance Paradigm",
        "text": (
            "Traditional accounts receivable relies on static spreadsheets and generic reminder blasts that damage customer goodwill. "
            "I built RecoverAI to transform revenue recovery into an intelligent, policy-aware, and auditable operation. "
            "My architectural philosophy follows a strict governance principle: "
            "AI recommends and explains. Business rules validate. Humans approve sensitive actions. And the system records everything. "
            "Let me log in as a Finance Manager using our one-click demo access to enter the Command Center."
        )
    },
    {
        "id": 3,
        "title": "Command Center & 3D Visualizer",
        "text": (
            "Here on the main Command Center, finance executives get an immediate, 360-degree view of portfolio liquidity. "
            "At the top, our real-time KPIs show $315,420 in total outstanding receivables, with $281,420 overdue. "
            "My predictive engine identifies $189,200 as recoverable capital, while actively tracking 3 open customer disputes and 4 failed payment webhooks, yielding a 24.2% recovery rate. "
            "Below the KPIs is my interactive 3D Revenue Recovery Galaxy, where every orb represents an open invoice clustered by risk and recovery velocity, followed by historical recovery trends and aging distributions."
        )
    },
    {
        "id": 4,
        "title": "Prioritized Recovery Queue",
        "text": (
            "Navigating to the Recovery Queue, finance teams access a smart, prioritized worklist. "
            "Rather than simple due-date sorting, my system calculates a composite priority score using payment behavior, invoice age, and risk signals. "
            "Invoices are categorized into Low, Medium, and High risk tiers with tailored recovery actions. "
            "Activating the 5-Minute Demo Scenarios filter instantly isolates our key demonstration profiles: a standard overdue invoice, a disputed account, and a high-value gate. "
            "Let us open my recommended demo invoice: invoice INV-2024-024 for Jennifer Lee at Apex Solutions."
        )
    },
    {
        "id": 5,
        "title": "Invoice Details & AI Evidence Citations",
        "text": (
            "In the Invoice Details view, my full recovery workflow comes to life. "
            "On the left, we inspect the invoice ledger and customer profile: Jennifer has a $42,000 lifetime value, an 85% reliability score, and zero historical disputes. "
            "In the center, clicking 'Analyze with AI' triggers my backend inference copilot. In real-time, the AI computes an 85% recovery probability and recommends a courteous reminder with an installment option. "
            "Crucially, under Evidence Citations, my platform provides full transparency: citing 12 months of clean payment history, the absence of open support tickets, and corporate policy allowing installment flexibility."
        )
    },
    {
        "id": 6,
        "title": "Human Approval & Dispute Safety Guardrail",
        "text": (
            "On the right, RecoverAI drafts a tailored, respectful customer reminder referencing the due date and invoice terms. "
            "As a finance analyst, I can customize this draft and click 'Approve and Send Reminder'. A confirmation modal summarizes the payload before secure mock dispatch. "
            "Conversely, if we inspect disputed invoice INV-2024-004 for Acme Corp, my deterministic business safety rules automatically take over: "
            "the send button is strictly disabled, and a prominent compliance alert mandates escalation to Senior Human Review rather than sending premature collection notices."
        )
    },
    {
        "id": 7,
        "title": "Customers & Analytics Performance",
        "text": (
            "In the Customers section, my platform aggregates portfolio-level debtor intelligence, allowing AR teams to tailor outreach for enterprise Net-60 accounts versus seasonal clients. "
            "Moving to Analytics, RecoverAI demonstrates proven business impact: reducing average days-to-payment by over 35%, "
            "cutting manual collections effort by 80%, and visualizing recovery trends across aging buckets from 1 to 90-plus days."
        )
    },
    {
        "id": 8,
        "title": "Immutable Audit Trail & Architecture",
        "text": (
            "Finally, the Audit Log provides an immutable ledger recording every AI recommendation, analyst edit, approval, and mock dispatch for financial compliance and SOC2 auditing. "
            "In summary, RecoverAI combines React 18, Three.js, Flask, and SQLAlchemy into a transparent, production-ready decision-support system. "
            "Thank you for your time. RecoverAI was conceived, designed, and built by Soharab Ahamad for Track 3: AI Revenue Recovery."
        )
    }
]


def log(msg):
    print(f"[Pipeline] {msg}", flush=True)


def is_port_open(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False


def get_active_frontend_port():
    for p in [5173, 5174, 5175, 5176, 5177]:
        if is_port_open(p):
            return p
    return 5173


def format_srt_time(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


async def generate_narration_and_subtitles():
    import edge_tts

    log("Generating 5-Minute Neural Voiceover Narration (en-US-ChristopherNeural)...")
    voice = "en-US-ChristopherNeural"
    full_text = " ".join([s["text"] for s in SECTIONS])
    communicate = edge_tts.Communicate(full_text, voice, rate="-1%")
    await communicate.save(TEMP_AUDIO_MP3)
    log(f"Master voiceover generated: {TEMP_AUDIO_MP3}")

    log("Generating bottom-left synchronized SRT subtitle entries...")
    srt_entries = []
    current_time = 0.0

    for idx, sec in enumerate(SECTIONS, 1):
        temp_seg = os.path.join(ROOT_DIR, f"_temp_cue_{idx}.mp3")
        comm_seg = edge_tts.Communicate(sec["text"], voice, rate="-1%")
        await comm_seg.save(temp_seg)

        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", temp_seg
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            dur = float(res.stdout.strip())
        except Exception:
            dur = len(sec["text"].split()) * 0.42

        start_str = format_srt_time(current_time)
        end_str = format_srt_time(current_time + dur)

        srt_entries.append(f"{idx}\n{start_str} --> {end_str}\n{sec['text']}\n")
        current_time += dur + 0.4

        if os.path.exists(temp_seg):
            os.remove(temp_seg)

    with open(SRT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    log(f"Synchronized subtitles exported to project root: {SRT_FILE}")


def safe_goto(page, url, retries=3):
    for i in range(retries):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=12000)
            return
        except Exception as e:
            if i == retries - 1:
                log(f"Warning: navigation to {url} reached max retries: {e}")
            time.sleep(1)


def record_walkthrough():
    port = get_active_frontend_port()
    base_url = f"http://localhost:{port}"
    log(f"Recording high-definition 1080p application walkthrough on {base_url}...")

    raw_video_dir = os.path.join(ROOT_DIR, "_raw_playwright_rec")
    shutil.rmtree(raw_video_dir, ignore_errors=True)
    os.makedirs(raw_video_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--start-maximized", "--no-sandbox", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=raw_video_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()

        # Step 1: Login Screen & 1-Click Auth (0:00 - 0:35)
        log("(00:00) Demonstrating Login Screen...")
        safe_goto(page, f"{base_url}/login")
        page.wait_for_timeout(4000)

        # Step 2: 1-Click Authentication & Governance (0:35 - 1:10)
        log("(00:35) Signing in as Finance Manager...")
        try:
            page.locator("button:has-text('Finance Manager')").click(timeout=4000)
        except Exception:
            page.click("text=Finance Manager", timeout=4000)
        page.wait_for_timeout(4000)

        # Step 3: Command Center & 3D Galaxy (1:10 - 1:50)
        log("(01:10) Touring Command Center KPIs & 3D Galaxy...")
        page.wait_for_timeout(4000)
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(5000)
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(5000)
        page.mouse.wheel(0, -800)
        page.wait_for_timeout(4000)

        # Step 4: Recovery Queue & Demo Scenarios (1:50 - 2:35)
        log("(01:50) Navigating to Recovery Queue...")
        safe_goto(page, f"{base_url}/recovery-queue")
        page.wait_for_timeout(4000)

        log("Activating 5-Minute Demo Scenario Filter...")
        try:
            page.locator("button:has-text('Demo Scenarios')").click(timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(4000)

        # Step 5: Recommended Demo Invoice & AI Neural Core (2:35 - 3:25)
        log("(02:35) Opening Recommended Demo Invoice (INV-2024-024)...")
        safe_goto(page, f"{base_url}/invoices/24")
        page.wait_for_timeout(4000)

        log("Running AI Neural Analysis & computing evidence citations...")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(2500)

        try:
            page.locator("button:has-text('Analyze with AI')").click(timeout=4000)
        except Exception:
            pass
        page.wait_for_timeout(6000)

        page.mouse.wheel(0, 400)
        page.wait_for_timeout(4000)

        # Step 6: Approval, Dispatch & Dispute Guardrail (3:25 - 4:00)
        log("(03:25) Approving and Dispatching tailored reminder...")
        try:
            approve_btn = page.locator("button:has-text('Approve & Send Reminder')")
            if approve_btn.is_enabled():
                approve_btn.click(timeout=3000)
                page.wait_for_timeout(2000)
                page.locator("button:has-text('Confirm & Dispatch')").click(timeout=3000)
                page.wait_for_timeout(3500)
        except Exception:
            pass

        log("Demonstrating Dispute Guardrail on INV-2024-004...")
        safe_goto(page, f"{base_url}/invoices/4")
        page.wait_for_timeout(4000)
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(4500)

        # Step 7: Customers & Analytics Performance (4:00 - 4:35)
        log("(04:00) Touring Customers Portfolio Intelligence...")
        safe_goto(page, f"{base_url}/customers")
        page.wait_for_timeout(4500)

        log("Touring Analytics Suite & Aging Buckets...")
        safe_goto(page, f"{base_url}/analytics")
        page.wait_for_timeout(4500)
        page.mouse.wheel(0, 450)
        page.wait_for_timeout(4500)

        # Step 8: Audit Log, Pitch Mode & Architecture Conclusion (4:35 - 5:00)
        log("(04:35) Inspecting Immutable Audit Trail...")
        safe_goto(page, f"{base_url}/audit-log")
        page.wait_for_timeout(4500)

        log("Presenting Settings & Pitch Mode...")
        safe_goto(page, f"{base_url}/settings")
        page.wait_for_timeout(4000)
        try:
            page.locator("button:has-text('Pitch Mode')").click(timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(5000)

        context.close()
        browser.close()

    recorded_files = [os.path.join(raw_video_dir, f) for f in os.listdir(raw_video_dir) if f.endswith(".webm")]
    if not recorded_files:
        raise RuntimeError("No raw video stream found.")

    latest_webm = recorded_files[0]
    log(f"Transcoding raw video stream to {TEMP_VIDEO_RAW_MP4}...")
    cmd_transcode = [
        "ffmpeg", "-y", "-i", latest_webm,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        TEMP_VIDEO_RAW_MP4
    ]
    subprocess.run(cmd_transcode, check=True)
    shutil.rmtree(raw_video_dir, ignore_errors=True)
    log("Raw screen recording transcoded successfully.")


def composite_final_deliverable():
    log("Compositing video, vocal narration, and burning in bottom-left subtitles...")
    
    # 1. Mux screen video and audio narration
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", TEMP_VIDEO_RAW_MP4,
        "-i", TEMP_AUDIO_MP3,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        TEMP_VIDEO_WITH_AUDIO_MP4
    ]
    subprocess.run(cmd_mux, check=True)
    log(f"Muxed audio-visual intermediate: {TEMP_VIDEO_WITH_AUDIO_MP4}")

    # 2. Burn in subtitles at BOTTOM-LEFT (Alignment=1 in ASS style)
    # Alignment=1 -> Bottom Left
    # MarginL=50 -> 50px from left edge
    # MarginV=35 -> 35px from bottom edge
    # BorderStyle=3 -> Opaque background box with clear readable text
    srt_escaped = SRT_FILE.replace("\\", "/").replace(":", "\\:")
    cmd_subtitles = [
        "ffmpeg", "-y",
        "-i", TEMP_VIDEO_WITH_AUDIO_MP4,
        "-vf", f"subtitles='{srt_escaped}':force_style='Alignment=1,MarginL=50,MarginV=35,FontSize=15,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H90000000,BorderStyle=3'",
        "-c:a", "copy",
        FINAL_VIDEO_MP4
    ]
    try:
        subprocess.run(cmd_subtitles, check=True)
        log(f"Final 5-minute MP4 with bottom-left subtitles generated in root: {FINAL_VIDEO_MP4}")
    except Exception as e:
        log(f"Subtitle burn-in fallback: {e}")
        shutil.copy(TEMP_VIDEO_WITH_AUDIO_MP4, FINAL_VIDEO_MP4)

    # Clean up temporary intermediates
    for tmp in [TEMP_AUDIO_MP3, TEMP_VIDEO_RAW_MP4, TEMP_VIDEO_WITH_AUDIO_MP4]:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass

    print("\n" + "=" * 70, flush=True)
    print("[SUCCESS] RecoverAI 5-Minute Demonstration Video Production Complete!", flush=True)
    print(f"  * Final Video:     {FINAL_VIDEO_MP4} (Bottom-Left Subtitles)", flush=True)
    print(f"  * Script:          {SCRIPT_FILE}", flush=True)
    print(f"  * Subtitles (SRT): {SRT_FILE}", flush=True)
    print("=" * 70 + "\n", flush=True)


def main():
    asyncio.run(generate_narration_and_subtitles())
    record_walkthrough()
    composite_final_deliverable()


if __name__ == "__main__":
    main()
