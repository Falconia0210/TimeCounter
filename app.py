import streamlit as st
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

# --- 状態管理 ---
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = now_jst
if 'count_1min' not in st.session_state:
    # 起動時のカウントをルールに従って計算
    elapsed_minutes = int((now_jst - start_time).total_seconds() // 60)
    st.session_state.count_1min = min(elapsed_minutes + 1, 1000)  # 1分カウント
if 'count_5min' not in st.session_state:
    # 5分単位のカウントを計算
    elapsed_minutes = int((now_jst - start_time).total_seconds() // 60)
    st.session_state.count_5min = min(elapsed_minutes // 5 + 1, 200)  # 5分カウント

# --- 更新処理（ボタンを押した時間を基準にカウント進行） ---
def update_counts():
    # ボタンが押された時点の時間を取得
    now_jst = datetime.now(JST)
    elapsed_minutes = int((now_jst - start_time).total_seconds() // 60)
    
    # 1分ごとのカウントは、5:00以降から開始する
    st.session_state.count_1min = min(elapsed_minutes + 1, 1000)  # 5:00から1分カウント開始
    st.session_state.count_5min = min(elapsed_minutes // 5 + 1, 200)  # 5:00から5分カウント開始
    st.session_state.last_updated = now_jst  # 更新時刻を記録

# --- 更新ボタン ---
if st.button('Sync'):
    update_counts()

# --- スリープ状態チェック ---
if st.session_state.count_1min >= 1000 or st.session_state.count_5min >= 200:
    sleep_until = start_time.replace(hour=5, minute=0, second=0, microsecond=0) + timedelta(days=1)
    if now_jst < sleep_until:
        # 5時までスリープ状態
        sleep_message = "Sleep"
        st.session_state.count_1min = st.session_state.count_5min = None  # カウント停止
    else:
        # 5時を過ぎたらカウント再開
        sleep_message = ""
else:
    sleep_message = ""

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
    """, unsafe_allow_html=True
)

# --- 表示 ---
if st.session_state.count_1min is not None and st.session_state.count_5min is not None:
    st.markdown('<div class="counter">{:03d}</div>'.format(st.session_state.count_1min), unsafe_allow_html=True)
    st.markdown('<div class="counter">{:03d}</div>'.format(st.session_state.count_5min), unsafe_allow_html=True)

else:
    st.markdown('<div class="sleep-message">Sleep</div>', unsafe_allow_html=True)

st.markdown(f'<div class="timestamp">現在時刻（JST）: {now_jst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
