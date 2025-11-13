# Copilot Directives:
# - Build Streamlit UI: one text_input, one "Phân loại cảm xúc" button,
#   one "Tải lại lịch sử" button, and a dataframe (latest 50).
# - On click: normalize_vi(text) -> predict_sentiment() -> save to SQLite.
# - Validate: length >= 5; else st.error and return, no DB write.
# - Use st.spinner when calling the pipeline. Handle exceptions gracefully.
# - Never block UI: keep pipeline cached in nlp.py; do NOT re-create it here.
# - Columns in history: ID, Text, Sentiment, Score (2 decimals), Time.

import streamlit as st
import pandas as pd
from preprocess import normalize_vi
from nlp import predict_sentiment
from db import add_record, list_latest, init_db
from reclassify_db import reclassify_all

# Initialize database on app startup
init_db()

# Set page config
st.set_page_config(
    page_title="Vietnamese Sentiment Assistant",
    page_icon="🎭",
    layout="wide"
)

# Header
st.title("🎭 Vietnamese Sentiment Assistant")
st.markdown("Phân loại cảm xúc câu tiếng Việt: **POSITIVE** / **NEUTRAL** / **NEGATIVE**")
st.divider()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input(
        "Nhập câu tiếng Việt:",
        placeholder="Ví dụ: Hôm nay trời đẹp quá!",
        max_chars=200
    )

    # Small note about how confidence is reported in the UI
    st.info(
        "Lưu ý: Giá trị 'độ tin cậy' hiển thị là xác suất tổng hợp của lớp (POSITIVE/NEUTRAL/NEGATIVE)\n"
        "(tổng các xác suất nhãn 'star' thuộc cùng lớp) — giúp trực quan hơn cho người dùng.\n"
        "Quyết định nhãn vẫn tuân theo logic lõi của mô hình (nhãn sao có xác suất cao nhất với ngưỡng trung lập = 0.50).",
        icon="ℹ️"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    classify_btn = st.button("🔍 Phân loại cảm xúc", type="primary", width='stretch')

# Classification logic
if classify_btn:
    if len(user_input.strip()) < 5:
        st.error("⚠️ Vui lòng nhập ít nhất 5 ký tự!")
    else:
        with st.spinner("Đang phân loại..."):
            try:
                # Normalize Vietnamese text (use tokenization if available for better matching)
                normalized_text = normalize_vi(user_input, use_tokenize=True)
                
                # Predict sentiment (follow SPEC: threshold = 0.50)
                label, score = predict_sentiment(normalized_text, neutral_threshold=0.50)
                
                # Save to database
                add_record(text=normalized_text, sentiment=label, score=score)
                
                # Display result with color coding
                if label == "POSITIVE":
                    st.success(f"✅ Kết quả: **{label}** (độ tin cậy: {score:.2f})")
                elif label == "NEGATIVE":
                    st.error(f"❌ Kết quả: **{label}** (độ tin cậy: {score:.2f})")
                else:
                    st.info(f"ℹ️ Kết quả: **{label}** (độ tin cậy: {score:.2f})")
                    
            except Exception as ex:
                st.error(f"❌ Không phân loại được: {ex}")

st.divider()

# History section
col_title, col_reload = st.columns([4, 1])

with col_title:
    st.subheader("📊 Lịch sử phân loại (50 bản ghi mới nhất)")

with col_reload:
    if st.button("🔄 Tải lại lịch sử", width='stretch'):
        st.rerun()

    # Reclassify history button (update records using current pipeline)
    if st.button("♻️ Cập nhật lịch sử (Reclassify)", width='stretch'):
        with st.spinner("Đang cập nhật lịch sử... Vui lòng chờ (có thể vài giây)"):
            try:
                updated = reclassify_all(limit=5000)
                st.success(f"Đã cập nhật {updated} bản ghi theo logic hiện tại.")
                # Some Streamlit versions don't have experimental_rerun; use st.rerun()
                try:
                    st.rerun()
                except Exception:
                    st.info("Vui lòng nhấn 'Tải lại lịch sử' để làm mới giao diện.")
            except Exception as e:
                st.error(f"Lỗi khi cập nhật lịch sử: {e}")

# Fetch and display history
history = list_latest(limit=50)

if history:
    df = pd.DataFrame(
        history,
        columns=["ID", "Text", "Sentiment", "Score", "Time"]
    )
    
    # Format score to 2 decimals
    df["Score"] = df["Score"].apply(lambda x: f"{x:.2f}")
    
    # Display with styling
    st.dataframe(
        df,
        width='stretch',
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Text": st.column_config.TextColumn("Text", width="large"),
            "Sentiment": st.column_config.TextColumn("Sentiment", width="medium"),
            "Score": st.column_config.TextColumn("Score", width="small"),
            "Time": st.column_config.TextColumn("Time", width="medium"),
        }
    )
else:
    st.info("Chưa có dữ liệu. Hãy phân loại câu đầu tiên!")

# Footer
st.divider()
st.caption("Powered by Hugging Face Transformers & Streamlit | Model: nlptown/bert-base-multilingual-uncased-sentiment")
