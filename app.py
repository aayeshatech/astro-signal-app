import streamlit as st
from datetime import datetime, timedelta, time as dtime
import pandas as pd

# --- UI Inputs ---
st.set_page_config("🔭 Astro Market Analyzer", layout="wide")

st.title("📊 Astro-Based Market Outlook")

# Select Date & Time Range
col1, col2, col3 = st.columns(3)
with col1:
    selected_date = st.date_input("Select Date", datetime.today())
with col2:
    start_time = st.time_input("Start Time", dtime(9, 15))
with col3:
    end_time = st.time_input("End Time", dtime(15, 30))

# Index Selector
selected_index = st.selectbox("📈 Select Stock Index", ["Nifty", "Bank Nifty", "Gold", "Crude", "BTC", "Dow"])

# --- Simulated Astro Report Generator (mocking DeepSeek) ---
def generate_mock_report(date):
    # Simulate real-time astro timing (dynamic with date)
    base = datetime.combine(date, dtime(0, 51))
    periods = [
        ("Venus", "Pushya", "Moon-Venus", "🟢 Bullish", "Steady upside, banking stocks strong", "Buy on dips", 3.8),
        ("Sun", "Pushya", "Moon-Sun volatility", "🔴 Bearish", "Risk of gap-down or sudden drop", "Avoid new longs", 1.2),
        ("Moon", "Pushya", "Emotional stability", "🟢 Bullish", "Recovery possible, good for intraday longs", "Short-term longs", 1.95),
        ("Mars", "Pushya", "Aggressive moves", "🟠 Neutral", "Volatile swings, no clear direction", "Wait for confirmation", 1.37),
        ("Rahu", "Pushya", "Rahu manipulation", "🔴 Bearish", "Sharp corrections, false breakouts likely", "Caution – Hedge", 3.52),
        ("Jupiter", "Pushya", "Optimism, expansion", "🟢 Bullish", "Rally in heavyweights (HDFC, ICICI, RIL)", "Best for longs", 3.13),
        ("Ketu", "Ashlesha", "Mercury Retro starts", "🔴 Bearish", "Panic selling, sudden drops", "Avoid trades", 2.01),
        ("Ketu", "Ashlesha", "Declination weakens", "🟠 Choppy", "Sideways close, low volumes", "Stay flat", 2.13),
    ]
    
    data = []
    current = base
    for p in periods:
        next_time = current + timedelta(hours=p[6])
        data.append({
            "Start": current.time().strftime("%H:%M"),
            "End": next_time.time().strftime("%H:%M"),
            "Moon’s Sub-Lord": p[0],
            "Nakshatra": p[1],
            "Planetary Aspect": p[2],
            "Sentiment": p[3],
            "Expected Market Move": p[4],
            "Trading Bias": p[5],
            "start_dt": current,
            "end_dt": next_time
        })
        current = next_time
    return pd.DataFrame(data)

# --- Generate report for selected date ---
report_df = generate_mock_report(selected_date)

# --- Filter by selected time range ---
start_dt = datetime.combine(selected_date, start_time)
end_dt = datetime.combine(selected_date, end_time)

filtered_df = report_df[
    (report_df["start_dt"] >= start_dt) & (report_df["end_dt"] <= end_dt)
].copy()

# --- Display Table ---
st.subheader(f"🔭 Astro Report for {selected_index} — {selected_date.strftime('%d %b %Y')}")
st.dataframe(
    filtered_df.drop(columns=["start_dt", "end_dt"]).reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

# --- Summary Generation ---
def generate_summary(df):
    if df.empty:
        return "No astro events in selected range."
    best_long = df[df['Sentiment'] == '🟢 Bullish']
    best_short = df[df['Sentiment'] == '🔴 Bearish']
    long_row = best_long.iloc[0] if not best_long.empty else None
    short_row = best_short.iloc[0] if not best_short.empty else None
    summary = "📌 **Summary:**\n"
    if long_row is not None:
        summary += f"- ✅ Best Long Time: `{long_row['Start']} – {long_row['End']}` | `{long_row['Expected Market Move']}`\n"
    if short_row is not None:
        summary += f"- ❌ Best Short Time: `{short_row['Start']} – {short_row['End']}` | `{short_row['Expected Market Move']}`\n"
    return summary

# --- Show Summary ---
st.markdown("---")
st.markdown(generate_summary(filtered_df))
