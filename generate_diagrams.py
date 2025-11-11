"""
Script tự động vẽ Sơ đồ khối và Flowchart cho báo cáo đồ án.
Sử dụng thư viện graphviz để tạo sơ đồ chuyên nghiệp.

Cài đặt:
    pip install graphviz

Chạy:
    python generate_diagrams.py

Output:
    - block_diagram.png (Sơ đồ khối)
    - flowchart.png (Lưu đồ chi tiết)
"""

try:
    from graphviz import Digraph
    import os
except ImportError:
    print("❌ Chưa cài graphviz. Chạy: pip install graphviz")
    exit(1)


def create_block_diagram():
    """Tạo sơ đồ khối kiến trúc hệ thống"""
    dot = Digraph(comment='Block Diagram', format='png')
    dot.attr(rankdir='TB', size='10,12')
    dot.attr('node', shape='box', style='filled', fontname='Arial', fontsize='11')
    
    # Title
    dot.attr(label='Vietnamese Sentiment Assistant - Sơ đồ Khối Hệ Thống',
             labelloc='t', fontsize='16', fontname='Arial Bold')
    
    # Nodes (các khối)
    dot.node('UI', '1. GIAO DIỆN NGƯỜI DÙNG\n(Frontend)\n\n• Streamlit UI\n• Text Input\n• Buttons\n• Data Table',
             fillcolor='lightblue')
    
    dot.node('PRE', '2. TIỀN XỬ LÝ VĂN BẢN\n(Preprocessing)\n\n• preprocess.py\n• Lowercase\n• Typo correction\n• Tokenization',
             fillcolor='lightgreen')
    
    dot.node('MODEL', '3. MÔ HÌNH NLP\n(Transformer)\n\n• nlp.py\n• BERT multilingual\n• Pipeline cached\n• nlptown/bert-base',
             fillcolor='orange')
    
    dot.node('POST', '4. XỬ LÝ KẾT QUẢ\n(Post-processing)\n\n• Logic threshold\n• if score < 0.35\n  → NEUTRAL',
             fillcolor='yellow')
    
    dot.node('DB', '5. LƯU TRỮ DỮ LIỆU\n(Database)\n\n• db.py\n• SQLite\n• 5 columns\n• Timestamp',
             fillcolor='plum')
    
    dot.node('SHOW', '6. HIỂN THỊ KẾT QUẢ\n(Output)\n\n• st.success/error\n• Label + Score\n• History table (50)',
             fillcolor='lightblue')
    
    # Edges (mũi tên)
    dot.edge('UI', 'PRE', label='Input text')
    dot.edge('PRE', 'MODEL', label='Normalized text')
    dot.edge('MODEL', 'POST', label='Label + Score')
    dot.edge('POST', 'DB', label='Final result')
    dot.edge('DB', 'SHOW', label='History data')
    
    return dot


