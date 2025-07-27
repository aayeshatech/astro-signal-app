import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# === Page Config ===
st.set_page_config(page_title="📈 Astro Market Report", layout="wide")

# === App Title ===
st.title("🔮 Astro Market Timing & Sentiment Report")
st.markdown("Select date, time range, and index. Click **Refresh Report** to update based on planetary changes.")

# === Inputs ===
col1, col2, col3 = st.columns(3)
with col1:
    selected_date = st.date_input("📅 Select Date", datetime.today())
with col2:
    start_time = st.time_input("⏰ Start Time", time(9, 15))
with col3:
    end_time = st.time_input("⏰ End Time", time(15, 30))

index = st.selectbox("📊 Select Index", ["Nifty", "Bank Nifty", "Sensex", "Gold", "Crude", "BTC", "Dow Jones"])
refresh = st.button("🔄 Refresh Report")

# === Sample Transit Data (Replace with actual logic/data from Jagannatha Hora) ===
def generate_transit_data(date, start, end):
    raw_periods = [
        ("00:51", "04:43", "Venus", "Pushya", "Moon-Venus influence", "🟢", "Steady upside, banking stocks strong", "Buy on dips"),
        ("04:43", "05:53", "Sun", "Pushya", "Moon-Sun volatility", "🔴", "Risk of gap-down or sudden drop", "Avoid new longs"),
        ("05:53", "07:50", "Moon", "Pushya", "Emotional stability", "🟢", "Recovery possible, good for intraday longs", "Short-term longs"),
        ("07:50", "09:12", "Mars", "Pushya", "Aggressive moves", "🟠", "Volatile swings, no clear direction", "Wait for confirmation"),
        ("09:12", "12:43", "Rahu", "Pushya", "Rahu manipulation", "🔴", "Sharp corrections, false breakouts likely", "Caution – Hedge"),
        ("12:43", "15:51", "Jupiter", "Pushya", "Optimism, expansion", "🟢", "Rally in heavyweights (HDFC, ICICI, RIL)", "Best for longs"),
        ("15:51", "17:52", "Ketu", "Ashlesha", "Mercury Retrograde starts", "🔴", "Panic selling, sudden drops", "Avoid trades"),
        ("17:52", "23:59", "Ketu", "Ashlesha", "Declination weakens", "🟠", "Sideways close, low volumes", "Stay flat")
    ]

    filtered = []
    for entry in raw_periods:
        period_start = datetime.combine(date, datetime.strptime(entry[0], "%H:%M").time())
        period_end = datetime.combine(date, datetime.strptime(entry[1], "%H:%M").time())
        user_start = datetime.combine(date, start)
        user_end = datetime.combine(date, end)
        if period_end >= user_start and period_start <= user_end:
            filtered.append({
                "Time": f"{entry[0]} – {entry[1]}",
                "Moon’s Sub-Lord": entry[2],
                "Nakshatra": entry[3],
                "Planetary Aspect": entry[4],
                "Sentiment": entry[5],
                "Expected Market Move": entry[6],
                "Trading Bias": entry[7],
            })
    return filtered

# === Summary ===
def generate_summary(data):
    if not data:
        return "No data in selected period."
    best_long = ""
    best_short = ""
    for d in data:
        if d["Sentiment"] == "🟢":
            best_long = d["Time"] + " – " + d["Expected Market Move"]
        elif d["Sentiment"] == "🔴":
            best_short = d["Time"] + " – " + d["Expected Market Move"]
    return best_long, best_short

# === Report Generation ===
if refresh:
    data = generate_transit_data(selected_date, start_time, end_time)
    df = pd.DataFrame(data)

    st.subheader(f"📌 Astro Report for {index} — {selected_date.strftime('%d-%b-%Y')}")
    st.dataframe(df, use_container_width=True)

    # Summary
    long_summary, short_summary = generate_summary(data)
    st.markdown("### 📈 Summary")
    st.markdown(f"**🔵 Best Long Period:** {long_summary if long_summary else 'Not Found'}")
    st.markdown(f"**🔴 Best Short Period:** {short_summary if short_summary else 'Not Found'}")
