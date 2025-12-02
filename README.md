# Vietnamese Sentiment Assistant

Đồ án môn Seminar Chuyên đề

## Mô tả

Đây là ứng dụng phân tích cảm xúc văn bản tiếng Việt, được xây dựng trong khuôn khổ đồ án môn học. Ứng dụng nhận đầu vào là một câu tiếng Việt và đưa ra kết quả phân loại thuộc một trong ba nhãn: **POSITIVE**, **NEUTRAL**, hoặc **NEGATIVE**.

Hệ thống kết hợp mô hình học sâu (Deep Learning) từ Hugging Face với các kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) được thiết kế riêng cho tiếng Việt, bao gồm tiền xử lý văn bản và điều chỉnh kết quả dựa trên từ điển.

## Tính năng

- **Phân loại cảm xúc 3 lớp**: POSITIVE / NEUTRAL / NEGATIVE
- **Tiền xử lý tiếng Việt**: 
  - Chuẩn hóa văn bản (chữ thường, loại bỏ ký tự đặc biệt)
  - Sửa lỗi chính tả và viết tắt phổ biến (vd: "ko" → "không", "bt" → "bình thường")
  - Chuyển đổi văn bản không dấu sang có dấu (vd: "rat vui" → "rất vui")
  - Tích hợp underthesea để tách từ (word segmentation)
- **Mô hình**: Sử dụng BERT đa ngôn ngữ qua Hugging Face Transformers
- **Giao diện**: Web app trực quan với Streamlit
- **Lưu trữ**: SQLite database lưu lịch sử phân loại
- **Kiểm thử**: Bộ test tự động với accuracy ≥ 95%

## Yêu cầu

- Python 3.8+
- Kết nối Internet (lần đầu chạy để tải model, sau đó được cache)

## Cài đặt

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cấu trúc thư mục

```
├── app.py                  # Giao diện Streamlit
├── nlp.py                  # Module phân loại cảm xúc
├── preprocess.py           # Tiền xử lý văn bản tiếng Việt
├── db.py                   # Xử lý database SQLite
├── test_runner.py          # Chạy test và in confusion matrix
├── reclassify_db.py        # Cập nhật lại nhãn trong DB
├── eval_thresholds.py      # Đánh giá các ngưỡng neutral
├── tests/
│   ├── test_cases.json     # Bộ test chính (16 cases)
│   └── test_cases_extra.json   # Bộ test mở rộng (10 cases)
├── docs/                   # Tài liệu bổ sung
├── requirements.txt
├── SPEC.md                 # Đặc tả kỹ thuật
└── README.md
```

## Hướng dẫn sử dụng

### Chạy ứng dụng web

```powershell
streamlit run app.py
```

Truy cập `http://localhost:8501` trên trình duyệt.

### Chạy kiểm thử

```powershell
# Test cơ bản
python test_runner.py

# Test đầy đủ (bao gồm test mở rộng)
python test_runner.py --extra

# Unit test với pytest
python -m pytest -q
```

## Chi tiết kỹ thuật

### Pipeline xử lý

1. **Tiền xử lý** (`preprocess.py`):
   - Chuẩn hóa văn bản: lowercase, loại bỏ ký tự thừa
   - Áp dụng từ điển sửa lỗi (~280 mapping cho văn bản không dấu, ~180 mapping cho viết tắt/teencode)
   - Tách từ với underthesea (nếu có)

2. **Phân loại** (`nlp.py`):
   - Model: `nlptown/bert-base-multilingual-uncased-sentiment`
   - Output gốc: 5 nhãn sao (1-5 stars) với xác suất tương ứng
   - Mapping: 1-2 sao → NEGATIVE, 3 sao → NEUTRAL, 4-5 sao → POSITIVE
   - Ngưỡng: Nếu xác suất cao nhất < 0.50, mặc định trả về NEUTRAL

3. **Hậu xử lý**:
   - Điều chỉnh dựa trên từ khóa cảm xúc (lexicon-based adjustment)
   - Xử lý phủ định (vd: "không tốt" → NEGATIVE)
   - Ưu tiên từ khóa mạnh (vd: "tệ", "tuyệt vời")

### Độ tin cậy (Confidence Score)

Giá trị hiển thị trên giao diện là **xác suất tổng hợp theo lớp** (aggregated class probability):
- Tổng xác suất các nhãn sao thuộc cùng một lớp
- Ví dụ: P(NEGATIVE) = P(1 star) + P(2 stars)

Cách tính này cho giá trị trực quan hơn so với chỉ lấy xác suất của nhãn sao cao nhất.

## Kết quả đánh giá

| Metric | Giá trị |
|--------|---------|
| Accuracy | ≥ 95% |
| Test cases | 26 (16 cơ bản + 10 mở rộng) |
| Pass threshold | 95% |

## Hạn chế và hướng phát triển

**Hạn chế hiện tại:**
- Model đa ngôn ngữ chưa tối ưu cho tiếng Việt
- Phụ thuộc vào từ điển thủ công cho các trường hợp đặc biệt
- Chưa xử lý tốt các câu dài hoặc phức tạp

**Hướng phát triển:**
- Thay thế bằng model tiếng Việt (PhoBERT, ViSoBERT)
- Fine-tune trên tập dữ liệu tiếng Việt lớn hơn
- Tích hợp CI/CD với GitHub Actions

