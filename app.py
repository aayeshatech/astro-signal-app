import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# === Simulated Astro Data Function (Mimics DeepSeek AI Output) ===
def get_astro_report(date_str, start_time, end_time, symbol):
    # Simulated transitions during the day
    transitions = [
        ("09:15", "10:03", "Moon", "Pushya", "Moon-Sun", "🟢 Bullish", "Mild upmove", "Buy on dips"),
        ("10:03", "10:58", "Sun", "Pushya", "Moon-Venus", "🔴 Bearish", "Sudden drop", "Avoid longs"),
        ("10:58", "11:33", "Mars", "Pushya", "Moon-Mars", "🟠 Neutral", "Volatile", "Wait"),
        ("11:33", "12:43", "Rahu", "Pushya", "Moon-Rahu", "🔴 Bearish", "False breakout", "Hedge"),
        ("12:43", "13:49", "Jupiter", "Pushya", "Moon-Jupiter", "🟢 Bullish", "Index rally", "Go long"),
        ("13:49", "14:55", "Saturn", "Ashlesha", "Moon-Saturn", "🟠 Choppy", "Sideways", "Stay flat"),
        ("14:55", "15:30", "Mercury", "Ashlesha", "Mercury Retro", "🔴 Bearish", "Drop likely", "Avoid trade"),
    ]

    report_data = []
    for t in transitions:
        from_time = datetime.strptime(f"{date_str} {t[0]}", "%Y-%m-%d %H:%M")
        to_time = datetime.strptime(f"{date_str} {t[1]}", "%Y-%m-%d %H:%M")
        if from_time.time() >= start_time and to_time.time() <= end_time:
            report_data.append({
                "Time": f"{t[0]} – {t[1]}",
                "Sub-Lord": t[2],
                "Nakshatra": t[3],
                "Aspect": t[4],
                "Sentiment": t[5],
                "Market Move": t[6],
                "Bias": t[7]
            })

    return pd.DataFrame(report_data)

# === Streamlit UI ===
st.set_page_config("🔭 Astro Market Report", layout="wide")

st.title("🔭 Astro Market Intraday Report")
st.markdown("Get planetary sentiment breakdown from DeepSeek-style logic for Nifty, Bank Nifty, Gold, etc.")

# Input widgets
selected_date = st.date_input("📅 Select Date", value=datetime.today())
col1, col2 = st.columns(2)
with col1:
    start_str = st.time_input("🕒 Start Time", value=datetime.strptime("09:15", "%H:%M").time())
with col2:
    end_str = st.time_input("🕓 End Time", value=datetime.strptime("15:30", "%H:%M").time())

symbol = st.text_input("📈 Enter Stock/Index (e.g., Nifty, BankNifty, Gold)", value="Nifty")

# Button to trigger search
if st.button("🔍 Get Astro Market Report"):
    with st.spinner("Fetching planetary transitions..."):
        df = get_astro_report(str(selected_date), start_str, end_str, symbol)
        if not df.empty:
            st.success(f"Showing astro report for {symbol} on {selected_date}")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No transitions found for selected time range.")
