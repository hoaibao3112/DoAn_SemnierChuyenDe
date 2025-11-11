# Hướng dẫn vẽ 2 Sơ đồ cho Báo cáo Đồ án

## 1. SƠ ĐỒ KHỐI (Block Diagram) - Kiến trúc tổng quát

### Mục đích:
Mô tả kiến trúc tổng thể của hệ thống, các thành phần chính và cách chúng kết nối.

### Các thành phần (Blocks):

```
┌─────────────────────────────────────────────────────────────┐
│                   VIETNAMESE SENTIMENT ASSISTANT             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│  1. GIAO DIỆN   │ ← Streamlit UI
│   NGƯỜI DÙNG    │   - Text Input
│  (Frontend)     │   - Buttons
│                 │   - Data Table
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. TIỀN XỬ LÝ  │ ← preprocess.py
│   VĂN BẢN       │   - Lowercase
│ (Preprocessing) │   - Typo correction
│                 │   - Tokenization
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. MÔ HÌNH NLP │ ← nlp.py
│  (Transformer)  │   - Pipeline cached
│                 │   - BERT multilingual
│  nlptown/bert   │   - Star → Sentiment
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. XỬ LÝ KẾT  │ ← Logic threshold
│     QUẢ         │   - if score < 0.35
│ (Post-process)  │     → NEUTRAL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. LƯU TRỮ DỮ │ ← db.py
│     LIỆU        │   - SQLite
│   (Database)    │   - 5 columns
│                 │   - Timestamp
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. HIỂN THỊ    │ ← Streamlit UI
│   KẾT QUẢ       │   - Label + Score
│                 │   - History (50)
└─────────────────┘
```

### Cách vẽ trong draw.io hoặc PowerPoint:

**Bước 1:** Tạo 6 hình chữ nhật (Rectangle) đại diện cho 6 khối:
1. **Giao diện người dùng** (màu xanh dương nhạt)
2. **Tiền xử lý văn bản** (màu xanh lá nhạt)
3. **Mô hình NLP** (màu cam)
4. **Xử lý kết quả** (màu vàng)
5. **Lưu trữ dữ liệu** (màu tím nhạt)
6. **Hiển thị kết quả** (màu xanh dương nhạt)

**Bước 2:** Vẽ mũi tên (Arrow) nối các khối theo thứ tự 1→2→3→4→5→6

**Bước 3:** Thêm text mô tả bên cạnh mỗi khối:
- Giao diện: "Streamlit UI, Text Input, Buttons"
- Tiền xử lý: "preprocess.py, Lowercase, Typo fix"
- Mô hình: "nlp.py, BERT, Pipeline cached"
- Xử lý KQ: "Threshold logic (0.35)"
- Database: "db.py, SQLite, 5 cột"
- Hiển thị: "st.success/error, History table"

**Bước 4:** Thêm viền khung bao quanh toàn bộ với tiêu đề "Vietnamese Sentiment Assistant"

---

## 2. FLOWCHART (Lưu đồ chi tiết) - Luồng xử lý

### Mục đích:
Mô tả chi tiết từng bước xử lý, bao gồm các điều kiện logic và quyết định.

### Các ký hiệu chuẩn:
- **Oval (Hình bầu dục)**: Bắt đầu/Kết thúc
- **Rectangle (Hình chữ nhật)**: Xử lý/Hành động
- **Diamond (Hình thoi)**: Điều kiện/Quyết định
- **Parallelogram (Hình bình hành)**: Input/Output
- **Arrow (Mũi tên)**: Luồng dữ liệu

### Lưu đồ chi tiết:

```
        ┌─────────────┐
        │   BẮT ĐẦU   │ (Oval - màu xanh)
        └──────┬──────┘
               │
               ▼
    ┌──────────────────────┐
    │  Người dùng nhập câu │ (Parallelogram - Input)
    │   tiếng Việt (text)  │
    └──────────┬───────────┘
               │
               ▼
         ┌─────────┐
         │ len(text)│◄─────── (Diamond - Decision)
         │  >= 5?  │
         └────┬────┘
              │
      ┌───────┴───────┐
      │ NO            │ YES
      ▼               ▼
┌──────────┐    ┌──────────────────┐
│st.error()│    │ normalize_vi()   │ (Rectangle)
│"Nhập ít  │    │ - Lowercase      │
│nhất 5 ký │    │ - Fix typos      │
│tự"       │    │ - Tokenize       │
└────┬─────┘    └────────┬─────────┘
     │                   │
     │                   ▼
     │          ┌──────────────────┐
     │          │predict_sentiment()│ (Rectangle)
     │          │ - Load pipeline  │
     │          │ - Run model      │
     │          │ - Get label+score│
     │          └────────┬─────────┘
     │                   │
     │                   ▼
     │            ┌──────────┐
     │            │ score <  │◄─────── (Diamond)
     │            │  0.35?   │
     │            └─────┬────┘
     │                  │
     │          ┌───────┴────────┐
     │          │ YES            │ NO
     │          ▼                ▼
     │    ┌──────────┐    ┌────────────┐
     │    │ sentiment│    │Keep original│
     │    │= NEUTRAL │    │  sentiment  │
     │    └─────┬────┘    └──────┬─────┘
     │          │                │
     │          └────────┬───────┘
     │                   │
     │                   ▼
     │          ┌──────────────────┐
     │          │  add_record()    │ (Rectangle)
     │          │  - Lưu vào SQLite│
     │          │  - Timestamp     │
     │          └────────┬─────────┘
     │                   │
     │                   ▼
     │          ┌──────────────────┐
     │          │  st.success()    │ (Parallelogram - Output)
     │          │ Hiển thị kết quả:│
     │          │ Label + Score    │
     │          └────────┬─────────┘
     │                   │
     └───────────────────┤
                         │
                         ▼
                ┌──────────────────┐
                │ list_latest(50)  │ (Rectangle)
                │ Lấy lịch sử từ DB│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Hiển thị bảng   │ (Parallelogram - Output)
                │   lịch sử 50     │
                │   bản ghi        │
                └────────┬─────────┘
                         │
                         ▼
                    ┌─────────┐
                    │ KẾT THÚC│ (Oval)
                    └─────────┘
```

