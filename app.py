import streamlit as st
import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta
import pytz
import math

# --- Location & timezone (Mumbai by default) ---
LAT, LON = 19.0760, 72.8777
TZ = pytz.timezone("Asia/Kolkata")

# --- Configure page ---
st.set_page_config(page_title="🌓 Moon Nakshatra + Sub Lord + Aspects", layout="wide")
st.title("🌕 Moon Nakshatra + D9 + Sub Lord + Aspect Timeline")

# --- Date Input ---
selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 14))

# --- Swiss Ephemeris setup ---
swe.set_ephe_path('/usr/share/ephe')  # Change if using .se1 files elsewhere

# --- Nakshatra mapping ---
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# --- Planet names ---
planet_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# --- Get Nakshatra ---
def get_nakshatra(moon_long):
    return nakshatras[int(moon_long // (360 / 27))]

# --- Get D9 Navamsa Sign ---
def get_d9_sign(moon_long):
    d9_index = int((moon_long % 30) // 3.333)
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    base_sign = int(moon_long // 30)
    offset = (d9_index + base_sign * 9) % 12
    return signs[offset]

# --- Get Sub Lord ---
def get_sub_lord(jd):
    # Use cusp calculation to simulate Sub Lord using KP method (Placidus)
    cusps, _ = swe.houses(jd, LAT, LON)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = moon_pos[0]
    sublord_index = int((moon_long % 13.3333) // (13.3333 / 9))  # 13°20' is 1 Nakshatra
    return planet_names[sublord_index % len(planet_names)]

# --- Check for major aspects with Moon ---
def check_moon_aspects(jd, moon_long):
    aspects = []
    major_aspects = {
        0: "Conjunct", 60: "Sextile", 90: "Square",
        120: "Trine", 180: "Opposition"
    }
    orb = 3.0  # degrees of allowable error

    for planet_id in [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]:
        pl_pos, _ = swe.calc_ut(jd, planet_id)
        diff = abs((moon_long - pl_pos[0]) % 360)
        for angle, label in major_aspects.items():
            if abs(diff - angle) <= orb or abs((360 - diff) - angle) <= orb:
                aspects.append(f"{planet_names[planet_id]} {label}")
    return ", ".join(aspects) if aspects else ""

# --- Time Setup ---
start_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=4))
end_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=23, minutes=59))
step = timedelta(minutes=5)

data = []
prev_nak, prev_d9, prev_sub = None, None, None

curr_dt = start_dt
while curr_dt <= end_dt:
    jd = swe.julday(curr_dt.year, curr_dt.month, curr_dt.day,
                    curr_dt.hour + curr_dt.minute / 60.0)

    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = float(moon_pos[0])

    try:
        nak = get_nakshatra(moon_long)
        d9 = get_d9_sign(moon_long)
        sub = get_sub_lord(jd)
        aspects = check_moon_aspects(jd, moon_long)
    except Exception as e:
        st.warning(f"Error at {curr_dt.strftime('%H:%M')}: {e}")
        curr_dt += step
        continue

    if nak != prev_nak or d9 != prev_d9 or sub != prev_sub:
        data.append({
            "Time": curr_dt.strftime("%H:%M"),
            "Nakshatra": nak,
            "D9 Navamsa": d9,
            "Sub Lord": sub,
            "Moon Aspects": aspects
        })
        prev_nak, prev_d9, prev_sub = nak, d9, sub

    curr_dt += step

# --- Show Table ---
df = pd.DataFrame(data)
st.markdown(f"### 🌕 Astro Timeline for {selected_date.strftime('%d-%b-%Y')}")
st.dataframe(df, use_container_width=True)
