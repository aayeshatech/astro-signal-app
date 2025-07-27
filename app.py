def check_aspect_signal(jd, moon_long):
    aspects = []
    signal = "Neutral"
    orb = 3.0
    aspect_types = {
        60: ("Sextile", "Bullish"),
        120: ("Trine", "Bullish"),
        90: ("Square", "Bearish"),
        180: ("Opposition", "Bearish"),
        0: ("Conjunct", "Neutral")  # We’ll ignore this
    }

    found_bullish = False
    found_bearish = False

    for pid in [swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]:
        pl_pos, _ = swe.calc_ut(jd, pid)
        diff = abs((moon_long - pl_pos[0]) % 360)

        for deg, (label, sentiment) in aspect_types.items():
            if abs(diff - deg) <= orb or abs((360 - diff) - deg) <= orb:
                aspects.append(f"{planet_names[pid]} {label}")
                if sentiment == "Bullish":
                    found_bullish = True
                elif sentiment == "Bearish":
                    found_bearish = True

    # Signal priority: Bullish > Bearish > Neutral
    if found_bullish:
        signal = "🟢 Bullish"
    elif found_bearish:
        signal = "🔴 Bearish"
    else:
        signal = "⚪ No Aspect"

    return ", ".join(aspects), signal
