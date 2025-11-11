# GIẢI THÍCH CHI TIẾT LƯU ĐỒ XỬ LÝ CHI TIẾT

## Vietnamese Sentiment Assistant - Lưu Đồ Xử Lý Chi Tiết

### Mô tả tổng quan:
Lưu đồ mô tả quy trình xử lý phân loại cảm xúc từ lúc người dùng nhập câu tiếng Việt cho đến khi hiển thị kết quả và lưu vào cơ sở dữ liệu. Quy trình bao gồm 11 bước với 2 điểm kiểm tra (decision points) để đảm bảo tính chính xác và xử lý lỗi.

---

## CHI TIẾT TỪNG BƯỚC:

### **BƯỚC 1: BẮT ĐẦU** 
- **Hình dạng**: Hình Ellipse màu xanh lá
- **Mô tả**: Điểm khởi đầu của quy trình khi người dùng truy cập vào ứng dụng Streamlit
- **File liên quan**: `app.py`

---

### **BƯỚC 2: Nhập câu tiếng Việt**
- **Hình dạng**: Hình chữ nhật màu vàng nhạt (Input/Output)
- **Mô tả**: Người dùng nhập câu văn bản tiếng Việt vào ô text input trên giao diện
- **Ví dụ input**: 
  - "Hôm nay trời đẹp quá!"
  - "Dịch vụ tệ, nhân viên thái độ xấu"
- **File liên quan**: `app.py` - dòng `user_input = st.text_input()`

---

### **BƯỚC 3: DECISION POINT 1 - Kiểm tra độ dài**
- **Hình dạng**: Hình thoi màu vàng (Decision)
- **Điều kiện**: `len(text) >= 5?`
- **Mục đích**: Validation đầu vào để đảm bảo câu có ý nghĩa
- **File liên quan**: `app.py`

#### **Nhánh NO (< 5 ký tự):**
- **Đi đến**: BƯỚC 4A - st.error()
- **Hình dạng**: Hình chữ nhật màu đỏ nhạt
- **Xử lý**: 
  - Hiển thị thông báo lỗi: `st.error("⚠️ Vui lòng nhập ít nhất 5 ký tự!")`
  - **KHÔNG lưu vào database**
  - Chuyển thẳng đến BƯỚC 10 (Hiển thị lịch sử)
- **Lý do**: Câu quá ngắn không đủ ngữ cảnh để phân loại cảm xúc chính xác

#### **Nhánh YES (≥ 5 ký tự):**
- **Đi đến**: BƯỚC 5 - normalize_vi()
- **Tiếp tục**: Quy trình xử lý bình thường

---

### **BƯỚC 5: normalize_vi() - Tiền xử lý văn bản**
- **Hình dạng**: Hình chữ nhật màu xanh dương nhạt (Processing)
- **Chức năng**: Chuẩn hóa văn bản đầu vào
- **File liên quan**: `preprocess.py`
- **Các thao tác thực hiện**:
  1. **Lowercase**: Chuyển toàn bộ về chữ thường
     - Input: "Hôm Nay Trời ĐẸP Quá!"
     - Output: "hôm nay trời đẹp quá!"
  
  2. **Fix typos**: Sửa lỗi gõ phổ biến theo bảng mapping
     - "rat" → "rất"
     - "hom" → "hôm"
     - "ko" → "không"
     - "hnay" → "hôm nay"
     - "wa" → "quá"
     - "tot" → "tốt"
     - "dep" → "đẹp"
     - *(Tổng cộng 40+ mappings)*
  
  3. **Loại bỏ khoảng trắng thừa**:
     - Input: "món   ăn    rất   ngon"
     - Output: "món ăn rất ngon"
  
  4. **Giới hạn độ dài**: Cắt về tối đa 200 ký tự

- **Ví dụ**:
  - Input: "Hom nay mon an rat ngon!"
  - Output: "hôm nay món ăn rất ngon!"

---

### **BƯỚC 6: predict_sentiment() - Dự đoán cảm xúc**
- **Hình dạng**: Hình chữ nhật màu cam (Processing)
- **Chức năng**: Chạy model BERT để dự đoán cảm xúc
- **File liên quan**: `nlp.py`
- **Các thao tác thực hiện**:
  
  1. **Load pipeline cached**:
     - Gọi `get_sentiment_pipeline()` (đã cache, không tải lại model)
     - Model: `nlptown/bert-base-multilingual-uncased-sentiment`
  
  2. **Truncate text**: Giới hạn về 256 ký tự cho model
  
  3. **Run BERT model**:
     - Input: Văn bản đã chuẩn hóa
     - Output: 
       - `star_label`: "1 star", "2 stars", "3 stars", "4 stars", hoặc "5 stars"
       - `score`: Độ tin cậy (0.0 - 1.0)
  
  4. **Mapping stars → sentiment**:
     - 1-2 stars → `NEGATIVE`
     - 3 stars → `NEUTRAL`
     - 4-5 stars → `POSITIVE`

- **Ví dụ**:
  - Input: "hôm nay món ăn rất ngon!"
  - Model output: "4 stars", score = 0.72
  - Sentiment: `POSITIVE`

