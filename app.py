import streamlit as st
import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- Location & timezone (default Mumbai) ---
LAT, LON = 19.0760, 72.8777
TZ = pytz.timezone("Asia/Kolkata")

# --- Date Input ---
st.set_page_config(page_title="🌓 Moon Nakshatra + Sub Lord", layout="wide")
st.title("🌕 Moon Nakshatra + D9 + Sub Lord Timeline")

selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 14))

# --- Swiss Ephemeris Config ---
swe.set_ephe_path('/usr/share/ephe')  # Update if you're using local .se1 files

# --- Nakshatra mapping ---
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

def get_nakshatra(moon_long):
    return nakshatras[int(moon_long // (360 / 27))]

def get_d9_sign(moon_long):
    # 3°20' per Navamsa
    d9_index = int((moon_long % 30) // 3.333)
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    base_sign = int(moon_long // 30)
    offset = (d9_index + base_sign * 9) % 12
    return signs[offset]

# --- Time Loop to Track Transitions ---
start_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=4))
end_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=23, minutes=59))
step = timedelta(minutes=5)

data = []
prev_nak, prev_d9 = None, None

curr_dt = start_dt
while curr_dt <= end_dt:
    jd = swe.julday(curr_dt.year, curr_dt.month, curr_dt.day, curr_dt.hour + curr_dt.minute / 60.0)
    moon_long, _ = swe.calc_ut(jd, swe.MOON)[0:2]
    
    nak = get_nakshatra(moon_long)
    d9 = get_d9_sign(moon_long)

    if nak != prev_nak or d9 != prev_d9:
        data.append({
            "Time": curr_dt.strftime("%H:%M"),
            "Nakshatra": nak,
            "D9 Navamsa": d9
        })
        prev_nak, prev_d9 = nak, d9

    curr_dt += step

df = pd.DataFrame(data)

st.markdown(f"### 🌕 Moon Nakshatra + D9 Navamsa Ingress — {selected_date.strftime('%d-%b-%Y')}")
st.dataframe(df, use_container_width=True)
