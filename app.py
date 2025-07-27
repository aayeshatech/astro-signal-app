import streamlit as st
import requests
import json
from datetime import date, datetime

# === Streamlit Page Config ===
st.set_page_config(page_title="🔭 Astro Transits Viewer", layout="wide")

st.title("🔭 Vedic Astro Transits Viewer (Almanac API)")
st.markdown("View planetary transits time-wise from [Astronomics Almanac](https://data.astronomics.ai/almanac/).")

# === Input Section ===
selected_date = st.date_input("📅 Select Date", date.today())

# === Fetch Astro Data ===
def fetch_astro_data(date_str):
    url = f"https://data.astronomics.ai/almanac?date={date_str}"
    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return None, f"❌ HTTP {response.status_code}: Failed to fetch astro data."

        try:
            data = response.json()
        except json.JSONDecodeError:
            return None, "❌ Invalid JSON received from astro API."

        if not data or "transits" not in data:
            return None, "⚠️ No transit data found in API response."

        return data, None

    except requests.exceptions.RequestException as e:
        return None, f"❌ Network error: {e}"

# === Display Results ===
st.subheader(f"📈 Planetary Transits for {selected_date.isoformat()}")
data, error = fetch_astro_data(selected_date.isoformat())

if error:
    st.error(error)
elif data:
    transits = data["transits"]
    if not transits:
        st.warning("No transits found for this date.")
    else:
        # Sort by time
        sorted_transits = sorted(transits, key=lambda x: x.get("timestamp", ""))
        for t in sorted_transits:
            planet = t.get("planet", "Unknown")
            event = t.get("event", "Transit")
            nakshatra = t.get("nakshatra", {}).get("name", "")
            sign = t.get("sign", {}).get("name", "")
            time_str = t.get("timestamp", "N/A")

            # Format time nicely
            try:
                t_dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                local_time = t_dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")
            except:
                local_time = time_str

            st.markdown(f"🔹 **{planet}** – `{event}`")
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;🕒 `{local_time}` &nbsp;&nbsp;🔯 Nakshatra: `{nakshatra}` &nbsp;&nbsp;♒ Sign: `{sign}`")
            st.markdown("---")
else:
    st.info("Select a date to view planetary transits.")

