# Vietnamese Sentiment Assistant – SPEC (theo đề bài)

## Mục tiêu bắt buộc
1) Ứng dụng Python chạy độc lập, giao diện **Streamlit** (ưu tiên).
2) Nhận 1 câu tiếng Việt và phân loại **POSITIVE / NEUTRAL / NEGATIVE** bằng **Transformer pre-trained** của Hugging Face (không fine-tuning).
3) Lưu lịch sử vào **SQLite** (id, text, sentiment, score, timestamp).
4) Hiển thị lịch sử (tối đa 50 bản ghi mới nhất).
5) Độ chính xác ≥ **95%** trên bộ **10 test case** tiếng Việt có sẵn.

## Chỉ định kỹ thuật
- Model mặc định: `nlptown/bert-base-multilingual-uncased-sentiment`.
- Mapping 1–2★→NEGATIVE, 3★→NEUTRAL, 4–5★→POSITIVE.
- Nếu `score < 0.50` → ép về `NEUTRAL`.
- Tiền xử lý: lowercase, fix lỗi gõ phổ biến (rat→rất, hom→hôm…), optional `underthesea.word_tokenize`.
- UI:
  - Ô nhập văn bản.
  - Nút **Phân loại cảm xúc**.
  - Thông báo lỗi nếu input < 5 ký tự.
  - Bảng lịch sử (50 bản ghi), nút **Tải lại**.
- DB: SQLite, **parameterized queries**, tránh SQL injection.

## Deliverables
- Chạy: `streamlit run app.py`
- Test: `python test_runner.py` (in accuracy và confusion matrix)
- Tệp: `app.py, nlp.py, preprocess.py, db.py, models.py, tests/test_cases.json, README.md, requirements.txt`

## Acceptance Tests (theo rubrics)
- App khởi động < 3s sau khi tải model lần đầu (cache pipeline).
- Giao diện có đủ 4 thành phần: input, button, label kết quả, lịch sử.
- DB có đúng 5 cột; `timestamp` dạng `YYYY-MM-DD HH:MM:SS`.
- Test runner báo `Accuracy >= 95%`.
- Lỗi nhập liệu (<5 ký tự) có popup cảnh báo và **không** lưu DB.
