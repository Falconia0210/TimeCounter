import streamlit as st
import time
from datetime import datetime, timedelta
import pytz

# タイトルとページ設定
st.set_page_config(page_title="カウントタイマー", layout="centered")

# 日本時間に変換
JST = pytz.timezone('Asia/Tokyo')
now_jst = datetime.now(JST)

# 今日の5:00 JST
start_time = now_jst.replace(hour=5, minute=0, second=0, microsecond=0)
if now_jst < start_time:
    start_time -= timedelta(days=1)

# 経過時間（分）
elapsed_minutes = int((now_jst - start_time).total_seconds() // 60)
count_1min = min(elapsed_minutes, 1000)
count_5min = min(elapsed_minutes // 5, 200)

# スリープ状態チェック
if count_1min >= 1000 or count_5min >= 200:
    sleep_until = start_time.replace(hour=5, minute=0, second=0, microsecond=0) + timedelta(days=1)
    if now_jst < sleep_until:
        # 5時までスリープ状態
        sleep_message = "Sleep"
        count_1min = count_5min = None  # カウント停止
    else:
        # 5時を過ぎたらカウント再開
        sleep_message = ""
else:
    sleep_message = ""

# --- 状態管理 ---
if 'count_1min' not in st.session_state:
    st.session_state.count_1min = count_1min
if 'count_5min' not in st.session_state:
    st.session_state.count_5min = count_5min

# --- 自動更新機能 ---
st.write("現在、タイマーは自動で更新されます。更新ボタンは必要ありません。")

# --- デザイン ---
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
        font-family: sans-serif;
    }
    .counter {
        font-size: 72px;
        color: white;
        font-weight: bold;
        text-align: center;
        font-family: sans-serif;
        text-shadow: 0 0 10px white;
    }
    .label {
        font-size: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        font-family: sans-serif;
    }
    .timestamp {
        font-size: 14px;
        color: gray;
        text-align: center;
        margin-top: 40px;
        font-family: sans-serif;
    }
    .sleep-message {
        font-size: 36px;
        color: white;
        font-weight: bold;
        text-align: center;
        margin-top: 40px;
        font-family: sans-serif;
    }
    .button-container {
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 表示 ---
if st.session_state.count_1min is not None and st.session_state.count_5min is not None:
    st.markdown('<div class="counter">{:03d}</div>'.format(st.session_state.count_1min), unsafe_allow_html=True)
    st.markdown('<div class="label">1分カウント（最大1000）</div>', unsafe_allow_html=True)

    st.markdown('<div class="counter">{:03d}</div>'.format(st.session_state.count_5min), unsafe_allow_html=True)
    st.markdown('<div class="label">5分カウント（最大200）</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="sleep-message">Sleep</div>', unsafe_allow_html=True)

st.markdown(f'<div class="timestamp">現在時刻（JST）: {now_jst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

# --- 更新ボタン表示位置 ---
st.markdown('<div class="button-container"></div>', unsafe_allow_html=True)

# --- 自動更新処理（更新間隔 1秒ごとにリフレッシュ） ---
time.sleep(1)  # 1秒ごとに自動更新
st.experimental_rerun()
