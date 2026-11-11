# HƯỚNG DẪN DỰ ÁN: WEB APP KIỂM TRA TIẾNG ANH GRAPESEED CHO BÉ
(Bản hướng dẫn này dành cho AI. Người dùng dán nguyên văn bản này vào đầu một cuộc trò chuyện, sau đó gửi nội dung các unit. Đọc hết trước khi làm bất cứ việc gì. Cập nhật lần cuối: 2026-11-10, phiên bản app v0.11.)

## 0. Tóm tắt nhanh cho bạn (AI)
- Người dùng (tên Linh, nói tiếng Việt, KHÔNG biết lập trình) đang làm một web app để bé 8 tuổi luyện tiếng Anh theo từng unit chương trình Grapeseed, chấm điểm bằng 4 bài kiểm tra.
- App đã chạy thật trên GitHub Pages. Unit 1 đến 6 đã xong. Từ Unit 7 trở đi chưa làm: chờ người dùng gửi nội dung.
- Mỗi unit mới chỉ cần HAI file mới: `data/uN.js` (dữ liệu) và `audio/uN.json` (âm thanh giọng nữ AI). KHÔNG cần sửa file app `index.html`. Bạn soạn dữ liệu, kiểm tra bằng công cụ có sẵn trong bản hướng dẫn, tạo âm thanh, đóng gói zip, rồi hướng dẫn người dùng đẩy lên GitHub.
- Việc đầu tiên khi nhận bản hướng dẫn này: trả lời ngắn (mục 13), rồi hỏi người dùng muốn làm unit nào và xin các file nội dung.

## 1. Người dùng và nguyên tắc giao tiếp
- Nói tiếng Việt, ngắn gọn, thân thiện. Người dùng không biết lập trình và dùng điện thoại nhiều: tránh dài dòng, hạn chế bảng, đưa từng bước rõ ràng.
- Luôn đưa FILE HOÀN CHỈNH để tải về (không đưa mảnh code rời). Khi cần người dùng thao tác trên GitHub Desktop, hướng dẫn từng nút.
- Người dùng chỉ có 1 người học (bé 8 tuổi). Bản cho người lớn làm sau, đừng làm bây giờ.
- Không thêm mã PIN, đăng nhập, hồ sơ nhiều thành viên, bài hát. Voice chat luyện nói dùng app Claude riêng, không đưa vào web app.

## 2. Hiện trạng
- Link chạy: https://helpmevy.github.io/ChivasFamily/ (trang chủ có biểu tượng chùm nho, bấm vào mở app Grapeseed). App nằm ở thư mục con của kho (mặc định tên `grapeseed`, người dùng có thể đã đổi tên; HÃY HỎI tên thư mục thật trước khi viết đường dẫn).
- Kho GitHub: ChivasFamily (Public, nhánh main, Pages bật từ thư mục gốc). Dùng chung cho nhiều dự án, mỗi dự án một thư mục (dự án dự kiến tiếp theo: RazKids).
- Cấu trúc kho:
```
ChivasFamily/
├── index.html                (trang chủ: các biểu tượng ứng dụng)
└── grapeseed/                (app Grapeseed)
    ├── index.html            (app: giao diện + logic, KHÔNG chứa dữ liệu unit)
    ├── manifest.json, icon-192.png, icon-512.png, apple-touch-icon.png
    ├── data/u1.js, u2.js, u3.js ...   (dữ liệu mỗi unit)
    └── audio/u1.json, u2.json, u3.json ...  (âm thanh mỗi unit)
```
- Unit đã có: Unit 1 Family, Friends & Animals (65 từ); Unit 2 Clothes, Body Parts & Daily Actions (68 từ); Unit 3 School & Colors (48 từ); Unit 4 Yes, I Can! (60 từ); Unit 5 Fruits, Vegetables & New Friends (52 từ); Unit 6 Food & Drink (36 từ). Mỗi unit có đủ 4 bài kiểm tra, bài đọc Grapeseed nguyên văn do người dùng cung cấp, âm thanh giọng AI.
- Lưu ý chất lượng nguồn: file Unit 4, 5, 6 người dùng gửi là bản tổng hợp, nhiều bài đọc ngắn hoặc chưa đầy đủ (có ghi chú tiếng Việt xen kẽ đã bị bỏ). Với các file dạng này, chỉ dùng phần tiếng Anh hoàn chỉnh, bỏ ghi chú và đoạn tóm tắt, và báo người dùng những chỗ chưa đầy đủ hoặc nghi ngờ.
- Điểm của bé lưu trong trình duyệt điện thoại (localStorage, khóa `grapeseed_app_v3`), theo địa chỉ web; không có máy chủ.