---

### **BƯỚC 7: DECISION POINT 2 - Kiểm tra threshold**
- **Hình dạng**: Hình thoi màu vàng (Decision)
- **Điều kiện**: `score < 0.35?`
- **Mục đích**: Đảm bảo độ tin cậy đủ cao trước khi kết luận cảm xúc
- **File liên quan**: `nlp.py`

#### **Nhánh YES (score < 0.35):**
- **Đi đến**: BƯỚC 8A - sentiment = NEUTRAL
- **Hình dạng**: Hình chữ nhật màu vàng
- **Lý do**: 
  - Độ tin cậy quá thấp (model không chắc chắn)
  - Ép về NEUTRAL để an toàn hơn
  - Tránh phân loại sai khi model không chắc chắn
- **Ví dụ**:
  - Sentiment gốc: POSITIVE, score = 0.32
  - Sau khi áp dụng threshold: NEUTRAL, score = 0.32

#### **Nhánh NO (score ≥ 0.35):**
- **Đi đến**: BƯỚC 8B - Giữ nguyên sentiment
- **Hình dạng**: Hình chữ nhật màu xanh lá nhạt
- **Xử lý**: 
  - Giữ nguyên sentiment từ mapping (POSITIVE/NEGATIVE/NEUTRAL)
  - Giữ nguyên score
- **Ví dụ**:
  - Sentiment: POSITIVE, score = 0.85
  - Kết quả: POSITIVE, score = 0.85 (không thay đổi)

---

### **BƯỚC 9: add_record() - Lưu vào SQLite**
- **Hình dạng**: Hình chữ nhật màu tím nhạt (Database operation)
- **Chức năng**: Lưu kết quả phân loại vào cơ sở dữ liệu
- **File liên quan**: `db.py`
- **Thông tin lưu trữ**:
  - `text`: Văn bản đã chuẩn hóa
  - `sentiment`: POSITIVE / NEUTRAL / NEGATIVE
  - `score`: Độ tin cậy (2 chữ số thập phân)
  - `timestamp`: Tự động thêm với format `YYYY-MM-DD HH:MM:SS`
  - `id`: Tự động tăng (AUTO_INCREMENT)

- **Bảng database**: `sentiments`
- **5 cột**:
  ```sql
  CREATE TABLE sentiments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      text TEXT NOT NULL,
      sentiment TEXT NOT NULL,
      score REAL NOT NULL,
      timestamp TEXT NOT NULL
  )
  ```

- **Bảo mật**: Sử dụng parameterized queries (`?`) để tránh SQL injection

- **Ví dụ bản ghi**:
  ```
  id: 1
  text: "hôm nay trời đẹp quá"
  sentiment: "POSITIVE"
  score: 0.60
  timestamp: "2025-11-07 14:30:25"
  ```

---

### **BƯỚC 10: st.success() - Hiển thị kết quả**
- **Hình dạng**: Hình chữ nhật màu xanh lá nhạt (Output)
- **Chức năng**: Hiển thị thông báo kết quả cho người dùng
- **File liên quan**: `app.py`
- **Hiển thị theo loại cảm xúc**:

  1. **POSITIVE**:
     ```python
     st.success(f"✅ Kết quả: **POSITIVE** (độ tin cậy: {score:.2f})")
     ```
     - Màu xanh lá
     - Icon ✅

  2. **NEGATIVE**:
     ```python
     st.error(f"❌ Kết quả: **NEGATIVE** (độ tin cậy: {score:.2f})")
     ```
     - Màu đỏ
     - Icon ❌

  3. **NEUTRAL**:
     ```python
     st.info(f"ℹ️ Kết quả: **NEUTRAL** (độ tin cậy: {score:.2f})")
     ```
     - Màu xanh dương
     - Icon ℹ️

- **Ví dụ**:
  - `✅ Kết quả: **POSITIVE** (độ tin cậy: 0.85)`

---

### **BƯỚC 11: list_latest(50) - Lấy lịch sử**
- **Hình dạng**: Hình chữ nhật màu xanh dương nhạt (Database operation)
- **Chức năng**: Truy vấn 50 bản ghi mới nhất từ database
- **File liên quan**: `db.py`
- **SQL query**:
  ```sql
  SELECT id, text, sentiment, score, timestamp 
  FROM sentiments 
  ORDER BY id DESC 
  LIMIT 50
  ```

- **Kết quả**: List of tuples `[(id, text, sentiment, score, timestamp), ...]`

---

### **BƯỚC 12: Hiển thị bảng lịch sử**
- **Hình dạng**: Hình chữ nhật màu xanh dương nhạt (Output)
- **Chức năng**: Hiển thị bảng lịch sử 50 bản ghi mới nhất
- **File liên quan**: `app.py`
- **Định dạng bảng**:
  - **ID**: Số thứ tự (số nguyên)
  - **Text**: Câu văn bản đã phân loại
  - **Sentiment**: POSITIVE / NEUTRAL / NEGATIVE
  - **Score**: Độ tin cậy (2 chữ số thập phân)
  - **Time**: Timestamp định dạng `YYYY-MM-DD HH:MM:SS`

