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
st.title("🌙 Moon Nakshatra + Sign Lord + Sub Lord + Aspect Signal")

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
] * 3  # 27 nakshatras

zodiac_signs = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

sign_lords = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"
]

aspect_sentiment = {
    "Conjunct": "🟡 Volatile",
    "Sextile": "🟢 Bullish",
    "Square": "🔴 Bearish",
    "Trine": "🟢 Bullish",
    "Opposition": "🔴 Bearish"
}

# === Functions ===
def get_nakshatra_deg(moon_long):
    nak_index = int(moon_long // (360 / 27))
    nak_deg = (moon_long % (360 / 27)) * 60 / (360 / 27)  # degrees within nakshatra
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
    signals = []
    orb = 3.0
    aspect_types = {0: "Conjunct", 60: "Sextile", 90: "Square", 120: "Trine", 180: "Opposition"}

    for pid in [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]:
        pl_pos, _ = swe.calc_ut(jd, pid)
        diff = abs((moon_long - pl_pos[0]) % 360)
        for deg, label in aspect_types.items():
            if abs(diff - deg) <= orb or abs((360 - diff) - deg) <= orb:
                aspects.append(f"{planet_names[pid]} {label}")
                signals.append(aspect_sentiment[label])
    return ", ".join(aspects), max(signals, default="⚪ Neutral")

# === Timeline ===
start_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=4))
end_dt = TZ.localize(datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=23, minutes=59))
step = timedelta(minutes=5)

data = []
prev_vals = None

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
        motion = "Direct"  # Moon is always direct
    except Exception as e:
        curr_dt += step
        continue

    current = (nak, zodiac, sub_lord)
    if current != prev_vals:
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
        prev_vals = current

    curr_dt += step

# === Output ===
df = pd.DataFrame(data)
st.markdown(f"### 🌕 Astro Signal Timeline for {symbol} on {selected_date.strftime('%d-%b-%Y')}")
st.dataframe(df, use_container_width=True)
