# PROMPT 1: TẠO WEBAPP GRAPESEED TỪ ĐẦU (TỪ FILE PDF CÁC UNIT)

(Người dùng dán nguyên văn nội dung này cho AI và đính kèm file PDF của các unit cần làm. Không cần file cũ nào khác.)

---

## 0. Vai trò và bối cảnh

Bạn đóng hai vai: **lập trình viên web** và **giáo viên tiếng Anh cho trẻ em**.

- Người dùng **không biết code**. Trả lời bằng **tiếng Việt**, ngắn gọn, hướng dẫn từng bước đơn giản.
- Người học là **bé 8 tuổi** học chương trình **GrapeSEED**, đã có nền tảng. Dạng câu hỏi ở mức **Cambridge Movers (A1)**, không phải mức Starters.
- Sản phẩm là **webapp tĩnh** (HTML/JS thuần), đăng lên **GitHub Pages** bằng cách kéo file vào thư mục repo rồi push.
- Nhiệm vụ: **tự đọc các file PDF unit người dùng đính kèm, tự lấy dữ liệu, rồi dựng app và âm thanh** từ đầu.
- Mục tiêu dài hạn: về sau thêm unit mới chỉ cần thêm file, không sửa `index.html`, không làm lại unit cũ.
- Nguồn nội dung duy nhất là **PDF người dùng đưa**. Không tự bịa nội dung unit, không lấy từ internet.
- Nội dung PDF là tài liệu có bản quyền dùng cho việc học của gia đình: chỉ lấy **chữ**, không đưa hình ảnh/trang sách vào app.

---

## 1. Việc cần làm (tóm tắt)

1. Đọc từng PDF → trích dữ liệu → tạo `data/uN.json` (mục 4).
2. Sinh âm thanh bằng **Kokoro, giọng nữ `af_heart`** → `audio/uN.json` (mục 5).
3. Viết `index.html` chung + `units.json` + `manifest.json` + icon (mục 2, 3, 6).
4. Kiểm tra (mục 8) rồi bàn giao một **file ZIP** (mục 9).

---

## 2. Kiến trúc bắt buộc

```
grapeseed/
├── index.html        ← khung app CỐ ĐỊNH, không chứa dữ liệu unit
├── manifest.json     ← cài như app trên điện thoại
├── icon-192.png, icon-512.png, apple-touch-icon.png   ← icon đơn giản bạn tự tạo
├── units.json        ← danh sách unit + cài đặt giọng đọc (file NHỎ)
├── data/u1.json, u2.json, ...    ← nội dung từng unit
└── audio/u1.json, u2.json, ...   ← âm thanh từng unit
```

- `index.html` khi chạy `fetch("units.json?v=<version>")` rồi vẽ danh sách unit; khi mở một unit mới tải `data/uN.json` và `audio/uN.json` (kèm `?v=<rev>` để không bị kẹt cache).
- **Không service worker. Không thư viện/CDN ngoài.** Font: Nunito (Google Fonts) kèm font dự phòng hệ thống.
- Mọi đường dẫn **tương đối** (không bắt đầu bằng `/`), vì chạy trong thư mục con của GitHub Pages.
- Giao diện **tiếng Việt**, ưu tiên điện thoại, nút lớn, chế độ sáng/tối theo hệ thống (`prefers-color-scheme`).
- Lưu tiến độ trong `localStorage`, luôn bọc `try/catch`, và app vẫn chạy bình thường khi không lưu được.
- `manifest.json`: tên "Grapeseed", `display: standalone`, `start_url: "./"`, `scope: "./"`, `theme_color #2F6BFF`, `background_color #F2F7FF`, icon 192 và 512.

---

## 3. Định dạng dữ liệu

### 3.1 `units.json`

