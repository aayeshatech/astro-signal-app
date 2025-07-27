import streamlit as st
from datetime import datetime, time, timedelta
import pandas as pd

# ==== Page Config ====
st.set_page_config(page_title="🔭 Astro Sentiment Timeline", layout="centered")

st.title("📈 Astro Sentiment Timeline by Date & Time")

# ==== Input Widgets ====
col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Select Date", value=datetime(2025, 7, 25))
with col2:
    selected_stock = st.selectbox("Select Stock/Index", ["Nifty", "BankNifty", "Gold", "Crude", "BTC", "Dow Jones"])

time_range = st.slider("Select Time Range", value=(time(4, 30), time(18, 30)), format="HH:mm")

# ==== Sample Astro Timeline Generator ====
def get_mocked_astro_sentiment(selected_date, start_time, end_time, stock):
    # This simulates a DeepSeek-style astro report.
    sample_data = [
        {"Time": "00:51 – 04:43", "Sub-Lord": "Venus (Ve)", "Nakshatra": "Pushya (Sa)", "Aspect": "Moon-Venus", "Sentiment": "🟢 Bullish", "Market Move": "Steady upside", "Bias": "Buy on dips"},
        {"Time": "04:43 – 05:53", "Sub-Lord": "Sun (Su)", "Nakshatra": "Pushya (Sa)", "Aspect": "Moon-Sun", "Sentiment": "🔴 Bearish", "Market Move": "Risk of gap-down", "Bias": "Avoid longs"},
        {"Time": "05:53 – 07:50", "Sub-Lord": "Moon (Mo)", "Nakshatra": "Pushya (Sa)", "Aspect": "Stable emotions", "Sentiment": "🟢 Bullish", "Market Move": "Recovery", "Bias": "Go Long"},
        {"Time": "07:50 – 09:12", "Sub-Lord": "Mars (Ma)", "Nakshatra": "Pushya (Sa)", "Aspect": "Aggressive Mars", "Sentiment": "🟠 Neutral", "Market Move": "Volatile", "Bias": "Wait"},
        {"Time": "09:12 – 12:43", "Sub-Lord": "Rahu (Ra)", "Nakshatra": "Pushya (Sa)", "Aspect": "Rahu Manipulation", "Sentiment": "🔴 Bearish", "Market Move": "Sharp correction", "Bias": "Caution"},
        {"Time": "12:43 – 15:51", "Sub-Lord": "Jupiter (Ju)", "Nakshatra": "Pushya (Sa)", "Aspect": "Expansion", "Sentiment": "🟢 Bullish", "Market Move": "Heavyweight rally", "Bias": "Best for longs"},
        {"Time": "15:51 – 17:52", "Sub-Lord": "Ketu (Ke)", "Nakshatra": "Ashlesha (Me)", "Aspect": "Mercury Rx", "Sentiment": "🔴 Bearish", "Market Move": "Sudden drop", "Bias": "Avoid"},
        {"Time": "17:52 – EOD", "Sub-Lord": "Ketu (Ke)", "Nakshatra": "Ashlesha (Me)", "Aspect": "Weak Declination", "Sentiment": "🟠 Choppy", "Market Move": "Sideways", "Bias": "Stay flat"},
    ]

    # Filter by time range
    filtered_data = []
    for row in sample_data:
        try:
            time_range_str = row["Time"].replace("EOD", "23:59")
            start_str, end_str = time_range_str.split("–")
            t_start = datetime.strptime(start_str.strip(), "%H:%M").time()
            t_end = datetime.strptime(end_str.strip(), "%H:%M").time()

            if t_start >= start_time and t_start <= end_time:
                filtered_data.append(row)
        except:
            continue

    return pd.DataFrame(filtered_data)

# ==== Process ====
if st.button("🔍 Generate Astro Sentiment Report"):
    df_result = get_mocked_astro_sentiment(
        selected_date,
        start_time=time_range[0],
        end_time=time_range[1],
        stock=selected_stock
    )

    if not df_result.empty:
        st.success(f"Showing Astro Sentiment for {selected_stock} on {selected_date.strftime('%d-%b-%Y')}")
        st.dataframe(df_result, use_container_width=True)
    else:
        st.warning("No sentiment data found for selected time range.")

# ==== Footer ====
st.caption("🔭 Powered by Astro-Simulation (DeepSeek-style mock) – No API access yet")
