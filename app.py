from astropy.coordinates import get_body, solar_system_ephemeris
from astropy.coordinates import GeocentricTrueEcliptic
from astropy.time import Time
import astropy.units as u
from datetime import datetime, timedelta
import pytz

def get_transits_for_day(date):
    """Returns a list of important transits for a given date with signal meanings"""
    
    # Timezone setup
    tz = pytz.timezone("Asia/Kolkata")
    start_dt = tz.localize(datetime.combine(date, datetime.min.time()))
    end_dt = start_dt + timedelta(days=1)

    step_minutes = 10  # checks every 10 minutes
    transits = []
    checked_times = []

    # Planet pairs to check for transits
    planets = ['moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'neptune']
    aspects = {
        0: "Conjunction",      # 0°
        60: "Sextile",         # 60°
        90: "Square",          # 90°
        120: "Trine",          # 120°
        180: "Opposition"      # 180°
    }

    signal_map = {
        "Moon conjunct Saturn": "🔴 Bearish",
        "Venus trine Jupiter": "🟢 Bullish",
        "Mars sextile Mercury": "🟡 Volatile",
        "Sun opposite Neptune": "🔴 Bearish",
        "Moon trine Venus": "🟢 Bullish",
    }

    with solar_system_ephemeris.set('de432s'):
        current_time = start_dt
        while current_time < end_dt:
            t = Time(current_time)
            positions = {}
            for planet in planets:
                pos = get_body(planet, t)
                ecliptic = pos.transform_to(GeocentricTrueEcliptic())
                lon = ecliptic.lon.to(u.deg).value % 360
                positions[planet] = lon

            # Check all pairs for aspect
            for p1 in planets:
                for p2 in planets:
                    if p1 == p2: continue
                    angle = abs(positions[p1] - positions[p2])
                    angle = angle if angle <= 180 else 360 - angle
                    for asp_deg, asp_name in aspects.items():
                        if abs(angle - asp_deg) < 1.0:  # Orb of ±1°
                            label = f"{p1.capitalize()} {asp_name.lower()} {p2.capitalize()}"
                            label_sorted = " ".join(sorted(label.split()))
                            readable_time = current_time.strftime("%I:%M %p")
                            signal = signal_map.get(label, None)
                            if signal and readable_time not in checked_times:
                                transits.append({
                                    "time": readable_time,
                                    "transit": label,
                                    "signal": signal
                                })
                                checked_times.append(readable_time)

            current_time += timedelta(minutes=step_minutes)

    return transits
