import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# === Streamlit Setup ===
st.set_page_config(page_title="📈 Astro Sub-Lord Market Report", layout="wide")

# === Inputs ===
st.title("📊 Intraday Astro Market Report")
report_date = st.date_input("Select Date", datetime.now().date())
index_choice = st.selectbox("Select Index", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow Jones"])
start_time = st.time_input("Start Time", datetime.strptime("09:15", "%H:%M").time())
end_time = st.time_input("End Time", datetime.strptime("15:30", "%H:%M").time())

# === Simulated Astro Sub-Lord transitions (Replace with Jagannatha Hora data) ===
transits = [
    {"start": "09:15", "end": "10:35", "sublord": "Venus", "nakshatra": "Pushya", "aspect": "Moon-Venus", "sentiment": "🟢 Bullish", "move": "Steady upside, banking stocks strong", "bias": "Buy on dips"},
    {"start": "10:35", "end": "11:25", "sublord": "Sun", "nakshatra": "Pushya", "aspect": "Moon-Sun", "sentiment": "🔴 Bearish", "move": "Risk of drop, avoid new longs", "bias": "Wait & Watch"},
    {"start": "11:25", "end": "12:45", "sublord": "Moon", "nakshatra": "Pushya", "aspect": "Emotional phase", "sentiment": "🟢 Bullish", "move": "Recovery likely", "bias": "Scalp longs"},
    {"start": "12:45", "end": "14:15", "sublord": "Rahu", "nakshatra": "Pushya", "aspect": "Rahu manipulation", "sentiment": "🔴 Bearish", "move": "False breakouts", "bias": "Hedge / short"},
    {"start": "14:15", "end": "15:30", "sublord": "Jupiter", "nakshatra": "Pushya", "aspect": "Jupiter optimism", "sentiment": "🟢 Bullish", "move": "Heavyweight rally", "bias": "Long RIL, ICICI, HDFC"}
]

# === Filter Transits by Time Range ===
start_dt = datetime.combine(report_date, start_time)
end_dt = datetime.combine(report_date, end_time)

def parse_time(t_str):
    return datetime.strptime(t_str, "%H:%M")

report_data = []
for t in transits:
    t_start = datetime.combine(report_date, parse_time(t["start"]).time())
    t_end = datetime.combine(report_date, parse_time(t["end"]).time())
    if t_start >= start_dt and t_start <= end_dt:
        report_data.append([f"{t['start']} – {t['end']}", t["sublord"], t["nakshatra"], t["aspect"], t["sentiment"], t["move"], t["bias"]])

df = pd.DataFrame(report_data, columns=["Time", "Moon’s Sub-Lord", "Nakshatra", "Planetary Aspect", "Sentiment", "Expected Market Move", "Trading Bias"])
st.dataframe(df, use_container_width=True)

# === Summary Recommendation ===
bullish_periods = [row for row in report_data if "🟢" in row[4]]
bearish_periods = [row for row in report_data if "🔴" in row[4]]

st.subheader("🔍 Summary Insight")
if bullish_periods:
    best_long = bullish_periods[0][0]
    st.success(f"✅ **Best Long Period**: {best_long} based on {bullish_periods[0][3]}")
else:
    st.warning("No clear long signal during the day.")

if bearish_periods:
    best_short = bearish_periods[0][0]
    st.error(f"🚫 **Best Short Period**: {best_short} due to {bearish_periods[0][3]}")
else:
    st.info("No strong bearish signal.")

