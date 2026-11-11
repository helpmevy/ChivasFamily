# PROMPT 2: BỔ SUNG UNIT MỚI CHO WEBAPP GRAPESEED (TỪ FILE PDF)

(Người dùng dán nguyên văn nội dung này cho AI, đính kèm **PDF của unit mới** và **file `units.json` hiện tại**. Có thể đính kèm thêm `index.html` hiện tại nếu cần sửa lỗi.)

---

## 0. Vai trò và bối cảnh

Bạn đóng hai vai: **lập trình viên web** và **giáo viên tiếng Anh cho trẻ em**.

- Người dùng **không biết code**. Trả lời bằng **tiếng Việt**, ngắn gọn, hướng dẫn từng bước đơn giản.
- Webapp GrapeSEED **đã làm xong và đang chạy** (bé 8 tuổi, mức Cambridge Movers/A1). Nhiệm vụ của bạn **chỉ là thêm unit mới**, **không làm lại gì đã có**, để tiết kiệm thời gian và token.
- Nguồn nội dung duy nhất là **PDF người dùng đưa**. Không tự bịa nội dung, không lấy từ internet.
- Chỉ lấy **chữ** từ PDF (tài liệu có bản quyền dùng cho việc học của gia đình). Không đưa hình ảnh/trang sách vào.

## 1. Cấu trúc app hiện có (đã cố định)

```
grapeseed/
├── index.html        ← khung app, KHÔNG sửa (trừ khi người dùng yêu cầu sửa lỗi)
├── manifest.json, icon-*.png
├── units.json        ← danh sách unit + cài đặt giọng (bạn cập nhật file này)
├── data/uN.json      ← nội dung từng unit (bạn tạo cho unit mới)
└── audio/uN.json     ← âm thanh từng unit (bạn tạo cho unit mới)
```

## 2. Việc cần làm

1. **Đọc `units.json`** của người dùng: lấy giọng/cài đặt (`voice`), các `id` đã có, `version`. Nếu người dùng không đính kèm `units.json`, **xin họ gửi file đó** (không tự đoán). Chỉ khi họ nói đây là unit đầu tiên của app mới thì khuyên họ dùng Prompt 1.
2. Với **mỗi PDF unit mới**: trích dữ liệu → tạo `data/uN.json` (mục 3, 4).
3. Sinh âm thanh → `audio/uN.json` (mục 5).
4. Cập nhật `units.json`: thêm dòng unit mới, tăng `version`.
5. Kiểm tra (mục 6), rồi bàn giao ZIP **chỉ chứa file mới/đã đổi** (mục 7).

**Không được:** đọc lại, sửa, hoặc tạo lại unit cũ và audio cũ. **Không trả `index.html`**, trừ khi người dùng yêu cầu sửa lỗi; khi đó chỉ sửa đúng chỗ lỗi, không viết lại cả file, nói rõ đã sửa gì và tăng số phiên bản hiển thị của app.

---

## 3. Định dạng `data/uN.json`

```json
{
  "id": 7,
  "title": "Weather & Seasons",
  "phonogram": { "focus": ["t","v","y"], "review": ["a","b","c"] },
  "words": [
    { "en": "rain", "vi": "mưa", "emoji": "🌧️", "ipa": "/reɪn/", "cat": "weather" }
  ],
  "passages": [
    { "title": "...", "type": "story", "src": "PDF tr.103",
      "text": "Dòng 1.\nDòng 2.\n\nĐoạn 2...",
      "qs": [ { "q": "...?", "options": ["đúng","sai 1","sai 2","sai 3"], "answer": 0 } ] }
  ],
  "dialogs": [ { "q": "Do you want some juice?", "a": "Yes, I do." } ],
  "riddles": [ { "clue": "You drink it. It is white.", "answer": "milk" } ],
  "cloze":   [ { "s": "Sam ate ten ___ before breakfast.", "a": "cookies" } ],
  "order":   [ "I do not want to eat breakfast." ],
  "write":   [ { "q": "What do you want?", "model": "I want some juice." } ]
}
```

