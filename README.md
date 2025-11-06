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

## cach chay do an 
## .\.venv\Scripts\Activate.ps1 
## streamlit run app.py