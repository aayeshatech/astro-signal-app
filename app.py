import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, time

st.set_page_config(page_title="🌌 Astro Transit Signal", layout="wide")

# --- Title
st.title("🌠 Intraday Astro Signal Report (Transit-Based)")
st.markdown("Using [Astronomics.ai Almanac](https://data.astronomics.ai/almanac/)")

# --- Inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    date = st.date_input("Select Date", datetime.today())
with col2:
    start_time = st.time_input("Start Time", time(9, 15))
with col3:
    end_time = st.time_input("End Time", time(15, 30))
with col4:
    stock = st.selectbox("Select Index", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow Jones"])

if st.button("🔄 Refresh Astro Report"):
    # --- Format inputs
    date_str = date.strftime('%Y-%m-%d')
    start_dt = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)

    # --- Fetch data from Astronomics API
    url = f"https://data.astronomics.ai/almanac/?date={date_str}"
    try:
        r = requests.get(url)
        data = r.json()
        events = data['events']

        df = pd.DataFrame(events)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Filter by time window
        df = df[(df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)]

        if df.empty:
            st.warning("⚠️ No astro transit found for the selected time range.")
        else:
            # Format for better readability
            df['Time'] = df['timestamp'].dt.strftime('%H:%M')
            df['Planet'] = df['planet'].str.capitalize()
            df['Event'] = df['event_type'].str.replace("_", " ").str.title()
            df = df[['Time', 'Planet', 'Event']]

            # --- Add logic for Bullish/Bearish Tagging (very basic)
            bias_map = {
                'Moon Enters Aries': '🟢 Bullish',
                'Moon Enters Scorpio': '🔴 Bearish',
                'Moon Combust': '🔴 Bearish',
                'Venus Enters Taurus': '🟢 Bullish',
                'Mars Enters Gemini': '🟡 Volatile',
                'Rahu Ketu Transit': '🔴 Reversal',
            }

            df['Sentiment'] = df['Event'].map(bias_map).fillna('🟡 Neutral')

            # Show table
            st.subheader(f"🔭 Astro Transit Report – {stock}")
            st.dataframe(df, use_container_width=True)

            # --- Summary Block
            st.subheader("🧠 Summary Recommendation")
            long_times = df[df['Sentiment'] == '🟢 Bullish']['Time'].tolist()
            short_times = df[df['Sentiment'] == '🔴 Bearish']['Time'].tolist()

            if long_times:
                st.success(f"📈 **Best Long Period(s)**: {', '.join(long_times)}")
            else:
                st.info("📈 No strong long signals found")

            if short_times:
                st.error(f"📉 **Best Short Period(s)**: {', '.join(short_times)}")
            else:
                st.info("📉 No strong short signals found")

    except Exception as e:
        st.error(f"Error fetching astro data: {e}")