```json
{
  "version": "2026-11-12.1",
  "voice": { "engine": "Kokoro", "voice": "af_heart", "lang_code": "a",
             "speed_normal": 1.0, "speed_slow": 0.7,
             "format": "mp3, 24000 Hz, mono, 40 kbps" },
  "units": [
    { "id": 6, "title": "Food, Drink & Helping Others", "data": "data/u6.json", "audio": "audio/u6.json", "rev": 1 }
  ]
}
```
Thêm unit = thêm một dòng. Sửa một unit = tăng `rev` của unit đó và `version`. `title` tạo từ chủ đề chính của unit trong PDF.

### 3.2 `data/uN.json`

```json
{
  "id": 6,
  "title": "Food, Drink & Helping Others",
  "phonogram": { "focus": ["i","j","p"], "review": ["a","b","c"] },
  "words": [
    { "en": "cookie", "vi": "bánh quy", "emoji": "🍪", "ipa": "/ˈkʊki/", "cat": "food" }
  ],
  "passages": [
    { "title": "Sad Sam", "type": "story", "src": "PDF tr.103",
      "text": "Dòng 1.\nDòng 2.\n\nĐoạn 2...",
      "qs": [ { "q": "What did Sam eat before breakfast?",
                "options": ["Ten cookies","Five donuts","Ice cream","Cake and chips"], "answer": 0 } ] }
  ],
  "dialogs": [ { "q": "Do you want some juice?", "a": "Yes, I do." } ],
  "riddles": [ { "clue": "You drink it. It is white.", "answer": "milk" } ],
  "cloze":   [ { "s": "Sam ate ten ___ before breakfast.", "a": "cookies" } ],
  "order":   [ "I do not want to eat breakfast." ],
  "write":   [ { "q": "What do you want?", "model": "I want some juice." } ]
}
```

Quy ước:
- `words[].en`: dạng từ điển, viết thường (ví dụ `egg`, `pancake`). Từ ghép dạng `a/b` trong PDF (empty/full, fat/thin, hard/soft, on/off, before/after, breakfast/lunch/dinner) **tách thành từng từ riêng**. Ngày trong tuần viết hoa chữ đầu theo chuẩn nhưng khóa audio vẫn chuẩn hóa (mục 5).
- `vi`: nghĩa tiếng Việt ngắn, đúng nghĩa trong chủ đề, bạn tự viết (PDF không có).
- `ipa`: phiên âm IPA tiếng Anh Mỹ, bạn tự viết, có dấu `/ /`.
- `emoji`: chỉ điền khi emoji **thật sự mô tả đúng từ**; nếu không chắc để rỗng `""`. Từ không có emoji **không được dùng trong câu hỏi chọn hình**.
- `cat`: nhóm nghĩa (food, drink, animal, family, body, action, clothes, feeling, time, place, thing...) để tạo đáp án nhiễu cùng nhóm.
- `passages`: gồm **các bài đọc có văn bản đầy đủ trong PDF** (Story, Story Dictionary, và Poem / Big Book / Chant / Song nếu PDF có đủ lời), mỗi bài có `type` (story, storydict, poem, bigbook, chant, song) và `src` (số trang PDF). Văn bản **đúng từng chữ như PDF**, giữ dấu câu và dấu nháy cong (’ “ ”). Mỗi câu/dòng một hàng, đoạn cách nhau một dòng trống.
- `qs` (câu hỏi đọc hiểu): 3–6 câu mỗi bài, bạn soạn từ **nội dung bài**, 4 đáp án, đáp án sai hợp lý. `answer` là vị trí đáp án đúng; **app tự xáo trộn** khi hiển thị.
- `dialogs`: các cặp hỏi–đáp lấy từ mẫu câu/chant/bài học trong PDF (ví dụ "Do you want some orange juice?" / "Yes, I do.").
- `riddles`: câu đố định nghĩa **bằng tiếng Anh đơn giản** cho các từ cụ thể (3–8 câu), bạn soạn.
- `cloze`, `order`, `write`: soạn từ câu có trong bài/mẫu câu của unit. `write[].model` là đáp án mẫu để bố mẹ đối chiếu.
- Nếu unit không đủ dữ liệu cho một trường, để mảng rỗng. App phải **tự bỏ qua** phần test thiếu dữ liệu, không báo lỗi.

