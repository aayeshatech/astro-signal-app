import streamlit as st
from datetime import datetime, timedelta, time as dtime
import pandas as pd
import pytz
from astropy.coordinates import get_body, solar_system_ephemeris, get_body_barycentric_posvel
from astropy.coordinates import GeocentricTrueEcliptic
from astropy.time import Time
import astropy.units as u
import math

# === Streamlit Page Config ===
st.set_page_config(page_title="🌕 Astro Market Signal App", layout="wide")

# === UI ===
st.title("🌌 Astro Market Signal Generator")
st.markdown("Generate Astro Bullish/Bearish Signal Timeline by Date and Market")

# === Sidebar Inputs ===
st.sidebar.header("🗓️ Input Config")
selected_date = st.sidebar.date_input("Select Date", datetime.now().date())
start_time = st.sidebar.time_input("Start Time", dtime(4, 30))
end_time = st.sidebar.time_input("End Time", dtime(23, 59))

market_option = st.sidebar.selectbox("Select Market", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow Jones"])

# === Define Planets for Aspects ===
planet_list = ["moon", "sun", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]

# === Aspect Check Function ===
def calculate_aspects(target_date):
    events = []
    tz = pytz.timezone("Asia/Kolkata")
    start_dt = tz.localize(datetime.combine(target_date, start_time))
    end_dt = tz.localize(datetime.combine(target_date, end_time))
    
    current = start_dt
    delta = timedelta(minutes=15)
    
    with solar_system_ephemeris.set('builtin'):
        while current <= end_dt:
            t = Time(current)
            longitudes = {}
            for planet in planet_list:
                body = get_body(planet, t)
                geo = body.transform_to(GeocentricTrueEcliptic())
                longitudes[planet] = geo.lon.degree % 360
            
            # Check aspects between each planet pair
            for i, p1 in enumerate(planet_list):
                for p2 in planet_list[i+1:]:
                    diff = abs(longitudes[p1] - longitudes[p2])
                    diff = min(diff, 360 - diff)
                    
                    for angle, label in zip([0, 60, 90, 120, 180], ["Conjunction", "Sextile", "Square", "Trine", "Opposition"]):
                        if abs(diff - angle) < 1.5:
                            events.append({
                                "time": current.strftime("%H:%M"),
                                "aspect": label,
                                "planets": f"{p1.capitalize()}-{p2.capitalize()}",
                                "angle": angle
                            })
            current += delta
    return pd.DataFrame(events)

# === Mapping Aspects to Sentiment ===
def interpret_aspect(row):
    if row['aspect'] in ["Conjunction", "Trine"]:
        return "🟢 Bullish"
    elif row['aspect'] in ["Square", "Opposition"]:
        return "🔴 Bearish"
    else:
        return "🟡 Neutral"

# === Generate Report ===
if st.button("🔍 Generate Astro Signal Report"):
    st.subheader(f"📊 Astro Report for {market_option} | {selected_date.strftime('%d-%b-%Y')}")
    report_df = calculate_aspects(selected_date)
    if report_df.empty:
        st.warning("No major aspects found in selected time range.")
    else:
        report_df['Sentiment'] = report_df.apply(interpret_aspect, axis=1)
        report_df = report_df.sort_values(by="time")
        for _, row in report_df.iterrows():
            st.markdown(f"**{row['time']}** | {row['planets']} | {row['aspect']} ({row['angle']}°) → {row['Sentiment']}")

        # Summary block
        bullish = report_df[report_df['Sentiment'].str.contains("Bullish")].shape[0]
        bearish = report_df[report_df['Sentiment'].str.contains("Bearish")].shape[0]
        neutral = report_df[report_df['Sentiment'].str.contains("Neutral")].shape[0]

        st.markdown("---")
        st.markdown(f"🔎 **Summary:** 🟢 Bullish: {bullish} | 🔴 Bearish: {bearish} | 🟡 Neutral: {neutral}")

        st.info("Next Step: Add Trading Protocols and Risk Zones per aspect")