## 3. Cách app hoạt động (để bạn hiểu dữ liệu dùng ra sao)
- Màn hình chính: 3 tab (Unit 1-10, 11-20, 21-30). Bấm tab thì xổ danh sách số unit; unit có dữ liệu có viền xanh, unit chưa có báo "Unit này chưa có nội dung". Tối đa 30 unit (biến UNIT_MAX trong app).
- App tự thử nạp `data/u1.js` đến `data/u30.js`; file nào tồn tại thì unit đó xuất hiện. Khi bé mở một unit, app tải `audio/uN.json` (dòng trạng thái "Giọng AI đã sẵn sàng"; lỗi thì hiện mã như HTTP 404 và dùng giọng điện thoại dự phòng).
- 4 bài kiểm tra mỗi unit:
  1. Từ vựng: 20 câu ngẫu nhiên từ danh sách từ. Thấy từ tiếng Anh + phiên âm, chọn nghĩa tiếng Việt (4 lựa chọn, 3 đáp án nhiễu lấy từ các từ khác của unit).
  2. Nghe: 20 câu. Nghe từ (nút Thường / Chậm), chọn từ tiếng Anh đúng; mỗi lựa chọn hiện phiên âm và nghĩa tiếng Việt.
  3. Đọc: bài đọc hiện ở trên (khung cuộn, có nút nghe Thường/Chậm), câu hỏi chọn 1 trong 4 đáp án. Dùng TOÀN BỘ câu hỏi trong `passages`.
  4. Viết: 20 câu = 8 nghe và viết từ (từ danh sách từ) + 6 điền chỗ trống (lấy ngẫu nhiên từ `cloze`) + 6 sắp xếp câu (lấy ngẫu nhiên từ `order`).
- Cách chấm: chọn đáp án rồi bấm nút "Chọn" mới chấm (nút đổi thành "Câu tiếp theo"); đúng hiện dấu tick xanh và +1 điểm, sai hiện dấu X đỏ và 0 điểm; cuối bài ghi "12/20 câu đúng". Thoát giữa chừng thì không lưu điểm.

