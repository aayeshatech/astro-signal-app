import streamlit as st
from datetime import datetime, time
import pandas as pd

# === Astro Mock Aspect Data ===
astro_data = [
    {"time": "08:18", "event": "Moon ⛓ Saturn", "sentiment": "Bearish", "note": "Stop hunt risk"},
    {"time": "14:43", "event": "Venus 🔁 Retrograde", "sentiment": "Bullish", "note": "Trend reversal begins"},
    {"time": "16:26", "event": "Mars 🔗 Rahu", "sentiment": "Bullish", "note": "+1.5% spike likely"},
    {"time": "20:50", "event": "Moon 🔥 Mars", "sentiment": "Bullish", "note": "Overnight follow-up"},
]

# === UI Elements ===
st.set_page_config(page_title="Astro Aspect Timeline Finder", layout="centered")
st.title("🔭 Astro Aspect Bullish/Bearish Timeline")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 25))
with col2:
    start_time = st.time_input("⏱ Start Time", value=time(9, 15))
with col3:
    end_time = st.time_input("⏱ End Time", value=time(15, 30))

symbol = st.text_input("🔍 Enter Stock/Index (e.g., Nifty, BankNifty, Gold)", value="Nifty")

if st.button("🔎 Search Astro Aspects"):
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute

    def is_within_range(t):
        t_obj = datetime.strptime(t, "%H:%M").time()
        total_min = t_obj.hour * 60 + t_obj.minute
        return start_minutes <= total_min <= end_minutes

    filtered_data = [d for d in astro_data if is_within_range(d["time"])]

    if filtered_data:
        st.markdown(f"### 📈 Astro Events for **{symbol.upper()}** on {selected_date.strftime('%A, %d %B %Y')}")
        df = pd.DataFrame(filtered_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No astro events found within the selected time range.")
