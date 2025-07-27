import streamlit as st
from datetime import datetime, time

# === Sample astro transit events for 15-Jul-2025 ===
# Times are stored as strings here but parsed later to time objects
astro_events = [
    {"time": "10:15", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
    {"time": "11:30", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
    {"time": "13:05", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
    {"time": "14:40", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
    {"time": "16:20", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
]

st.title("🪐 Astro Transit Timeline for NIFTY")

# Select date (only 2025-07-15 for this demo)
selected_date = st.date_input("Select Date", datetime(2025, 7, 15))

# Start and end time inputs
start_time_str = st.text_input("Start Time (HH:MM, 24h format)", "06:30")
end_time_str = st.text_input("End Time (HH:MM, 24h format)", "20:30")

try:
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
except ValueError:
    st.error("Please enter valid start and end times in HH:MM format.")
    st.stop()

# Convert event times to time objects for filtering
for event in astro_events:
    event["time_obj"] = datetime.strptime(event["time"], "%H:%M").time()

# Filter events within start and end time
filtered_events = [
    e for e in astro_events if start_time <= e["time_obj"] <= end_time
]

st.markdown(f"### Astro Events on {selected_date.strftime('%Y-%m-%d')} from {start_time_str} to {end_time_str}")

if filtered_events:
    # Display filtered events as a table
    st.write(
        {
            "Time": [e["time"] for e in filtered_events],
            "Event": [e["event"] for e in filtered_events],
            "Signal": [e["signal"] for e in filtered_events],
        }
    )
else:
    st.info("No astro events found in the selected time range.")
