# aqi_utils.py


# CPCB BREAKPOINTS
pm25_cpcb = [
    (0, 30, 0, 50),
    (30, 60, 50, 100),
    (60, 90, 100, 200),
    (90, 120, 200, 300),
    (120, 250, 300, 400),
    (250, 1000, 400, 500)
]

pm10_cpcb = [
    (0, 50, 0, 50),
    (50, 100, 50, 100),
    (100, 250, 100, 200),
    (250, 350, 200, 300),
    (350, 430, 300, 400),
    (430, 1000, 400, 500)
]

# WHO BREAKPOINTS
pm25_who = [
    (0, 5, 0, 50),
    (5, 15, 50, 100),
    (15, 25, 100, 200),
    (25, 50, 200, 300),
    (50, 1000, 300, 500)
]

pm10_who = [
    (0, 15, 0, 50),
    (15, 45, 50, 100),
    (45, 75, 100, 200),
    (75, 150, 200, 300),
    (150, 1000, 300, 500)
]

# CORE FUNCTION
def sub_index(C, bp):
    for BLO, BHI, ILO, IHI in bp:
        if BLO <= C <= BHI:
            return ((IHI - ILO)/(BHI - BLO)) * (C - BLO) + ILO

    return None 


# FINAL AQI FUNCTIONS
def get_cpcb_aqi(pm25, pm10):
    aqi25 = sub_index(pm25, pm25_cpcb)
    aqi10 = sub_index(pm10, pm10_cpcb)

    values = [v for v in [aqi25, aqi10] if v is not None]

    if not values:
        return None

    return round(max(values), 2)


def get_who_aqi(pm25, pm10):
    aqi25 = sub_index(pm25, pm25_who)
    aqi10 = sub_index(pm10, pm10_who)

    values = [v for v in [aqi25, aqi10] if v is not None]

    if not values:
        return None

    return round(max(values), 2)