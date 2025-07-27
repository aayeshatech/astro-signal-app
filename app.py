import streamlit as st
import requests
from datetime import datetime
import pytz

# === Helper ===
def geocode_location(city_name):
    # Replace with your actual OpenCage API key or any geocoding API
    GEOCODE_API_KEY = "YOUR_API_KEY"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={GEOCODE_API_KEY}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data['results']:
            geometry = data['results'][0]['geometry']
            return geometry['lat'], geometry['lng']
    return None, None

# === UI ===
st.title("♃ Astro Transit Timeline")

city_input = st.text_input("Enter city (e.g., Mumbai, India)", "Mumbai, India")
date_input = st.date_input("Select Date", datetime.today())

if st.button("🔄 Load Astro Data"):
    with st.spinner("Fetching transit data..."):
        lat, lon = geocode_location(city_input)
        if not lat:
            st.error("❌ Could not find location.")
        else:
            date_str = date_input.strftime("%Y-%m-%d")
            api_url = f"https://data.astronomics.ai/almanac/?lat={lat}&lon={lon}&date={date_str}"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    transits = data.get("transits", [])
                    
                    if not transits:
                        st.warning("⚠ No transits found.")
                    else:
                        st.subheader(f"Transits for {date_str}")
                        for item in transits:
                            st.write(f"🪐 **{item['planet']}** → {item['event']} at **{item['time']}**")
                else:
                    st.error(f"❌ Failed to fetch data. Status: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error fetching data: {e}")
