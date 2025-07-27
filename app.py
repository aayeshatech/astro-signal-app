import streamlit as st
import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta
import pytz

# === Setup ===
LAT, LON = 19.0760, 72.8777
TZ = pytz.timezone("Asia/Kolkata")
swe.set_ephe_path('/usr/share/ephe')

st.set_page_config(page_title="🌙 Astro Timeline", layout="wide")
st.title("🌙 Moon Nakshatra + Lords + Aspect Signal Timeline")

selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 14))
symbol = st.selectbox("📈 Select Symbol", ["NIFTY", "Bank NIFTY", "GOLD", "CRUDE", "BTC", "DOW JONES"])

# === Basic Mappings ===
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

planet_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
rulers = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
] * 3  # for 27 nakshatras

zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

sign_lords = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

# === Astro Functions ===
def get_nakshatra_deg(moon_long):
    nak_index = int(moon_long // (360 / 27))
    nak_deg = (moon_long % (360 / 27)) * 60 / (360 / 27)
    return nakshatras[nak_index], rulers[nak_index], round(nak_deg, 2)

def get_sub_lord(jd):
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = moon_pos[0]
    sublord_index = int((moon_long % 13.3333) // (13.3333 / 9))
    return planet_names[sublord_index % 9]

def get_zodiac(moon_long):
    sign_index = int(moon_long // 30)
    return zodiac_signs[sign_index], sign_lords[sign_index]

def check_aspect_signal(jd, moon_long):
    aspects = []
    signal = "⚪ No Aspect"
    orb = 3.0
    aspect_types = {
        60: ("Sextile", "Bullish"),
        120: ("Trine", "Bullish"),
        90: ("Square", "Bearish"),
        180: ("Opposition", "Bearish"),
    }

    found_bullish = False
    found_bearish = False

    for pid in [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]:
        pl_pos, _ = swe.calc_ut(jd, pid)
        diff = abs((moon_long - pl_pos[0]) % 360)

        for deg, (label, sentiment) in aspect_types.items():
            if abs(diff - deg) <= orb or abs((360 - diff) - deg) <= orb:
                aspects.append(f"{planet_names[pid]} {label}")
                if sentiment == "Bullish":
                    found_bullish = True
                elif sentiment == "Bearish":
                    found_bearish = True

    if found_bullish:
        signal = "🟢 Bullish"
    elif found_bearish:
        signal = "🔴 Bearish"

    return ", ".join(aspects), signal

# === Timeline Calculation ===
start_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=4))
end_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=23, minutes=59))
step = timedelta(minutes=5)

data = []
prev_signal = None

curr_dt = start_dt
while curr_dt <= end_dt:
    jd = swe.julday(curr_dt.year, curr_dt.month, curr_dt.day,
                    curr_dt.hour + curr_dt.minute / 60.0)
    moon_pos, _ = swe.calc_ut(jd, swe.MOON)
    moon_long = float(moon_pos[0])

    try:
        nak, star_lord, nak_deg = get_nakshatra_deg(moon_long)
        zodiac, sign_lord = get_zodiac(moon_long)
        sub_lord = get_sub_lord(jd)
        aspects, signal = check_aspect_signal(jd, moon_long)
        motion = "Direct"
    except Exception as e:
        curr_dt += step
        continue

    # Append only if signal changed
    if signal != prev_signal and signal in ["🟢 Bullish", "🔴 Bearish"]:
        data.append({
            "Time": curr_dt.strftime("%H:%M"),
            "Symbol": symbol,
            "Zodiac": zodiac,
            "Sign Lord": sign_lord,
            "Nakshatra": nak,
            "Star Lord": star_lord,
            "Deg in Nak": nak_deg,
            "Sub Lord": sub_lord,
            "Motion": motion,
            "Moon Aspects": aspects,
            "Signal": signal
        })
        prev_signal = signal

    curr_dt += step

# === Output ===
df = pd.DataFrame(data)
st.markdown(f"### 🔁 Signal Flip Timeline for {symbol} on {selected_date.strftime('%d-%b-%Y')}")
st.dataframe(df, use_container_width=True)
