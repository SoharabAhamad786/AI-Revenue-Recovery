"""
RecoverAI - 5-Minute Demo Video with Voiceover Only (NO Subtitles)
Author & Developer: Soharab Ahamad
Track: Track 3: AI Revenue Recovery

Muxes the master neural voiceover onto the clean 1080p screen recording without any subtitles.
"""

import os
import asyncio
import subprocess
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(ROOT, "RecoverAI_5Min_Demo.mp4")
TEMP_AUDIO = os.path.join(ROOT, "_temp_voice_nosubs.mp3")
OUTPUT_VIDEO = os.path.join(ROOT, "RecoverAI_5Min_Demo_Final.mp4")
SYNC_5MIN = os.path.join(ROOT, "RecoverAI_5Min_Demo.mp4")
SYNC_COMPLETE = os.path.join(ROOT, "RecoverAI_Complete_Demo.mp4")
SCRIPT_FILE = os.path.join(ROOT, "RecoverAI_Demo_Script.txt")

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
    print(f"[VoiceOnly] {msg}", flush=True)


async def generate_voice():
    import edge_tts
    log("Generating master neural voiceover narration...")
    voice = "en-US-ChristopherNeural"
    full_text = " ".join(s["text"] for s in SECTIONS)
    comm = edge_tts.Communicate(full_text, voice, rate="-2%")
    await comm.save(TEMP_AUDIO)
    log(f"Voiceover saved: {TEMP_AUDIO}")


def mux_video_audio():
    # Make sure we read from a pure screen video (without burned subtitles)
    # Let's check if we need to mux directly
    temp_target = os.path.join(ROOT, "_temp_final_nosubs.mp4")
    
    log("Muxing neural voiceover with clean screen recording (no subtitles)...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", INPUT_VIDEO,
        "-i", TEMP_AUDIO,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-af", "apad",
        "-shortest",
        temp_target
    ], check=True)
    
    shutil.move(temp_target, OUTPUT_VIDEO)
    shutil.copy(OUTPUT_VIDEO, SYNC_5MIN)
    shutil.copy(OUTPUT_VIDEO, SYNC_COMPLETE)
    log(f"Final video generated without subtitles: {OUTPUT_VIDEO}")
    
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)

    # Check duration
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", OUTPUT_VIDEO],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    dur = float(res.stdout.strip()) if res.stdout.strip() else 0

    print("\n" + "=" * 60, flush=True)
    print("[SUCCESS] RecoverAI 5-Minute Demo Video (Voiceover Only, NO Subtitles)!", flush=True)
    print(f"  File:      {OUTPUT_VIDEO}", flush=True)
    print(f"  Duration:  {dur:.1f}s ({dur/60:.1f} min)", flush=True)
    print(f"  Voice:     Neural narration (en-US-ChristopherNeural)", flush=True)
    print(f"  Subtitles: NONE (Clean screen)", flush=True)
    print("=" * 60, flush=True)


def main():
    asyncio.run(generate_voice())
    mux_video_audio()


if __name__ == "__main__":
    main()
