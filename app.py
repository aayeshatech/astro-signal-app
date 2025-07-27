import streamlit as st
from datetime import datetime, date, time, timedelta
from skyfield.api import load, wgs84
import pandas as pd
import pytz

st.set_page_config(page_title="🔭 Astro Timing Report", layout="wide")
st.title("Astro Market Signal Generator")

# Inputs
report_date = st.date_input("Select Date", date.today())
start_time = st.time_input("Start Time", time(9,15))
end_time = st.time_input("End Time", time(15,30))
market_type = st.selectbox("Market Type", ["Indian Market", "Global Market"])
symbol = st.text_input("Symbol/Index (e.g., NIFTY, BANKNIFTY)", value="NIFTY")

planets_all = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]
selected_planets = st.multiselect("Planets to include", planets_all, default=["Moon","Mars","Venus","Sun","Jupiter","Saturn"])

if st.button("Generate Report"):
    tz = pytz.timezone("Asia/Kolkata") if "Indian" in market_type else pytz.UTC
    start_dt = tz.localize(datetime.combine(report_date, start_time))
    end_dt = tz.localize(datetime.combine(report_date, end_time))

    ts = load.timescale()
    eph = load('de421.bsp')
    loc = wgs84.latlon(28.6139, 77.2090) if "Indian" in market_type else None

    aspects = {"Conjunction": 0, "Sextile": 60, "Square": 90, "Trine": 120, "Opposition": 180}
    orb = 2.0  # ±2°
    interval = timedelta(minutes=10)

    times = []
    t = start_dt
    while t <= end_dt:
        times.append(t)
        t += interval

    records = []
    for t in times:
        tt = ts.utc(t.year, t.month, t.day, t.hour, t.minute)
        longitudes = {}
        for p in selected_planets:
            body = eph[p.lower()]
            if loc:
                ast = (eph['earth'] + loc).at(tt).observe(body).apparent()
            else:
                ast = eph['earth'].at(tt).observe(body).apparent()
            lon = ast.ecliptic_latlon()[0].degrees % 360
            longitudes[p] = lon

        for p1 in selected_planets:
            for p2 in selected_planets:
                if p1 >= p2: continue
                diff = abs(longitudes[p1] - longitudes[p2])
                angle = min(diff, 360 - diff)
                for asp, deg in aspects.items():
                    if abs(angle - deg) <= orb:
                        sentiment = "🟢 Bullish" if asp in ["Conjunction","Sextile","Trine"] else "🔴 Bearish"
                        records.append({
                            "Time": t.strftime("%H:%M"),
                            "Aspect": f"{p1} {asp} {p2}",
                            "Angle": round(angle,1),
                            "Sentiment": sentiment
                        })

    df = pd.DataFrame(records)
    if df.empty:
        st.warning("No aspects found in the given time range.")
    else:
        st.success(f"Found {len(df)} Astro Events for {symbol} on {report_date} ({market_type})")
        st.dataframe(df)

        bull = df[df.Sentiment.str.contains("Bullish")]
        bear = df[df.Sentiment.str.contains("Bearish")]

        st.subheader("🟢 Bullish Aspect Times")
        st.dataframe(bull[["Time","Aspect"]])

        st.subheader("🔴 Bearish Aspect Times")
        st.dataframe(bear[["Time","Aspect"]])

        # Summary of best windows
        if not bull.empty:
            long_time = bull.Time.iloc[0] + " – " + bull.Time.iloc[-1]
        else:
            long_time = "None"
        if not bear.empty:
            short_time = bear.Time.iloc[0] + " – " + bear.Time.iloc[-1]
        else:
            short_time = "None"

        st.markdown(f"**Best Long Period**: {long_time}")
        st.markdown(f"**Best Short Period**: {short_time}")

        # Download
        st.download_button("📥 Download Report CSV", data=df.to_csv(index=False), file_name="astro_aspects.csv")
