# RecoverAI — Demo Video Production Suite
**Project:** RecoverAI — Intelligent Invoice and Payment Recovery Assistant  
**Project Owner:** Soharab Ahamad  
**Track:** Track 3: AI Revenue Recovery  

This directory contains the automated pipeline and assets for generating the 5-minute internship pitch video for RecoverAI, complete with 1080p screen recording, neural TTS voiceover, and synchronized burned-in subtitles.

---

## 📁 Directory Structure & Deliverables

| File | Purpose |
|---|---|
| [`demo_video_script.md`](../demo_video_script.md) | Full 5-minute timed script with presenter cues and narration. |
| [`demo_voiceover.mp3`](./demo_voiceover.mp3) | High-fidelity Microsoft Neural TTS voiceover (`en-US-ChristopherNeural`). |
| [`recoverai_demo_subtitles.srt`](./recoverai_demo_subtitles.srt) | Synchronized subtitle transcript with microsecond timestamps. |
| [`screen_raw.mp4`](./screen_raw.mp4) | High-definition (1920x1080) browser recording. |
| [`recoverai_demo_with_audio.mp4`](./recoverai_demo_with_audio.mp4) | Composite video synchronized with voiceover narration. |
| [`recoverai_demo_final.mp4`](./recoverai_demo_final.mp4) | **Final Pitch Video** with burned-in subtitles and crisp audio. |
| [`generate_audio.py`](./generate_audio.py) | Audio generator (supports `edge-tts` & `pyttsx3` fallback). |
| [`record_and_produce.py`](./record_and_produce.py) | End-to-end recording and video production automation script. |
| [`manual_recording_guide.md`](./manual_recording_guide.md) | Step-by-step instructions for manual video recording with OBS / Loom. |

---

## 🚀 How to Re-Run Video Generation

### Step 1: Ensure RecoverAI is Running
```bash
python run_server.py
```
*(Confirms `http://localhost:5173` is active)*

### Step 2: Generate Audio & Subtitles
```bash
python demo_video/generate_audio.py
```

### Step 3: Record Screen & Produce Final Video
```bash
python demo_video/record_and_produce.py
```

---

## 🎙️ Replacing the Voiceover with a Human Recording

If Soharab Ahamad wishes to record his own human voiceover:
1. Open [`demo_video_script.md`](../demo_video_script.md).
2. Record your voice using a microphone in Audacity, OBS, or Voice Recorder, speaking along with the timed sections.
3. Save your audio file as `demo_video/demo_voiceover.mp3` (replacing the TTS file).
4. Run:
   ```bash
   python demo_video/record_and_produce.py
   ```
   FFmpeg will automatically remux the video with your new vocal track and synchronize the subtitles.

---

## ⚙️ Adjusting Subtitles

Subtitles are stored in standard SRT format in [`recoverai_demo_subtitles.srt`](./recoverai_demo_subtitles.srt). You can edit any line or timestamp directly with any text editor or Subtitle Edit.

To re-burn the edited subtitles into the video:
```bash
ffmpeg -y -i recoverai_demo_with_audio.mp4 -vf "subtitles=recoverai_demo_subtitles.srt:force_style='FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,MarginV=25'" -c:a copy recoverai_demo_final.mp4
```

---

## 🏆 Project Ownership & Credits

- **Built By:** Soharab Ahamad
- **Application:** RecoverAI
- **Track:** Track 3 AI Revenue Recovery
- **All rights reserved.**