### Cách vẽ trong draw.io:

**Bước 1:** Chọn các shape chuẩn:
- Oval cho "Bắt đầu" và "Kết thúc"
- Rectangle cho các bước xử lý
- Diamond cho điều kiện IF
- Parallelogram cho Input/Output

**Bước 2:** Sắp xếp theo chiều dọc từ trên xuống:
1. **Oval**: "Bắt đầu"
2. **Parallelogram**: "Người dùng nhập câu"
3. **Diamond**: "len(text) >= 5?"
   - Nhánh NO → Rectangle "st.error()"
   - Nhánh YES → tiếp tục
4. **Rectangle**: "normalize_vi(text)"
5. **Rectangle**: "predict_sentiment()"
6. **Diamond**: "score < 0.35?"
   - YES → "sentiment = NEUTRAL"
   - NO → "Keep sentiment"
7. **Rectangle**: "add_record() - Lưu DB"
8. **Parallelogram**: "st.success() - Hiển thị"
9. **Rectangle**: "list_latest(50)"
10. **Parallelogram**: "Hiển thị bảng lịch sử"
11. **Oval**: "Kết thúc"

**Bước 3:** Vẽ mũi tên nối các bước

**Bước 4:** Tô màu theo logic:
- Màu xanh lá: Input/Processing
- Màu vàng: Decision (Diamond)
- Màu đỏ nhạt: Error
- Màu xanh dương: Output

---

## 3. Công cụ đề xuất để vẽ

### Option 1: **draw.io** (Miễn phí, online/offline)
- Link: https://app.diagrams.net/
- Ưu điểm: Miễn phí, dễ dùng, export PNG/PDF/SVG
- Cách dùng:
  1. Mở link
  2. Chọn "Create New Diagram"
  3. Kéo thả các shape từ sidebar bên trái
  4. File → Export as → PNG (chọn độ phân giải 300 DPI)

### Option 2: **Microsoft PowerPoint**
- Ưu điểm: Quen thuộc, có sẵn trong Office
- Cách dùng:
  1. Insert → Shapes
  2. Chọn Rectangle, Oval, Diamond
  3. Insert → Text box để thêm text
  4. Save as → PDF hoặc PNG

### Option 3: **Lucidchart** (Online, có free tier)
- Link: https://www.lucidchart.com/
- Ưu điểm: Templates có sẵn, đẹp professional
- Giới hạn: Free chỉ 3 documents

### Option 4: **Visual Paradigm Online** (Free)
- Link: https://online.visual-paradigm.com/
- Ưu điểm: Templates flowchart chuẩn

---

## 4. Checklist sau khi vẽ xong

### Sơ đồ khối:
- [ ] Có đầy đủ 6 khối chính
- [ ] Mũi tên chỉ rõ hướng luồng dữ liệu
- [ ] Mỗi khối có tên file Python tương ứng (app.py, nlp.py, db.py...)
- [ ] Có tiêu đề "Sơ đồ khối hệ thống Vietnamese Sentiment Assistant"
- [ ] Font chữ rõ ràng (Arial/Calibri size 10-12)

### Flowchart:
- [ ] Bắt đầu bằng Oval
- [ ] Kết thúc bằng Oval
- [ ] Tất cả Decision (Diamond) có 2 nhánh YES/NO rõ ràng
- [ ] Logic threshold (score < 0.35) được thể hiện
- [ ] Có bước validation (len >= 5)
- [ ] Có bước lưu DB và hiển thị
- [ ] Font chữ rõ ràng, mũi tên không chồng chéo

---

## 5. Đặt sơ đồ vào báo cáo

Trong file Word báo cáo của bạn:

**Mục 3.1 - Sơ đồ khối:**
```
3.1. Sơ đồ khối hệ thống

Hệ thống Vietnamese Sentiment Assistant bao gồm 6 thành phần chính:

[Chèn ảnh sơ đồ khối ở đây]

Hình 3.1: Sơ đồ khối kiến trúc hệ thống

Giải thích:
1. Giao diện người dùng: Sử dụng Streamlit framework...
2. Tiền xử lý văn bản: Module preprocess.py thực hiện...
3. Mô hình NLP: Sử dụng BERT multilingual từ Hugging Face...
...
```

**Mục 3.2 - Flowchart:**
```
3.2. Lưu đồ xử lý chi tiết

Luồng xử lý phân loại cảm xúc được thực hiện qua các bước sau:

[Chèn ảnh flowchart ở đây]

Hình 3.2: Lưu đồ chi tiết quá trình phân loại cảm xúc

Chi tiết các bước:
- Bước 1: Người dùng nhập câu tiếng Việt vào text input...
- Bước 2: Kiểm tra độ dài >= 5 ký tự...
- Bước 3: Chuẩn hóa văn bản bằng normalize_vi()...
...
```

---

## 6. Tôi có thể tạo code Python vẽ tự động không?

Có! Tôi có thể tạo script Python dùng thư viện `graphviz` hoặc `matplotlib` để tự động vẽ. Bạn có muốn không?

Nếu muốn, chạy:
```powershell
pip install graphviz
python generate_diagrams.py
```

Sẽ tạo ra 2 file PNG chất lượng cao ngay lập tức!