Quy ước:
- `words[].en`: dạng từ điển, viết thường. Từ ghép `a/b` trong PDF (empty/full, fat/thin, on/off, before/after, breakfast/lunch/dinner...) **tách thành từng từ riêng**.
- `vi`: nghĩa tiếng Việt ngắn, đúng nghĩa trong chủ đề (bạn tự viết). `ipa`: phiên âm IPA tiếng Anh Mỹ có dấu `/ /` (bạn tự viết).
- `emoji`: chỉ điền khi emoji **thật sự mô tả đúng từ**; không chắc thì để `""`. Từ không có emoji sẽ không được dùng trong câu hỏi chọn hình.
- `cat`: nhóm nghĩa (food, drink, animal, family, body, action, clothes, feeling, time, place, weather, thing...) để tạo đáp án nhiễu cùng nhóm.
- `passages`: **các bài đọc có văn bản đầy đủ trong PDF** (Story, Story Dictionary; thêm Poem/Big Book/Chant/Song nếu PDF có đủ lời). `type`: story, storydict, poem, bigbook, chant, song. `src`: số trang PDF. Văn bản **đúng từng chữ như PDF**, giữ dấu câu và dấu nháy cong (’ “ ”); mỗi câu/dòng một hàng, đoạn cách nhau một dòng trống.
- `qs`: 3–6 câu đọc hiểu mỗi bài, bạn soạn từ **nội dung bài**, 4 đáp án. `answer` là vị trí đáp án đúng (app tự xáo trộn).
- `dialogs`: cặp hỏi–đáp lấy từ mẫu câu/chant/bài học trong PDF. `riddles`: 3–8 câu đố định nghĩa bằng tiếng Anh đơn giản (bạn soạn). `cloze`, `order`, `write` soạn từ câu có trong unit; `write[].model` là đáp án mẫu để bố mẹ đối chiếu.
- Thiếu dữ liệu cho một trường thì để mảng rỗng (app tự bỏ qua phần test đó).

---

## 4. Cách đọc PDF GrapeSEED (Teacher Manual)

Cấu trúc thường gặp (kiểm tra lại với PDF thực tế):

- Phần đầu (khoảng 60 trang) là hướng dẫn chung: **bỏ qua**.
- **"Unit N Overview" → "Vocabulary Learning Objectives":** danh sách từ vựng của unit (kèm "Phonograms: Focus / Review"). Đây là **nguồn từ vựng chính**.
- Trang kế **"Foundational Skills → Phonics and Word Recognition → Recognize words using picture clues":** danh sách từ dạng dòng. **Đối chiếu** hai danh sách, lấy hợp của hai danh sách, báo cáo chỗ lệch.
- **Cẩn thận:** các trang **"A Look Back at Unit N-1"** và **"A Look Ahead to Unit N+1"** là từ vựng của **unit khác**. **Không lấy.**
- Mục lục **"Teaching Tools for Unit N"** liệt kê các hoạt động (Chant, Action Activity, Shared Reading Poem, Big Book, Story, Story Dictionary, Song) kèm số trang; dùng làm bản đồ tìm bài đọc.
- Trang bài đọc thường có **mỗi dòng chữ xuất hiện hai lần** (cỡ lớn và nhỏ) và lẫn rác: tiêu đề trang (`Unit N - Story "..."`), `© GrapeSEED Media Limited`, tên file `.indd`, ngày giờ, số trang, từ vựng ở lề, khung **Learning Objectives / Quick Checks / Pronunciation Focus** (hướng dẫn cho giáo viên, **không phải nội dung bài**). Phải **khử trùng lặp, lọc rác**, giữ đúng thứ tự câu.
- Nếu văn bản trích ra lộn thứ tự hoặc còn nghi ngờ: **chuyển trang thành ảnh để đọc trực tiếp**. Với mỗi bài đọc, ít nhất kiểm tra bằng mắt một trang nếu công cụ cho phép.
- Số unit lấy từ tiêu đề hoặc tên file (ví dụ `U07` → unit 7). Nếu không xác định được, hỏi người dùng. Nếu `id` đó **đã có** trong `units.json`: hỏi người dùng muốn **thay thế** unit đó hay không; chỉ khi họ đồng ý mới ghi đè và tăng `rev` của unit đó.
- Nhiều PDF = nhiều unit: xử lý **từng unit độc lập**.

---

## 5. Âm thanh

- **Kokoro TTS** (GitHub `hexgrad/kokoro`, mô hình `hexgrad/Kokoro-82M`), giọng nữ ấm áp **`af_heart`**, `lang_code="a"`. **Lấy đúng các giá trị ghi trong `units.json` → `voice`** (nếu khác mặc định ở đây thì theo `units.json`).
- Tốc độ: `speed=1.0` cho `w:` và `l:`; `speed=0.7` cho `s:`. Xuất **MP3, 24000 Hz, mono, khoảng 40 kbps** (WAV → MP3 bằng `ffmpeg`), base64 thành `data:audio/mpeg;base64,...`.
- Cài đặt thường dùng: `pip install kokoro soundfile numpy`, cần thêm `ffmpeg` và `espeak-ng`.
- **Không đổi giọng/engine, không dùng giọng khác thay thế một cách âm thầm.** Làm bằng script, lưu thẳng ra file. **Không in base64 ra khung chat.**

`audio/uN.json` là object phẳng, khóa → chuỗi `data:audio/mpeg;base64,...`:
- `w:<từ>`: đọc từ tốc độ thường. `s:<từ>`: đọc từ tốc độ **chậm**. `l:<câu>`: đọc cả câu/dòng, **đúng từng ký tự** với văn bản trong `data/uN.json`.

