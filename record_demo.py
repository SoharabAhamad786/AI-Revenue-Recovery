"""
RecoverAI — Clean 5-Minute Demo Screen Recording (No Subtitles)
Records a full 1080p browser walkthrough of the live RecoverAI application.
Target duration: ~5 minutes (300+ seconds)
Output: RecoverAI_5Min_Demo.mp4 in the project root.
"""

import os
import time
import socket
import shutil
import subprocess
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.abspath(__file__))
FINAL_MP4 = os.path.join(ROOT, "RecoverAI_5Min_Demo.mp4")
RAW_DIR = os.path.join(ROOT, "_raw_demo_rec")


def log(msg):
    print(f"[RecoverAI Demo] {msg}", flush=True)


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


def record():
    port = get_port()
    base = f"http://localhost:{port}"
    log(f"Recording 5-minute 1080p walkthrough on {base}")

    shutil.rmtree(RAW_DIR, ignore_errors=True)
    os.makedirs(RAW_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=RAW_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = ctx.new_page()

        # ═══════════════════════════════════════════════════════
        # LOGIN SCREEN  (0:00 - 0:40)  ~40s
        # ═══════════════════════════════════════════════════════
        log("[0:00] Login Screen")
        safe_goto(page, f"{base}/login")
        page.wait_for_timeout(10000)

        page.mouse.wheel(0, 200)
        page.wait_for_timeout(6000)
        page.mouse.wheel(0, -200)
        page.wait_for_timeout(6000)

        page.mouse.move(960, 540)
        page.wait_for_timeout(6000)

        # Hover over Finance Manager button
        page.mouse.move(960, 600)
        page.wait_for_timeout(5000)

        # ═══════════════════════════════════════════════════════
        # ONE-CLICK LOGIN  (0:40 - 0:55)  ~15s
        # ═══════════════════════════════════════════════════════
        log("[0:40] One-Click Login as Finance Manager")
        safe_click(page, "button:has-text('Finance Manager')")
        page.wait_for_timeout(8000)

        # ═══════════════════════════════════════════════════════
        # COMMAND CENTER DASHBOARD  (0:55 - 2:10)  ~75s
        # ═══════════════════════════════════════════════════════
        log("[0:55] Dashboard - KPI Cards")
        page.wait_for_timeout(15000)

        log("[1:07] Dashboard - 3D Galaxy")
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(15000)

        log("[1:19] Dashboard - Recovery Trends")
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(10000)

        log("[1:29] Dashboard - Aging Distribution")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(10000)

        log("[1:39] Dashboard - Recent Activity")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(10000)

        log("[1:49] Dashboard - Back to top")
        page.mouse.wheel(0, -1500)
        page.wait_for_timeout(8000)

        # ═══════════════════════════════════════════════════════
        # RECOVERY QUEUE  (2:10 - 2:50)  ~40s
        # ═══════════════════════════════════════════════════════
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

        # ═══════════════════════════════════════════════════════
        # INVOICE DETAIL & AI ANALYSIS  (2:50 - 3:40)  ~50s
        # ═══════════════════════════════════════════════════════
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

        # ═══════════════════════════════════════════════════════
        # APPROVE & SEND  (3:40 - 3:55)  ~15s
        # ═══════════════════════════════════════════════════════
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

        # ═══════════════════════════════════════════════════════
        # DISPUTE GUARDRAIL  (3:55 - 4:15)  ~20s
        # ═══════════════════════════════════════════════════════
        log("[3:55] Dispute Guardrail - INV-2024-004")
        safe_goto(page, f"{base}/invoices/4")
        page.wait_for_timeout(8000)

        page.mouse.wheel(0, 300)
        page.wait_for_timeout(7000)

        page.mouse.wheel(0, 300)
        page.wait_for_timeout(7000)

        # ═══════════════════════════════════════════════════════
        # CUSTOMERS  (4:15 - 4:30)  ~15s
        # ═══════════════════════════════════════════════════════
        log("[4:15] Customers")
        safe_goto(page, f"{base}/customers")
        page.wait_for_timeout(8000)

        page.mouse.wheel(0, 350)
        page.wait_for_timeout(8000)

        # ═══════════════════════════════════════════════════════
        # ANALYTICS  (4:30 - 4:50)  ~20s
        # ═══════════════════════════════════════════════════════
        log("[4:30] Analytics")
        safe_goto(page, f"{base}/analytics")
        page.wait_for_timeout(8000)

        page.mouse.wheel(0, 400)
        page.wait_for_timeout(7000)

        page.mouse.wheel(0, 400)
        page.wait_for_timeout(9000)

        # ═══════════════════════════════════════════════════════
        # AUDIT LOG  (4:50 - 5:05)  ~15s
        # ═══════════════════════════════════════════════════════
        log("[4:50] Audit Log")
        safe_goto(page, f"{base}/audit-log")
        page.wait_for_timeout(8000)

        page.mouse.wheel(0, 300)
        page.wait_for_timeout(8000)

        # ═══════════════════════════════════════════════════════
        # SETTINGS  (5:05 - 5:20)  ~15s
        # ═══════════════════════════════════════════════════════
        log("[5:05] Settings")
        safe_goto(page, f"{base}/settings")
        page.wait_for_timeout(8000)

        safe_click(page, "button:has-text('Pitch Mode')")
        page.wait_for_timeout(6000)

        page.mouse.wheel(0, 300)
        page.wait_for_timeout(6000)

        # Final pause
        page.wait_for_timeout(5000)

        log("Recording complete. Closing browser...")
        ctx.close()
        browser.close()

    # Find the recorded .webm
    webm_files = [os.path.join(RAW_DIR, f) for f in os.listdir(RAW_DIR) if f.endswith(".webm")]
    if not webm_files:
        raise RuntimeError("No recorded video found!")

    webm = webm_files[0]
    log(f"Transcoding {webm} -> {FINAL_MP4}")

    subprocess.run([
        "ffmpeg", "-y", "-i", webm,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        "-an",
        FINAL_MP4
    ], check=True)

    shutil.rmtree(RAW_DIR, ignore_errors=True)

    # Verify duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", FINAL_MP4],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    duration = float(result.stdout.strip()) if result.stdout.strip() else 0

    print("\n" + "=" * 60, flush=True)
    print("[SUCCESS] RecoverAI 5-Minute Demo Video Recorded!", flush=True)
    print(f"  File:     {FINAL_MP4}", flush=True)
    print(f"  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)", flush=True)
    print(f"  Format:   1920x1080 H.264 MP4 (no subtitles)", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    record()