---

## 4. Cách đọc PDF GrapeSEED (Teacher Manual)

Cấu trúc thường gặp (kiểm tra lại với PDF thực tế, vì mỗi unit có thể hơi khác):

- Phần đầu (khoảng 60 trang) là hướng dẫn chung của chương trình: **bỏ qua**.
- **"Unit N Overview" → "Vocabulary Learning Objectives":** danh sách từ vựng của unit (cạnh đó là "Phonograms: Focus / Review"). Đây là **nguồn từ vựng chính**.
- Trang kế tiếp **"Foundational Skills → Phonics and Word Recognition → Recognize words using picture clues":** danh sách từ vựng dạng dòng. **Đối chiếu** hai danh sách này; lấy hợp của hai danh sách; báo cáo chỗ lệch.
- **Cẩn thận:** các trang **"A Look Back at Unit N-1"** và **"A Look Ahead to Unit N+1"** là từ vựng của **unit khác**. **Không lấy.**
- Mục lục **"Teaching Tools for Unit N"** liệt kê các hoạt động: Chant, Action Activity, Shared Reading Poem, Shared Reading Big Book, Story, Story Dictionary, Song... kèm số trang. Dùng làm bản đồ để tìm văn bản bài đọc.
- Trang bài đọc (Story, Story Dictionary) thường có **mỗi dòng chữ xuất hiện hai lần** (cỡ lớn và cỡ nhỏ) và lẫn nhiều rác: tiêu đề trang (`Unit N - Story "..."`), `© GrapeSEED Media Limited`, tên file `.indd`, ngày giờ, số trang, từ vựng ghi ở lề, khung **Learning Objectives / Quick Checks / Pronunciation Focus** (đó là hướng dẫn cho giáo viên, **không phải nội dung bài**). Phải **khử trùng lặp và lọc rác**, giữ đúng thứ tự câu.
- Nếu văn bản trích ra bị lộn thứ tự hoặc còn nghi ngờ: **chuyển trang đó thành ảnh để đọc trực tiếp** rồi đối chiếu. Với mỗi bài đọc, ít nhất kiểm tra bằng mắt một trang nếu công cụ cho phép.
- Số unit lấy từ tiêu đề PDF hoặc tên file (ví dụ `U06` → unit 6). Nếu không xác định được, hỏi người dùng.
- Nhiều PDF = nhiều unit: xử lý **từng unit độc lập**.

---

## 5. Âm thanh (giọng đọc phải thống nhất cho mọi unit)

### 5.1 Giọng và định dạng
- **Kokoro TTS** (GitHub `hexgrad/kokoro`, mô hình `hexgrad/Kokoro-82M`), giọng nữ ấm áp **`af_heart`**, `lang_code="a"` (tiếng Anh Mỹ).
- Tốc độ: `speed=1.0` cho `w:` và `l:`; `speed=0.7` cho `s:`.
- Xuất **MP3, 24000 Hz, mono, khoảng 40 kbps** (WAV → MP3 bằng `ffmpeg`), mã hóa base64 thành `data:audio/mpeg;base64,...`.
- Cài đặt thường dùng: `pip install kokoro soundfile numpy`, cần thêm `ffmpeg` và `espeak-ng`.
- **Không đổi giọng, đổi engine hay dùng giọng khác thay thế một cách âm thầm.**
- Làm bằng script, lưu thẳng ra file. **Không in base64 ra khung chat.**

### 5.2 `audio/uN.json`
Một object phẳng, khóa → chuỗi `data:audio/mpeg;base64,...`:
- `w:<từ>`: đọc từ, tốc độ thường (từ viết thường, bỏ khoảng trắng hai đầu, ví dụ `w:ice cream`).
- `s:<từ>`: đọc từ, tốc độ **chậm**.
- `l:<câu>`: đọc cả câu/dòng, **đúng từng ký tự** với văn bản trong `data/uN.json`.

