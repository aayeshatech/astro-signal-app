import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# ========== Page Setup ==========
st.set_page_config(page_title="🔭 Astro Market Insight", layout="wide")

st.title("🔮 Astro Market Timeline – DeepSeek Simulated Report")

# ========== User Inputs ==========
col1, col2, col3 = st.columns(3)

with col1:
    selected_date = st.date_input("📅 Select Date", datetime(2025, 7, 25))

with col2:
    start_time = st.time_input("⏰ Start Time", datetime.strptime("09:15", "%H:%M").time())

with col3:
    end_time = st.time_input("⏰ End Time", datetime.strptime("15:30", "%H:%M").time())

symbol = st.selectbox("📈 Select Stock / Index", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow Jones"])

# ========== Simulated DeepSeek Report (Mock Astro Data) ==========
astro_data = [
    ("00:51", "04:43", "Venus (Ve)", "Pushya (Sa)", "Moon-Venus influence", "🟢 Bullish", "Steady upside, banking stocks strong", "Buy on dips"),
    ("04:43", "05:53", "Sun (Su)", "Pushya (Sa)", "Moon-Sun volatility", "🔴 Bearish", "Risk of gap-down or sudden drop", "Avoid new longs"),
    ("05:53", "07:50", "Moon (Mo)", "Pushya (Sa)", "Emotional stability", "🟢 Bullish", "Recovery possible, good for intraday longs", "Short-term longs"),
    ("07:50", "09:12", "Mars (Ma)", "Pushya (Sa)", "Aggressive moves", "🟠 Neutral", "Volatile swings, no clear direction", "Wait for confirmation"),
    ("09:12", "12:43", "Rahu (Ra)", "Pushya (Sa)", "Rahu manipulation", "🔴 Bearish", "Sharp corrections, false breakouts likely", "Caution – Hedge"),
    ("12:43", "15:51", "Jupiter (Ju)", "Pushya (Sa)", "Optimism, expansion", "🟢 Bullish", "Rally in heavyweights (HDFC, ICICI, RIL)", "Best for longs"),
    ("15:51", "17:52", "Ketu (Ke)", "Ashlesha (Me)", "Mercury Retrograde starts", "🔴 Bearish", "Panic selling, sudden drops", "Avoid trades"),
    ("17:52", "23:59", "Ketu (Ke)", "Ashlesha (Me)", "Declination weakens", "🟠 Choppy", "Sideways close, low volumes", "Stay flat")
]

# ========== Filter Logic ==========
filtered_data = []
summary_long = []
summary_short = []

for entry in astro_data:
    start_str, end_str, *rest = entry
    t_start = datetime.combine(selected_date, datetime.strptime(start_str, "%H:%M").time())
    t_end = datetime.combine(selected_date, datetime.strptime(end_str, "%H:%M").time())

    user_start = datetime.combine(selected_date, start_time)
    user_end = datetime.combine(selected_date, end_time)

    if t_end >= user_start and t_start <= user_end:
        filtered_data.append((start_str + " – " + end_str, *rest))

        # Summary logic
        sentiment = rest[3]
        if sentiment == "🟢 Bullish":
            summary_long.append((start_str + " – " + end_str, rest[2], rest[3]))
        elif sentiment == "🔴 Bearish":
            summary_short.append((start_str + " – " + end_str, rest[2], rest[3]))

# ========== Display Table ==========
st.markdown(f"### 📊 Astro Timeline for {symbol} on {selected_date.strftime('%d-%b-%Y')}")
if filtered_data:
    df = pd.DataFrame(filtered_data, columns=[
        "Time", "Moon’s Sub-Lord", "Nakshatra", "Planetary Aspect",
        "Sentiment", "Expected Market Move", "Trading Bias"
    ])
    st.dataframe(df, use_container_width=True)

    # ===== Summary Section =====
    st.markdown("---")
    st.markdown("### 🟩 Best Bullish Time Window")
    for time, aspect, senti in summary_long:
        st.markdown(f"- 🕒 `{time}` → {senti} ({aspect})")

    st.markdown("### 🟥 Best Bearish Time Window")
    for time, aspect, senti in summary_short:
        st.markdown(f"- 🕒 `{time}` → {senti} ({aspect})")
else:
    st.warning("No astro data found for the selected time range.")

# ========== Footer ==========
st.caption("This is a simulated DeepSeek AI report based on planetary transits. Actual real-time AI integration coming soon.")
