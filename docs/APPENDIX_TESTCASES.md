# Phụ lục A — Bộ Test Cases (15 câu)

Bảng dưới đây liệt kê 15 câu kiểm thử dùng trong báo cáo. Cột `Expected` là nhãn mong đợi (ground truth) dùng để đánh giá accuracy.

| STT | Câu test (Tiếng Việt)                                  | Expected  |
|-----|---------------------------------------------------------|-----------|
| 1   | Hôm nay trời đẹp quá!                                   | POSITIVE  |
| 2   | Món ăn rat ngon, tôi rất thích!                         | POSITIVE  |
| 3   | Dịch vụ tệ, nhân viên thái độ xấu.                      | NEGATIVE  |
| 4   | Sản phẩm kém chất lượng, giá lại đắt.                   | NEGATIVE  |
| 5   | Bình thường thôi, không có gì đặc biệt.                 | NEUTRAL   |
| 6   | Tôi không biết nói gì về điều này.                     | NEUTRAL   |
| 7   | Tuyệt vời! Đây là trải nghiệm tốt nhất.                 | POSITIVE  |
| 8   | Thất vọng quá, lãng phí tiền bạc.                       | NEGATIVE  |
| 9   | Cũng được, chấp nhận được.                              | NEUTRAL   |
| 10  | Rất hài lòng với chất lượng sản phẩm!                   | POSITIVE  |
| 11  | Quá tuyệt vời, tôi rất yêu thích!                       | POSITIVE  |
| 12  | Siêu tốt, dịch vụ tuyệt vời!                            | POSITIVE  |
| 13  | Chán quá, không muốn dùng nữa.                          | NEGATIVE  |
| 14  | Tệ hại, lần sau không quay lại.                         | NEGATIVE  |
| 15  | OK, bình thường.                                        | NEUTRAL   |

Ghi chú:
- Bộ test gồm các câu ngắn/tiêu chuẩn, bao phủ POSITIVE / NEUTRAL / NEGATIVE.
- Bảng này được tham chiếu trong Mục 6 (Đánh giá hiệu suất) của báo cáo.
- Bạn có thể mở rộng bộ test bằng cách thêm các câu vào `tests/test_cases.json` hoặc tạo file test mới.
