# 📊 HƯỚNG DẪN SỬ DỤNG 2 SƠ ĐỒ CHO BÁO CÁO

## ✅ Đã hoàn thành tự động:

Tôi đã tạo sẵn 2 file sơ đồ PNG chất lượng cao trong thư mục `docs/`:

1. **`docs/block_diagram_simple.png`** - Sơ đồ khối hệ thống
2. **`docs/flowchart_simple.png`** - Lưu đồ xử lý chi tiết

---

## 📝 CÁCH CHÈN VÀO BÁO CÁO WORD

### Bước 1: Mở file báo cáo Word của bạn

### Bước 2: Đi tới mục "3. THIẾT KẾ HỆ THỐNG"

### Bước 3: Chèn Sơ đồ khối

Tại mục **3.1. Sơ đồ khối hệ thống**, gõ:

```
3.1. Sơ đồ khối hệ thống

Hệ thống Vietnamese Sentiment Assistant được thiết kế theo kiến trúc 
phân lớp với 6 thành phần chính, mỗi thành phần đảm nhiệm một nhiệm vụ 
cụ thể trong quy trình phân loại cảm xúc:

[Nhấn Enter và chèn ảnh ở đây]
```

**Cách chèn ảnh:**
1. Đặt con trỏ ở vị trí cần chèn
2. Ribbon menu → **Insert** → **Pictures** → **This Device**
3. Chọn file: `C:\Users\PC\Desktop\DoAnSemnierChuyenDe\docs\block_diagram_simple.png`
4. Nhấn **Insert**
5. Click chuột phải vào ảnh → **Wrap Text** → **In Line with Text**
6. Resize ảnh cho vừa trang (kéo góc để giữ tỷ lệ)

**Thêm caption cho ảnh:**
- Click chuột phải vào ảnh → **Insert Caption**
- Caption: `Hình 3.1: Sơ đồ khối kiến trúc hệ thống`
- Position: Below selected item
- Nhấn OK

**Giải thích từng thành phần** (gõ sau ảnh):

```
Giải thích chi tiết các thành phần:

1. Giao diện người dùng (Frontend):
   - Sử dụng framework Streamlit để xây dựng giao diện web
   - Cung cấp ô nhập liệu (text input) để người dùng nhập câu tiếng Việt
   - Nút "Phân loại cảm xúc" để kích hoạt quá trình xử lý
   - Bảng hiển thị lịch sử 50 bản ghi phân loại gần nhất

2. Tiền xử lý văn bản (Preprocessing):
   - Module preprocess.py thực hiện chuẩn hóa văn bản đầu vào
   - Chuyển toàn bộ chữ về lowercase để đồng nhất
   - Sửa các lỗi gõ phổ biến (rat→rất, ko→không, hom→hôm...)
   - Tokenization tùy chọn với thư viện underthesea

3. Mô hình NLP (Transformer):
   - Module nlp.py quản lý mô hình BERT multilingual
   - Sử dụng pipeline từ Hugging Face Transformers
   - Model: nlptown/bert-base-multilingual-uncased-sentiment
   - Pipeline được cache (singleton pattern) để tối ưu hiệu năng
   - Dự đoán cảm xúc dựa trên thang điểm 1-5 sao

4. Xử lý kết quả (Post-processing):
   - Áp dụng logic threshold: nếu score < 0.35 → ép về NEUTRAL
   - Mapping từ thang điểm sao sang 3 nhãn:
     • 1-2 sao → NEGATIVE
     • 3 sao → NEUTRAL  
     • 4-5 sao → POSITIVE

5. Lưu trữ dữ liệu (Database):
   - Module db.py quản lý SQLite database
   - Lưu trữ 5 cột: id, text, sentiment, score, timestamp
   - Sử dụng parameterized queries để tránh SQL injection
   - Timestamp format: YYYY-MM-DD HH:MM:SS

6. Hiển thị kết quả (Output):
   - Hiển thị nhãn cảm xúc (POSITIVE/NEUTRAL/NEGATIVE) 
   - Hiển thị độ tin cậy (confidence score) với 2 chữ số thập phân
   - Bảng lịch sử 50 bản ghi mới nhất với đầy đủ thông tin
```

