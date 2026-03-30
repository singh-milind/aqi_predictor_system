# feature_builder.py

import numpy as np
import pandas as pd

# REGION MAPPING

city_to_region = {
    "Chandigarh": "North", "Shimla": "North", "Chandigarh_PB": "North",
    "Jaipur": "North", "Lucknow": "North", "Dehradun": "North",

    "Amaravati": "South", "Bengaluru": "South", "Thiruvananthapuram": "South",
    "Chennai": "South", "Hyderabad": "South",

    "Patna": "East", "Ranchi": "East", "Bhubaneswar": "East", "Kolkata": "East",

    "Panaji": "West", "Gandhinagar": "West", "Mumbai": "West",

    "Raipur": "Central", "Bhopal": "Central",

    "Itanagar": "Northeast", "Dispur": "Northeast", "Imphal": "Northeast",
    "Shillong": "Northeast", "Aizawl": "Northeast", "Kohima": "Northeast",
    "Gangtok": "Northeast", "Agartala": "Northeast",

    "Delhi": "NCR", "Gurugram": "NCR", "Noida": "NCR",
    "Faridabad": "NCR", "Ghaziabad": "NCR"
}

# SEASON LOGIC

def get_season(region, month):

    if region == 'South':
        if month in [1, 2]: return 'Winter'
        elif month in [3, 4, 5]: return 'Summer'
        elif month in [6, 7, 8, 9]: return 'Southwest Monsoon'
        else: return 'Retreating Monsoon'

    elif region == 'Northeast':
        if month in [12, 1, 2]: return 'Winter'
        elif month in [3, 4]: return 'Pre-Monsoon'
        elif month in [5, 6, 7, 8, 9, 10]: return 'Extended Monsoon'
        else: return 'Post-Monsoon'

    else:
        if month in [12, 1, 2]: return 'Winter'
        elif month in [3, 4, 5, 6]: return 'Summer'
        elif month in [7, 8, 9]: return 'Monsoon'
        else: return 'Post-Monsoon'


# MAIN FEATURE BUILDER

def build_features(input_dict, cols25, cols10):

    data = input_dict.copy()

    # REGION & SEASON
    month = data.get("month")
    city = data.get("city")
    if city!=None:
        region = city_to_region.get(city)
        season = get_season(region, month)

        if region is None:
            raise ValueError(f"City '{city}' not mapped")

        data[f"season_region_{season}_{region}"] = 1

    # INTERACTION FEATURES
    if(data['temperature_2m'] !=None and
       data['wind_speed_10m'] !=None and 
       data['precipitation'] !=None and 
       data['surface_pressure']!=None and
       data['relative_humidity_2m'] != None):
        
        data['temp_humidity'] = data['temperature_2m'] * data['relative_humidity_2m']
        data['wind_precip'] = data['wind_speed_10m'] * data['precipitation']
        data['pressure_temp'] = data['surface_pressure'] * data['temperature_2m']

    # CYCLIC FEATURES
    data['month_sin'] = np.sin(2*np.pi*data['month']/12)
    data['month_cos'] = np.cos(2*np.pi*data['month']/12)

    data['dow_sin'] = np.sin(2*np.pi*data['day_of_week']/7)
    data['dow_cos'] = np.cos(2*np.pi*data['day_of_week']/7)

    data['day_sin'] = np.sin(2*np.pi*data['day']/30)
    data['day_cos'] = np.cos(2*np.pi*data['day']/30)

    data['wind_dir_sin'] = np.sin(np.deg2rad(data['wind_direction_10m']))
    data['wind_dir_cos'] = np.cos(np.deg2rad(data['wind_direction_10m']))

    # DROP ORIGINALS
    for col in ['month', 'day', 'day_of_week', 'wind_direction_10m']:
        data.pop(col, None)

    # DATAFRAME
    df = pd.DataFrame([data])

    # ALIGN WITH TRAIN
    df25 = df.reindex(columns=cols25, fill_value=0)
    df10 = df.reindex(columns=cols10, fill_value=0)

    return df25, df10