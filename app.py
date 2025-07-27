import streamlit as st
import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd

# ============ CONFIG ============
st.set_page_config(page_title="📊 Astro Signal Timeline", layout="centered")

# ============ HEADER ============
st.title("📈 Astro Transit Timeline Report")

# ============ INPUT ============
symbol = st.text_input("Stock or Index Name (e.g., NIFTY, BANKNIFTY, GOLD)", value="NIFTY")

ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist).replace(second=0, microsecond=0)
start_dt = st.datetime_input("Start Date & Time (IST)", value=now_ist)

refresh_button = st.button("🔄 Refresh Report")

# ============ HELPER ============
astro_sentiment_map = {
    "conjunct": "🔴 Bearish",
    "opposite": "🔴 Bearish",
    "square": "🔴 Bearish",
    "trine": "🟢 Bullish",
    "sextile": "🟡 Volatile",
    "quincunx": "🟡 Volatile",
}

def fetch_transits(start_date):
    url = f"https://astroapi.dev/astro/transits?date={start_date.strftime('%Y-%m-%d')}&location=Mumbai"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"❌ Failed to fetch data from Astro API. Status code: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        return None

# ============ MAIN LOGIC ============
if refresh_button or symbol or start_dt:
    with st.spinner("🔍 Fetching astro transit data..."):
        astro_data = fetch_transits(start_dt)

    if astro_data and "transits" in astro_data:
        st.subheader(f"📅 Transit Timeline for {symbol.upper()} on {start_dt.strftime('%d %b %Y')}")

        rows = []
        for transit in astro_data["transits"]:
            try:
                event_time_utc = datetime.fromisoformat(transit["datetime"])
                event_time_ist = event_time_utc.astimezone(ist)
                aspect = transit["aspect"].lower()

                sentiment = "⚪ Neutral"
                for key in astro_sentiment_map:
                    if key in aspect:
                        sentiment = astro_sentiment_map[key]
                        break

                rows.append({
                    "Time (IST)": event_time_ist.strftime("%I:%M %p"),
                    "Transit": f"{transit['planet_1']} {transit['aspect']} {transit['planet_2']}",
                    "Sentiment": sentiment
                })
            except Exception:
                continue

        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No valid transits found.")
    else:
        st.warning("⚠️ Could not load astro data or no transits available.")
