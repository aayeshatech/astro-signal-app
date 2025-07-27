import streamlit as st
from skyfield.api import load
from datetime import datetime, timedelta
import pandas as pd
import pytz

# === Setup ===
st.set_page_config(page_title="🔭 Astro Market Signal", layout="wide")
st.title("📊 Astro Market Signal Generator")

# === User Inputs ===
date_input = st.date_input("Select Market Date", datetime(2025, 7, 26))
start_time_str = st.text_input("Start Time (HH:MM)", value="09:15")
end_time_str = st.text_input("End Time (HH:MM)", value="15:30")

submit = st.button("🔍 Generate Astro Report")

if submit:
    # Convert to datetime
    tz = pytz.timezone("Asia/Kolkata")
    start_dt = tz.localize(datetime.combine(date_input, datetime.strptime(start_time_str, "%H:%M").time()))
    end_dt = tz.localize(datetime.combine(date_input, datetime.strptime(end_time_str, "%H:%M").time()))

    # Load ephemeris
    planets = load('de421.bsp')
    ts = load.timescale()

    moon = planets['moon']
    major_planets = {
        'Sun': planets['sun'],
        'Mercury': planets['mercury'],
        'Venus': planets['venus'],
        'Mars': planets['mars'],
        'Jupiter': planets['jupiter barycenter'],
        'Saturn': planets['saturn barycenter']
    }

    times = []
    current = start_dt
    while current <= end_dt:
        times.append(ts.utc(current.astimezone(pytz.utc)))
        current += timedelta(minutes=15)

    rows = []
    for t in times:
        row = {'Time': t.utc_datetime().astimezone(tz).strftime('%H:%M')}
        obs = planets['earth'].at(t)
        moon_lon = obs.observe(moon).ecliptic_latlon()[1].degrees % 360
        signals = []

        for name, planet in major_planets.items():
            pl_lon = obs.observe(planet).ecliptic_latlon()[1].degrees % 360
            diff = abs(moon_lon - pl_lon)
            diff = 360 - diff if diff > 180 else diff

            # Check for conjunction
            if diff <= 5:
                if name in ['Jupiter', 'Venus', 'Sun']:
                    signals.append(f"🟢 Moon Conj {name}")
                elif name in ['Saturn', 'Mars']:
                    signals.append(f"🔴 Moon Conj {name}")
            elif 170 <= diff <= 190:
                if name in ['Mars', 'Saturn']:
                    signals.append(f"🔴 Moon Opp {name}")
                elif name == 'Jupiter':
                    signals.append(f"🟢 Moon Opp {name}")
        
        if signals:
            row['Signals'] = " | ".join(signals)
        else:
            row['Signals'] = "–"
        
        rows.append(row)

    df = pd.DataFrame(rows)
    st.write(f"### Astro Report for Nifty & Bank Nifty on {date_input.strftime('%d %b %Y')}")
    st.dataframe(df, use_container_width=True)
