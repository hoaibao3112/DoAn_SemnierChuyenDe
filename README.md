# Vietnamese Sentiment Assistant

## Giới thiệu

Vietnamese Sentiment Assistant là một ứng dụng phân tích cảm xúc cho câu tiếng Việt. Ứng dụng sử dụng mô hình pre-trained qua Hugging Face pipeline, kèm theo một lớp tiền xử lý và một vài luật hậu xử lý để cải thiện kết quả cho ngôn ngữ tiếng Việt.

Ứng dụng nhận một câu tiếng Việt làm đầu vào, trả về nhãn cảm xúc thuộc một trong ba lớp: POSITIVE, NEUTRAL, NEGATIVE; đồng thời lưu kết quả vào cơ sở dữ liệu SQLite kèm timestamp.

## Tính năng chính

- Phân loại cảm xúc 3 lớp: POSITIVE / NEUTRAL / NEGATIVE
- Tiền xử lý văn bản tiếng Việt: chuẩn hóa, sửa lỗi gõ phổ biến và map viết tắt/no-diacritic
- Sử dụng pipeline Hugging Face (model mặc định: nlptown/bert-base-multilingual-uncased-sentiment)
- Giao diện web đơn giản bằng Streamlit
- Lưu trữ kết quả vào SQLite với các trường: id, text, sentiment, score, timestamp
- Bộ kiểm thử tự động (pytest + test_runner) để đánh giá accuracy và in confusion matrix

## Yêu cầu hệ thống

- Python 3.8 trở lên
- Truy cập Internet khi lần đầu tải model (sẽ được cache sau đó)
- Các thư viện có trong `requirements.txt`

## Cài đặt

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cấu trúc dự án (tóm tắt)

```
DoAnSemnierChuyenDe/
├── app.py
├── nlp.py
├── preprocess.py
├── db.py
├── test_runner.py
├── eval_thresholds.py
├── eval_thresholds_detailed.py
├── tests/
├── requirements.txt
├── README.md
├── SPEC.md
└── .gitignore
```

## Cách chạy

1. Kích hoạt môi trường ảo theo hướng dẫn ở trên.
2. Chạy ứng dụng web:

```powershell
streamlit run app.py
```

3. Chạy test runner để đánh giá accuracy và in confusion matrix:

```powershell
.\.venv\Scripts\python.exe test_runner.py
```

Để chạy test mở rộng với file extra:

```powershell
.\.venv\Scripts\python.exe test_runner.py --extra
```

Chạy pytest cho unit tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Tóm tắt kỹ thuật

- Tiền xử lý (`preprocess.normalize_vi`): chuẩn hóa (lowercase), sửa lỗi gõ phổ biến, map các từ không dấu về dạng có dấu, và sử dụng tokenization nếu `underthesea` được cài.
- Mô hình: pipeline `sentiment-analysis` từ transformers; mặc định dùng `nlptown/bert-base-multilingual-uncased-sentiment`.
- Mapping: nhãn "star" (1..5) được map sang lớp cảm xúc: 1–2 → NEGATIVE, 3 → NEUTRAL, 4–5 → POSITIVE.
- Quyết định nhãn: theo nhãn sao có xác suất cao nhất. Nếu xác suất top-star < `neutral_threshold` (mặc định 0.50) thì trả về NEUTRAL.
- Post-processing: một số luật từ khoá và phủ định được áp dụng để điều chỉnh kết quả khi cần.

## Độ tin cậy (confidence) — diễn giải

Ứng dụng hiển thị một chỉ số "độ tin cậy" khi phân loại. Cách tính và ý nghĩa:

- Model trả về xác suất cho từng nhãn "1 star".."5 stars".
- Ứng dụng tính tổng xác suất của các nhãn "star" thuộc cùng một lớp để có một xác suất cấp lớp (class-level aggregated probability). Giá trị này được dùng để hiển thị vì thường trực quan hơn cho người dùng.
- Quyết định nhãn vẫn tuân theo logic top-star và `neutral_threshold = 0.50` (hiện tại là hành vi đã được đánh giá trên bộ test).

Ví dụ ngắn: một câu có top-star score = 0.27 nhưng tổng xác suất cho lớp NEGATIVE có thể là 0.80; UI sẽ hiển thị giá trị tổng hợp để người dùng dễ hiểu hơn.

## Test và đánh giá

- Tập test chính có trong `tests/test_cases.json` (15 cases). Có thể mở rộng bằng `tests/test_cases_extra.json`.
- Sử dụng `eval_thresholds.py` và `eval_thresholds_detailed.py` để thử các giá trị `neutral_threshold` khác nhau và quan sát confusion matrix.
- Ghi chú: test runner trong repository hiện đã được chỉnh để yêu cầu pass threshold là 95% (PASS nếu accuracy >= 0.95).

## Những thay đổi quan trọng đã thực hiện

- Bổ sung một số mapping trong `preprocess.py` để cải thiện chuẩn hoá no-diacritic và viết tắt.
- Trong `nlp.py` tính toán aggregated class probability để hiển thị confidence trực quan hơn, đồng thời giữ nguyên logic quyết định nhãn theo top-star + `neutral_threshold` để duy trì accuracy đã được kiểm chứng.
- `test_runner.py` đã được cập nhật để pass threshold là 95%.

## Hướng phát triển tiếp

- Thay model sang một model thuần tiếng Việt (ví dụ phobert) để cải thiện chất lượng trên dữ liệu tiếng Việt.
- Fine-tune model nếu có tập dữ liệu nhãn tiếng Việt đủ lớn.
- Thêm CI (GitHub Actions) để tự động chạy `test_runner.py` và pytest khi có commit.

## Ghi chú

Nếu cần tôi có thể giúp thêm: mở rộng bộ test, chỉnh UI để hiển thị cả top-star score và class score, hoặc bổ sung CI. Xin cho biết lựa chọn bạn muốn tiếp theo.