**Chuẩn hóa khóa (bắt buộc ở cả app và script):** khi tạo và khi tra khóa, đều: đổi `’ ‘` thành `'`, đổi `“ ”` thành `"`, gộp nhiều khoảng trắng thành một, bỏ khoảng trắng hai đầu, và với `w:`/`s:` thì đổi thành chữ thường.

**Quy tắc phủ âm thanh:** mọi văn bản app có thể đọc thành tiếng đều phải có khóa:
- mỗi `words[].en` → `w:` và `s:`;
- mỗi dòng của `passages[].text` (bỏ dòng trống) → `l:`;
- mỗi `dialogs[].q` và `dialogs[].a` → `l:`;
- mỗi câu của `order[]` → `l:`;
- mỗi `cloze[].s` với `___` thay bằng đáp án → `l:`;
- mỗi `write[].q` → `l:`.

### 5.3 Nếu không chạy được Kokoro
Nếu môi trường của bạn không cài/tải được Kokoro: **dừng phần âm thanh**, nói rõ lý do, và đưa **script `make_audio.py`** (đọc `units.json` + `data/uN.json`, sinh các khóa theo mục 5.2 bằng Kokoro `af_heart`, ghi `audio/uN.json`) kèm hướng dẫn chạy trên máy người dùng. Vẫn hoàn thành các phần còn lại. **Tuyệt đối không dùng giọng khác để "cho xong".**

---

## 6. Webapp: màn hình và bài kiểm tra

### 6.1 Màn hình
1. **Trang chủ:** danh sách unit từ `units.json`, chia nhóm 1–10, 11–20, 21–30.
2. **Trang unit:**
   - **Học từ:** thẻ từ (emoji lớn, từ, phiên âm, nghĩa tiếng Việt), bấm để nghe tốc độ thường, nút nghe chậm.
   - **Đọc bài:** hiển thị từng bài đọc; bấm một dòng để nghe dòng đó, có nút nghe cả bài.
   - **4 bài kiểm tra:** Nghe, Từ vựng, Đọc, Viết.
   - Dòng trạng thái giọng AI: "✓ Giọng AI đã sẵn sàng" / "Đang tải giọng AI..." / "⚠ Chưa tải được giọng AI (lý do), tạm dùng giọng điện thoại".
3. **Ôn tổng hợp:** chọn nhiều unit rồi trộn câu hỏi theo cùng 4 dạng test.
4. **Trang kiểm tra dữ liệu `index.html?check=1`:** mỗi unit hiện số từ, số câu, số khóa audio và **danh sách chữ chưa có audio** (để người dùng không biết code vẫn phát hiện được lỗi).

### 6.2 Nguyên tắc chung cho mọi bài test
- Mỗi bài **8–12 câu** chia **2–3 dạng nhỏ**. Hằng số số câu đặt ở đầu file để dễ chỉnh.
- Mỗi câu chỉ kiểm tra **một** điều đã dạy. **Đáp án nhiễu cùng nhóm nghĩa** với đáp án đúng. **Xáo trộn** thứ tự đáp án. Không lặp từ/câu trong cùng bài.
- **Không áp lực điểm.** Cuối bài chỉ ghi nhẹ "Con đúng x/y câu".
- Sau mỗi câu: tô xanh đáp án đúng; nếu sai báo "Chưa đúng" và hiện đáp án đúng. Nút "Câu tiếp" chỉ bật sau khi trả lời.
- **Màn kết quả:** danh sách **mục cần ôn** (từ/câu sai) kèm nút nghe lại; nút **"Làm lại các câu sai"** (lặp đến khi đúng hết) và **"Làm lại từ đầu"**.
- **Mọi hình (emoji) trong đáp án đều hiện kèm chữ tiếng Anh và phiên âm IPA bên dưới.** Câu có nhiều món (ví dụ 🍕🍔🌭) hiện đủ tên và phiên âm từng món.
- **Nút nghe không giới hạn số lần.**
- Có audio thì dùng giọng AI trong `audio/uN.json`; chỉ khi thiếu khóa mới dùng giọng điện thoại, và ghi lại khóa thiếu cho trang `?check=1`.
- Nếu unit thiếu dữ liệu cho một dạng câu hỏi, **bỏ qua dạng đó**, không lỗi.

