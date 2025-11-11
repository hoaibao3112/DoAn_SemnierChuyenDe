# 🎭 Vietnamese Sentiment Assistant

## Giới thiệu

**Vietnamese Sentiment Assistant** là ứng dụng phân tích cảm xúc văn bản tiếng Việt sử dụng công nghệ Machine Learning tiên tiến. Dự án được xây dựng với mục tiêu phân loại tự động cảm xúc của người dùng thông qua các câu văn tiếng Việt, hỗ trợ doanh nghiệp và tổ chức hiểu rõ hơn về phản hồi của khách hàng.

### 🏆 Thành tựu chính

- ✅ **Độ chính xác cao**: Đạt **80% accuracy** trên bộ test 15 câu (vượt yêu cầu 65%)
- ✅ **Xử lý tiếng Việt tốt**: Hỗ trợ lỗi gõ, viết tắt và biến thể ngôn ngữ phổ biến
- ✅ **Giao diện thân thiện**: Web app đơn giản, dễ sử dụng với Streamlit
- ✅ **Lưu trữ lịch sử**: Database SQLite để tra cứu và phân tích sau
- ✅ **Hiệu năng tối ưu**: Pipeline được cache, phản hồi nhanh chóng

### 🎯 Tính năng

- 🔍 **Phân loại 3 cảm xúc**: **POSITIVE** (tích cực) / **NEUTRAL** (trung lập) / **NEGATIVE** (tiêu cực)
- 🤖 **Model AI mạnh mẽ**: `nlptown/bert-base-multilingual-uncased-sentiment` từ Hugging Face
- 💾 **Lưu trữ thông minh**: SQLite database với timestamp đầy đủ
- 🌐 **Giao diện web**: Streamlit UI hiện đại, responsive
- 📊 **Hiển thị lịch sử**: Xem 50 bản ghi phân loại mới nhất
- ⚡ **Tiền xử lý nâng cao**: Tự động sửa lỗi gõ, chuẩn hóa văn bản tiếng Việt
- ✅ **Test suite đầy đủ**: 15 test cases với confusion matrix chi tiết

### 📈 Kết quả đánh giá

```
Accuracy: 80.0% (12/15 test cases)

Confusion Matrix:
- POSITIVE: 5/6 đúng (83.3%)
- NEUTRAL:  4/4 đúng (100%)
- NEGATIVE: 3/5 đúng (60%)
```

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
├── app.py                     # Streamlit UI - Giao diện web chính
├── nlp.py                     # Hugging Face model logic với cached pipeline
├── preprocess.py              # Vietnamese text preprocessing (30+ typo mappings)
├── db.py                      # SQLite database handlers
├── test_runner.py             # Test suite runner với confusion matrix
├── eval_thresholds.py         # Script đánh giá threshold (optional)
├── tests/
│   └── test_cases.json        # 15 test cases đa dạng
├── requirements.txt           # Dependencies (streamlit, transformers, torch, pandas, underthesea)
├── README.md                  # Tài liệu này
├── SPEC.md                    # Tài liệu yêu cầu dự án
└── .gitignore                 # Git ignore rules
```

## 🎮 Cách chạy dự án

### Bước 1: Kích hoạt môi trường ảo
```powershell
.\.venv\Scripts\Activate.ps1
```

### Bước 2: Chạy ứng dụng web
```powershell
streamlit run app.py
```

Trình duyệt sẽ tự động mở tại `http://localhost:8501`

Lưu ý: Theo SPEC của đề bài, dự án này tuân theo quy tắc **score < 0.50 => NEUTRAL**. Vì vậy code mặc định hiện đang sử dụng ngưỡng trung lập `neutral_threshold = 0.50` để đảm bảo tính tương thích với yêu cầu chấm điểm.

### Bước 3: Kiểm tra độ chính xác (Optional)
```powershell
.\.venv\Scripts\python.exe test_runner.py
```

Kết quả mong đợi: **Accuracy ≥ 80%**

---

## 🛠️ Công nghệ sử dụng

### Backend & AI
- **Python 3.8+**: Ngôn ngữ lập trình chính
- **Transformers (Hugging Face)**: Thư viện AI/ML cho NLP
- **PyTorch**: Framework deep learning
- **nlptown/bert-base-multilingual-uncased-sentiment**: Pre-trained BERT model hỗ trợ đa ngôn ngữ
- **Underthesea**: Thư viện NLP tiếng Việt (word tokenization, optional)

### Frontend & Data
- **Streamlit**: Framework web app nhanh và đơn giản
- **SQLite**: Database nhẹ, không cần server
- **Pandas**: Xử lý và hiển thị dữ liệu dạng bảng

### Kiến trúc
- **Singleton Pattern**: Cache model pipeline để tăng tốc độ
- **Parameterized Queries**: Bảo mật SQL injection
- **Preprocessing Pipeline**: Chuẩn hóa văn bản đầu vào

---

## 💡 Ứng dụng thực tế

### 1. Phân tích phản hồi khách hàng
- Tự động phân loại review sản phẩm/dịch vụ
- Phát hiện khách hàng không hài lòng để xử lý kịp thời
- Thống kê xu hướng cảm xúc theo thời gian

### 2. Giám sát mạng xã hội
- Theo dõi phản ứng cộng đồng về thương hiệu
- Phát hiện crisis truyền thông sớm
- Đánh giá hiệu quả chiến dịch marketing

### 3. Hỗ trợ customer service
- Ưu tiên xử lý tin nhắn tiêu cực
- Phân loại ticket tự động
- Đo lường mức độ hài lòng khách hàng

### 4. Nghiên cứu thị trường
- Phân tích sentiment trong khảo sát
- Hiểu insight khách hàng
- So sánh với đối thủ cạnh tranh

---

## 🎓 Học hỏi từ dự án

### Kiến thức đạt được
- ✅ Sử dụng pre-trained models từ Hugging Face
- ✅ Xây dựng web app với Streamlit
- ✅ Xử lý ngôn ngữ tự nhiên tiếng Việt
- ✅ Thiết kế database và quản lý dữ liệu
- ✅ Testing và evaluation trong ML
- ✅ Git version control và GitHub workflow

### Kỹ năng phát triển
- 🔧 **NLP Engineering**: Preprocessing, model selection, threshold tuning
- 💻 **Full-stack Development**: Backend (Python) + Frontend (Streamlit) + Database (SQLite)
- 📊 **ML Evaluation**: Accuracy, confusion matrix, error analysis
- 📝 **Documentation**: README, code comments, SPEC

---