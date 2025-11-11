"""
Script vẽ sơ đồ đơn giản sử dụng matplotlib (không cần graphviz).
Phù hợp nếu bạn gặp khó khăn cài graphviz.

Cài đặt:
    pip install matplotlib

Chạy:
    python generate_diagrams_simple.py

Output:
    - docs/block_diagram_simple.png
    - docs/flowchart_simple.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os


def create_block_diagram_simple():
    """Tạo sơ đồ khối đơn giản bằng matplotlib"""
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(5, 13.5, 'Vietnamese Sentiment Assistant', 
            ha='center', fontsize=16, fontweight='bold')
    ax.text(5, 13, 'Sơ đồ Khối Hệ Thống', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Block positions [x, y, width, height]
    blocks = [
        (2, 11, 6, 1.2, '1. GIAO DIỆN NGƯỜI DÙNG\nStreamlit UI, Input, Buttons', 'lightblue'),
        (2, 9, 6, 1.2, '2. TIỀN XỬ LÝ VĂN BẢN\npreprocess.py: lowercase, typo fix', 'lightgreen'),
        (2, 7, 6, 1.2, '3. MÔ HÌNH NLP\nnlp.py: BERT multilingual, cached', 'orange'),
        (2, 5, 6, 1.2, '4. XỬ LÝ KẾT QUẢ\nThreshold logic (score < 0.35)', 'yellow'),
        (2, 3, 6, 1.2, '5. LƯU TRỮ DỮ LIỆU\ndb.py: SQLite, 5 columns', 'plum'),
        (2, 1, 6, 1.2, '6. HIỂN THỊ KẾT QUẢ\nLabel, Score, History (50)', 'lightblue'),
    ]
    
    # Draw blocks
    for x, y, w, h, text, color in blocks:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=9, multialignment='center')
    
    # Draw arrows
    arrow_positions = [
        (5, 11, 5, 10.2),      # 1 -> 2
        (5, 9, 5, 8.2),        # 2 -> 3
        (5, 7, 5, 6.2),        # 3 -> 4
        (5, 5, 5, 4.2),        # 4 -> 5
        (5, 3, 5, 2.2),        # 5 -> 6
    ]
    
    for x1, y1, x2, y2 in arrow_positions:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', mutation_scale=20, linewidth=2,
                               color='black')
        ax.add_patch(arrow)
    
    plt.tight_layout()
    os.makedirs('docs', exist_ok=True)
    plt.savefig('docs/block_diagram_simple.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Đã tạo: docs/block_diagram_simple.png")


def create_flowchart_simple():
    """Tạo flowchart đơn giản bằng matplotlib"""
    fig, ax = plt.subplots(figsize=(10, 16))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 18)
    ax.axis('off')
    
    # Title
    ax.text(5, 17.5, 'Vietnamese Sentiment Assistant', 
            ha='center', fontsize=16, fontweight='bold')
    ax.text(5, 17, 'Lưu Đồ Xử Lý Chi Tiết', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Helper function to draw shapes
    def draw_box(x, y, w, h, text, color='lightblue'):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                              edgecolor='black', facecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=8, multialignment='center')
    
    def draw_ellipse(x, y, w, h, text, color='lightgreen'):
        ellipse = patches.Ellipse((x + w/2, y + h/2), w, h,
                                 edgecolor='black', facecolor=color, linewidth=1.5)
        ax.add_patch(ellipse)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=9, fontweight='bold')
    
    def draw_diamond(x, y, w, h, text, color='yellow'):
        diamond = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                        edgecolor='black', facecolor=color, 
                                        linewidth=1.5, transform=ax.transData)
        # Rotate to make diamond shape (approximate)
        ax.add_patch(diamond)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontsize=8, multialignment='center')
    
    def draw_arrow(x1, y1, x2, y2, label=''):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', mutation_scale=15, linewidth=1.5,
                               color='black')
        ax.add_patch(arrow)
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.3, mid_y, label, fontsize=7, 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Flow elements
    draw_ellipse(3.5, 15.5, 3, 0.8, 'BẮT ĐẦU', 'lightgreen')
    draw_box(3, 14, 4, 0.8, 'Nhập câu tiếng Việt', 'lightyellow')
    draw_diamond(3.2, 12.5, 3.6, 0.8, 'len(text) >= 5?', 'yellow')
    
    # NO branch (left)
    draw_box(0.5, 11, 2, 0.6, 'st.error()\nNhập ít nhất\n5 ký tự', 'lightcoral')
    
    # YES branch (continue down)
    draw_box(3, 10.5, 4, 0.8, 'normalize_vi()\nLowercase, Fix typos', 'lightblue')
    draw_box(3, 9, 4, 0.8, 'predict_sentiment()\nRun BERT model', 'orange')
    draw_diamond(3.2, 7.5, 3.6, 0.8, 'score < 0.35?', 'yellow')
    
    # Threshold branches
    draw_box(0.5, 6, 2, 0.6, 'sentiment =\nNEUTRAL', 'yellow')
    draw_box(7.5, 6, 2, 0.6, 'Giữ nguyên\nsentiment', 'lightgreen')
    
    # Continue flow
    draw_box(3, 4.5, 4, 0.8, 'add_record()\nLưu vào SQLite', 'plum')
    draw_box(3, 3, 4, 0.8, 'st.success()\nHiển thị kết quả', 'lightgreen')
    draw_box(3, 1.5, 4, 0.8, 'list_latest(50)\nLịch sử', 'lightblue')
    draw_ellipse(3.5, 0, 3, 0.8, 'KẾT THÚC', 'lightcoral')
    
    # Arrows
    draw_arrow(5, 15.5, 5, 14.8)
    draw_arrow(5, 14, 5, 13.3)
    draw_arrow(3.8, 12.5, 1.5, 11.6, 'NO')
    draw_arrow(5.4, 12.5, 5, 11.3, 'YES')
    draw_arrow(5, 10.5, 5, 9.8)
    draw_arrow(5, 9, 5, 8.3)
    draw_arrow(3.8, 7.5, 1.5, 6.6, 'YES')
    draw_arrow(5.4, 7.5, 8.5, 6.6, 'NO')
    draw_arrow(1.5, 6, 1.5, 5)
    draw_arrow(8.5, 6, 8.5, 5)
    draw_arrow(1.5, 5, 5, 5.3)
    draw_arrow(8.5, 5, 5, 5.3)
    draw_arrow(5, 4.5, 5, 3.8)
    draw_arrow(5, 3, 5, 2.3)
    draw_arrow(5, 1.5, 5, 0.8)
    
    # Error path
    draw_arrow(1.5, 11, 1.5, 2)
    draw_arrow(1.5, 2, 3, 2.3)
    
    plt.tight_layout()
    plt.savefig('docs/flowchart_simple.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Đã tạo: docs/flowchart_simple.png")


def main():
    print("🎨 Đang tạo sơ đồ bằng matplotlib...")
    print("(Phương án đơn giản, không cần graphviz)")
    print()
    
    try:
        create_block_diagram_simple()
        create_flowchart_simple()
        
        print("\n" + "="*60)
        print("✅ HOÀN THÀNH! Đã tạo 2 file:")
        print("   1. docs/block_diagram_simple.png")
        print("   2. docs/flowchart_simple.png")
        print("="*60)
        print("\n📝 Chèn vào Word: Insert → Pictures → chọn file PNG")
        print("💡 Nếu muốn sơ đồ đẹp hơn, chạy: python generate_diagrams.py")
        print("   (Cần cài: pip install graphviz)")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("Đảm bảo đã cài: pip install matplotlib")


if __name__ == '__main__':
    main()
