import streamlit as st
from datetime import datetime
import pandas as pd

# === Streamlit App Layout ===
st.set_page_config(page_title="📈 Astro Signal Timeline", layout="centered")

# === User Input: Date & Stock Name ===
selected_date = st.date_input("📅 Select Astro Date", value=datetime.now().date())
stock_name = st.text_input("📈 Stock/Index Name", value="NIFTY")

# === Dummy Astro Transit Data Function ===
def get_astro_transits(date, symbol):
    # Replace this with actual astro logic or API integration
    return pd.DataFrame([
        {"Time": "10:15 AM", "Transit": "Moon conjunct Saturn", "Signal": "🔴 Bearish"},
        {"Time": "11:30 AM", "Transit": "Venus trine Jupiter", "Signal": "🟢 Bullish"},
        {"Time": "01:05 PM", "Transit": "Mars sextile Mercury", "Signal": "🟡 Volatile"},
        {"Time": "02:40 PM", "Transit": "Sun opposite Neptune", "Signal": "🔴 Bearish"},
        {"Time": "04:20 PM", "Transit": "Moon trine Venus", "Signal": "🟢 Bullish"},
    ])

# === Fetch and Show Astro Table ===
if selected_date and stock_name:
    astro_df = get_astro_transits(selected_date, stock_name)
    st.markdown(f"### 📊 Astro Transit Timeline for **{stock_name.upper()}** on `{selected_date.strftime('%d-%b-%Y')}`")
    st.table(astro_df)
else:
    st.warning("Please select date and enter stock name.")
