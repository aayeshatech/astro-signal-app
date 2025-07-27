import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

tz = pytz.timezone("Asia/Kolkata")

st.set_page_config(page_title="📈 Astro Transit Timeline", layout="centered")
st.title("📈 Astro Transit Timeline")

location = "Mumbai, India"
st.markdown(f"**Location:** {location}")

selected_date = st.date_input("📅 Select Date", value=datetime.now(tz).date())

start_time = st.time_input("⏰ Start Time", value=time(9, 0))  # default 9 AM
end_time = st.time_input("⏰ End Time", value=time(17, 0))   # default 5 PM

def get_transits_for_date(date):
    base_transits = [
        {"time": "10:15 AM", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
        {"time": "11:30 AM", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
        {"time": "01:05 PM", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
        {"time": "02:40 PM", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
        {"time": "04:20 PM", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
    ]
    shift = date.day % len(base_transits)
    rotated = base_transits[shift:] + base_transits[:shift]
    return rotated

astro_transits = get_transits_for_date(selected_date)

def str_to_time(tstr):
    return datetime.strptime(tstr, "%I:%M %p").time()

# Convert and add event time object for sorting/filtering
for event in astro_transits:
    event["event_time_obj"] = str_to_time(event["time"])

# Sort events by time ascending
astro_transits_sorted = sorted(astro_transits, key=lambda x: x["event_time_obj"])

# Filter events within start_time and end_time
filtered_transits = [
    event for event in astro_transits_sorted
    if start_time <= event["event_time_obj"] <= end_time
]

# Remove the helper field before display
for event in filtered_transits:
    event.pop("event_time_obj")

df_transits = pd.DataFrame(filtered_transits)

st.markdown(f"### 🪐 Astro Transit Timeline for **NIFTY** on {selected_date.strftime('%d-%b-%Y')}")
st.markdown(f"Showing events from **{start_time.strftime('%I:%M %p')}** to **{end_time.strftime('%I:%M %p')}**")

st.table(df_transits)
