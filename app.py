import streamlit as st
from datetime import datetime
import pandas as pd
import swisseph as swe
from astropy.coordinates import get_body, GeocentricTrueEcliptic
from astropy.time import Time
import astropy.units as u

# === Nakshatra Names (27) ===
nakshatras = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# === Streamlit Config ===
st.set_page_config(page_title="🌓 Planetary Nakshatra Report", layout="centered")
st.title("🌌 Planetary Nakshatra + Longitude")

# === Date Picker ===
selected_date = st.date_input("Select Date", value=datetime.now().date())

# === Helper: Nakshatra by Degree ===
def get_nakshatra(degree):
    segment = degree % 360
    nak_index = int(segment // (360 / 27))
    return nakshatras[nak_index]

# === Main Report Function ===
def calculate_positions(selected_date):
    report = []
    year, month, day = selected_date.year, selected_date.month, selected_date.day
    jd = swe.julday(year, month, day)
    t = Time(selected_date.isoformat())

    astro_planets = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]

    # Astropy Planets
    for planet in astro_planets:
        try:
            body = get_body(planet, t)
            ecl = body.transform_to(GeocentricTrueEcliptic())
            lon = ecl.lon.deg
            nak = get_nakshatra(lon)
            report.append({
                'Planet': planet.capitalize(),
                'Longitude': round(lon, 2),
                'Nakshatra': nak,
                'Source': 'Astropy'
            })
        except Exception as e:
            report.append({'Planet': planet.capitalize(), 'Longitude': 'Error', 'Nakshatra': '-', 'Source': str(e)})

    # Swisseph: Rahu & Ketu
    rahu_lon = swe.calc_ut(jd, swe.TRUE_NODE)[0]
    ketu_lon = (rahu_lon + 180) % 360
    report.append({'Planet': 'Rahu (True)', 'Longitude': round(rahu_lon, 2), 'Nakshatra': get_nakshatra(rahu_lon), 'Source': 'Swisseph'})
    report.append({'Planet': 'Ketu (True)', 'Longitude': round(ketu_lon, 2), 'Nakshatra': get_nakshatra(ketu_lon), 'Source': 'Swisseph'})

    return pd.DataFrame(report)

# === Display Report ===
if selected_date:
    df = calculate_positions(selected_date)
    st.subheader(f"📅 Planetary Nakshatra Positions — {selected_date.strftime('%d %b %Y')}")
    st.dataframe(df)
