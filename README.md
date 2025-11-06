# Vietnamese Sentiment Assistant

Ứng dụng phân loại cảm xúc tiếng Việt sử dụng Hugging Face Transformers và Streamlit.

## 🎯 Tính năng

- ✅ Phân loại cảm xúc: **POSITIVE** / **NEUTRAL** / **NEGATIVE**
- ✅ Model: `nlptown/bert-base-multilingual-uncased-sentiment`
- ✅ Lưu lịch sử vào SQLite
- ✅ Giao diện đơn giản với Streamlit
- ✅ Độ chính xác ≥ 65% trên test cases

## 📋 Yêu cầu hệ thống

- Python 3.8+
- pip

## 🚀 Cài đặt

### Windows (PowerShell)

```powershell
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt
```

### Linux/macOS

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
source .venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

## 📦 Cấu trúc dự án

```
DoAnSemnierChuyenDe/
├── app.py                  # Streamlit UI
├── nlp.py                  # Hugging Face model logic
├── preprocess.py           # Vietnamese text preprocessing
├── db.py                   # SQLite database handlers
├── test_runner.py          # Test suite runner
├── tests/
│   └── test_cases.json     # 10 test cases
├── requirements.txt        # Dependencies
├── README.md              # This file
└── SPEC.md                # Project specification
```

## 🎮 Sử dụng

### Chạy ứng dụng web

```powershell
streamlit run app.py
```

Trình duyệt sẽ tự động mở tại `http://localhost:8501`

### Chạy test suite

```powershell
python test_runner.py
```

Kết quả:
- In ra accuracy (%)
- Confusion matrix
- Exit code 0 nếu accuracy ≥ 65%, ngược lại exit code 1

## 📊 Database Schema

SQLite database: `sentiments.db`

Bảng `sentiments`:
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
- `text` (TEXT NOT NULL) - Văn bản đã chuẩn hóa
- `sentiment` (TEXT NOT NULL) - POSITIVE/NEUTRAL/NEGATIVE
- `score` (REAL NOT NULL) - Độ tin cậy (0.0 - 1.0)
- `timestamp` (TEXT NOT NULL) - Format: YYYY-MM-DD HH:MM:SS

## 🧪 Test Cases

File `tests/test_cases.json` chứa 10 test cases tiếng Việt với cảm xúc đa dạng:
- 4 POSITIVE
- 3 NEUTRAL
- 3 NEGATIVE

## 🛠️ Kỹ thuật

### Model
- **nlptown/bert-base-multilingual-uncased-sentiment**
- Mapping: 1-2★ → NEGATIVE, 3★ → NEUTRAL, 4-5★ → POSITIVE
- Threshold: Score < 0.50 → ép về NEUTRAL

### Tiền xử lý
- Lowercase
- Loại bỏ khoảng trắng thừa
- Sửa lỗi gõ phổ biến: `rat`→`rất`, `hom`→`hôm`, `ko`→`không`, etc.
- Giới hạn độ dài: 200 ký tự (input), 256 ký tự (model)

### Validation
- Input tối thiểu: 5 ký tự
- Hiển thị lỗi với `st.error()` nếu không hợp lệ
- Không lưu vào DB nếu input không hợp lệ

## 📝 Checklist chất lượng

- [x] App chạy không lỗi với `streamlit run app.py`
- [x] UI có đủ: input, button, label kết quả, bảng lịch sử
- [x] Validation input < 5 ký tự
- [x] Database có đúng 5 cột với timestamp đúng format
- [x] Pipeline được cache (singleton pattern)
- [x] Test runner đạt accuracy ≥ 65%
- [x] README có hướng dẫn đầy đủ

## 🔧 Troubleshooting

### Lỗi khi tải model
```
Error: Could not load model...
```
**Giải pháp**: Kiểm tra kết nối internet, model sẽ tự động download lần đầu (~500MB)

### Lỗi PowerShell execution policy
```
cannot be loaded because running scripts is disabled
```
**Giải pháp**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Lỗi thiếu module
```
ModuleNotFoundError: No module named 'streamlit'
```
**Giải pháp**: Đảm bảo đã activate virtual environment và chạy `pip install -r requirements.txt`

## 📄 License

MIT License - Dự án học tập cho môn Seminar Chuyên Đề

## 👥 Tác giả

Dự án được xây dựng theo SPEC.md với sự hỗ trợ của GitHub Copilot
