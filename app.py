# astro_signal_app.py

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import pytz
from skyfield.api import load
from skyfield.data import mpc

# === Streamlit Page Setup ===
st.set_page_config(page_title="🔭 Astro Signal Finder", layout="wide")
st.title("🔭 Astro Signal Finder (Bullish/Bearish Timing)")

# === Inputs ===
symbol = st.text_input("Enter Symbol Name (e.g. Nifty, BankNifty, Gold)", value="Nifty")

col1, col2 = st.columns(2)
with col1:
    start_dt = st.datetime_input("Start Date & Time (IST)", value=datetime.now())
with col2:
    end_dt = st.datetime_input("End Date & Time (IST)", value=datetime.now() + timedelta(hours=8))

# === Button to Refresh ===
if st.button("🔁 Refresh Astro Report"):
    # Load ephemeris
    eph = load('de421.bsp')
    ts = load.timescale()

    # Convert time range to UTC
    ist = pytz.timezone('Asia/Kolkata')
    start_utc = ist.localize(start_dt).astimezone(pytz.utc)
    end_utc = ist.localize(end_dt).astimezone(pytz.utc)

    # Time list every 5 minutes
    times = []
    current = start_utc
    while current <= end_utc:
        times.append(ts.utc(current.year, current.month, current.day, current.hour, current.minute))
        current += timedelta(minutes=5)

    # Load planet data
    planets = eph
    moon = planets['moon']
    sun = planets['sun']
    earth = planets['earth']

    # Transit detection
    data = []
    last_status = None
    for t in times:
        astrometric = earth.at(t).observe(moon).apparent()
        ecliptic = astrometric.ecliptic_latlon()
        moon_deg = ecliptic[1].degrees % 360

        # Logic: Example - Use moon position to simulate bullish/bearish
        if 0 <= moon_deg < 90:
            status = "Bullish"
        elif 90 <= moon_deg < 180:
            status = "Bearish"
        elif 180 <= moon_deg < 270:
            status = "Volatile"
        else:
            status = "Bullish"

        if status != last_status:
            data.append({
                "Time (IST)": t.utc_datetime().astimezone(ist).strftime('%Y-%m-%d %H:%M'),
                "Moon Degree": round(moon_deg, 2),
                "Signal": status
            })
            last_status = status

    # === Display Result ===
    df = pd.DataFrame(data)
    st.subheader(f"🕰️ Astro Transits for {symbol}")
    st.dataframe(df, use_container_width=True)

    # === Summary ===
    st.subheader("📊 Summary")
    bullish_periods = df[df["Signal"] == "Bullish"]
    bearish_periods = df[df["Signal"] == "Bearish"]

    if not bullish_periods.empty:
        st.success(f"📈 Best Long Bullish Start: {bullish_periods.iloc[0]['Time (IST)']}")

    if not bearish_periods.empty:
        st.error(f"📉 Best Short Bearish Start: {bearish_periods.iloc[0]['Time (IST)']}")

else:
    st.info("⏳ Enter details and press **Refresh Astro Report** to begin.")