---

### Bước 4: Chèn Flowchart

Tại mục **3.2. Lưu đồ xử lý chi tiết**, gõ:

```
3.2. Lưu đồ xử lý chi tiết

Quy trình phân loại cảm xúc được thực hiện qua các bước tuần tự sau,
bao gồm cả xử lý lỗi và logic điều kiện:

[Nhấn Enter và chèn ảnh ở đây]
```

**Chèn ảnh tương tự bước 3:**
- Insert → Pictures → Chọn `flowchart_simple.png`
- Caption: `Hình 3.2: Lưu đồ chi tiết quá trình phân loại cảm xúc`

**Giải thích từng bước** (gõ sau ảnh):

```
Chi tiết các bước trong lưu đồ:

Bước 1: Khởi động và nhập liệu
   - Người dùng truy cập giao diện Streamlit
   - Nhập câu tiếng Việt vào ô text input
   - Nhấn nút "Phân loại cảm xúc"

Bước 2: Kiểm tra validation (Decision Point)
   - Điều kiện: len(text) >= 5?
   - Nếu NO (< 5 ký tự):
     • Hiển thị lỗi: st.error("Vui lòng nhập ít nhất 5 ký tự")
     • Không lưu vào database
     • Chuyển trực tiếp đến hiển thị lịch sử
   - Nếu YES (>= 5 ký tự):
     • Tiếp tục xử lý

Bước 3: Chuẩn hóa văn bản (normalize_vi)
   - Chuyển toàn bộ về lowercase
   - Thay thế các lỗi gõ phổ biến theo bảng mapping:
     rat → rất, hom → hôm, ko → không, etc.
   - Loại bỏ khoảng trắng thừa
   - Giới hạn độ dài tối đa 200 ký tự

Bước 4: Dự đoán cảm xúc (predict_sentiment)
   - Lấy pipeline đã cache (get_sentiment_pipeline)
   - Truncate text về 256 ký tự cho model
   - Chạy BERT model để dự đoán
   - Output: star_label (1-5 stars) và confidence score

Bước 5: Áp dụng threshold logic (Decision Point)
   - Điều kiện: score < 0.35?
   - Nếu YES (độ tin cậy thấp):
     • sentiment = NEUTRAL (an toàn hơn)
   - Nếu NO (độ tin cậy đủ):
     • Giữ nguyên sentiment từ mapping:
       1-2 sao → NEGATIVE
       3 sao → NEUTRAL
       4-5 sao → POSITIVE

Bước 6: Lưu vào database (add_record)
   - Gọi hàm db.add_record(text, sentiment, score)
   - Tự động thêm timestamp hiện tại
   - Lưu vào bảng sentiments với 5 cột
   - Sử dụng parameterized query để bảo mật

Bước 7: Hiển thị kết quả (st.success)
   - Nếu POSITIVE: Hiển thị màu xanh lá với icon ✅
   - Nếu NEGATIVE: Hiển thị màu đỏ với icon ❌
   - Nếu NEUTRAL: Hiển thị màu xanh dương với icon ℹ️
   - Format: "Kết quả: {sentiment} (độ tin cậy: {score:.2f})"

Bước 8: Lấy và hiển thị lịch sử (list_latest)
   - Gọi db.list_latest(50) để lấy 50 bản ghi mới nhất
   - Sắp xếp theo id giảm dần (DESC)
   - Hiển thị bảng với 5 cột: ID, Text, Sentiment, Score, Time

Bước 9: Kết thúc
   - Người dùng có thể nhập câu mới (quay lại bước 1)
   - Hoặc nhấn nút "Tải lại lịch sử" để refresh bảng
```

