```
[
    {
      "query": "Learn có mấy lộ trình chính?",
      "expected_answer": "Hai lộ trình: giao tiếp và từ vựng.",
      "source_id": "learn_ov"
    },
    {
      "query": "Lộ trình giao tiếp của Learn có bao nhiêu chủ đề?",
      "expected_answer": "16 chủ đề thông dụng.",
      "source_id": "learn_comm"
    },
    {
      "query": "Các bước học trong lộ trình giao tiếp là gì?",
      "expected_answer": "Nạp cụm → Thực hành → Mở rộng nâng cao.",
      "source_id": "learn_comm"
    },
    {
      "query": "Đối tượng nào phù hợp với Learn?",
      "expected_answer": "Người trình độ A1–đầu A2.",
      "source_id": "learn_ov"
    },
    {
      "query": "Onion GPT có cho phép cá nhân hoá kịch bản không?",
      "expected_answer": "Có – học viên tự tạo tình huống theo nhu cầu.",
      "source_id": "onion_custom"
    },
    {
      "query": "Onion GPT hiện có mấy chủ đề giao tiếp?",
      "expected_answer": "6 chủ đề.",
      "source_id": "onion_path"
    },
    {
      "query": "Trình độ tối thiểu để dùng Onion GPT?",
      "expected_answer": "Giữa A2 trở lên.",
      "source_id": "onion_custom"
    },
    {
      "query": "Gym có bao nhiêu phòng Club?",
      "expected_answer": "20 phòng.",
      "source_id": "gym_club"
    },
    {
      "query": "Mỗi phòng Club chứa tối đa bao nhiêu người?",
      "expected_answer": "2 người chơi và 1 người dự thính.",
      "source_id": "gym_club"
    },
    {
      "query": "Nghe hiểu trong Gym có bao nhiêu bài, mấy cấp độ?",
      "expected_answer": "138 bài, 6 cấp độ.",
      "source_id": "gym_listen"
    },
    {
      "query": "Thư viện IPA của Gym có bao nhiêu bài?",
      "expected_answer": "123 bài, bao phủ 18 cặp âm.",
      "source_id": "gym_ipa"
    },
    {
      "query": "Phương pháp chunking gồm mấy loại cụm?",
      "expected_answer": "2 loại: cụm cấu trúc và cụm thông tin.",
      "source_id": "method_chunk"
    },
    {
      "query": "Spaced repetition là gì?",
      "expected_answer": "Ôn theo chu kỳ giờ-ngày-tuần-tháng để đưa kiến thức vào trí nhớ dài hạn.",
      "source_id": "method_spaced"
    },
    {
      "query": "Shadowing phải thực hiện như thế nào?",
      "expected_answer": "Lặp lại câu vừa nghe sau khoảng 150 ms.",
      "source_id": "method_shadow"
    },
    {
      "query": "Lợi ích chính của chunking?",
      "expected_answer": "Tăng tốc phản xạ, bớt lo ngữ pháp vì cấu trúc đã nằm trong cụm.",
      "source_id": "method_chunk_benefit"
    },
    {
      "query": "Profile trong app dùng để làm gì?",
      "expected_answer": "Tổng kết kết quả học, kiểm tra nói, xếp hạng và cài đặt tài khoản.",
      "source_id": "profile_feat"
    },
    {
      "query": "Điểm khác biệt của The Coach so với app khác?",
      "expected_answer": "Có môi trường luyện tập giả lập giống giao tiếp với người thật.",
      "source_id": "value_time"
    },
    {
      "query": "Học phí app khoảng bao nhiêu tiền?",
      "expected_answer": "Khoảng 700 k – 1 500 k VNĐ.",
      "source_id": "value_money"
    },
    {
      "query": "Cảm xúc người học khi dùng app?",
      "expected_answer": "Học nhẹ nhàng, không nhồi nhét; thoải mái và tự tin khi trò chuyện với AI.",
      "source_id": "value_emotion"
    },
    {
      "query": "Chunking giúp giải quyết vấn đề ngữ pháp như thế nào?",
      "expected_answer": "Cụm chứa sẵn cấu trúc nên người học không phải loay hoay tạo câu.",
      "source_id": "method_chunk_benefit"
    }
  ]
  
```

Tôi có bộ query này. 

1. Viết hàm def(input ...) -> output: text
sử dụng API ơcợc cung cấp 

2. Def chạy test hàng loạt (làm sao để sau chuỷen sang ccs dạng file khác cũng ddễ