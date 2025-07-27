import streamlit as st
from datetime import datetime, time, timedelta
import pandas as pd
import pytz
from skyfield.api import load
from skyfield.api import N, E, wgs84  # ✅ E added here

# === Streamlit Page Config ===
st.set_page_config(page_title="🔭 Astro Signal Generator", layout="wide")
st.title("🔭 Astro Market Signal Generator")

# === Sidebar Inputs ===
st.sidebar.header("Select Inputs")
market_date = st.sidebar.date_input("Select Market Date", datetime.today())
market_type = st.sidebar.selectbox("Choose Market Type", ["Indian Market (9:15 AM - 3:30 PM)", "Global Market (24x7)"])
astro_symbols = st.sidebar.multiselect(
    "Select Astro Planets",
    ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],
    default=["Sun", "Moon", "Mercury"]
)

# === Load Ephemeris ===
eph = load('de421.bsp')
ts = load.timescale()

# === Location (Delhi) ===
location = wgs84.latlon(28.6139 * N, 77.2090 * E)

# === Market Time Range ===
if "Indian" in market_type:
    start_time = time(9, 15)
    end_time = time(15, 30)
    interval_minutes = 15
else:
    start_time = time(0, 0)
    end_time = time(23, 59)
    interval_minutes = 60

dt_start = datetime.combine(market_date, start_time)
dt_end = datetime.combine(market_date, end_time)

times = []
cur_time = dt_start
while cur_time <= dt_end:
    times.append(cur_time)
    cur_time += timedelta(minutes=interval_minutes)

t_sf = ts.utc(
    [t.year for t in times],
    [t.month for t in times],
    [t.day for t in times],
    [t.hour for t in times],
    [t.minute for t in times]
)

# === Planet Mapping ===
planet_map = {
    "Sun": eph['sun'],
    "Moon": eph['moon'],
    "Mercury": eph['mercury'],
    "Venus": eph['venus'],
    "Mars": eph['mars'],
    "Jupiter": eph['jupiter barycenter'],
    "Saturn": eph['saturn barycenter'],
    "Uranus": eph['uranus barycenter'],
    "Neptune": eph['neptune barycenter'],
    "Pluto": eph['pluto barycenter']
}

signal_rows = []

if not astro_symbols:
    st.warning("Please select at least one planet to proceed.")
else:
    for i, t in enumerate(t_sf):
        row = {"Time": times[i].strftime("%H:%M")}
        for planet in astro_symbols:
            astrometric = (eph['earth'] + location).at(t).observe(planet_map[planet]).apparent()
            lon, lat, dist = astrometric.ecliptic_latlon()
            row[planet] = round(lon.degrees % 360, 2)
        signal_rows.append(row)

    df = pd.DataFrame(signal_rows)

    # === Display Table ===
    st.subheader(f"📊 Astro Signals for {market_date.strftime('%Y-%m-%d')} ({market_type})")
    st.dataframe(df.set_index("Time"))

    # === Download Option ===
    st.download_button("📥 Download Astro Data as CSV", data=df.to_csv(index=False), file_name="astro_signals.csv")
