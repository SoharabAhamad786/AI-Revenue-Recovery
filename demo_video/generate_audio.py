"""
RecoverAI - Voiceover & Subtitles Generator
Generates high-quality TTS audio narration (using edge-tts or pyttsx3 fallback)
and exports synchronized .srt subtitles.

Author: Soharab Ahamad
Project: RecoverAI - Track 3 AI Revenue Recovery
"""

import os
import sys
import asyncio
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_AUDIO_MP3 = os.path.join(SCRIPT_DIR, "demo_voiceover.mp3")
OUTPUT_AUDIO_WAV = os.path.join(SCRIPT_DIR, "demo_voiceover.wav")
OUTPUT_SRT = os.path.join(SCRIPT_DIR, "recoverai_demo_subtitles.srt")

# Timed script segments for 5-minute pitch video
SECTIONS = [
    {
        "id": 1,
        "title": "Problem Statement",
        "text": (
            "Welcome. In every B2B and SaaS business, accounts receivable is one of the most critical "
            "yet inefficient financial workflows. Every month, companies lose millions of dollars to overdue invoices "
            "and failed payments."
        )
    },
    {
        "id": 2,
        "title": "Problem - Manual Inefficiency",
        "text": (
            "Today, finance teams rely on manual follow-ups. Analysts spend hours digging through spreadsheets, "
            "drafting repetitive emails, and guessing which customer to contact next. "
            "This process is slow, inconsistent, and often strains customer relationships."
        )
    },
    {
        "id": 3,
        "title": "Problem - The Need for Transparent AI",
        "text": (
            "Finance teams do not need a black-box bot blindly sending aggressive collection notices. "
            "They need an intelligent, transparent copilot that prioritizes the ledger, predicts recovery likelihood, "
            "drafts personalized communications, and keeps humans firmly in control of every financial decision."
        )
    },
    {
        "id": 4,
        "title": "Product Overview - RecoverAI",
        "text": (
            "Enter RecoverAI. RecoverAI is built by Soharab Ahamad as an internship project for Track 3: AI Revenue Recovery."
        )
    },
    {
        "id": 5,
        "title": "Product Overview - Dashboard KPIs",
        "text": (
            "Here on the main executive dashboard, RecoverAI delivers immediate financial clarity. "
            "At a single glance, finance leaders see total outstanding debt, total overdue volume, "
            "and our real-time recovery rate."
        )
    },
    {
        "id": 6,
        "title": "Product Overview - 3D Revenue Galaxy",
        "text": (
            "Our 3D Revenue Galaxy visualizes the entire accounts ledger by risk level and dollar volume. "
            "High-risk overdue accounts are highlighted in glowing crimson, while healthy accounts orbit securely. "
            "Below, our recovery velocity metrics track days-to-payment improvements and segment health."
        )
    },
    {
        "id": 7,
        "title": "Product Overview - Safety Principle",
        "text": (
            "Everything is governed by our core principle: AI recommends and explains. Business rules validate. "
            "Humans approve sensitive actions. And the system records everything."
        )
    },
    {
        "id": 8,
        "title": "Live Demo - Queue Prioritization",
        "text": (
            "Let us see RecoverAI in action. Navigating to the Recovery Queue, our system prioritizes overdue invoices "
            "dynamically using composite risk scoring."
        )
    },
    {
        "id": 9,
        "title": "Live Demo - Recommended Invoice",
        "text": (
            "We toggle the Demo Scenario mode and select our recommended demo invoice: invoice INV-2024-024 for customer "
            "Jennifer Lee, representing four thousand eight hundred and fifty dollars overdue by twelve days."
        )
    },
    {
        "id": 10,
        "title": "Live Demo - AI Inference",
        "text": (
            "When we open the invoice detail and click 'Analyze with AI', RecoverAI's neural recovery engine engages in real-time. "
            "Within milliseconds, the AI synthesizes Jennifer's payment history, credit reliability score of eighty-five percent, "
            "and zero dispute history."
        )
    },
    {
        "id": 11,
        "title": "Live Demo - Recommendation & Evidence",
        "text": (
            "The AI computes an eighty-five percent recovery probability, recommends a polite early reminder, and cites exact "
            "evidence from the customer's prior transaction logs. It even authorizes a flexible payment plan option based on corporate policy."
        )
    },
    {
        "id": 12,
        "title": "Approval & Guardrails - Review & Send",
        "text": (
            "Notice that RecoverAI drafts a tailored, respectful reminder message ready for review. "
            "As a finance analyst, I can edit the wording directly. When satisfied, I click 'Approve and Send'. "
            "The confirmation modal logs the dispatch, updates the invoice timeline, and sends the notice through our secure payment gateway."
        )
    },
    {
        "id": 13,
        "title": "Approval & Guardrails - Dispute Blocking",
        "text": (
            "Now, what happens if an invoice has an active dispute? Let us open invoice INV-2024-004 for Acme Corporation."
        )
    },
    {
        "id": 14,
        "title": "Approval & Guardrails - Guardrail Enforcement",
        "text": (
            "Here, our deterministic safety engine takes over. Notice that the 'Approve and Send' button is strictly disabled "
            "with a red guardrail notice: 'Sending reminders is disabled for disputed invoices — Escalate to Human review required.' "
            "RecoverAI prevents embarrassing or legally risky automated collection messages when a customer has an unresolved dispute."
        )
    },
    {
        "id": 15,
        "title": "Technical Architecture",
        "text": (
            "Under the hood, RecoverAI is built with a modern, production-grade full-stack architecture. "
            "The frontend is crafted in React eighteen with TypeScript, Vite, and Three.js for interactive 3D spatial depth. "
            "The backend is powered by Python Flask with SQLAlchemy and a comprehensive REST API, backed by a deterministic business validation engine."
        )
    },
    {
        "id": 16,
        "title": "Audit Trail & Compliance",
        "text": (
            "Crucially, every single action in RecoverAI is logged to our immutable Audit Trail. "
            "Whether an analyst signs in, triggers an AI inference, edits a message, or escalates an account, "
            "the event is recorded with timestamps, user IDs, and cryptographic payload details. "
            "Finance teams can export the entire log to CSV for compliance audits at any time."
        )
    },
    {
        "id": 17,
        "title": "Business Impact",
        "text": (
            "Finally, looking at our Analytics suite, the business impact is undeniable. "
            "RecoverAI cuts days-to-payment by over thirty-five percent, reduces manual follow-up time by eighty percent, "
            "and recovers twenty-four percent more revenue while protecting valuable customer relationships."
        )
    },
    {
        "id": 18,
        "title": "Closing & Credits",
        "text": (
            "RecoverAI proves that artificial intelligence in finance works best when paired with human judgment, "
            "clear explainability, and bulletproof safety guardrails. "
            "Thank you for watching. RecoverAI is built by Soharab Ahamad for Track 3: AI Revenue Recovery."
        )
    }
]


