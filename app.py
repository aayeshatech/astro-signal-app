import streamlit as st
from datetime import datetime
import pandas as pd

astro_events = [
    {"time": "10:15", "event": "Moon conjunct Saturn", "signal": "Bearish", "color": "red"},
    {"time": "11:30", "event": "Venus trine Jupiter", "signal": "Bullish", "color": "green"},
    {"time": "13:05", "event": "Mars sextile Mercury", "signal": "Volatile", "color": "orange"},
    {"time": "14:40", "event": "Sun opposite Neptune", "signal": "Bearish", "color": "red"},
    {"time": "16:20", "event": "Moon trine Venus", "signal": "Bullish", "color": "green"},
]

st.title("🪐 Astro Transit Timeline for NIFTY")

selected_date = st.date_input("Select Date", datetime(2025, 7, 9))
start_time_str = st.text_input("Start Time (HH:MM, 24h format)", "06:30")
end_time_str = st.text_input("End Time (HH:MM, 24h format)", "20:30")

try:
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
except ValueError:
    st.error("Please enter valid start and end times in HH:MM format.")
    st.stop()

for event in astro_events:
    event["time_obj"] = datetime.strptime(event["time"], "%H:%M").time()

filtered_events = [e for e in astro_events if start_time <= e["time_obj"] <= end_time]

st.markdown(f"### Astro Events on {selected_date.strftime('%Y-%m-%d')} from {start_time_str} to {end_time_str}")

if filtered_events:
    # Prepare formatted data with colored signals
    rows = []
    for e in filtered_events:
        signal_text = f"<span style='color:{e['color']}; font-weight:bold;'>{e['signal']}</span>"
        rows.append({"Time": e["time"], "Event": e["event"], "Signal": signal_text})

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Render table with unsafe_allow_html to enable color styling
    st.write(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )
else:
    st.info("No astro events found in the selected time range.")