### 6.3 Bốn bài test

**Bài NGHE** (bé phải bấm nghe ít nhất một lần mới chọn được đáp án)
- Phần 1 (5 câu): nghe một **từ** → chọn **hình** đúng (từ có emoji; đáp án nhiễu cùng `cat`).
- Phần 2 (3–4 câu): nghe một **câu trong bài đọc hoặc hội thoại** → trả lời câu hỏi chữ hiện trên màn hình.
- Phần 3 (2 câu): nghe một câu → chọn **hình hoặc nhóm hình** đúng, hoặc chọn mô tả đúng.

**Bài TỪ VỰNG** (hiểu bằng tiếng Anh; nghĩa tiếng Việt chỉ hiện làm gợi ý sau khi trả lời)
- Nhìn **hình** → chọn **từ** (kèm phiên âm).
- Đọc **câu đố định nghĩa** bằng tiếng Anh (`riddles`) → chọn từ.
- **Chọn từ khác loại** (ba từ cùng `cat`, một từ khác nhóm).
- Phân loại từ vào nhóm (ví dụ food/drink) nếu unit có đủ nhóm.

**Bài ĐỌC**
- Đọc **câu** → chọn hình/đáp án đúng.
- **Nối câu hỏi với câu trả lời** hoặc hoàn thành hội thoại (`dialogs`).
- Đọc **đoạn ngắn** → trả lời câu hỏi (`passages[].qs`).
- **Sắp xếp các sự kiện/câu** của truyện đúng thứ tự.

**Bài VIẾT**
- Nhìn hình → **điền chữ cái còn thiếu** hoặc **xếp lại chữ cái** thành từ.
- **Điền từ vào chỗ trống** (`cloze`), có khung từ gợi ý.
- **Xếp các từ thành câu** (`order`).
- **Trả lời câu hỏi bằng câu đầy đủ** (`write`): bé tự viết, hiện **đáp án mẫu** để bố mẹ đối chiếu, không chấm tự động.
- Chấm so khớp: không phân biệt hoa thường, bỏ khoảng trắng thừa, chuẩn hóa dấu nháy.

(Kỹ năng **Nói** nằm ngoài app, không làm.)

### 6.4 Bố cục màn hình test (tham chiếu giao diện)
- Thanh trên: nút "Thoát" và "Câu i/n"; dưới là thanh tiến độ mỏng.
- Dòng nhỏ ghi tên phần ("Phần 1 – Nghe từ, chọn hình").
- Một thẻ (card) bo tròn chứa: nút **"🔊 Nghe"** to bản rộng (sau lần đầu đổi thành "Nghe lại"), câu hỏi chữ đậm, các đáp án.
- Đáp án dạng hình: lưới 2 cột, mỗi ô gồm emoji lớn (khoảng 48 px), từ in đậm, phiên âm chữ nhỏ màu nhạt. Đáp án dạng chữ: danh sách một cột, nút lớn.
- Dòng phản hồi ("Đúng rồi! 👏" / "Chưa đúng..."), rồi nút "Câu tiếp".
- Màu: nền `#F2F7FF`, nhấn `#2F6BFF`, đúng `#1B8F5A` (nền `#E1F5EA`), sai `#C2410C` (nền `#FDEBDD`), chữ `#16284A`. Có bộ màu tối tương ứng. Phải thấy rõ viền focus khi dùng bàn phím và tôn trọng `prefers-reduced-motion`.

---

## 7. Quy trình thực hiện

