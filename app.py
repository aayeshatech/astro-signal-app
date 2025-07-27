import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# === Streamlit Page Config ===
st.set_page_config(page_title="🪐 Astro Transit Report", layout="wide")

# === UI Inputs ===
st.title("🌠 Astro Transit Report")
selected_date = st.date_input("Select date", datetime.today())
location = st.text_input("Enter location (lat,lon)", "19.0760,72.8777")  # Default: Mumbai
refresh_data = st.button("🔄 Refresh Astro Data")

# === Fetch Astro Data ===
@st.cache_data(ttl=3600, show_spinner="Fetching astro data...")
def fetch_astro_data(date, loc):
    try:
        base_url = "https://data.astronomics.ai/almanac"
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "location": loc
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"❌ HTTP {response.status_code} error while fetching data.")
            return None
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

# === Trigger Fetch ===
if refresh_data:
    astro_data = fetch_astro_data(selected_date, location)

    if astro_data:
        st.success(f"✅ Loaded astro data for {selected_date}")
        st.json(astro_data)  # Show raw if needed

        # Sample processing if format is known (example only)
        if "transits" in astro_data:
            df = pd.DataFrame(astro_data["transits"])
            st.dataframe(df)
        else:
            st.warning("⚠️ 'transits' field not found in data.")
    else:
        st.error("❌ Could not load astro data.")
else:
    st.info("👈 Select date/location and click 'Refresh Astro Data'.")

