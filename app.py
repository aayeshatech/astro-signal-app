import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Sector Astro Timeline", layout="wide")
st.title("📊 Sector-wise Astro Trend (Selected Date Only)")

# === Sample Data ===
data = {
    "Sector": [
        "Power", "Pharma", "FMCG", "Auto", "PSUBank", "PvtBank", "Chemical",
        "Oil & Gas", "Defence", "Telecom", "Tea", "Metals", "IT", "Sugar"
    ],
    "AM": ["🟢", "🔴", "🟡", "🔴", "🟢", "🟢", "🔴", "🟢", "🔴", "🟢", "🟡", "🔴", "🟢", "🔴"],
    "Midday": ["🟡", "🔴", "🔴", "🟢", "🟢", "🟡", "🟡", "🟢", "🟡", "🔴", "🟢", "🟡", "🟡", "🟢"],
    "PM": ["🔴", "🟢", "🔴", "🟢", "🟡", "🔴", "🔴", "🔴", "🟢", "🔴", "🔴", "🔴", "🔴", "🟢"],
    "Astro Comment": [
        "Mars aspect Moon = weak close",
        "Venus trine Moon = late rally",
        "Mercury afflicted = weak",
        "Moon-Jupiter trine boosts post-lunch",
        "Moon in Aries + Jupiter in trine",
        "Mars-Ketu affliction weakens closing strength",
        "Venus combust + Mercury afflicted",
        "Sun-Moon trine early strength, fades later",
        "Ketu + Saturn late bullish shift",
        "Volatile Moon-Mercury aspect",
        "Saturn aspect wanes PM",
        "Sun square Rahu = volatility",
        "Mercury combust = weak close",
        "Venus Moon trine supports recovery"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display as styled table
st.dataframe(
    df.style.set_properties(
        **{
            "text-align": "center",
            "font-size": "16px"
        }
    ).set_table_styles([
        {"selector": "th", "props": [("font-size", "18px"), ("text-align", "center")]}])
)
