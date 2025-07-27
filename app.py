import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="🔭 Astro Transits Signal", layout="wide")

# === Inputs ===
st.title("📊 Astro Market Transits Report")
col1, col2, col3 = st.columns(3)

with col1:
    selected_date = st.date_input("Select Date", datetime.now().date())

with col2:
    start_time = st.time_input("From Time", datetime.strptime("09:15", "%H:%M").time())

with col3:
    end_time = st.time_input("To Time", datetime.strptime("15:30", "%H:%M").time())

stock_index = st.selectbox("Select Index", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow"])

refresh_data = st.button("🔁 Refresh Astro Data")

# === Convert to ISO format ===
start_dt = datetime.combine(selected_date, start_time)
end_dt = datetime.combine(selected_date, end_time)

# === Load Transits from API ===
@st.cache_data(ttl=3600, show_spinner="Fetching astro transits...")
def load_transits(date_str):
    url = f"https://data.astronomics.ai/almanac/?date={date_str}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return data
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

# === On Button Click: Refresh ===
if refresh_data:
    with st.spinner("⏳ Generating Astro Report..."):
        transits_data = load_transits(selected_date.strftime("%Y-%m-%d"))

        if not transits_data:
            st.error("❌ Could not load astro data.")
        else:
            df_transits = pd.DataFrame(transits_data.get("transits", []))

            if df_transits.empty:
                st.warning("⚠️ No transits found.")
            else:
                df_transits["start_time"] = pd.to_datetime(df_transits["start_time"])
                df_transits["end_time"] = pd.to_datetime(df_transits["end_time"])
                df_transits["mid_time"] = df_transits["start_time"] + (df_transits["end_time"] - df_transits["start_time"]) / 2

                # Filter by selected time range
                df_filtered = df_transits[
                    (df_transits["start_time"] >= start_dt) &
                    (df_transits["end_time"] <= end_dt)
                ].copy()

                if df_filtered.empty:
                    st.warning("⚠️ No transits found in selected time range.")
                else:
                    st.subheader(f"🔭 Transits for {selected_date.strftime('%Y-%m-%d')} ({stock_index})")

                    df_filtered["Time Window"] = df_filtered["start_time"].dt.strftime("%H:%M") + " – " + df_filtered["end_time"].dt.strftime("%H:%M")
                    df_filtered = df_filtered[["Time Window", "planet", "nakshatra", "interpretation", "signal", "summary"]]
                    df_filtered.columns = ["🕒 Time", "🌍 Planet", "✨ Nakshatra", "📖 Interpretation", "📈 Bias", "🧠 Summary"]

                    st.dataframe(df_filtered, use_container_width=True)

                    # === Summary ===
                    bullish = df_filtered[df_filtered["📈 Bias"] == "🟢 Bullish"]
                    bearish = df_filtered[df_filtered["📈 Bias"] == "🔴 Bearish"]

                    best_long = bullish.sort_values(by="🕒 Time").head(1)
                    best_short = bearish.sort_values(by="🕒 Time").head(1)

                    st.markdown("---")
                    st.subheader("🌟 Summary: Astro Trade Window")

                    colA, colB = st.columns(2)
                    with colA:
                        if not best_long.empty:
                            st.success(f"**🔼 Best Long:** {best_long.iloc[0]['🕒 Time']} – {best_long.iloc[0]['🧠 Summary']}")
                        else:
                            st.info("No strong long signals")

                    with colB:
                        if not best_short.empty:
                            st.error(f"**🔽 Best Short:** {best_short.iloc[0]['🕒 Time']} – {best_short.iloc[0]['🧠 Summary']}")
                        else:
                            st.info("No strong short signals")