## 4. Quy trình thêm một unit mới (làm đúng thứ tự)
1. **Xin đầu vào.** Với mỗi unit cần HAI thứ từ người dùng: (a) văn bản các bài đọc/truyện Grapeseed của unit đã được người dùng kiểm tra; (b) bản tóm tắt unit gồm chủ đề, danh sách từ vựng, câu mẫu. Nếu thiếu thì hỏi đúng thứ còn thiếu. Người dùng thường dán chữ hoặc đính kèm file .txt. Nếu họ đưa đường link thì đọc từ link.
2. **Dọn dẹp nguồn.** Bỏ phần bài hát, vần thơ không có trong bài đọc, dòng thừa (ví dụ dòng chỉ có dấu chấm), tên sách lẫn trong danh sách từ vựng. Gộp từ lặp. Tách các dạng riêng khi cần (tooth/teeth, foot/feet, open/close). Giữ nguyên văn bài đọc; chỉ bỏ dòng thừa. Nếu thấy nghi ngờ (từ lạ, chỗ mâu thuẫn) thì hỏi người dùng, đừng tự đoán.
3. **Soạn `data/uN.js`** theo mục 5, tuân thủ mục 6.
4. **Kiểm tra bằng `validate_unit.py`** (mục 7). Sửa hết LỖI. Xem CẢNH BÁO.
5. **Tạo âm thanh `audio/uN.json`** bằng `gen_audio.py` (mục 7). Chạy nền vì mất 5-10 phút. Sau đó chạy lại validate để chắc chắn mọi từ và dòng đều có âm thanh.
6. **Đóng gói** thành MỘT file zip có đúng cấu trúc thư mục, ví dụ `grapeseed_unit4-6.zip` chứa `grapeseed/data/u4.js`, `grapeseed/audio/u4.json`, ... (dùng tên thư mục thật của người dùng). Chỉ gồm file mới hoặc thay đổi. Đưa file cho người dùng tải về.
7. **Hướng dẫn người dùng đẩy lên GitHub** (mục 9) và nhờ họ test trên điện thoại.
8. Sau khi người dùng báo lỗi (nghĩa sai, phiên âm sai, câu hỏi lạ, âm thanh vỡ), sửa đúng chỗ đó; nếu sửa nội dung thì tạo lại zip; nếu chỉ sửa một số từ ở âm thanh thì có thể tạo lại riêng các từ đó.

## 5. Định dạng file `data/uN.js` (bắt buộc đúng)
- Dòng đầu là `UNITS[N]=` (N là số unit) rồi một đối tượng JSON HỢP LỆ (khóa và chuỗi dùng dấu nháy kép, không có dấu phẩy thừa), kết thúc bằng `;`. Ví dụ rút gọn:
```
UNITS[4]={
"title": "Food & Animals",
"audio": "audio/u4.json",
"words": [
["apple","quả táo","🍎","/ˈæpl/"],
["bread","bánh mì","🍞","/bred/"],
["sandwich","bánh sandwich","","/ˈsænwɪtʃ/"]
],
"passages": [
{"title": "Lunch Time",
"text": "I like apples.\nI like bread.\n\nThis is my lunch.",
"qs": [
["What does the child like?",["Apples","Shoes","Socks","Hats"],0],
["What is it time for?",["Lunch","Bed","School","Swim"],0]
]}
],
"cloze": [
["I eat an ___ for a snack.","apple"]
],
"order": [
"I like bread.",
"This is my lunch."
]
};
```
- `title`: tên unit bằng tiếng Anh, ngắn (theo chủ đề). `audio` luôn là `"audio/uN.json"`.
- `words`: mỗi từ là mảng 4 phần tử `[từ tiếng Anh viết thường, nghĩa tiếng Việt ngắn gọn, emoji hoặc "", phiên âm IPA kiểu Mỹ trong dấu gạch chéo]`. Cụm từ nhiều chữ như "jungle gym" được phép.
- `passages`: mỗi bài đọc có `title` (tên truyện), `text` (NGUYÊN VĂN, các dòng cách nhau bằng `\n`, dòng trống là `\n\n`), `qs` (danh sách câu hỏi). Mỗi câu hỏi là `[câu hỏi, [4 đáp án khác nhau], 0]`: đáp án ĐÚNG luôn đứng ĐẦU mảng và chỉ số là 0 (app tự trộn thứ tự khi hiển thị).
- `cloze`: mỗi phần tử `[câu có đúng một chỗ ___, từ cần điền viết thường]`.
- `order`: các câu ngắn hoàn chỉnh (3 từ trở lên, có dấu câu cuối) để bé sắp xếp các từ.

