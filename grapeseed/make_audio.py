#!/usr/bin/env python3
"""
make_audio.py — Sinh file audio/uN.json bằng Kokoro TTS (giọng af_heart)
Chạy trên máy của bạn (cần GPU hoặc CPU khá, khoảng 5–15 phút/unit).

Cài đặt:
  pip install kokoro soundfile numpy
  # cần ffmpeg và espeak-ng
  # Ubuntu: sudo apt install ffmpeg espeak-ng
  # macOS: brew install ffmpeg espeak

Cách chạy (từ thư mục grapeseed):
  python make_audio.py
  # hoặc chỉ 1 unit: python make_audio.py 1
"""

import json
import os
import re
import sys
import tempfile
import subprocess
from pathlib import Path

try:
    from kokoro import KPipeline
    import soundfile as sf
    import numpy as np
except ImportError:
    print("Chưa cài kokoro. Chạy: pip install kokoro soundfile numpy")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
UNITS_FILE = ROOT / "units.json"
DATA_DIR = ROOT / "data"
AUDIO_DIR = ROOT / "audio"
SAMPLE_RATE = 24000

def normalize_key(text: str, for_word: bool = False) -> str:
    """Chuẩn hóa khóa audio theo quy tắc app."""
    if not text:
        return ""
    t = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = re.sub(r"\s+", " ", t).strip()
    if for_word:
        t = t.lower()
    return t

def collect_keys(unit_data: dict) -> dict:
    """Trả về dict {key: text_to_speak}"""
    keys = {}
    # words
    for w in unit_data.get("words", []):
        en = normalize_key(w["en"], for_word=True)
        if en:
            keys[f"w:{en}"] = en
            keys[f"s:{en}"] = en
    # passages lines
    for p in unit_data.get("passages", []):
        for line in (p.get("text") or "").splitlines():
            line = line.strip()
            if line:
                nk = normalize_key(line)
                keys[f"l:{nk}"] = line
    # dialogs
    for d in unit_data.get("dialogs", []):
        for part in ("q", "a"):
            txt = d.get(part, "").strip()
            if txt:
                nk = normalize_key(txt)
                keys[f"l:{nk}"] = txt
    # order
    for sent in unit_data.get("order", []):
        if sent.strip():
            nk = normalize_key(sent)
            keys[f"l:{nk}"] = sent
    # cloze (điền đáp án)
    for c in unit_data.get("cloze", []):
        s = c.get("s", "").replace("___", c.get("a", "")).strip()
        if s:
            nk = normalize_key(s)
            keys[f"l:{nk}"] = s
    # write questions
    for w in unit_data.get("write", []):
        q = w.get("q", "").strip()
        if q:
            nk = normalize_key(q)
            keys[f"l:{nk}"] = q
    return keys

def wav_to_mp3_base64(wav_path: Path) -> str:
    """Chuyển WAV → MP3 24kHz mono ~40kbps rồi base64 data URI."""
    mp3_path = wav_path.with_suffix(".mp3")
    cmd = [
        "ffmpeg", "-y", "-i", str(wav_path),
        "-ar", "24000", "-ac", "1", "-b:a", "40k",
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    import base64
    data = mp3_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    mp3_path.unlink(missing_ok=True)
    return f"data:audio/mpeg;base64,{b64}"

def generate_unit(unit_id: int, pipeline, voice: str = "af_heart"):
    data_path = DATA_DIR / f"u{unit_id}.json"
    audio_path = AUDIO_DIR / f"u{unit_id}.json"
    if not data_path.exists():
        print(f"  Không tìm thấy {data_path}")
        return
    with open(data_path, encoding="utf-8") as f:
        unit = json.load(f)
    keys = collect_keys(unit)
    print(f"  Unit {unit_id}: cần {len(keys)} khóa audio")

    result = {}
    if audio_path.exists():
        try:
            with open(audio_path, encoding="utf-8") as f:
                result = json.load(f)
        except Exception:
            result = {}

    missing = [k for k in keys if k not in result or not result[k].startswith("data:audio")]
    print(f"  Đã có {len(keys) - len(missing)}, còn thiếu {len(missing)}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for i, key in enumerate(missing, 1):
            text = keys[key]
            speed = 0.7 if key.startswith("s:") else 1.0
            print(f"    [{i}/{len(missing)}] {key[:60]}... (speed={speed})")
            try:
                gen = pipeline(text, voice=voice, speed=speed)
                audio = None
                for _, _, a in gen:
                    audio = a
                    break
                if audio is None:
                    print("      → không có audio")
                    continue
                wav_path = tmp / "t.wav"
                sf.write(wav_path, audio, SAMPLE_RATE)
                result[key] = wav_to_mp3_base64(wav_path)
            except Exception as e:
                print(f"      → lỗi: {e}")
                continue

    AUDIO_DIR.mkdir(exist_ok=True)
    with open(audio_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, separators=(",", ":"))
    size_mb = audio_path.stat().st_size / (1024 * 1024)
    print(f"  Đã ghi {audio_path} ({size_mb:.2f} MB), tổng {len(result)} khóa")

def main():
    with open(UNITS_FILE, encoding="utf-8") as f:
        units_meta = json.load(f)
    voice = units_meta.get("voice", {}).get("voice", "af_heart")
    print(f"Giọng: Kokoro / {voice}")
    print("Đang tải model (lần đầu sẽ lâu)...")
    pipeline = KPipeline(lang_code="a")
    print("Model sẵn sàng.\n")

    ids = []
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1:]]
    else:
        ids = [u["id"] for u in units_meta["units"]]

    for uid in ids:
        print(f"=== Unit {uid} ===")
        generate_unit(uid, pipeline, voice=voice)
        print()

    print("Xong! Kiểm tra bằng cách mở index.html?check=1")

if __name__ == "__main__":
    main()
