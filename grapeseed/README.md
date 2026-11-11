# Grapeseed Webapp – Unit 1

## Cách dùng nhanh (GitHub Pages)

1. Giải nén → chép toàn bộ thư mục `grapeseed` vào repo GitHub.
2. Commit + push.
3. Bật GitHub Pages (Settings → Pages → Deploy from branch `/ (root)` hoặc `/docs`).
4. Đợi 1–2 phút, mở link, nhấn **Ctrl+Shift+R** (hoặc tab ẩn danh).
5. Mở `index.html?check=1` để xem unit thiếu bao nhiêu audio.

## Tạo giọng AI Kokoro (bắt buộc để có audio)

Môi trường tạo app **không tải được model Kokoro** (file ~80MB bị treo), nên `audio/u1.json` hiện **trống**.

Trên máy bạn (khuyến nghị có GPU hoặc máy mạnh):

```bash
cd grapeseed
pip install kokoro soundfile numpy
# Ubuntu: sudo apt install ffmpeg espeak-ng
# macOS:  brew install ffmpeg espeak
python make_audio.py 1
```

Script sẽ sinh `audio/u1.json` (có thể 3–8 MB). Sau đó commit + push lại.

Giọng: **Kokoro `af_heart`** (nữ, ấm), tốc độ 1.0 / 0.7, MP3 24 kHz mono ~40 kbps.

## Cấu trúc

```
grapeseed/
├── index.html
├── units.json
├── manifest.json
├── icon-192.png, icon-512.png, apple-touch-icon.png
├── data/u1.json
├── audio/u1.json          ← chạy make_audio.py để tạo
└── make_audio.py
```

Thêm unit mới = thêm `data/uN.json` + 1 dòng trong `units.json` + chạy lại `make_audio.py N`.
