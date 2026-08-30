"""
Add voiceover narration and small bottom-left subtitles to the existing
RecoverAI_5Min_Demo.mp4 screen recording.

Output: RecoverAI_5Min_Demo_Final.mp4
"""

import os
import asyncio
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_VIDEO = os.path.join(ROOT, "RecoverAI_5Min_Demo.mp4")
SRT_FILE = os.path.join(ROOT, "RecoverAI_Demo_Subtitles.srt")
SCRIPT_FILE = os.path.join(ROOT, "RecoverAI_Demo_Script.txt")
TEMP_AUDIO = os.path.join(ROOT, "_temp_voice.mp3")
TEMP_MUX = os.path.join(ROOT, "_temp_mux.mp4")
FINAL_VIDEO = os.path.join(ROOT, "RecoverAI_5Min_Demo_Final.mp4")

# Timed narration sections matched to the screen recording
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
    print(f"[Voice+Subs] {msg}", flush=True)


def fmt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


async def generate_audio_and_srt():
    import edge_tts

    log("Generating neural voiceover narration...")
    voice = "en-US-ChristopherNeural"
    full_text = " ".join(s["text"] for s in SECTIONS)
    comm = edge_tts.Communicate(full_text, voice, rate="-2%")
    await comm.save(TEMP_AUDIO)
    log(f"Voiceover saved: {TEMP_AUDIO}")

    # Generate SRT with per-section timing
    log("Generating bottom-left SRT subtitles...")
    srt_lines = []
    for i, sec in enumerate(SECTIONS, 1):
        srt_lines.append(f"{i}")
        srt_lines.append(f"{fmt(sec['start'])} --> {fmt(sec['end'])}")
        srt_lines.append(sec["text"])
        srt_lines.append("")

    with open(SRT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_lines))
    log(f"Subtitles saved: {SRT_FILE}")

    # Save script
    with open(SCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write("RecoverAI — 5-Minute Demo Narration Script\n")
        f.write("Developer: Soharab Ahamad\n")
        f.write("Track: Track 3: AI Revenue Recovery\n\n")
        for sec in SECTIONS:
            f.write(f"[{fmt(sec['start'])} - {fmt(sec['end'])}]\n")
            f.write(sec["text"] + "\n\n")
    log(f"Script saved: {SCRIPT_FILE}")


def mux_and_burn():
    log("Muxing voiceover audio onto screen recording (padding audio to match video)...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", INPUT_VIDEO,
        "-i", TEMP_AUDIO,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-af", "apad",
        "-shortest",
        TEMP_MUX
    ], check=True)
    log(f"Audio muxed: {TEMP_MUX}")

    # Burn subtitles at BOTTOM-LEFT, small font
    # Alignment=1 = bottom-left in SSA/ASS
    # FontSize=13 = small
    # MarginL=40 = 40px from left edge
    # MarginV=25 = 25px from bottom
    # BorderStyle=3 = opaque background box for readability
    srt_path = SRT_FILE.replace("\\", "/").replace(":", "\\:")
    subtitle_filter = (
        f"subtitles='{srt_path}':force_style='"
        f"Alignment=1,"
        f"MarginL=40,"
        f"MarginV=25,"
        f"FontSize=13,"
        f"Fontname=Arial,"
        f"PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,"
        f"BackColour=&HA0000000,"
        f"BorderStyle=3"
        f"'"
    )

    log("Burning small bottom-left subtitles into final video...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", TEMP_MUX,
        "-vf", subtitle_filter,
        "-c:a", "copy",
        FINAL_VIDEO
    ], check=True)
    log(f"Final video: {FINAL_VIDEO}")

    # Clean up temps
    for f in [TEMP_AUDIO, TEMP_MUX]:
        if os.path.exists(f):
            os.remove(f)

    # Verify
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", FINAL_VIDEO],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    dur = float(res.stdout.strip()) if res.stdout.strip() else 0

    print("\n" + "=" * 60, flush=True)
    print("[SUCCESS] RecoverAI Demo Video with Voice + Subtitles!", flush=True)
    print(f"  File:      {FINAL_VIDEO}", flush=True)
    print(f"  Duration:  {dur:.1f}s ({dur/60:.1f} min)", flush=True)
    print(f"  Voice:     Neural narration (en-US-ChristopherNeural)", flush=True)
    print(f"  Subtitles: Small, bottom-left (Alignment=1, FontSize=13)", flush=True)
    print("=" * 60, flush=True)


def main():
    asyncio.run(generate_audio_and_srt())
    mux_and_burn()


if __name__ == "__main__":
    main()
