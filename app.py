import streamlit as st
import swisseph as swe
from datetime import datetime, timedelta, time as dtime
import pytz
import pandas as pd

# Set path to ephemeris
swe.set_ephe_path("/usr/share/ephe")  # adjust if you're using local ephemeris files

# Constants
NODES = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
PLANET_NAMES = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
PLANET_COLORS = {
    'Sun': '#FFD700',
    'Moon': '#C0C0C0',
    'Mars': '#FF4500',
    'Mercury': '#7FFFD4',
    'Jupiter': '#FFA500',
    'Venus': '#FF69B4',
    'Saturn': '#8A2BE2',
}

NAKSHATRA_LIST = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu',
    'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
    'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
    'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
    'Uttara Bhadrapada', 'Revati'
]

SIGN_LORDS = [
    'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury',
    'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'
]

def get_moon_details(jd):
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]
    moon_long = moon_pos[0]
    
    nak_index = int((moon_long % 360) // (360 / 27))
    nakshatra = NAKSHATRA_LIST[nak_index]
    
    sign_index = int(moon_long // 30)
    sign_lord = SIGN_LORDS[sign_index]

    sublord_index = int(((moon_long % (360 / 27)) / (360 / 27)) * 9) % 9
    sublord = NODES[sublord_index]

    return moon_long, nakshatra, sign_lord, sublord

def get_signal(sign_lord, sublord):
    bullish_set = {'Moon', 'Venus', 'Jupiter'}
    bearish_set = {'Saturn', 'Mars', 'Rahu', 'Ketu'}
    
    if sign_lord in bullish_set or sublord in bullish_set:
        return '🟢 Bullish'
    elif sign_lord in bearish_set or sublord in bearish_set:
        return '🔴 Bearish'
    else:
        return '🟡 Neutral'

def generate_astro_timeline(selected_date):
    ist = pytz.timezone('Asia/Kolkata')
    timeline = []
    start_dt = ist.localize(datetime.combine(selected_date, dtime(9, 15)))
    end_dt = ist.localize(datetime.combine(selected_date, dtime(15, 30)))
    
    current_time = start_dt
    while current_time <= end_dt:
        utc_time = current_time.astimezone(pytz.utc)
        jd = swe.julday(utc_time.year, utc_time.month, utc_time.day, utc_time.hour + utc_time.minute / 60.0)

        try:
            moon_long, nakshatra, sign_lord, sublord = get_moon_details(jd)
            signal = get_signal(sign_lord, sublord)

            timeline.append({
                "Time": current_time.strftime("%I:%M %p"),
                "Moon Long°": round(moon_long, 2),
                "Nakshatra": nakshatra,
                "Sign Lord": sign_lord,
                "Sub Lord": sublord,
                "Signal": signal
            })
        except Exception as e:
            st.error(f"Error generating data for {current_time}: {e}")

        current_time += timedelta(minutes=30)

    return pd.DataFrame(timeline)

# ==== Streamlit UI ====
st.set_page_config(page_title="🌙 Astro Timeline", layout="wide")
st.title("🪐 Moon Astro Timeline: Bullish vs Bearish")

selected_date = st.date_input("📅 Select Date", datetime.now().date())

if st.button("Generate Timeline"):
    df = generate_astro_timeline(selected_date)

    if not df.empty:
        st.write("### 🔍 Astro Timeline Result")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data generated for this date.")
