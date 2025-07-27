import streamlit as st
import pandas as pd
from datetime import datetime

# === Streamlit Page Config ===
st.set_page_config(page_title="📊 Sector-Wise Astro Dashboard", layout="wide")

st.title("📊 Sector-Wise Astro Outlook Dashboard")

# === Sidebar Date Picker ===
selected_date = st.sidebar.date_input("Select Date", datetime.today())
st.sidebar.markdown("---")

# === Sample Sector-Wise Data (Selected Date Only) ===
data = {
    "Sector": [
        "Power", "Pharma", "FMCG", "Auto", "Metal", "Chemical", "Sugar", "IT",
        "Telecom", "Defence", "Oil & Gas", "PSU Bank", "Pvt Bank"
    ],
    "AM": ["🟢", "🔴", "🟡", "🔴", "🟢", "🟢", "🟡", "🔴", "🟢", "🟢", "🟡", "🔴", "🟢"],
    "Midday": ["🟡", "🔴", "🔴", "🟢", "🟡", "🟡", "🟢", "🟡", "🟡", "🔴", "🟢", "🟡", "🟢"],
    "PM": ["🔴", "🟢", "🔴", "🟢", "🔴", "🟢", "🟢", "🟢", "🟡", "🟢", "🔴", "🟢", "🔴"],
    "Astro Comment": [
        "Mars aspect Moon = weak close",
        "Venus trine Moon = late rally",
        "Mercury afflicted = weak",
        "Moon-Jupiter trine = steady recovery",
        "Rahu affliction = evening drop",
        "Jupiter-Venus harmony = recovery",
        "Moon in Cancer = positive bias",
        "Mercury Rx = tech jittery",
        "Moon trine Mercury = volatile",
        "Mars trine Sun = strength PM",
        "Chandra-Guru yoga = mid strength",
        "Saturn affliction = AM pressure",
        "Jupiter trine = strength AM"
    ]
}

# === Convert to DataFrame ===
df = pd.DataFrame(data)

# === Display Summary Table ===
st.subheader(f"🪐 Astro Trend for: {selected_date.strftime('%A, %d %B %Y')}")
st.dataframe(df, use_container_width=True, hide_index=True)
