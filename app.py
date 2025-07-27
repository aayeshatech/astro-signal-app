import streamlit as st
import requests
from datetime import datetime
import pytz

# === Streamlit Config ===
st.set_page_config(page_title="🌍 Astro Transit Report", layout="centered")

# === Title ===
st.title("🔭 Astro Transit Report")

# === Input: City Name and Date ===
city = st.text_input("Enter city name", value="Mumbai")
selected_date = st.date_input("Select Date", value=datetime.today())
refresh = st.button("🔁 Refresh Data")

# === Geolocation Helper ===
def get_lat_lon(city_name):
    try:
        api_key = "YOUR_OPENCAGE_API_KEY"  # Replace with your real key
        geo_url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}"
        response = requests.get(geo_url)
        data = response.json()
        lat = data["results"][0]["geometry"]["lat"]
        lon = data["results"][0]["geometry"]["lng"]
        return lat, lon
    except:
        return None, None

# === Fetch Astro Data ===
def fetch_astro_data(lat, lon, date):
    try:
        url = f"https://data.astronomics.ai/almanac/?latitude={lat}&longitude={lon}&date={date}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return None

# === Format and Display Astro Transits ===
def show_transits(data):
    if not data or "transits" not in data:
        st.error("❌ Could not load astro data.")
        return

    st.subheader("📆 Transits for " + selected_date.strftime("%Y-%m-%d"))

    transits = data["transits"]
    rows = []

    for t in transits:
        planet = t["planet"]
        sign = t["sign"]
        nakshatra = t["nakshatra"]
        start = t["start"]
        end = t["end"]
        start_time = datetime.fromisoformat(start).strftime("%H:%M")
        end_time = datetime.fromisoformat(end).strftime("%H:%M")
        rows.append((start_time + " – " + end_time, planet, sign, nakshatra))

    df = st.dataframe(
        {
            "🕒 Time": [r[0] for r in rows],
            "🌍 Planet": [r[1] for r in rows],
            "♒ Sign": [r[2] for r in rows],
            "✨ Nakshatra": [r[3] for r in rows],
        }
    )

# === Main Logic ===
if city and selected_date and refresh:
    with st.spinner("Fetching coordinates..."):
        lat, lon = get_lat_lon(city)

    if lat is None:
        st.error("❌ Could not find location.")
    else:
        with st.spinner("Fetching transit data..."):
            date_str = selected_date.strftime("%Y-%m-%d")
            astro_data = fetch_astro_data(lat, lon, date_str)
            show_transits(astro_data)
