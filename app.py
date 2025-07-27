import streamlit as st
from datetime import datetime, time
import pytz

# Set up Streamlit page
st.set_page_config(page_title="🪐 Astro Event Filter", layout="wide")
st.title("🪐 Astro Transit Timeline")

# Timezone
tz = pytz.timezone("Asia/Kolkata")

# --- Sample Astro Events (for 12 July 2025) ---
astro_events = [
    ("10:15", "Moon conjunct Saturn", "🔴 Bearish"),
    ("11:30", "Venus trine Jupiter", "🟢 Bullish"),
    ("13:05", "Mars sextile Mercury", "🟡 Volatile"),
    ("14:40", "Sun opposite Neptune", "🔴 Bearish"),
    ("16:20", "Moon trine Venus", "🟢 Bullish"),
]

# --- Streamlit User Inputs ---
selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 12))

col1, col2 = st.columns(2)
with col1:
    start_time = st.time_input("⏰ Start Time", value=time(6, 30))
with col2:
    end_time = st.time_input("⏰ End Time", value=time(20, 30))

# Convert inputs to timezone-aware datetime
start_dt = tz.localize(datetime.combine(selected_date, start_time))
end_dt = tz.localize(datetime.combine(selected_date, end_time))

# --- Filter Events within Selected Time Range ---
filtered_events = []
for t_str, event, signal in astro_events:
    event_dt = tz.localize(datetime.combine(selected_date, datetime.strptime(t_str, "%H:%M").time()))
    if start_dt <= event_dt <= end_dt:
        filtered_events.append({
            "Time": t_str,
            "Event": event,
            "Signal": signal
        })

# --- Display Results ---
st.markdown(f"### 🪐 Astro Events on {selected_date.strftime('%d-%b-%Y')} from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
if filtered_events:
    st.table(filtered_events)
else:
    st.warning("❌ No astro events found in the selected time range.")