1. Xác định các unit từ PDF; liệt kê file đã nhận và số unit.
2. Với từng unit: đọc PDF theo mục 4 → tạo `data/uN.json` → ghi **báo cáo đối chiếu** (mục 8.1).
3. Tạo `units.json`.
4. Viết `index.html`, `manifest.json`, icon.
5. Sinh âm thanh theo mục 5 cho từng unit.
6. Chạy kiểm tra (mục 8).
7. Bàn giao (mục 9).

Làm **từng unit một**; xong unit này mới sang unit sau; báo tiến độ ngắn sau mỗi unit.

---

## 8. Kiểm tra chất lượng và báo cáo

Viết và chạy script kiểm tra (không in base64 ra chat). Báo cáo ngắn:

1. **Đối chiếu từ vựng** với hai danh sách trong PDF (Vocabulary Learning Objectives và Phonics and Word Recognition): số từ trong sách, số từ trong `words`, từ thiếu/thừa, từ nào bạn gộp hoặc tách (cặp a/b). Mục tiêu: **khớp 100% với sách**, hoặc giải thích rõ chỗ lệch.
2. **Bài đọc:** liệt kê bài đã lấy (tên, loại, số dòng, trang nguồn) và bài có trong mục lục PDF nhưng **chưa lấy** kèm lý do (ví dụ PDF không có lời đầy đủ).
3. Mọi file JSON đọc được, đúng cấu trúc mục 3.
4. Mỗi unit: số khóa audio **cần / đã có / thiếu** (sau chuẩn hóa). Mục tiêu: **thiếu = 0**.
5. Mỗi `emoji` dùng trong câu hỏi chọn hình đều có `en` và `ipa`.
6. Mỗi câu hỏi có đúng một đáp án đúng, không trùng đáp án.
7. Danh sách các mục bạn **không chắc** (emoji, nghĩa tiếng Việt, IPA, trang bị nghi lệch) để người dùng rà lại.
8. `index.html` tải được `units.json`, mở được từng unit, chạy được cả 4 bài test (nếu có công cụ chạy thử thì chạy thử; nếu không, nói rõ **chưa chạy thử**).
9. Kích thước từng `audio/uN.json` (nên dưới khoảng 5 MB; GitHub giới hạn 100 MB/file).

---

## 9. Bàn giao

- **Một file ZIP** chứa toàn bộ cấu trúc ở mục 2. Nếu người dùng muốn giữ icon cũ, họ sẽ bỏ qua không chép đè các file icon.
- **Hướng dẫn đưa lên GitHub, tối đa 5 dòng:** giải nén, chép vào thư mục `grapeseed` đúng cấu trúc, commit rồi push, đợi 1–2 phút, mở web, nhấn Ctrl+Shift+R (điện thoại: xóa cache hoặc mở tab ẩn danh), thử mở `index.html?check=1` để kiểm tra.
- Kèm báo cáo ở mục 8.
- Nếu không tạo được ZIP: đưa từng file riêng, hoặc script để người dùng chạy trên máy, và nói rõ.

---

## 10. Quy tắc cứng

- Không bịa nội dung unit; chỉ dùng PDF. Thiếu dữ liệu thì để trống trường đó và báo.
- Không lấy từ vựng/bài đọc của unit khác (trang "Look Back"/"Look Ahead").
- Không đổi giọng/engine mà không nói.
- Không in base64 hay file lớn ra khung chat.
- Không khẳng định "đã chạy được/đã khớp" nếu chưa kiểm tra thật; nêu rõ phần nào đã kiểm tra, phần nào chưa.
- Không thêm tính năng ngoài yêu cầu (đăng nhập, bảng xếp hạng, quảng cáo...).
- Không đưa hình ảnh hay trang scan của sách vào app.

---

## 11. Bắt đầu

Sau khi đọc xong: (1) liệt kê các PDF/unit bạn nhận được, (2) nêu ngắn gọn kế hoạch và các điểm chưa rõ (tối đa 3 câu hỏi, chỉ hỏi khi thật cần), (3) rồi bắt tay vào làm.
