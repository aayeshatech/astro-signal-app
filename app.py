import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Set timezone and Streamlit page config
tz = pytz.timezone("Asia/Kolkata")
st.set_page_config(page_title="📈 Astro Transit Timeline", layout="centered")

# Title
st.title("📈 Astro Transit Timeline")

# Set fixed location
location = "Mumbai, India"
st.markdown(f"**Location:** {location}")

# Date input
selected_date = st.date_input("📅 Select Date", value=datetime.now(tz).date())

# Define a mock transit list (same events each day — can be replaced with real API logic)
astro_transits = [
    {"time": "10:15 AM", "event": "Moon conjunct Saturn", "signal": "🔴 Bearish"},
    {"time": "11:30 AM", "event": "Venus trine Jupiter", "signal": "🟢 Bullish"},
    {"time": "01:05 PM", "event": "Mars sextile Mercury", "signal": "🟡 Volatile"},
    {"time": "02:40 PM", "event": "Sun opposite Neptune", "signal": "🔴 Bearish"},
    {"time": "04:20 PM", "event": "Moon trine Venus", "signal": "🟢 Bullish"},
]

# Create a DataFrame for display
df_transits = pd.DataFrame(astro_transits)

# Display heading for report
st.markdown(f"### 🪐 Astro Transit Timeline for **NIFTY** on {selected_date.strftime('%d-%b-%Y')}")

# Show transit table
st.table(df_transits)
