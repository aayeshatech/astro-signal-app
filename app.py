import streamlit as st
from datetime import datetime, time
import pandas as pd
import random

# === Streamlit Config ===
st.set_page_config(page_title="🔮 Astro Market Timer", layout="wide")

# === Inputs ===
st.title("🔭 Astro Market Report Generator")

date_input = st.date_input("📅 Select Date", datetime.today())
symbol = st.selectbox("📈 Choose Index/Symbol", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow Jones"])
start_time = st.time_input("🕒 Start Time", value=time(9, 15))
end_time = st.time_input("🕒 End Time", value=time(15, 30))

# === Simulate Astro Timings ===
def get_mocked_astro_data(date, symbol, start_time, end_time):
    # You can replace this with actual API call to DeepSeek or parsing logic
    data = [
        {"Time": "09:15 – 10:45", "Sub-Lord": "Venus", "Nakshatra": "Pushya", "Aspect": "Moon-Venus", "Sentiment": "🟢 Bullish", "Move": "Upside possible in early trade", "Bias": "Buy on dips"},
        {"Time": "10:45 – 12:43", "Sub-Lord": "Sun", "Nakshatra": "Pushya", "Aspect": "Moon-Sun", "Sentiment": "🔴 Bearish", "Move": "Possible drop / weak bounce", "Bias": "Caution advised"},
        {"Time": "12:43 – 14:30", "Sub-Lord": "Jupiter", "Nakshatra": "Pushya", "Aspect": "Moon-Jupiter", "Sentiment": "🟢 Bullish", "Move": "Heavyweights rally", "Bias": "Go Long"},
        {"Time": "14:30 – 15:30", "Sub-Lord": "Ketu", "Nakshatra": "Ashlesha", "Aspect": "Moon-Ketu", "Sentiment": "🔴 Bearish", "Move": "Volatility, drops likely", "Bias": "Avoid trades"},
    ]

    return pd.DataFrame(data)

# === Fetch Astro Data ===
if date_input and symbol:
    df = get_mocked_astro_data(date_input, symbol, start_time, end_time)
    st.subheader(f"📊 Astro Report for {symbol} on {date_input.strftime('%d-%b-%Y')} ({start_time.strftime('%H:%M')} – {end_time.strftime('%H:%M')})")
    st.dataframe(df, use_container_width=True)

    # === Summary Generator ===
    best_long = df[df['Sentiment'].str.contains("🟢")].iloc[0] if not df[df['Sentiment'].str.contains("🟢")].empty else None
    best_short = df[df['Sentiment'].str.contains("🔴")].iloc[0] if not df[df['Sentiment'].str.contains("🔴")].empty else None

    st.markdown("### 🧾 Astro Summary Recommendation")
    if best_long is not None:
        st.success(f"**Best Long Period**: `{best_long['Time']}` ➤ {best_long['Move']} | {best_long['Bias']}")
    else:
        st.info("No clear bullish signal for long trade.")

    if best_short is not None:
        st.error(f"**Best Short/Avoid Period**: `{best_short['Time']}` ➤ {best_short['Move']} | {best_short['Bias']}")
    else:
        st.info("No clear bearish signal for short/hedging.")

