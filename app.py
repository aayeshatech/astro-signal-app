import streamlit as st
from datetime import datetime, time
import pandas as pd

# === Page Setup ===
st.set_page_config(page_title="🌕 Aayeshatech GANN ASTRO-GOLD REPORT", layout="wide")

# === Default Astro Configuration for 25 July 2025 (example) ===
astro_events = [
    {"time": "08:18", "event": "Moon ⛓ Saturn", "sentiment": "🛑 Bearish", "note": "Stop hunt risk"},
    {"time": "14:43", "event": "Venus 🔁 RX", "sentiment": "🚨 Bullish", "note": "Trend reversal begins"},
    {"time": "16:26", "event": "Mars 🔗 Rahu", "sentiment": "🔥 Bullish", "note": "+1.5% spike likely"},
    {"time": "20:50", "event": "Moon 🔥 Mars", "sentiment": "🟢 Bullish", "note": "Overnight follow-up"}
]

core_theme = "Venus Retrograde Triggers Golden Reversal - Mars Fuels the Fire"
key_planets = [
    "♀ Venus Retrograde (14:43) - 72% historical bullish accuracy",
    "♂ Mars-Rahu (16:26) - Algorithmic spike catalyst",
    "☽ Moon-Sun (17:25) - Institutional confirmation"
]
trading_protocol = [
    "1. Avoid 01:10–14:43 (Whipsaw zone)",
    "2. Enter longs at Venus RX (14:43)",
    "3. Add positions at Mars-Rahu (16:26)",
    "4. Hold through Moon-Mars (20:50)"
]

# === Sidebar Input ===
st.sidebar.title("📅 Select Report Date & Time Range")
selected_date = st.sidebar.date_input("Choose Date", datetime(2025, 7, 25))
start_time = st.sidebar.time_input("Start Time", value=time(0, 0))
end_time = st.sidebar.time_input("End Time", value=time(23, 59))

# === Header ===
st.markdown(f"### 🌕 Aayeshatech GANN ASTRO-GOLD REPORT")
st.markdown(f"📅 **Date:** {selected_date.strftime('%A, %d %B %Y')} | 🕒 **IST Timeline**")

# === Core Theme ===
st.markdown(f"#### ⚡ CORE THEME: \"{core_theme}\"")

# === Key Planetary Configurations ===
st.markdown("### 🌌 KEY PLANETARY CONFIGURATIONS:")
for item in key_planets:
    st.markdown(f"- {item}")

# === Timeline Table ===
st.markdown("### ⏳ CRITICAL TIMELINE:")

timeline_df = pd.DataFrame(astro_events)
timeline_df["datetime"] = pd.to_datetime(selected_date.strftime("%Y-%m-%d") + " " + timeline_df["time"])
timeline_df = timeline_df[(timeline_df["datetime"].dt.time >= start_time) & (timeline_df["datetime"].dt.time <= end_time)]

st.dataframe(timeline_df[["time", "event", "sentiment", "note"]], use_container_width=True)

# === Trading Protocol ===
st.markdown("### 🎯 TRADING PROTOCOL:")
for rule in trading_protocol:
    st.markdown(f"- {rule}")

# === Risk Warning (If Exists) ===
for row in timeline_df.itertuples():
    if "Saturn" in row.event:
        st.markdown(f"### ⚠️ RISK ADVISORY:\n{row.event} at {row.time} may trigger stop hunts.")

# Footer
st.markdown("---")
st.markdown("🔮 Powered by **Aayeshatech Astro Engine** | No Gann Levels | All Timings in IST")