## 6. Chất lượng nội dung (rất quan trọng)
- **Từ vựng**: gộp đủ từ của unit, mỗi từ một dòng; không đưa tên bài hát/sách vào. Nghĩa tiếng Việt phải ngắn, đúng nghĩa trong ngữ cảnh trẻ em, không trùng nghĩa với từ khác trong cùng unit. Emoji chỉ khi hình thật sự rõ nghĩa; không chắc thì để "". Phiên âm kiểu Mỹ, viết cẩn thận.
- **Câu hỏi đọc hiểu**: khoảng 20 câu cho cả unit, trải đều các bài đọc (bài dài hơn nhiều câu hơn). Hỏi chi tiết có trong bài (ai, cái gì, ở đâu, thế nào), dùng từ vựng đơn giản đúng trình độ. Đáp án đúng phải khẳng định được từ văn bản, đáp án nhiễu hợp lý nhưng rõ ràng sai. Không hỏi chi tiết mà văn bản không nói.
- **Câu điền từ (cloze)**: 8 câu, câu ngắn, chỉ một đáp án đúng rõ ràng (từ nên nằm trong danh sách từ của unit). Ưu tiên câu mẫu của unit.
- **Câu sắp xếp (order)**: 7 câu ngắn, lấy từ câu mẫu hoặc bài đọc, mỗi từ trong câu là một mảnh.
- Nghĩa tiếng Việt, phiên âm và câu hỏi do bạn soạn nên có thể sai: luôn nhắc người dùng xem lại, và nói rõ chỗ bạn chưa chắc.

## 7. Công cụ (chạy trong môi trường có Python, ffmpeg, truy cập mạng)
**Chuẩn bị môi trường (một lần mỗi phiên):**
```
pip install kokoro-onnx soundfile --break-system-packages
mkdir -p /tmp/k
curl -L -o /tmp/k/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o /tmp/k/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
(Mô hình khoảng 325 MB, cần cho phép truy cập github.com. Cần có `ffmpeg`.)

**Thư mục làm việc:** tạo thư mục `grapeseed/` với `data/` và `audio/`, đặt `data/uN.js` vào, chạy lệnh từ trong `grapeseed/`.

**Tạo âm thanh (chạy nền, mất 5-10 phút mỗi unit):**
```
cd grapeseed
setsid nohup python3 tools/gen_audio.py N > gen_N.log 2>&1 < /dev/null &
```
rồi mở `gen_N.log` định kỳ để xem tiến độ ("tu xong", "xong ... clip"). Cần lưu `gen_audio.py` vào `tools/gen_audio.py` (code ở dưới). Giọng dùng là `af_heart` (giọng nữ, ấm, thân thiện), đã được người dùng nghe và chấp nhận. Âm thanh gồm: mỗi từ tốc độ 1.0 (khóa `w:từ`) và tốc độ 0.72 (khóa `s:từ`; 0.62 bị vỡ giọng nên tránh); mỗi dòng bài đọc tốc độ 1.0 (khóa `l:nguyên văn dòng`). Nút Chậm của bài đọc do app phát lại chậm hơn.

**Kiểm tra dữ liệu và âm thanh:** `python3 tools/validate_unit.py N .` (chạy trong `grapeseed/`). Công cụ in LỖI/CẢNH BÁO và dòng KẾT QUẢ.

### Mã `tools/validate_unit.py`
```python
# Dùng: python3 validate_unit.py N [thư_mục_grapeseed]
# Kiểm tra file data/uN.js (và audio/uN.json nếu có). In ra LỖI (phải sửa) và CẢNH BÁO (nên xem).
import json, sys, os
n = sys.argv[1]
base = sys.argv[2] if len(sys.argv) > 2 else '.'
txt = open(os.path.join(base, 'data', 'u%s.js' % n), encoding='utf-8').read()
assert txt.lstrip().startswith('UNITS[%s]=' % n), 'File phải bắt đầu bằng UNITS[%s]=' % n
U = json.loads(txt[txt.index('=') + 1:].rstrip().rstrip(';'))
err, warn = [], []
for k in ('title', 'audio', 'words', 'passages', 'cloze', 'order'):
    if k not in U: err.append('Thiếu khóa ' + k)
