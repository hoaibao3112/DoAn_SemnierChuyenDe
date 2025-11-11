# 📊 TÓM TẮT: ĐÃ TẠO 2 SƠ ĐỒ CHO BÁO CÁO

## ✅ Đã hoàn thành:

### 1. **Sơ đồ khối (Block Diagram)**
   - File: `docs/block_diagram_simple.png`
   - Kích thước: 10x12 inches
   - Resolution: 300 DPI (chất lượng in)
   - Mô tả 6 thành phần chính của hệ thống

### 2. **Flowchart (Lưu đồ chi tiết)**
   - File: `docs/flowchart_simple.png`
   - Kích thước: 10x16 inches
   - Resolution: 300 DPI
   - Mô tả 9 bước xử lý với 2 decision points

---

## 📂 Cấu trúc files đã tạo:

```
DoAnSemnierChuyenDe/
├── docs/
│   ├── block_diagram_simple.png       ← SƠ ĐỒ KHỐI
│   ├── flowchart_simple.png           ← FLOWCHART
│   ├── DIAGRAM_GUIDE.md               ← Hướng dẫn chi tiết cách vẽ
│   └── HUONG_DAN_SU_DUNG.md          ← Cách chèn vào Word
├── generate_diagrams.py               ← Script vẽ bằng graphviz (nâng cao)
└── generate_diagrams_simple.py        ← Script vẽ bằng matplotlib (đơn giản)
```

---

## 🎯 Cách sử dụng NHANH:

### Bước 1: Mở file báo cáo Word

### Bước 2: Chèn sơ đồ vào mục "3. Thiết kế hệ thống"

**Mục 3.1 - Sơ đồ khối:**
1. Insert → Pictures → Chọn `docs/block_diagram_simple.png`
2. Add caption: "Hình 3.1: Sơ đồ khối kiến trúc hệ thống"
3. Giải thích 6 thành phần (xem file `HUONG_DAN_SU_DUNG.md`)

**Mục 3.2 - Flowchart:**
1. Insert → Pictures → Chọn `docs/flowchart_simple.png`
2. Add caption: "Hình 3.2: Lưu đồ chi tiết quá trình phân loại cảm xúc"
3. Giải thích 9 bước (xem file `HUONG_DAN_SU_DUNG.md`)

### Bước 3: Đọc file hướng dẫn chi tiết

Mở và đọc: `docs/HUONG_DAN_SU_DUNG.md`
- Có sẵn đoạn text để copy vào báo cáo
- Có giải thích chi tiết từng thành phần/bước
- Có mẹo format đẹp trong Word

---

## 📖 Nội dung 2 sơ đồ:

### SƠ ĐỒ KHỐI (6 thành phần):

1. **Giao diện người dùng** (Frontend)
   - Streamlit UI, Text Input, Buttons, Data Table

2. **Tiền xử lý văn bản** (Preprocessing)
   - preprocess.py: lowercase, typo correction, tokenization

3. **Mô hình NLP** (Transformer)
   - nlp.py: BERT multilingual, Pipeline cached, nlptown/bert-base

4. **Xử lý kết quả** (Post-processing)
   - Threshold logic: if score < 0.35 → NEUTRAL

5. **Lưu trữ dữ liệu** (Database)
   - db.py: SQLite, 5 columns, Timestamp

6. **Hiển thị kết quả** (Output)
   - st.success/error, Label + Score, History table (50)

### FLOWCHART (9 bước + 2 decisions):

1. **Bắt đầu** → Người dùng nhập câu
2. **Decision 1**: len(text) >= 5?
   - NO → st.error() → Hiển thị lịch sử → Kết thúc
   - YES → Tiếp tục
3. **normalize_vi()** - Chuẩn hóa văn bản
4. **predict_sentiment()** - Chạy model BERT
5. **Decision 2**: score < 0.35?
   - YES → sentiment = NEUTRAL
   - NO → Giữ nguyên sentiment
6. **add_record()** - Lưu vào SQLite
7. **st.success()** - Hiển thị kết quả
8. **list_latest(50)** - Lấy lịch sử
9. **Hiển thị bảng** → Kết thúc

---

## 🔧 Nếu cần chỉnh sửa:

### Cách 1: Chạy lại script Python
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Chạy lại script tạo sơ đồ
.\.venv\Scripts\python.exe generate_diagrams_simple.py
```

### Cách 2: Vẽ lại bằng công cụ khác
- **draw.io**: https://app.diagrams.net/ (miễn phí)
- **PowerPoint**: Insert → Shapes
- **Lucidchart**: https://www.lucidchart.com/ (có free tier)

Xem chi tiết trong file `docs/DIAGRAM_GUIDE.md`

---

## 📊 Mapping với Rubric:

Việc có 2 sơ đồ này giúp bạn đạt điểm trong các mục:

- ✅ **Mục 3 (Xử lý ngôn ngữ VN)**: 
  - Sơ đồ thể hiện rõ module preprocess.py
  - Flowchart cho thấy logic xử lý lỗi nhập liệu

- ✅ **Mục 5 (Báo cáo & mã nguồn)**:
  - Báo cáo khoa học đầy đủ với sơ đồ minh họa (+0.25đ)
  - Mã nguồn sạch, có tài liệu kỹ thuật

---

## ✅ CHECKLIST:

- [x] Đã tạo sơ đồ khối (block_diagram_simple.png)
- [x] Đã tạo flowchart (flowchart_simple.png)
- [x] Đã tạo file hướng dẫn chi tiết (HUONG_DAN_SU_DUNG.md)
- [x] Đã tạo file giải thích kỹ thuật (DIAGRAM_GUIDE.md)
- [ ] **Bạn cần làm**: Chèn 2 ảnh vào báo cáo Word
- [ ] **Bạn cần làm**: Thêm giải thích văn bản (copy từ HUONG_DAN_SU_DUNG.md)

---

## 💡 LỜI KHUYÊN:

1. **Đọc kỹ file `HUONG_DAN_SU_DUNG.md`** trước khi chèn vào Word
2. **Copy đoạn text giải thích** có sẵn vào báo cáo (không cần viết lại)
3. **Căn giữa ảnh** và thêm caption đúng format
4. **Tham chiếu** đến hình khi viết văn bản: "Như thể hiện trong Hình 3.1..."

---

**Chúc bạn thành công! 🎓**

Nếu cần hỗ trợ thêm về sơ đồ hoặc báo cáo, cứ hỏi tôi!
