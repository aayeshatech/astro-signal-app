import streamlit as st
import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta, time as dt_time
import pytz

# Set ephemeris path
swe.set_ephe_path('/usr/share/ephe')  # Make sure ephemeris files are present
INDIA_TZ = pytz.timezone("Asia/Kolkata")

# === Get Moon Details Safely ===
def get_moon_details(jd):
    moon_result = swe.calc_ut(jd, swe.MOON)

    # Validate result
    if not isinstance(moon_result, (list, tuple)) or not isinstance(moon_result[0], (int, float)):
        raise ValueError("Invalid result from swe.calc_ut for Moon longitude.")

    moon_long = moon_result[0]

    # Calculate sign lord (zodiac), nakshatra index and sublord
    sign_lord = int(moon_long // 30)
    nak_index = int((moon_long % 30) // (13 + 1/3))
    sublord = int(((moon_long % (13 + 1/3)) / ((13 + 1/3) / 9)))

    return moon_long, sign_lord, nak_index, sublord

# === Check Planetary Aspects ===
def check_aspects(jd):
    events = []
    planets = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]
    names = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    for i, p1 in enumerate(planets):
        lon1 = swe.calc_ut(jd, p1)[0]
        for j, p2 in enumerate(planets):
            if i >= j:
                continue
            lon2 = swe.calc_ut(jd, p2)[0]
            diff = abs(lon1 - lon2) % 360
            if abs(diff - 0) < 1:
                events.append((names[i], names[j], 'Conjunct', '🔴 Bearish'))
            elif abs(diff - 60) < 1:
                events.append((names[i], names[j], 'Sextile', '🟢 Bullish'))
            elif abs(diff - 90) < 1:
                events.append((names[i], names[j], 'Square', '🔴 Bearish'))
            elif abs(diff - 120) < 1:
                events.append((names[i], names[j], 'Trine', '🟢 Bullish'))
            elif abs(diff - 180) < 1:
                events.append((names[i], names[j], 'Opposition', '🔴 Bearish'))
    return events

# === Astro Timeline Generator ===
def generate_astro_timeline(date, symbol, interval=15):
    start_dt = INDIA_TZ.localize(datetime.combine(date, dt_time(0, 0)))
    end_dt = start_dt + timedelta(days=1)
    current = start_dt

    timeline = []
    while current < end_dt:
        utc_dt = current.astimezone(pytz.utc)
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60)

        try:
            moon_long, sign_lord, nak_index, sublord = get_moon_details(jd)
        except Exception as e:
            moon_long, sign_lord, nak_index, sublord = 0.0, -1, -1, -1

        aspect_events = check_aspects(jd)

        signal = '🟡 Neutral'
        if any(e[3] == '🔴 Bearish' for e in aspect_events):
            signal = '🔴 Bearish'
        elif any(e[3] == '🟢 Bullish' for e in aspect_events):
            signal = '🟢 Bullish'

        timeline.append({
            'Symbol': symbol,
            'Time': current.strftime('%I:%M %p'),
            'Moon Long°': round(moon_long, 2),
            'Sign Lord': sign_lord,
            'Nakshatra': nak_index,
            'Sub Lord': sublord,
            'Aspects': ', '.join([f"{a[0]} {a[2]} {a[1]}" for a in aspect_events]),
            'Signal': signal
        })

        current += timedelta(minutes=interval)

    return pd.DataFrame(timeline)

# === Streamlit UI ===
st.set_page_config(page_title="🔮 Astro Signal Timeline", layout="wide")
st.title("📊 Astro Timeline Signal Viewer")

# UI Inputs
symbol_list = [
    "NIFTY", "BANKNIFTY", "PHARMA", "AUTO", "FMCG", "IT", "METAL",
    "PSUBANK", "PVT BANK", "OIL AND GAS", "GOLD", "BTC", "CRUDE", "SILVER",
    "DOWJONES", "NASDAQ"
]
selected_symbol = st.selectbox("📈 Select Symbol", symbol_list)
selected_date = st.date_input("📅 Select Date", value=datetime.now().date())

# Generate Timeline with error handling
with st.spinner("🔄 Calculating astro events..."):
    try:
        df = generate_astro_timeline(selected_date, selected_symbol)
        st.success("✅ Timeline Generated")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, f"{selected_symbol}_astro_{selected_date}.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error generating timeline: {e}")