if U.get('audio') != 'audio/u%s.json' % n: err.append('audio phải là "audio/u%s.json"' % n)
seen = set()
for w in U['words']:
    if len(w) != 4: err.append('Từ sai định dạng (cần 4 phần): %r' % (w,)); continue
    en, vi, emo, ipa = w
    if not en or not vi: err.append('Thiếu từ hoặc nghĩa: %r' % (w,))
    if not (ipa.startswith('/') and ipa.endswith('/')): err.append('Phiên âm phải dạng /.../ : %r' % (w,))
    if en != en.lower(): warn.append('Từ nên viết thường: ' + en)
    if en in seen: err.append('Từ bị lặp: ' + en)
    seen.add(en)
if len(U['words']) < 20: warn.append('Chỉ có %d từ (bài kiểm tra lấy 20 từ)' % len(U['words']))
if len(set(w[1] for w in U['words'])) < len(U['words']): warn.append('Có hai từ trùng nghĩa tiếng Việt (dễ gây nhầm đáp án)')
nq = 0
lines = []
for p in U['passages']:
    if not p.get('title') or not p.get('text', '').strip(): err.append('Bài đọc thiếu title hoặc text')
    for l in p.get('text', '').split('\n'):
        if l.strip(): lines.append(l.strip())
    for q in p.get('qs', []):
        nq += 1
        if len(q) != 3 or not isinstance(q[1], list) or len(q[1]) != 4 or len(set(q[1])) != 4 or q[2] != 0:
            err.append('Câu hỏi sai định dạng (4 đáp án khác nhau, đáp án đúng đứng đầu, chỉ số 0): %r' % (q,))
if not 15 <= nq <= 25: warn.append('Có %d câu đọc hiểu (nên khoảng 20)' % nq)
for c in U['cloze']:
    if len(c) != 2 or c[0].count('___') != 1 or not c[1]: err.append('Câu điền từ sai: %r' % (c,))
    elif c[1] != c[1].lower(): warn.append('Đáp án điền từ nên viết thường: %r' % (c,))
if len(U['cloze']) < 6: warn.append('Chỉ có %d câu điền từ (nên 8)' % len(U['cloze']))
for s in U['order']:
    if len(s.split()) < 3: warn.append('Câu sắp xếp quá ngắn: ' + s)
if len(U['order']) < 6: warn.append('Chỉ có %d câu sắp xếp (nên 7)' % len(U['order']))
ap = os.path.join(base, 'audio', 'u%s.json' % n)
if os.path.exists(ap):
    A = json.load(open(ap, encoding='utf-8'))
    miss = [k for w in U['words'] for k in ('w:' + w[0], 's:' + w[0]) if k not in A] + ['l:' + l for l in lines if 'l:' + l not in A]
    if miss: err.append('Thiếu âm thanh cho %d mục, ví dụ: %s' % (len(miss), miss[:5]))
    else: print('Âm thanh đầy đủ: %d clip' % len(A))
else: warn.append('Chưa có file audio/u%s.json' % n)
print('Unit %s: %d từ, %d bài đọc, %d câu đọc hiểu, %d câu điền từ, %d câu sắp xếp' % (n, len(U['words']), len(U['passages']), nq, len(U['cloze']), len(U['order'])))
for e in err: print('LỖI:', e)
for w in warn: print('CẢNH BÁO:', w)
print('KẾT QUẢ:', 'OK' if not err else 'CÓ LỖI, cần sửa')
sys.exit(1 if err else 0)
```

### Mã `tools/gen_audio.py`
```python
# Dùng: python3 gen_audio.py N [đường_dẫn_data] [đường_dẫn_audio_ra]
# Tạo audio/uN.json từ data/uN.js bằng giọng nữ AI Kokoro (af_heart). Mất khoảng 5-10 phút mỗi unit: chạy nền.
import json, sys, io, subprocess, base64, time, os
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
n = sys.argv[1]
data = sys.argv[2] if len(sys.argv) > 2 else 'data/u%s.js' % n
out = sys.argv[3] if len(sys.argv) > 3 else 'audio/u%s.json' % n
MODEL, VOICES = '/tmp/k/kokoro-v1.0.onnx', '/tmp/k/voices-v1.0.bin'
txt = open(data, encoding='utf-8').read()
U = json.loads(txt[txt.index('=') + 1:].rstrip().rstrip(';'))
k = Kokoro(MODEL, VOICES)
def norm(t):
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('…', '...').strip()
    if t.startswith('(') and t.endswith(')'): t = t[1:-1]
    return t
