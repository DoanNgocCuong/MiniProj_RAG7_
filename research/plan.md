# Simple RAG Pipeline Plan

## Bước 1: Data Ingestion
- Đọc file PDF (dùng PyPDF2 hoặc pdfplumber).
- Trích xuất toàn bộ text.

## Bước 2: Chunking
- Chia text thành các đoạn nhỏ (mỗi đoạn N câu hoặc N ký tự).

## Bước 3: Embedding
- Dùng model embedding (VD: sentence-transformers) để sinh vector cho từng chunk.

## Bước 4: Retrieval
- Khi có câu hỏi, sinh embedding cho câu hỏi.
- Tính cosine similarity giữa embedding câu hỏi và các chunk.
- Lấy top-k chunk liên quan nhất.

## Bước 5: Generation
- Đưa các chunk liên quan + câu hỏi vào LLM (VD: GPT-3.5-turbo) để sinh câu trả lời.

## Bước 6: Evaluation
- So sánh câu trả lời với ground truth (nếu có).
- Đánh giá bằng precision, recall đơn giản.

## Ghi chú
- Chỉ cần 1 file PDF mẫu, 1 câu hỏi mẫu, 1 ground truth để test.
- Chưa cần UI, chưa cần tối ưu hiệu năng/phức tạp. 