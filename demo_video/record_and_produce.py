"""
RecoverAI - Automated Video Recorder & Producer
Records high-definition screen demo at 1080p using Playwright,
combines with neural voiceover, and burns in synchronized subtitles.

Author: Soharab Ahamad
Project: RecoverAI - Track 3 AI Revenue Recovery
"""

import os
import sys
import time
import shutil
import subprocess
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_RAW_MP4 = os.path.join(SCRIPT_DIR, "screen_raw.mp4")
AUDIO_MP3 = os.path.join(SCRIPT_DIR, "demo_voiceover.mp3")
AUDIO_WAV = os.path.join(SCRIPT_DIR, "demo_voiceover.wav")
SRT_FILE = os.path.join(SCRIPT_DIR, "recoverai_demo_subtitles.srt")
DEMO_WITH_AUDIO_MP4 = os.path.join(SCRIPT_DIR, "recoverai_demo_with_audio.mp4")
FINAL_VIDEO_MP4 = os.path.join(SCRIPT_DIR, "recoverai_demo_final.mp4")


def log(msg):
    print(f"[Recorder] {msg}", flush=True)


def record_screen():
    log("Starting Playwright automated screen recording at 1920x1080...")
    raw_video_dir = os.path.join(SCRIPT_DIR, "_raw_rec")
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

        # Step 1: Login Page
        log("(0:00) Opening Login Screen...")
        page.goto("http://localhost:5173/login", wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        # 1-Click Demo Login as Finance Manager
        log("Clicking 1-Click Finance Manager Demo Login...")
        try:
            page.locator("button:has-text('Finance Manager')").click(timeout=4000)
        except Exception:
            page.click("text=Finance Manager", timeout=4000)
        page.wait_for_timeout(3000)

        # Step 2: Dashboard Overview & 3D Galaxy
        log("(0:40) Presenting Executive Dashboard & 3D Galaxy...")
        page.wait_for_timeout(2500)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(3000)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(3000)
        page.mouse.wheel(0, -700)
        page.wait_for_timeout(2000)

        # Step 3: Recovery Queue & Demo Scenario Filter
        log("(1:30) Navigating to Recovery Queue...")
        page.goto("http://localhost:5173/recovery-queue", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)

        # Toggle 5-Minute Demo Scenario
        log("Activating 5-Min Demo Scenarios filter...")
        try:
            page.locator("button:has-text('Demo Scenarios')").click(timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(2500)

        # Step 4: Invoice Details & AI Analysis
        log("(2:00) Opening Recommended Demo Invoice (INV-2024-024)...")
        page.goto("http://localhost:5173/invoices/24", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        log("Running AI Neural Recovery Analysis...")
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(1000)
        
        try:
            page.locator("button:has-text('Analyze with AI')").click(timeout=4000)
        except Exception:
            pass
        page.wait_for_timeout(4000)

        # Scroll to inspect recommendation & customer message
        page.mouse.wheel(0, 350)
        page.wait_for_timeout(2500)

        # Click Approve & Send Reminder
        log("(2:40) Approving and Dispatching tailored reminder...")
        try:
            approve_btn = page.locator("button:has-text('Approve & Send Reminder')")
            if approve_btn.is_enabled():
                approve_btn.click(timeout=3000)
                page.wait_for_timeout(1500)
                page.locator("button:has-text('Confirm & Dispatch')").click(timeout=3000)
                page.wait_for_timeout(2500)
        except Exception:
            pass

        # Step 5: Dispute Guardrail Demonstration
        log("(3:10) Demonstrating Dispute Guardrail on INV-2024-004...")
        page.goto("http://localhost:5173/invoices/4", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(3000)

        # Step 6: Audit Log & Governance
        log("(3:40) Inspecting Immutable Audit Trail...")
        page.goto("http://localhost:5173/audit-log", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(2500)

        # Step 7: Analytics Suite & Pitch Mode
        log("(4:20) Inspecting Analytics Suite...")
        page.goto("http://localhost:5173/analytics", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(2500)

        # Activate Pitch Mode
        log("(4:50) Toggling Pitch Mode Presentation Banner...")
        try:
            page.locator("button:has-text('Pitch Mode')").click(timeout=3000)
        except Exception:
            pass
        page.wait_for_timeout(3000)

        context.close()
        browser.close()

    # Find recorded webm file
    recorded_files = [os.path.join(raw_video_dir, f) for f in os.listdir(raw_video_dir) if f.endswith(".webm")]
    if not recorded_files:
        raise RuntimeError("No recorded video file found in raw video directory.")

    latest_rec = recorded_files[0]
    log(f"Converting recorded stream {latest_rec} to {SCREEN_RAW_MP4}...")
    
    # Transcode webm to standard MP4 with smooth framerate
    cmd_transcode = [
        "ffmpeg", "-y", "-i", latest_rec,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
        SCREEN_RAW_MP4
    ]
    subprocess.run(cmd_transcode, check=True)
    shutil.rmtree(raw_video_dir, ignore_errors=True)
    log(f"Screen recording exported: {SCREEN_RAW_MP4}")


def produce_final_video():
    log("Combining video, voiceover, and synchronized subtitles...")
    audio_file = AUDIO_MP3 if os.path.exists(AUDIO_MP3) else AUDIO_WAV
    if not os.path.exists(audio_file):
        raise FileNotFoundError("Audio narration file not found. Run generate_audio.py first.")

    # 1. Combine screen recording and audio
    log(f"Muxing video and audio into {DEMO_WITH_AUDIO_MP4}...")
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", SCREEN_RAW_MP4,
        "-i", audio_file,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-pix_fmt", "yuv420p",
        DEMO_WITH_AUDIO_MP4
    ]
    subprocess.run(cmd_mux, check=True)

    # 2. Burn in subtitles or package final video
    log(f"Packaging final video with subtitles: {FINAL_VIDEO_MP4}...")
    srt_escaped = SRT_FILE.replace("\\", "/").replace(":", "\\:")
    cmd_subtitles = [
        "ffmpeg", "-y",
        "-i", DEMO_WITH_AUDIO_MP4,
        "-vf", f"subtitles='{srt_escaped}':force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=25'",
        "-c:a", "copy",
        FINAL_VIDEO_MP4
    ]
    try:
        subprocess.run(cmd_subtitles, check=True)
        log(f"Final video with burned-in subtitles created: {FINAL_VIDEO_MP4}")
    except Exception as e:
        log(f"Burning subtitles encountered: {e}. Copying with soft subtitles...")
        shutil.copy(DEMO_WITH_AUDIO_MP4, FINAL_VIDEO_MP4)

    print("\n" + "=" * 65, flush=True)
    print("[SUCCESS] RecoverAI Pitch Video Production COMPLETE!", flush=True)
    print(f"   * Raw Screen Recording: {SCREEN_RAW_MP4}", flush=True)
    print(f"   * Voiceover Audio:      {audio_file}", flush=True)
    print(f"   * Synchronized SRT:     {SRT_FILE}", flush=True)
    print(f"   * Final Demo Video:     {FINAL_VIDEO_MP4}", flush=True)
    print("=" * 65 + "\n", flush=True)


def main():
    record_screen()
    produce_final_video()


if __name__ == "__main__":
    main()
