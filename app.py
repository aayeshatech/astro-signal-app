import streamlit as st
from datetime import datetime
import pandas as pd

# === Title and Inputs ===
st.title("📈 Astro Transit Timeline")
selected_stock = st.selectbox("Stock/Index", ["NIFTY", "BANKNIFTY", "GOLD", "CRUDE", "BTC"])
selected_date = st.date_input("Select Date", datetime.now().date())

# === Fetch Transit Data Dynamically ===
def get_transits_for_date(date):
    # Example dummy data based on date just for illustration
    if date == datetime(2025, 7, 30).date():
        return [
            ("10:15 AM", "Moon conjunct Saturn", "🔴 Bearish"),
            ("11:30 AM", "Venus trine Jupiter", "🟢 Bullish"),
            ("01:05 PM", "Mars sextile Mercury", "🟡 Volatile"),
            ("02:40 PM", "Sun opposite Neptune", "🔴 Bearish"),
            ("04:20 PM", "Moon trine Venus", "🟢 Bullish"),
        ]
    elif date == datetime(2025, 7, 31).date():
        return [
            ("09:30 AM", "Moon square Mars", "🔴 Bearish"),
            ("12:00 PM", "Mercury conjunct Sun", "🟢 Bullish"),
            ("03:15 PM", "Moon sextile Jupiter", "🟢 Bullish"),
        ]
    else:
        return [("No transits", "No transits for selected date", "⚪ Neutral")]

# === Generate DataFrame ===
transit_data = get_transits_for_date(selected_date)
df = pd.DataFrame(transit_data, columns=["Time", "Transit", "Signal"])

# === Display Output ===
st.subheader(f"Astro Transit Timeline for {selected_stock} on {selected_date.strftime('%d-%b-%Y')}")
st.table(df)
