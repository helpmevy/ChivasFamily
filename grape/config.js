/* GrapeSEED Test App - Cấu hình chung
   Chỉnh đường dẫn, âm lượng mặc định, số câu tại đây.
*/
window.GS_CONFIG = {
  // Đường dẫn thư mục (tương đối, chạy file:// và GitHub Pages đều được)
  audioBase: "audio/kokoro/",
  sfxBase: "audio/sfx/",
  imageBase: "images/",
  audioExt: ".mp3",
  imageExt: ".png",

  // Âm thanh nút bấm / hiệu ứng (tên file không đuôi)
  sfxNames: ["tap", "correct", "wrong", "retry", "star", "complete", "confetti"],

  // Cài đặt mặc định (có thể ghi đè trong Parent zone)
  defaults: {
    volume: 0.8,
    sfxVolume: 0.6,
    questionsEasy: 10,
    questionsHard: 12,
    allowHint: true,          // Dễ: sai 1 lần thì loại 1 đáp án
    maxReplayEasy: 99,        // nghe lại không giới hạn
    maxReplayHard: 2,
    speechRate: 0.85,         // tốc độ speechSynthesis dự phòng
    speechLang: "en-US"
  },

  // Thang sao
  stars: [
    { min: 95, stars: 5 },
    { min: 85, stars: 4 },
    { min: 70, stars: 3 },
    { min: 50, stars: 2 },
    { min: 0,  stars: 1 }
  ]
};
