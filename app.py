import streamlit as st
import pandas as pd
from datetime import datetime, time
import pytz

# Set timezone
tz = pytz.timezone("Asia/Kolkata")

# Page setup
st.set_page_config(page_title="🪐 Astro Transit Timeline", layout="wide")
st.title("🪐 Astro Transit Timeline Viewer")

# --- User input: Date and time range
selected_date = st.date_input("📅 Select Date", value=datetime(2025, 7, 14))
col1, col2 = st.columns(2)
with col1:
    start_time = st.time_input("⏰ Start Time", value=time(6, 0))
with col2:
    end_time = st.time_input("⏰ End Time", value=time(20, 15))

# Convert input times to datetime
start_dt = tz.localize(datetime.combine(selected_date, start_time))
end_dt = tz.localize(datetime.combine(selected_date, end_time))

# --- Upload Excel File ---
uploaded_file = st.file_uploader("📤 Upload Astro Events Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    st.info("Using sample data below until a file is uploaded.")
    sample_data = {
        "Date": ["2025-07-12", "2025-07-12", "2025-07-14", "2025-07-14", "2025-07-14"],
        "Time": ["10:15", "11:30", "08:50", "11:10", "17:20"],
        "Event": [
            "Moon conjunct Saturn",
            "Venus trine Jupiter",
            "Venus conjunct Moon",
            "Mars opposite Neptune",
            "Mercury trine Pluto"
        ],
        "Signal": ["🔴 Bearish", "🟢 Bullish", "🟢 Bullish", "🔴 Bearish", "🟢 Bullish"]
    }
    df = pd.DataFrame(sample_data)

# --- Process datetime column
df["datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"])
df["datetime"] = df["datetime"].dt.tz_localize("Asia/Kolkata")  # Ensure timezone awareness

# --- Filter by selected datetime range
filtered_df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

# --- Display Output
st.markdown(f"### 🪐 Astro Events on {selected_date.strftime('%d-%b-%Y')} from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
if not filtered_df.empty:
    st.dataframe(filtered_df[["Time", "Event", "Signal"]].reset_index(drop=True), use_container_width=True)
else:
    st.warning("⚠️ No astro events found in the selected time range.")
