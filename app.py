import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

# Set timezone
tz = pytz.timezone("Asia/Kolkata")

# Streamlit page config
st.set_page_config(page_title="📈 Astro Transit Timeline", layout="centered")
st.title("📈 Astro Transit Timeline")

# Fixed location display
location = "Mumbai, India"
st.markdown(f"**Location:** {location}")

# Date input
selected_date = st.date_input("📅 Select Date", value=datetime.now(tz).date())

# Start and End time inputs
start_time = st.time_input("⏰ Start Time", value=time(9, 0))   # Default 9:00 AM
end_time = st.time_input("⏰ End Time", value=time(17, 0))      # Default 5:00 PM

# Function to simulate transit data for given date
def get_transits_for_date(date):
    base_transits = [
        {"time": "10:15 AM", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
        {"time": "11:30 AM", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
        {"time": "01:05 PM", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
        {"time": "02:40 PM", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
        {"time": "04:20 PM", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
    ]
    # Rotate list to simulate changes by day
    shift = date.day % len(base_transits)
    rotated = base_transits[shift:] + base_transits[:shift]
    return rotated

astro_transits = get_transits_for_date(selected_date)

# Convert "hh:mm AM/PM" string to datetime.time object
def str_to_time(tstr):
    return datetime.strptime(tstr, "%I:%M %p").time()

# Add event_time_obj to help sorting/filtering
for event in astro_transits:
    event["event_time_obj"] = str_to_time(event["time"])

# Sort by event_time_obj ascending
astro_transits_sorted = sorted(astro_transits, key=lambda x: x["event_time_obj"])

# Filter events within selected start and end times
filtered_transits = [
    event for event in astro_transits_sorted
    if start_time <= event["event_time_obj"] <= end_time
]

# Remove helper key before displaying
for event in filtered_transits:
    event.pop("event_time_obj")

# Convert to DataFrame
df_transits = pd.DataFrame(filtered_transits)

# Show heading and filtered table
st.markdown(f"### 🪐 Astro Transit Timeline for **NIFTY** on {selected_date.strftime('%d-%b-%Y')}")
st.markdown(f"Showing events from **{start_time.strftime('%I:%M %p')}** to **{end_time.strftime('%I:%M %p')}**")
st.table(df_transits)