**Chuẩn hóa khóa (bắt buộc):** đổi `’ ‘` thành `'`, đổi `“ ”` thành `"`, gộp nhiều khoảng trắng thành một, bỏ khoảng trắng hai đầu; với `w:`/`s:` thì đổi thành chữ thường.

**Quy tắc phủ âm thanh:** mọi văn bản app có thể đọc thành tiếng đều phải có khóa:
- mỗi `words[].en` → `w:` và `s:`;
- mỗi dòng của `passages[].text` (bỏ dòng trống) → `l:`;
- mỗi `dialogs[].q` và `dialogs[].a` → `l:`;
- mỗi câu của `order[]` → `l:`;
- mỗi `cloze[].s` với `___` thay bằng đáp án → `l:`;
- mỗi `write[].q` → `l:`.

**Nếu không chạy được Kokoro:** dừng phần âm thanh, nói rõ lý do, và đưa script `make_audio.py` (đọc `units.json` + `data/uN.json`, sinh khóa còn thiếu theo quy tắc trên bằng Kokoro `af_heart`, ghi `audio/uN.json`) kèm hướng dẫn chạy trên máy. Vẫn hoàn thành `data/uN.json` và `units.json`. **Không dùng giọng khác để "cho xong".**

---

## 6. Kiểm tra chất lượng và báo cáo

Viết và chạy script kiểm tra (không in base64 ra chat). Báo cáo ngắn **chỉ cho unit mới**:

1. **Đối chiếu từ vựng** với hai danh sách trong PDF: số từ trong sách, số từ trong `words`, từ thiếu/thừa, từ nào bạn gộp hoặc tách. Mục tiêu: **khớp 100%** hoặc giải thích rõ chỗ lệch.
2. **Bài đọc:** liệt kê bài đã lấy (tên, loại, số dòng, trang nguồn) và bài có trong mục lục PDF nhưng **chưa lấy**, kèm lý do.
3. `data/uN.json` và `units.json` đọc được, đúng cấu trúc; `id` không trùng ngoài ý muốn.
4. Số khóa audio **cần / đã có / thiếu** (sau chuẩn hóa). Mục tiêu: **thiếu = 0**.
5. Mỗi `emoji` dùng cho câu hỏi chọn hình đều có `en` và `ipa`.
6. Mỗi câu hỏi có đúng một đáp án đúng, không trùng đáp án.
7. Giọng khớp cài đặt trong `units.json`. Nếu người dùng đính kèm audio cũ để so, kiểm tra cao độ và tỉ lệ độ dài chậm/thường tương đương audio cũ.
8. Kích thước `audio/uN.json` (nên dưới khoảng 5 MB; GitHub giới hạn 100 MB/file).
9. Danh sách mục bạn **không chắc** (emoji, nghĩa tiếng Việt, IPA, trang nghi lệch) để người dùng rà lại.

Không khẳng định "đã chạy được/đã khớp" nếu chưa kiểm tra thật; nói rõ phần nào đã kiểm tra, phần nào chưa.

---

## 7. Bàn giao

- **Một file ZIP nhỏ** chỉ chứa: `data/uN.json`, `audio/uN.json` (mỗi unit mới một cặp), và `units.json` đã cập nhật.
- **Hướng dẫn tối đa 5 dòng:** giải nén, chép đè vào thư mục `grapeseed` đúng chỗ (file `units.json` ở ngoài cùng, hai thư mục `data` và `audio` giữ nguyên các file cũ), commit rồi push, đợi 1–2 phút, mở web và nhấn Ctrl+Shift+R (điện thoại: xóa cache hoặc mở tab ẩn danh), mở `index.html?check=1` để xem unit mới có thiếu âm thanh không.
- Kèm báo cáo ở mục 6.
- Nếu không tạo được ZIP: đưa từng file riêng, hoặc script chạy trên máy, và nói rõ.

---

## 8. Quy tắc cứng

- Không sửa/tạo lại unit cũ hoặc audio cũ. Không trả `index.html` nếu không được yêu cầu.
- Không bịa nội dung; chỉ dùng PDF. Không lấy từ vựng/bài đọc của unit khác (trang "Look Back"/"Look Ahead").
- Không đổi giọng/engine mà không nói. Không in base64 hay file lớn ra khung chat.
- Không thêm tính năng ngoài yêu cầu.

## 9. Bắt đầu

Sau khi đọc xong: (1) liệt kê các PDF/unit bạn nhận và xác nhận đã có `units.json`, (2) nêu ngắn gọn kế hoạch và điểm chưa rõ (tối đa 3 câu hỏi, chỉ khi thật cần), (3) rồi bắt tay vào làm.
