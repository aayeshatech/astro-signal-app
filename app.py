import streamlit as st
import pandas as pd
from datetime import datetime, time

# === Page Config ===
st.set_page_config(page_title="📊 Astro Market Report", layout="centered")

st.title("📊 Sector-Wise Astro Outlook Dashboard")
st.caption("🪐 Astro Sentiment Timeline – Market Trend Analysis")

# === Sample Astro Report (Mimicking DeepSeek AI Output) ===
sample_data = [
    {"Time": "00:51 – 04:43", "Moon’s Sub-Lord": "Venus (Ve)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Moon-Venus influence", "Sentiment": "🟢 Bullish",
     "Expected Market Move": "Steady upside, banking stocks strong", "Trading Bias": "Buy on dips"},
    {"Time": "04:43 – 05:53", "Moon’s Sub-Lord": "Sun (Su)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Moon-Sun volatility", "Sentiment": "🔴 Bearish",
     "Expected Market Move": "Risk of gap-down or sudden drop", "Trading Bias": "Avoid new longs"},
    {"Time": "05:53 – 07:50", "Moon’s Sub-Lord": "Moon (Mo)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Emotional stability", "Sentiment": "🟢 Bullish",
     "Expected Market Move": "Recovery possible, good for intraday longs", "Trading Bias": "Short-term longs"},
    {"Time": "07:50 – 09:12", "Moon’s Sub-Lord": "Mars (Ma)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Aggressive moves", "Sentiment": "🟠 Neutral",
     "Expected Market Move": "Volatile swings, no clear direction", "Trading Bias": "Wait for confirmation"},
    {"Time": "09:12 – 12:43", "Moon’s Sub-Lord": "Rahu (Ra)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Rahu manipulation", "Sentiment": "🔴 Bearish",
     "Expected Market Move": "Sharp corrections, false breakouts likely", "Trading Bias": "Caution – Hedge"},
    {"Time": "12:43 – 15:51", "Moon’s Sub-Lord": "Jupiter (Ju)", "Nakshatra": "Pushya (Sa)",
     "Planetary Aspect": "Optimism, expansion", "Sentiment": "🟢 Bullish",
     "Expected Market Move": "Rally in heavyweights (HDFC, ICICI, RIL)", "Trading Bias": "Best for longs"},
    {"Time": "15:51 – 17:52", "Moon’s Sub-Lord": "Ketu (Ke)", "Nakshatra": "Ashlesha (Me)",
     "Planetary Aspect": "Mercury Retrograde starts", "Sentiment": "🔴 Bearish",
     "Expected Market Move": "Panic selling, sudden drops", "Trading Bias": "Avoid trades"},
    {"Time": "17:52 – EOD", "Moon’s Sub-Lord": "Ketu (Ke)", "Nakshatra": "Ashlesha (Me)",
     "Planetary Aspect": "Declination weakens", "Sentiment": "🟠 Choppy",
     "Expected Market Move": "Sideways close, low volumes", "Trading Bias": "Stay flat"},
]

df = pd.DataFrame(sample_data)

# === Inputs ===
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Select Report Date", datetime(2025, 7, 25))
with col2:
    start_time = st.time_input("From Time", time(0, 0))
    end_time = st.time_input("To Time", time(23, 59))

# === Filter Data Based on Time Range ===
def extract_start_minutes(time_str):
    """Extract start minute from time range string like '00:51 – 04:43'."""
    try:
        start_str = time_str.split("–")[0].strip()
        dt = datetime.strptime(start_str, "%H:%M")
        return dt.hour * 60 + dt.minute
    except:
        return -1  # for 'EOD'

start_minutes = start_time.hour * 60 + start_time.minute
end_minutes = end_time.hour * 60 + end_time.minute

df["Start_Minutes"] = df["Time"].apply(extract_start_minutes)
filtered_df = df[(df["Start_Minutes"] >= start_minutes) & (df["Start_Minutes"] <= end_minutes)].drop(columns=["Start_Minutes"])

# === Show Table ===
st.markdown(f"### 🗓️ Astro Report for {selected_date.strftime('%A, %d %B %Y')}")
st.dataframe(filtered_df, use_container_width=True)

# === Note ===
st.info("This dashboard simulates astro timing reports fetched from DeepSeek-style AI insight. Custom real-time integration available.")
