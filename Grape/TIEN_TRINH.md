# TIEN_TRINH.md - Web app Grapeseed (bàn giao sang tài khoản mới)

Ngày cập nhật: 2026-11-10
Phiên bản app: **v0.9** (biến APP_VERSION trong index.html)

## Tình trạng
- Làm xong: **Unit 1** (đã test trên điện thoại), **Unit 2 và Unit 3** (mới thêm ở v0.9, chưa test). Mỗi unit có 4 bài kiểm tra và giọng AI tải theo unit.
- QUYẾT ĐỊNH MỚI NHẤT: chạy app trên **GitHub Pages** (kho Public, tên khó đoán, có thẻ noindex), không dùng link Claude nữa. Link GitHub: (điền sau khi tạo).
- Bản cũ trên link Claude (https://claude.ai/artifact/M3vYsvkf1552joHEtniVYs) chỉ còn là bản thử v0.7, không cập nhật nữa.
- Mỗi lần Claude sửa xong, người dùng chép file mới vào thư mục kho GitHub, ghi đè file cũ rồi đẩy lên (commit/push). Điểm lưu theo địa chỉ web nên đổi link thì mất điểm.

## Quyết định đã chốt
- Chạy trên GitHub Pages (Public + noindex + tên kho khó đoán), làm trực tiếp trong chat, không dùng Project, không chuyển tài khoản. Hiện chưa có mã PIN và hồ sơ nhiều thành viên (chỉ 1 bé học; bản cho người lớn làm sau). Nội dung có bài đọc Grapeseed nguyên văn nên chỉ chia sẻ link trong gia đình.
- Bỏ bài hát; chỉ làm web app chấm điểm và kiểm tra: Từ vựng, Nghe, Đọc, Viết.
- Voice chat luyện nói dùng app Claude thuần, không đưa vào web app.
- Dạng đề theo tinh thần Cambridge Young Learners / TOEFL Primary (không phải đề chính thức).
- Mục tiêu cuối: đủ 30 unit (3 tab: Unit 1-10, 11-20, 21-30). Có thể chỉnh theo số unit thật.
- Bài đọc: Unit 1 dùng truyện Grapeseed chuẩn do người dùng cung cấp và đã kiểm tra. Từ Unit 2: ưu tiên văn bản chuẩn do người dùng gửi (dán chữ hoặc gửi link). Nếu chưa có thì Claude tự soạn bài đọc ngắn dùng từ vựng của unit và GHI RÕ trong app là "bài tự soạn", không chép nguyên văn từ web (có bản quyền, bản trên mạng nhiều lỗi).

## Kiến trúc kỹ thuật (v0.8)
- Cấu trúc kho GitHub:
  - index.html (~25 KB): toàn bộ giao diện và logic. Dữ liệu unit nằm trong khối UNITS ở đầu file. Mỗi unit có thuộc tính audio trỏ tới file âm thanh, ví dụ audio:"audio/u1.json".
  - thư mục audio/ chứa u1.json, u2.json ... (mỗi file ~1.5 MB, JSON gồm khóa -> data URI mp3 base64).
- App tải file âm thanh của unit khi bé mở unit đó (fetch(U.audio)), hiện dòng trạng thái "Giọng AI đã sẵn sàng". Lỗi thì hiện mã lỗi (ví dụ HTTP 404 = sai đường dẫn hoặc thiếu file) và dùng giọng điện thoại dự phòng.
- Khóa trong JSON âm thanh: "w:<từ>" (đọc thường), "s:<từ>" (đọc chậm), "l:<nguyên văn một dòng bài đọc>".
- Khóa lưu điểm: grapeseed_app_v3 (localStorage, theo địa chỉ web và trình duyệt).
- Khi thêm unit mới: Claude đưa index.html mới + audio/uN.json mới; người dùng chép vào kho (giữ đúng thư mục audio/) rồi đẩy lên GitHub.
- Không còn dùng asset/artifact của Claude.

## Cách tạo âm thanh (đã dùng cho Unit 1)
- pip install kokoro-onnx soundfile --break-system-packages ; cần ffmpeg.
- Tải mô hình từ github.com: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx (~325 MB) và .../voices-v1.0.bin.
- Giọng af_heart, lang en-us. Từ: tổng hợp "từ." tốc độ 1.0 (khóa w:) và 0.72 (khóa s:; 0.62 bị vỡ giọng). Dòng bài đọc: tốc độ 1.0 (nút Chậm của bài đọc phát lại với playbackRate 0.8). Cắt khoảng lặng đầu cuối, chuẩn hóa biên độ 0.9, ffmpeg mono 24 kHz 40 kbps mp3, mã hóa base64.
- Chạy nền (setsid nohup) vì mất vài phút; Unit 1: 65 từ x 2 + 75 dòng khoảng 4-5 phút.

## Tính năng app (v0.7)
- 3 tab, bấm tab xổ danh sách số unit, chọn unit thì hiện 4 bài kiểm tra. Unit chưa có nội dung báo "Unit này chưa có nội dung".
- Từ vựng 20 câu (thấy từ + phiên âm, chọn nghĩa tiếng Việt); Nghe 20 câu (nghe, chọn từ, có phiên âm và nghĩa); Đọc (câu hỏi chọn đáp án theo bài đọc, bài đọc có nút nghe Thường/Chậm); Viết 20 câu (nghe viết từ, điền chỗ trống, sắp xếp câu).
- Chấm điểm: chọn rồi bấm "Chọn" mới chấm; ✓ xanh +1 điểm, ✗ đỏ 0 điểm; ghi 12/20 câu đúng; nút đổi thành "Câu tiếp theo". Thoát giữa chừng không lưu điểm.
- Nút Thường / Chậm ở mọi chỗ có nghe.

## Unit đã có nội dung
- Unit 1 (Family, Friends & Animals): 65 từ, 5 bài đọc Grapeseed chuẩn (20 câu hỏi), âm thanh audio/u1.json.
- Unit 2 (Clothes, Body Parts & Daily Actions): 68 từ, 4 bài đọc Grapeseed chuẩn (Too Big Too Small; What Can You Do?; A Mother Who Lives in a Boot; Jonny Bear Goes to the Zoo), 20 câu hỏi, âm thanh audio/u2.json.
- Unit 3 (School & Colors): 48 từ, 5 bài đọc Grapeseed chuẩn (Marvin Goes to School; I Like These Things; Our Day at School; My Toy Box; Jonny Bear Helps His Mother), 20 câu hỏi, âm thanh audio/u3.json.
- Từ Unit 4 trở đi: chưa có.
- Câu hỏi đọc hiểu, câu điền từ, câu sắp xếp, nghĩa tiếng Việt, phiên âm do Claude soạn; bài đọc là văn bản người dùng cung cấp (đã bỏ dòng "." thừa trong Marvin Goes to School).

## Việc tiếp theo
1. Người dùng chép index.html và audio/u2.json, audio/u3.json vào kho GitHub rồi test Unit 2, Unit 3 trên điện thoại.
2. Sửa lỗi nếu có (nghĩa tiếng Việt, phiên âm, câu hỏi, âm thanh).
3. Làm các unit tiếp theo khi người dùng gửi bài đọc và danh sách từ.

## Việc còn mở
- Phiên âm do Claude soạn, cần người biết tiếng Anh kiểm tra.
- Câu điền chỗ trống và sắp xếp câu do Claude tự soạn.
- Không tải được file .js về điện thoại trước đó; âm thanh nay dùng .json (và bản .txt dự phòng).