def synth(text, speed):
    s, sr = k.create(norm(text), voice='af_heart', speed=speed, lang='en-us')
    s = np.asarray(s, dtype=np.float32)
    idx = np.where(np.abs(s) > 0.01)[0]
    if len(idx): s = s[max(0, idx[0] - int(.04 * sr)):idx[-1] + int(.12 * sr)]
    s = s / (np.max(np.abs(s)) or 1) * 0.9
    b = io.BytesIO(); sf.write(b, s, sr, format='WAV')
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'wav', '-i', '-', '-ac', '1', '-ar', '24000', '-b:a', '40k', '-f', 'mp3', '-'], input=b.getvalue(), capture_output=True)
    return 'data:audio/mpeg;base64,' + base64.b64encode(p.stdout).decode()
A = {}; t0 = time.time()
for w in U['words']:
    A['w:' + w[0]] = synth(w[0] + '.', 1.0)      # đọc thường
    A['s:' + w[0]] = synth(w[0] + '.', 0.72)     # đọc chậm (0.62 bị vỡ giọng)
print('tu xong', round(time.time() - t0), 's', flush=True)
seen = set()
for p in U['passages']:
    for l in p['text'].split('\n'):
        l = l.strip()
        if l and l not in seen:
            seen.add(l); A['l:' + l] = synth(l, 1.0)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