- **Sắp xếp**: Mới nhất lên đầu (DESC by id)

- **Ví dụ bảng**:
  ```
  ┌────┬─────────────────────────┬───────────┬───────┬─────────────────────┐
  │ ID │         Text            │ Sentiment │ Score │        Time         │
  ├────┼─────────────────────────┼───────────┼───────┼─────────────────────┤
  │ 13 │ hôm nay trời đẹp quá    │ POSITIVE  │ 0.55  │ 2025-11-06 22:39:45 │
  │ 12 │ hôm nay trời đẹp quá    │ POSITIVE  │ 0.55  │ 2025-11-06 13:53:40 │
  │ 11 │ ádfghjk                 │ NEUTRAL   │ 0.29  │ 2025-11-06 13:51:01 │
  └────┴─────────────────────────┴───────────┴───────┴─────────────────────┘
  ```

---

### **BƯỚC 13: KẾT THÚC**
- **Hình dạng**: Hình Ellipse màu đỏ nhạt
- **Mô tả**: Kết thúc một vòng lặp xử lý
- **Hành động tiếp theo**:
  - Người dùng có thể nhập câu mới (quay lại BƯỚC 2)
  - Hoặc nhấn nút "🔄 Tải lại lịch sử" để refresh bảng
  - Hoặc đóng ứng dụng

---

## TỔNG KẾT QUY TRÌNH:

### Luồng chính (Happy path):
```
BẮT ĐẦU 
  → Nhập câu 
  → Kiểm tra len >= 5 [YES] 
  → normalize_vi() 
  → predict_sentiment() 
  → Kiểm tra score >= 0.35 [YES] 
  → Giữ sentiment 
  → add_record() 
  → st.success() 
  → list_latest(50) 
  → Hiển thị bảng 
  → KẾT THÚC
```

### Luồng lỗi (Error path):
```
BẮT ĐẦU 
  → Nhập câu 
  → Kiểm tra len >= 5 [NO] 
  → st.error() 
  → list_latest(50) 
  → Hiển thị bảng 
  → KẾT THÚC
```

### Luồng threshold (Low confidence):
```
... 
  → predict_sentiment() 
  → Kiểm tra score >= 0.35 [NO] 
  → sentiment = NEUTRAL 
  → add_record() 
  ...
```

---

## CÁC ĐIỂM QUYẾT ĐỊNH (DECISION POINTS):

### 1. **Validation Input** (`len(text) >= 5?`)
- **Vị trí**: Sau khi nhập liệu
- **Mục đích**: Đảm bảo input đủ dài để phân loại
- **Impact**: 
  - YES → Tiếp tục xử lý
  - NO → Báo lỗi, không lưu DB

### 2. **Threshold Check** (`score < 0.35?`)
- **Vị trí**: Sau khi dự đoán
- **Mục đích**: Đảm bảo độ tin cậy đủ cao
- **Impact**:
  - YES → Ép về NEUTRAL (an toàn)
  - NO → Giữ nguyên sentiment từ model

---

## CÁC FILE PYTHON LIÊN QUAN:

1. **app.py**: 
   - BƯỚC 2 (Input)
   - BƯỚC 3 (Validation)
   - BƯỚC 4A (Error)
   - BƯỚC 10 (Success)
   - BƯỚC 12 (Display)

2. **preprocess.py**:
   - BƯỚC 5 (normalize_vi)

3. **nlp.py**:
   - BƯỚC 6 (predict_sentiment)
   - BƯỚC 7 (Threshold logic)
   - BƯỚC 8A, 8B (Apply threshold)

4. **db.py**:
   - BƯỚC 9 (add_record)
   - BƯỚC 11 (list_latest)

---

## ĐẶC ĐIỂM KỸ THUẬT:

### Performance:
- Pipeline cached → Không load model mỗi lần
- SQLite indexed → Truy vấn nhanh
- Limit 50 records → Không quá tải UI

### Security:
- Parameterized queries → Tránh SQL injection
- Input validation → Tránh input rỗng/spam

### Robustness:
- Error handling → try/except blocks
- Threshold logic → Tránh false positive
- Typo correction → Tăng accuracy

### Scalability:
- Singleton pattern → Memory efficient
- Database indexed → Query nhanh với nhiều records

---

## SO SÁNH VỚI RUBRIC:

✅ **Mục 3.1 (Xử lý lỗi nhập liệu)**: 
   - Có validation len >= 5
   - Hiển thị lỗi rõ ràng
   
✅ **Mục 3.2 (Phản hồi tự nhiên qua giao diện)**:
   - st.success/error/info theo từng loại
   - Icon và màu sắc phù hợp

✅ **Mục 4 (Lưu trữ lịch sử)**:
   - SQLite parameterized
   - 5 cột đầy đủ
   - Timestamp chính xác

---

**Ghi chú**: Sơ đồ này thể hiện đầy đủ quy trình xử lý thực tế trong code, 
bao gồm cả các trường hợp lỗi và logic điều kiện phức tạp.
