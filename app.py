import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

# Set timezone
tz = pytz.timezone("Asia/Kolkata")

st.set_page_config(page_title="📈 Astro Transit Timeline", layout="centered")
st.title("📈 Astro Transit Timeline")

location = "Mumbai, India"
st.markdown(f"**Location:** {location}")

# Date input widget
selected_date = st.date_input("📅 Select Date", value=datetime.now(tz).date())

# Start and End time input widgets
start_time = st.time_input("⏰ Start Time", value=time(9, 0))  # 9:00 AM default
end_time = st.time_input("⏰ End Time", value=time(17, 0))    # 5:00 PM default

# Simulate transit data function (same as before)
def get_transits_for_date(date):
    base_transits = [
        {"time": "10:15 AM", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
        {"time": "11:30 AM", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
        {"time": "01:05 PM", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
        {"time": "02:40 PM", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
        {"time": "04:20 PM", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
    ]
    # Rotate list based on date day to simulate change
    shift = date.day % len(base_transits)
    rotated = base_transits[shift:] + base_transits[:shift]
    return rotated

astro_transits = get_transits_for_date(selected_date)

# Helper function to convert "hh:mm AM/PM" string to time object
def str_to_time(tstr):
    return datetime.strptime(tstr, "%I:%M %p").time()

# Filter events by time range
filtered_transits = [
    event for event in astro_transits
    if start_time <= str_to_time(event["time"]) <= end_time
]

df_transits = pd.DataFrame(filtered_transits)

st.markdown(f"### 🪐 Astro Transit Timeline for **NIFTY** on {selected_date.strftime('%d-%b-%Y')}")
st.markdown(f"Showing events from **{start_time.strftime('%I:%M %p')}** to **{end_time.strftime('%I:%M %p')}**")

st.table(df_transits)
