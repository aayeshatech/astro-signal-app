import streamlit as st
from datetime import datetime, time

st.title("🪐 Astro Signal Viewer")

# Combine date and time inputs
start_date = st.date_input("Start Date", value=datetime.now().date())
start_time = st.time_input("Start Time", value=datetime.now().time())
start_dt = datetime.combine(start_date, start_time)

end_date = st.date_input("End Date", value=datetime.now().date())
end_time = st.time_input("End Time", value=(datetime.now().time()))
end_dt = datetime.combine(end_date, end_time)

st.write(f"Selected Time Period: {start_dt} → {end_dt}")
