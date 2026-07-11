#!/usr/bin/env python3
"""
MIST Meeting Transcriber
Run this on your Mac: python3 transcribe_mist.py
Requires: pip install openai-whisper
"""

import whisper
import sys
import os

AUDIO_FILE = os.path.expanduser("~/Downloads/Final_MIST_Meeting.m4a")

if not os.path.exists(AUDIO_FILE):
    # Try current directory
    AUDIO_FILE = "Final_MIST_Meeting.m4a"
    if not os.path.exists(AUDIO_FILE):
        print("ERROR: Could not find Final_MIST_Meeting.m4a")
        print("Put it in ~/Downloads/ or the same folder as this script")
        sys.exit(1)

print(f"Loading Whisper (small.en model - best quality/speed tradeoff)...")
print("First run will download ~500MB model, subsequent runs are instant.\n")

model = whisper.load_model("small.en")

print(f"Transcribing {AUDIO_FILE} ...")
print("This will take ~5-10 minutes for a 60-min recording.\n")

result = model.transcribe(
    AUDIO_FILE,
    language="en",
    verbose=True,
    initial_prompt="This is a meeting recording. Multiple speakers are present."
)

# Save full transcript
out_txt = "MIST_Meeting_transcript.txt"
with open(out_txt, "w") as f:
    f.write(result["text"])

print(f"\n✅ Transcript saved to: {out_txt}")
print(f"   Length: {len(result['text'])} characters\n")

# Also save with timestamps
out_ts = "MIST_Meeting_transcript_timestamped.txt"
with open(out_ts, "w") as f:
    for seg in result["segments"]:
        mins = int(seg["start"]) // 60
        secs = int(seg["start"]) % 60
        f.write(f"[{mins:02d}:{secs:02d}] {seg['text'].strip()}\n")

print(f"✅ Timestamped transcript saved to: {out_ts}")
print("\nPaste the contents of MIST_Meeting_transcript.txt back into Claude for summarization!")
