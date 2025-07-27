import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

# Set timezone
tz = pytz.timezone("Asia/Kolkata")

# Page setup
st.set_page_config(page_title="🪐 Astro Timeline", layout="wide")
st.title("🪐 Astro Transit Timeline")

# --- User input: Date and time range
selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 14))
col1, col2 = st.columns(2)
with col1:
    start_time = st.time_input("⏰ Start Time", value=time(6, 0))
with col2:
    end_time = st.time_input("⏰ End Time", value=time(20, 15))

# --- Load Astro Data ---
@st.cache_data
def load_astro_data():
    # Replace this with your actual file path (can be .csv or .xlsx)
    return pd.read_excel("astro_events.xlsx")

df = load_astro_data()

# --- Convert and Filter ---
# Parse Date and Time into datetime column
df["datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"])
df["datetime"] = df["datetime"].dt.tz_localize("Asia/Kolkata")  # Ensure timezone aware

# Filter based on user input
start_dt = tz.localize(datetime.combine(selected_date, start_time))
end_dt = tz.localize(datetime.combine(selected_date, end_time))

filtered_df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

# --- Display Results ---
st.markdown(f"### 🪐 Astro Events on {selected_date.strftime('%d-%b-%Y')} from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
if not filtered_df.empty:
    st.dataframe(filtered_df[["Time", "Event", "Signal"]].reset_index(drop=True))
else:
    st.warning("❌ No astro events found in the selected time range.")