---

## 🎯 MẸO ĐỂ BÁO CÁO ĐẸP HƠN

### 1. Định dạng ảnh trong Word:

- **Căn giữa ảnh:**
  - Click vào ảnh → Home tab → Align Center
  
- **Thêm viền:**
  - Click ảnh → Picture Format → Picture Border
  - Chọn màu xám nhạt, độ dày 1pt

- **Tăng độ rõ nét:**
  - Ảnh đã có resolution 300 DPI (chất lượng cao)
  - Không scale lên quá 100% để giữ độ nét

### 2. Đánh số và tham chiếu:

Khi viết văn bản, tham chiếu đến sơ đồ:

```
"Như thể hiện trong Hình 3.1, kiến trúc hệ thống bao gồm 6 thành phần..."

"Quy trình xử lý được mô tả chi tiết trong Hình 3.2, bắt đầu từ..."
```

### 3. Font chữ và kích thước:

- Tiêu đề mục: **Times New Roman, 14pt, Bold**
- Nội dung: **Times New Roman, 13pt, Regular**
- Caption ảnh: **Times New Roman, 12pt, Italic**
- Dãn dòng: **1.5 lines**

---

## 🔧 NẾU CẦN CHỈNH SỬA SƠ ĐỒ

### Cách 1: Chỉnh sửa code Python

Nếu muốn thay đổi nội dung, màu sắc, hoặc bố cục:

1. Mở file `generate_diagrams_simple.py`
2. Tìm phần text hoặc màu cần sửa
3. Sửa và lưu
4. Chạy lại: `.\.venv\Scripts\python.exe generate_diagrams_simple.py`
5. File PNG mới sẽ được tạo ra

### Cách 2: Vẽ lại bằng công cụ khác

Nếu muốn tùy biến nhiều hơn, sử dụng:

- **draw.io** (miễn phí): https://app.diagrams.net/
  - Mở file → Import → chọn PNG → chỉnh sửa → Export PNG
  
- **PowerPoint**:
  - Insert → Shapes → vẽ lại theo mẫu
  - Save as Picture → PNG

- **Lucidchart** (online): https://www.lucidchart.com/
  - Có templates flowchart sẵn

---

## ❓ CÂU HỎI THƯỜNG GẶP

**Q: Sơ đồ bị mờ trong Word?**
A: Đảm bảo không scale ảnh lên quá 100%. File PNG đã có resolution 300 DPI (rất nét).

**Q: Muốn thay đổi màu sắc?**
A: Sửa trong file `generate_diagrams_simple.py` dòng `color='...'` rồi chạy lại script.

**Q: Có thể vẽ bằng tay không?**
A: Có, dùng PowerPoint hoặc draw.io theo hướng dẫn trong file `docs/DIAGRAM_GUIDE.md`.

**Q: File PNG ở đâu?**
A: Trong thư mục `docs/` của dự án:
   - `C:\Users\PC\Desktop\DoAnSemnierChuyenDe\docs\block_diagram_simple.png`
   - `C:\Users\PC\Desktop\DoAnSemnierChuyenDe\docs\flowchart_simple.png`

---

## ✅ CHECKLIST TRƯỚC KHI NỘP

- [ ] Đã chèn Hình 3.1 (Sơ đồ khối) vào mục 3.1
- [ ] Đã chèn Hình 3.2 (Flowchart) vào mục 3.2
- [ ] Đã thêm caption cho 2 ảnh
- [ ] Đã giải thích chi tiết từng thành phần/bước
- [ ] Đã tham chiếu đến hình trong văn bản
- [ ] Ảnh căn giữa và có kích thước phù hợp
- [ ] Font chữ và format đồng nhất trong toàn báo cáo

---

**Chúc bạn hoàn thành báo cáo tốt! 🎓**

Nếu cần hỗ trợ thêm, hãy hỏi tôi!
