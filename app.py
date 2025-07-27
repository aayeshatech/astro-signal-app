from datetime import datetime
import pytz

# Input date and times
date_str = "2025-07-12"
start_time_str = "06:30"
end_time_str = "20:30"

tz = pytz.timezone('Asia/Kolkata')

# Convert to datetime with timezone
start_dt = tz.localize(datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M"))
end_dt = tz.localize(datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M"))

# Sample event list (time as string, event name, signal)
events = [
    ("10:15", "Moon conjunct Saturn", "Bearish"),
    ("11:30", "Venus trine Jupiter", "Bullish"),
    ("13:05", "Mars sextile Mercury", "Volatile"),
    ("14:40", "Sun opposite Neptune", "Bearish"),
    ("16:20", "Moon trine Venus", "Bullish")
]

filtered_events = []
for t_str, event, signal in events:
    event_dt = tz.localize(datetime.strptime(f"{date_str} {t_str}", "%Y-%m-%d %H:%M"))
    if start_dt <= event_dt <= end_dt:
        filtered_events.append((t_str, event, signal))

# Print filtered events
print("Astro Events on", date_str, "from", start_time_str, "to", end_time_str)
print("Time\tEvent\tSignal")
for t, e, s in filtered_events:
    print(f"{t}\t{e}\t{s}")
