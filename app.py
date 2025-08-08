# app.py

import streamlit as st
from datetime import datetime, timedelta

def get_current_count(start_time_str, interval_min, end_time_str):
    now = datetime.now()
    today = now.date()
    start = datetime.combine(today, datetime.strptime(start_time_str, "%H:%M").time())
    end = datetime.combine(today, datetime.strptime(end_time_str, "%H:%M").time())

    if now < start:
        return "まだ開始前です"
    elif now > end:
        return "カウント終了済み"
    else:
        delta = now - start
        count = delta.seconds // (interval_min * 60) + 1
        return f"カウント: {count}（{now.strftime('%H:%M:%S')} 現在）"

st.set_page_config(page_title="リアルタイムタイマー", layout="centered")

st.title("⏱ リアルタイムカウンター")

tab1, tab2 = st.tabs(["🕐 1分ごと", "🕔 5分ごと"])

with tab1:
    st.subheader("1分ごとのカウント（5:00〜21:39）")
    count_1min = get_current_count("05:00", 1, "21:39")
    st.success(count_1min)

with tab2:
    st.subheader("5分ごとのカウント（5:00〜21:35）")
    count_5min = get_current_count("05:00", 5, "21:35")
    st.info(count_5min)