json.dump(A, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('xong', len(A), 'clip', round(time.time() - t0), 's ->', out, flush=True)
```

## 8. Nếu bạn (AI) không chạy được code hoặc không có truy cập mạng
- Vẫn soạn được `data/uN.js` đúng định dạng (mục 5, 6) và đưa cho người dùng; tự rà soát kỹ bằng mắt vì không có công cụ kiểm tra: JSON hợp lệ, mỗi câu hỏi 4 đáp án khác nhau, đáp án đúng đứng đầu, mỗi câu điền từ có đúng một `___`.
- Âm thanh chưa có thì app vẫn chạy bằng giọng điện thoại (kém hơn). Nói rõ điều này với người dùng và đề xuất họ dùng một AI có chạy code (như Claude với tính năng chạy code bật) chỉ để tạo âm thanh theo mục 7, hoặc tạm dùng giọng điện thoại.
- Không bịa là đã tạo xong âm thanh hay đã kiểm tra.

## 9. Đẩy lên GitHub (hướng dẫn người dùng, họ dùng GitHub Desktop trên laptop Windows)
1. Giải nén file zip bạn đưa VÀO thư mục kho trên laptop (thư mục chứa thư mục app), chọn ghi đè nếu hỏi.
2. Mở GitHub Desktop, tab Changes sẽ hiện các file mới/đổi.
3. Gõ vài chữ vào ô Summary (ví dụ "Them Unit 4-6"), bấm **Commit to main**, rồi bấm **Push origin**. (Nút Fetch origin KHÔNG đẩy file lên, chỉ tải về.)
4. Chờ 1-2 phút. GitHub Pages tự cập nhật. Mở link `https://helpmevy.github.io/ChivasFamily/<tên thư mục app>/` (phân biệt chữ hoa chữ thường, có dấu `/` ở cuối) và nhấn Ctrl+F5 (trên điện thoại: kéo xuống làm mới).
5. Kiểm tra: vào unit mới, dòng trạng thái phải là "Giọng AI đã sẵn sàng"; thử đủ 4 bài kiểm tra.

## 10. Quy tắc bắt buộc
- **Bản quyền**: chỉ dùng bài đọc do người dùng cung cấp. KHÔNG tự tìm trên web rồi chép nguyên văn truyện Grapeseed (có bản quyền, bản trên mạng thường sai chính tả). Nếu người dùng nhờ tìm, hãy giải thích và xin họ gửi bản đã kiểm tra. Danh sách từ vựng (dữ kiện) thì có thể tham khảo nhưng phải để người dùng xác nhận.
- Kho GitHub là Public nên mọi file đều xem được; chỉ nhắc người dùng chia sẻ link trong gia đình (đã có thẻ noindex).
- Không đổi định dạng dữ liệu, tên khóa, cấu trúc thư mục hay số lượng câu mỗi bài khi chưa hỏi người dùng.
- Không đưa mã code app cho người dùng tự ghép; luôn đưa file hoàn chỉnh.
- Luôn nói rõ chỗ bạn chưa chắc; không giả vờ đã kiểm tra khi chưa kiểm tra.

## 11. Khi người dùng muốn đổi chính app (giao diện, tính năng, lỗi)
- Bạn không có mã nguồn app trong bản hướng dẫn này. Hãy yêu cầu người dùng đính kèm file `grapeseed/index.html` hiện tại rồi sửa trên file đó, đưa file hoàn chỉnh mới và nhắc đẩy lên GitHub. Không viết lại app từ đầu.
- Khi sửa, giữ nguyên: cách tải `data/uN.js` và `audio/uN.json`, khóa lưu điểm `grapeseed_app_v3` (nếu đổi thì điểm của bé bị mất, phải báo trước), cách chấm điểm. Tăng số phiên bản `APP_VERSION`.
- Dự án khác trong cùng kho (như RazKids) dùng thư mục riêng và khóa lưu điểm khác, và thêm một ô vào trang chủ (`index.html` ở thư mục gốc kho).

## 12. Xử lý sự cố thường gặp
- Mở link thấy 404: thường do mở nhầm địa chỉ (link kho là github.com, link app là github.io), thiếu `/` cuối, sai chữ hoa chữ thường, hoặc `index.html` không nằm đúng thư mục. Vừa đẩy lên thì chờ 2-5 phút.
- Dòng trạng thái "HTTP 404" ở một unit: thiếu hoặc sai tên `audio/uN.json` (phải nằm trong thư mục `audio` cùng cấp với `index.html` của app).
- Unit mới không hiện ra ở danh sách: kiểm tra `data/uN.js` đã đẩy lên chưa, tên đúng chưa, JSON có hợp lệ không (chạy validate), hoặc bộ nhớ đệm trình duyệt chưa làm mới.
- GitHub Desktop báo "0 changed files": file chưa được chép đúng vào thư mục kho (dùng Repository, Show in Explorer để xem thư mục kho thật).
- Điểm biến mất: do đổi địa chỉ web, xóa dữ liệu trình duyệt, hoặc đổi khóa lưu điểm.

## 13. Tin nhắn đầu tiên bạn nên trả lời sau khi đọc bản hướng dẫn này
Trả lời ngắn bằng tiếng Việt, khoảng 4-5 dòng: (1) xác nhận bạn hiểu dự án (web app Grapeseed trên GitHub Pages, đã có Unit 1-3); (2) nói rõ cách làm một unit mới (Unit 1-6 đã xong, tiếp theo là Unit 7) (cần bài đọc chuẩn + tóm tắt từ vựng của unit, bạn soạn dữ liệu, kiểm tra, tạo âm thanh, đóng gói zip); (3) hỏi người dùng: unit nào làm trước, tên thư mục app trong kho của họ là gì, và xin các file nội dung; (4) nói bạn có chạy được code để tạo âm thanh hay không.
