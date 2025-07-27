import streamlit as st
from datetime import datetime, time
import pandas as pd

# === Streamlit App Config ===
st.set_page_config(page_title="📈 Astro Transit Signal Viewer", layout="wide")

st.title("📈 Astro Signal Timeline Viewer")

# === Date and Time Inputs ===
now_ist = datetime.now()

start_date = st.date_input("📅 Select Start Date (IST)", value=now_ist.date())
start_time = st.time_input("🕒 Select Start Time (IST)", value=now_ist.time())
start_dt = datetime.combine(start_date, start_time)

# === Stock or Index Input ===
asset_name = st.text_input("📌 Enter Stock or Index Name (e.g. NIFTY, BANKNIFTY, GOLD)", value="NIFTY")

# === Sample Astro Transit Data (Replace this with real logic later) ===
astro_events = [
    {"time": "10:15", "event": "Moon conjunct Saturn", "impact": "🔴 Bearish"},
    {"time": "11:30", "event": "Venus trine Jupiter", "impact": "🟢 Bullish"},
    {"time": "13:05", "event": "Mars sextile Mercury", "impact": "🟡 Volatile"},
    {"time": "14:40", "event": "Sun opposite Neptune", "impact": "🔴 Bearish"},
    {"time": "16:20", "event": "Moon trine Venus", "impact": "🟢 Bullish"},
]

# === Convert times and filter ===
event_rows = []
for astro in astro_events:
    astro_time = datetime.combine(start_date, datetime.strptime(astro["time"], "%H:%M").time())
    if astro_time >= start_dt:
        event_rows.append({
            "Time": astro_time.strftime("%I:%M %p"),
            "Transit": astro["event"],
            "Signal": astro["impact"]
        })

# === Display Output ===
if event_rows:
    st.markdown(f"### 📊 Astro Transit Timeline for **{asset_name.upper()}** on {start_date.strftime('%d-%b-%Y')}")
    st.table(pd.DataFrame(event_rows))
else:
    st.warning("No upcoming astro transits after selected time.")
