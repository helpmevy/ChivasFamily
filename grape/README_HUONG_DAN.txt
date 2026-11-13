═══════════════════════════════════════════════════════════════
  GRAPESEED TEST APP – HƯỚNG DẪN SỬ DỤNG
  Webapp kiểm tra tiếng Anh GrapeSEED cho trẻ 6–10 tuổi
═══════════════════════════════════════════════════════════════

1. CÁCH CHẠY
   • Cách đơn giản nhất: mở file index.html bằng trình duyệt
     (Chrome / Edge / Safari / Firefox). Bấm đúp file là được.
   • Hoặc đưa lên GitHub Pages:
     1. Tạo repo mới trên GitHub
     2. Upload toàn bộ thư mục grapeseed-test-app
     3. Settings → Pages → Source: main branch / root
     4. Truy cập https://<user>.github.io/<repo>/

2. CÁCH THÊM ÂM THANH (Kokoro)
   • Mở file assets_needed/audio_list.csv – đây là danh sách
     TẤT CẢ từ và câu cần giọng đọc.
   • Tạo file .mp3 bằng Kokoro, đặt tên đúng theo cột "id"
     (ví dụ: bear.mp3, p_hello.mp3).
   • Bỏ vào thư mục: audio/kokoro/u01/
   • Khi có file thật, app tự dùng, không cần sửa code.

3. CÁCH THÊM HÌNH ẢNH
   • Mở assets_needed/image_list.csv.
   • Đặt file PNG tên đúng id (bear.png, tiger.png…)
     vào images/u01/
   • Nếu thiếu, app hiện emoji + nền màu pastel.

4. CÁCH THÊM ÂM THANH NÚT BẤM
   • Tạo file: tap.mp3, correct.mp3, wrong.mp3, retry.mp3,
     star.mp3, complete.mp3, confetti.mp3
   • Bỏ vào audio/sfx/
   • Nếu thiếu, app dùng tiếng "ting" đơn giản bằng WebAudio.

5. CÁCH NHỜ AI SỬA GIAO DIỆN
   • Chỉ cần gửi file index.html + mô tả muốn sửa.
   • AI sẽ trả về TOÀN BỘ index.html mới.
   • Dán đè file cũ. Không đụng data/u01.js trừ khi bạn yêu cầu.
   • Đọc khối chú thích đầu index.html để hiểu kiến trúc.

6. CẤU TRÚC THƯ MỤC
   grapeseed-test-app/
   ├── index.html          ← toàn bộ UI + logic
   ├── config.js           ← đường dẫn, số câu, âm lượng
   ├── data/
   │   ├── units.js        ← danh sách unit
   │   └── u01.js          ← dữ liệu Unit 1
   ├── audio/
   │   ├── kokoro/u01/     ← giọng đọc (đặt file vào đây)
   │   └── sfx/            ← hiệu ứng nút
   ├── images/u01/         ← hình ảnh
   ├── assets_needed/
   │   ├── audio_list.csv
   │   └── image_list.csv
   └── README_HUONG_DAN.txt

7. GIẢ ĐỊNH ĐÃ CHỌN
   • Chỉ xử lý Unit 1 vì chỉ nhận được 1 file Teacher Manual.
   • Tên unit: "Friends & Animals" (lấy từ chủ đề Friends,
     Animals, Zoo, Family trong giáo trình).
   • Số câu mặc định: Easy 10, Hard 12 (chỉnh trong Parent zone
     hoặc config.js).
   • Phonogram chỉ 5 âm Unit 1: d, f, k, m, z.
   • Câu hỏi chỉ dùng từ vựng / cụm / câu có trong file md
     Unit 1 (đã làm sạch nhiễu OCR).
   • Distractor Hard không lấy unit trước vì chưa có unit khác.
   • Linh vật tự vẽ "Grapey" (chùm nho) – không dùng nhân vật
     bản quyền GrapeSEED.
   • Không có bài nói / ghi âm (đúng yêu cầu).
   • Hồ sơ mặc định "Friend 🐵" khi mở lần đầu.

8. BÁO CÁO NỘI DUNG
   • Số unit đã xử lý: 1 (Unit 1)
   • Câu tiềm năng Easy: 40 câu
   • Câu tiềm năng Hard: 35 câu
   • Phần bỏ vì lỗi OCR / không chắc chắn:
     – Một số dòng truyện bị lặp chữ (ví dụ "the tree.tree..")
       → chỉ lấy câu sạch.
     – Bảng Scope & Sequence và bảng phonogram multi-letter
       không dùng làm câu hỏi (chỉ tham khảo).
     – Story Dictionary Jonny Bear: chỉ lấy grandfather /
       grandmother vì phần còn lại trùng với Story Family.
   • Unit còn lại: chưa có file md Unit 2–40. Khi có thêm file,
     chỉ cần tạo data/uNN.js theo đúng format và thêm vào
     data/units.js – app sẽ tự nhận.

9. KIỂM TRA ĐÃ LÀM
   • id câu hỏi không trùng.
   • Đáp án luôn nằm trong choices.
   • Mọi câu có trường source.
   • Từ trong câu hỏi / đáp án thuộc vocab hoặc texts Unit 1.
   • Mở index.html chạy được offline (file://).
   • Parent zone: nhấn giữ nút 🔒 2 giây.

Chúc các bé học vui và tiến bộ!
═══════════════════════════════════════════════════════════════
