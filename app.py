import streamlit as st
from datetime import datetime, time
import pandas as pd

# Mock Astro Events Data
astro_events = [
    {"datetime": "2025-07-25 08:30", "event": "Sun-Moon Square", "sentiment": "Bearish", "symbol": "Nifty"},
    {"datetime": "2025-07-25 09:45", "event": "Mercury Trine Jupiter", "sentiment": "Bullish", "symbol": "Bank Nifty"},
    {"datetime": "2025-07-25 11:00", "event": "Moon Sextile Venus", "sentiment": "Bullish", "symbol": "Gold"},
    {"datetime": "2025-07-25 14:43", "event": "Venus Retrograde", "sentiment": "Bullish", "symbol": "Nifty"},
    {"datetime": "2025-07-25 17:25", "event": "Moon Conjunct Sun", "sentiment": "Bearish", "symbol": "Bank Nifty"}
]

# Convert to DataFrame
df = pd.DataFrame(astro_events)
df['datetime'] = pd.to_datetime(df['datetime'])

# UI
st.title("🔭 Astro Aspect Report Search")

# Date and time input
date = st.date_input("📅 Select Report Date", datetime(2025, 7, 25).date())
start_time = st.time_input("⏱️ Start Time", time(9, 15))
end_time = st.time_input("⏱️ End Time", time(15, 30))
symbol = st.text_input("📈 Optional: Enter Stock/Index (e.g., Nifty, Bank Nifty, Gold)", "")

# Filter logic
start_dt = datetime.combine(date, start_time)
end_dt = datetime.combine(date, end_time)

mask = (df['datetime'] >= start_dt) & (df['datetime'] <= end_dt)
if symbol:
    mask &= df['symbol'].str.lower() == symbol.lower()

filtered_df = df.loc[mask]

# Result
st.subheader(f"🪐 Astro Aspect Events between {start_time} - {end_time} IST")
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        st.markdown(f"**{row['datetime'].strftime('%H:%M')}** | `{row['symbol']}` | *{row['event']}* → **{row['sentiment']}**")
else:
    st.info("No astro aspect events found in this time range.")