def create_flowchart():
    """Tạo flowchart chi tiết quá trình xử lý"""
    dot = Digraph(comment='Flowchart', format='png')
    dot.attr(rankdir='TB', size='8,14')
    dot.attr('node', fontname='Arial', fontsize='10')
    
    # Title
    dot.attr(label='Vietnamese Sentiment Assistant - Lưu Đồ Xử Lý Chi Tiết',
             labelloc='t', fontsize='16', fontname='Arial Bold')
    
    # Start/End nodes
    dot.node('START', 'BẮT ĐẦU', shape='ellipse', style='filled', fillcolor='lightgreen')
    dot.node('END', 'KẾT THÚC', shape='ellipse', style='filled', fillcolor='lightcoral')
    
    # Input/Output nodes
    dot.node('INPUT', 'Người dùng nhập câu\ntiếng Việt (text)', shape='parallelogram',
             style='filled', fillcolor='lightyellow')
    dot.node('ERROR', 'st.error()\n"Nhập ít nhất 5 ký tự"', shape='parallelogram',
             style='filled', fillcolor='lightcoral')
    dot.node('OUTPUT', 'st.success()\nHiển thị:\n• Label\n• Score', shape='parallelogram',
             style='filled', fillcolor='lightgreen')
    dot.node('HISTORY', 'Hiển thị bảng\nlịch sử 50 bản ghi', shape='parallelogram',
             style='filled', fillcolor='lightblue')
    
    # Processing nodes
    dot.node('NORM', 'normalize_vi()\n• Lowercase\n• Fix typos\n• Tokenize',
             shape='box', style='filled', fillcolor='lightblue')
    dot.node('PRED', 'predict_sentiment()\n• Load pipeline\n• Run model\n• Get label+score',
             shape='box', style='filled', fillcolor='orange')
    dot.node('SAVE', 'add_record()\n• Lưu vào SQLite\n• Timestamp',
             shape='box', style='filled', fillcolor='plum')
    dot.node('FETCH', 'list_latest(50)\nLấy lịch sử từ DB',
             shape='box', style='filled', fillcolor='lightblue')
    dot.node('SET_NEUTRAL', 'sentiment = NEUTRAL',
             shape='box', style='filled', fillcolor='yellow')
    dot.node('KEEP', 'Giữ nguyên sentiment',
             shape='box', style='filled', fillcolor='lightgreen')
    
    # Decision nodes
    dot.node('CHECK_LEN', 'len(text) >= 5?', shape='diamond',
             style='filled', fillcolor='lightyellow')
    dot.node('CHECK_SCORE', 'score < 0.35?', shape='diamond',
             style='filled', fillcolor='lightyellow')
    
    # Flow
    dot.edge('START', 'INPUT')
    dot.edge('INPUT', 'CHECK_LEN')
    
    # Validation branch
    dot.edge('CHECK_LEN', 'ERROR', label='NO')
    dot.edge('CHECK_LEN', 'NORM', label='YES')
    
    # Processing flow
    dot.edge('NORM', 'PRED')
    dot.edge('PRED', 'CHECK_SCORE')
    
    # Threshold logic
    dot.edge('CHECK_SCORE', 'SET_NEUTRAL', label='YES')
    dot.edge('CHECK_SCORE', 'KEEP', label='NO')
    
    # Merge paths
    dot.edge('SET_NEUTRAL', 'SAVE')
    dot.edge('KEEP', 'SAVE')
    
    # Continue to output
    dot.edge('SAVE', 'OUTPUT')
    dot.edge('ERROR', 'FETCH')
    dot.edge('OUTPUT', 'FETCH')
    dot.edge('FETCH', 'HISTORY')
    dot.edge('HISTORY', 'END')
    
    return dot


def main():
    """Generate both diagrams"""
    print("🎨 Đang tạo sơ đồ...")
    
    # Create output directory
    os.makedirs('docs', exist_ok=True)
    
    # Generate Block Diagram
    print("📊 Tạo Sơ đồ khối...")
    block_diagram = create_block_diagram()
    block_diagram.render('docs/block_diagram', cleanup=True)
    print("✅ Đã tạo: docs/block_diagram.png")
    
    # Generate Flowchart
    print("🔄 Tạo Flowchart...")
    flowchart = create_flowchart()
    flowchart.render('docs/flowchart', cleanup=True)
    print("✅ Đã tạo: docs/flowchart.png")
    
    print("\n" + "="*60)
    print("✅ HOÀN THÀNH! Đã tạo 2 file:")
    print("   1. docs/block_diagram.png - Sơ đồ khối")
    print("   2. docs/flowchart.png - Lưu đồ chi tiết")
    print("="*60)
    print("\n📝 Bạn có thể chèn 2 ảnh này vào báo cáo Word:")
    print("   Insert → Pictures → chọn file PNG")
    print("   Đặt ảnh ở mục '3. Thiết kế hệ thống'")


if __name__ == '__main__':
    main()