def format_srt_time(seconds: float) -> str:
    """Format float seconds into SRT timestamp HH:MM:SS,mmm"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"


async def generate_edge_tts():
    """Generate professional neural voiceover via edge-tts."""
    import edge_tts
    import tempfile

    print("[TTS] Generating neural voiceover via edge-tts (en-US-ChristopherNeural)...")
    voice = "en-US-ChristopherNeural"
    temp_files = []
    durations = []

    full_text = " ".join([s["text"] for s in SECTIONS])
    communicate = edge_tts.Communicate(full_text, voice, rate="+2%")
    await communicate.save(OUTPUT_AUDIO_MP3)
    print(f"[TTS] Successfully exported master audio: {OUTPUT_AUDIO_MP3}")

    # Generate individual segments to compute exact SRT subtitle timestamps
    srt_entries = []
    current_time = 0.0

    for idx, sec in enumerate(SECTIONS, 1):
        temp_seg = os.path.join(SCRIPT_DIR, f"_temp_seg_{idx}.mp3")
        comm_seg = edge_tts.Communicate(sec["text"], voice, rate="+2%")
        await comm_seg.save(temp_seg)
        
        # Get duration using ffprobe
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", temp_seg
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            dur = float(res.stdout.strip())
        except Exception:
            dur = len(sec["text"].split()) * 0.4

        start_str = format_srt_time(current_time)
        end_str = format_srt_time(current_time + dur)

        srt_entries.append(f"{idx}\n{start_str} --> {end_str}\n{sec['text']}\n")
        current_time += dur + 0.35  # small natural pause between sections
        
        if os.path.exists(temp_seg):
            os.remove(temp_seg)

    # Write SRT
    with open(OUTPUT_SRT, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
    print(f"[TTS] Successfully generated synchronized subtitles: {OUTPUT_SRT}")


def generate_pyttsx3():
    """Fallback offline TTS generation."""
    import pyttsx3
    print("[TTS] Using pyttsx3 fallback...")
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    full_text = " ".join([s["text"] for s in SECTIONS])
    engine.save_to_file(full_text, OUTPUT_AUDIO_WAV)
    engine.runAndWait()
    print(f"[TTS] Saved audio to {OUTPUT_AUDIO_WAV}")


def main():
    os.makedirs(SCRIPT_DIR, exist_ok=True)
    try:
        asyncio.run(generate_edge_tts())
    except Exception as e:
        print(f"[TTS] edge-tts error: {e}. Falling back to pyttsx3...")
        try:
            generate_pyttsx3()
        except Exception as e2:
            print(f"[TTS] Error during fallback: {e2}")


if __name__ == "__main__":
    main()
