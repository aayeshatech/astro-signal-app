import streamlit as st
from datetime import datetime, time

st.set_page_config(page_title="🔭 Astro Signal Timeline", layout="centered")
st.title("🔭 Astro Signal Timeline")

# === INPUTS ===
stock_name = st.text_input("🔎 Stock or Index Name (e.g., Nifty, BankNifty, Gold)", value="Nifty")

start_date = st.date_input("📅 Start Date", value=datetime.now().date())
start_time = st.time_input("🕒 Start Time", value=datetime.now().time())
start_dt = datetime.combine(start_date, start_time)

st.markdown(f"✅ **Selected Start Time:** `{start_dt.strftime('%Y-%m-%d %H:%M')}`")
st.markdown(f"📊 **Tracking Astro Signals for:** `{stock_name}`")

# === Simulated Transit Events (in real app, generate from astro engine or JHora) ===
# These are static; we filter only those after the selected time
transits = [
    {"planet": "Moon conjunct Saturn", "time": "2025-07-28 10:15", "signal": "🔴 Bearish"},
    {"planet": "Venus trine Jupiter", "time": "2025-07-28 11:30", "signal": "🟢 Bullish"},
    {"planet": "Mars sextile Mercury", "time": "2025-07-28 13:05", "signal": "🟡 Volatile"},
    {"planet": "Sun opposite Neptune", "time": "2025-07-28 14:40", "signal": "🔴 Bearish"},
    {"planet": "Moon trine Venus", "time": "2025-07-28 16:20", "signal": "🟢 Bullish"},
]

# Filter transits after selected datetime
filtered_transits = [t for t in transits if datetime.strptime(t["time"], "%Y-%m-%d %H:%M") >= start_dt]

# === Display Timeline ===
st.markdown("---")
st.subheader("📈 Astro Transit Timeline (Filtered)")

if filtered_transits:
    for t in filtered_transits:
        event_time = datetime.strptime(t["time"], "%Y-%m-%d %H:%M").strftime("%I:%M %p")
        st.write(f"**{event_time}** – {t['planet']} → {t['signal']}")
else:
    st.warning("⚠️ No transits after selected time.")
