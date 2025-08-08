import streamlit as st
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh

# --- 自動リフレッシュ（10秒ごと） ---
st_autorefresh(interval=10 * 1000, key="refresh")

# --- タイムゾーンを日本時間に設定 ---
def get_japan_time():
    jst = pytz.timezone('Asia/Tokyo')
    return datetime.now(jst)

# --- 現在のカウントを取得 ---
def get_current_count(start_time_str, interval_min, end_time_str):
    now = get_japan_time()
    today = now.date()
    start = datetime.combine(today, datetime.strptime(start_time_str, "%H:%M").time())
    end = datetime.combine(today, datetime.strptime(end_time_str, "%H:%M").time())

    if now < start:
        return ("まだ開始前です", None)
    elif now > end:
        return ("カウント終了済み", None)
    else:
        delta = now - start
        count = delta.seconds // (interval_min * 60) + 1
        return (f"{count}", now.strftime('%H:%M:%S'))

# --- ページ設定 ---
st.set_page_config(page_title="リアルタイムカウンター", layout="centered")

# --- カスタムCSSでデザインを強化 ---
st.markdown("""
    <style>
        .timer-box {
            background-color: #111;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            color: #39FF14;
            font-family: 'Courier New', monospace;
            font-size: 48px;
            letter-spacing: 2px;
            margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0,255,100,0.3);
        }
        .label {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⏱ リアルタイム・デジタルタイマー")

# --- タブで切り替え ---
tab1, tab2 = st.tabs(["🕐 1分ごとカウント", "🕔 5分ごとカウント"])

with tab1:
    st.markdown('<div class="label">1分ごとのカウント（5:00〜21:39）</div>', unsafe_allow_html=True)
    count, current_time = get_current_count("05:00", 1, "21:39")
    if current_time:
        st.markdown(f'<div class="timer-box">{count}</div>', unsafe_allow_html=True)
        st.caption(f"現在時刻（JST）：{current_time}")
    else:
        st.warning(count)

with tab2:
    st.markdown('<div class="label">5分ごとのカウント（5:00〜21:35）</div>', unsafe_allow_html=True)
    count5, current_time5 = get_current_count("05:00", 5, "21:35")
    if current_time5:
        st.markdown(f'<div class="timer-box">{count5}</div>', unsafe_allow_html=True)
        st.caption(f"現在時刻（JST）：{current_time5}")
    else:
        st.warning(count5)
