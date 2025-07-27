import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Set timezone
tz = pytz.timezone("Asia/Kolkata")

st.set_page_config(page_title="📈 Astro Transit Timeline", layout="centered")
st.title("📈 Astro Transit Timeline")

location = "Mumbai, India"
st.markdown(f"**Location:** {location}")

# Date input widget
selected_date = st.date_input("📅 Select Date", value=datetime.now(tz).date())

# Function to simulate different transits per date (just for demo)
def get_transits_for_date(date):
    # Simple logic to change event times slightly by date
    day = date.day
    base_transits = [
        {"time": "10:15 AM", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
        {"time": "11:30 AM", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
        {"time": "01:05 PM", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
        {"time": "02:40 PM", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
        {"time": "04:20 PM", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
    ]
    # Just to show something changes per date, rotate the list by day % length
    shift = day % len(base_transits)
    rotated = base_transits[shift:] + base_transits[:shift]
    return rotated

astro_transits = get_transits_for_date(selected_date)

df_transits = pd.DataFrame(astro_transits)

st.markdown(f"### 🪐 Astro Transit Timeline for **NIFTY** on {selected_date.strftime('%d-%b-%Y')}")

st.table(df_transits)
