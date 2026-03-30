# modules/predictor.py

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import joblib
import os
import requests
import zipfile
# import gdown
import pickle

from modules.feature_builder import build_features
from modules.aqi_utils import get_cpcb_aqi, get_who_aqi




# LOAD MODELS
@st.cache_resource
def load_models():
    # if not os.path.exists("models"):

    #     FILE_ID = "1ja_FHxj2I-lHJHjgbaOSDIljq5nrnCMP"
    #     url = f"https://drive.google.com/uc?id={FILE_ID}"

    #     # download zip
    #     gdown.download(url, "models.zip", quiet=False)

    #     # unzip
    #     with zipfile.ZipFile("models.zip", "r") as zip_ref:
    #         zip_ref.extractall("models")
    model_pm25 = joblib.load("models/weather_pm25_model.pkl")
    model_pm10 = joblib.load("models/weather_pm10_model.pkl")
    cols25 = joblib.load("models/weather_pm25_cols.pkl")
    cols10 = joblib.load("models/weather_pm10_cols.pkl")
    return model_pm25, model_pm10, cols25, cols10

model_pm25, model_pm10, cols25, cols10 = load_models()



# VERDICT FUNCTIONS
def get_who_verdict_emoji(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Moderate"
    elif aqi <= 200:
        return "🟠 Sensitive"
    elif aqi <= 300:
        return "🔴 Unhealthy"
    elif aqi <= 400:
        return "🟣 Very Unhealthy"
    else:
        return "⚫ Hazardous"


def get_cpcb_verdict_emoji(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Satisfactory"
    elif aqi <= 200:
        return "🟠 Moderate"
    elif aqi <= 300:
        return "🔴 Poor"
    elif aqi <= 400:
        return "🟣 Very Poor"
    else:
        return "⚫ Severe"

season_matrix = pd.DataFrame(
    {
        "Jan": ["Winter", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
        "Feb": ["Winter", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
        "Mar": ["Summer", "Pre-Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Apr": ["Summer", "Pre-Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "May": ["Summer", "Extended Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Jun": ["SW Monsoon", "Extended Monsoon", "Summer", "Summer", "Summer", "Summer", "Summer"],
        "Jul": ["SW Monsoon", "Extended Monsoon", "Summer", "Summer", "Monsoon", "Monsoon", "Summer"],
        "Aug": ["SW Monsoon", "Extended Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon"],
        "Sep": ["SW Monsoon", "Extended Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon", "Monsoon"],
        "Oct": ["Retreating Monsoon", "Extended Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon"],
        "Nov": ["Retreating Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon", "Post-Monsoon"],
        "Dec": ["Retreating Monsoon", "Winter", "Winter", "Winter", "Winter", "Winter", "Winter"],
    },
    index=["South", "Northeast", "North", "Central", "East", "West", "NCR"],
)

# Your dataframe (same as before)
df = season_matrix.copy()

# Color mapping
def color_map(val):
    colors = {
        "Winter": "rgba(79, 195, 247, 0.15)",
        "Summer": "rgba(255, 112, 67, 0.15)",
        "Monsoon": "rgba(38, 166, 154, 0.15)",
        "SW Monsoon": "rgba(38, 166, 154, 0.15)",
        "Extended Monsoon": "rgba(38, 166, 154, 0.15)",
        "Pre-Monsoon": "rgba(149, 117, 205, 0.15)",
        "Post-Monsoon": "rgba(255, 202, 40, 0.15)",
        "Retreating Monsoon": "rgba(240, 98, 146, 0.15)",
    }

    borders = {
        "Winter": "#4FC3F7",
        "Summer": "#FF7043",
        "Monsoon": "#26A69A",
        "SW Monsoon": "#26A69A",
        "Extended Monsoon": "#26A69A",
        "Pre-Monsoon": "#9575CD",
        "Post-Monsoon": "#FFCA28",
        "Retreating Monsoon": "#F06292",
    }

    return f"""
        background-color: {colors.get(val, "rgba(255,255,255,0.05)")};
        color: #EAEAEA;
        border: 1px solid {borders.get(val, "#444")};
        border-radius: 10px;
        text-align: center;
        padding: 6px;
        font-size: 12px;
    """

# MAIN FUNCTION
def run():
    resources = st.session_state.resources

    model_pm25 = resources["pm25_model"]
    model_pm10 = resources["pm10_model"]
    cols25 = resources["pm25_cols"]
    cols10 = resources["pm10_cols"]


    st.header("AQI Predictor (Weather Based)")
    st.caption("Predict air quality based on environmental conditions")
    st.divider()

    # CENTERED LAYOUT
    left, icenter, right = st.columns([2, 6, 2])

    with icenter:
        city = st.selectbox("📍 Select City", [
            'Agartala','Aizawl','Amaravati','Bengaluru','Bhopal','Bhubaneswar',
            'Chandigarh','Chennai','Dehradun','Delhi','Dispur','Faridabad',
            'Gandhinagar','Gangtok','Gurugram','Hyderabad','Imphal','Itanagar',
            'Jaipur','Kohima','Kolkata','Lucknow','Mumbai','Noida','Panaji',
            'Patna','Raipur','Ranchi','Shillong','Shimla','Thiruvananthapuram']
            ,accept_new_options=False)
        
        st.subheader("Weather Parameters")
        st.caption("Modify Parameters")
        ileft,iright = st.columns([3,3])

        # CITY
        with ileft:    
        # WEATHER GUIDE IMAGE
            with st.expander("View Weather Verdict Guide"):
                colA, colB, colC = st.columns([1.5,8,1.5])
                with colB:
                    st.caption(" ")
                    st.image("images/weather_verdict.png", width=800)
                    st.caption(" ")
                    



        # INPUTS
            col1, col2 = st.columns(2)

            with col1:
                temp = st.slider(" Temperature (°C)", 0, 50, 25)
                humidity = st.slider(" Humidity (%)", 0, 100, 60)

            with col2:
                precip = st.slider(" Precipitation (mm)", 0, 10, 0)
                pressure = st.slider(" Pressure (hPa)", 980, 1050, 1010)
        
        
        with iright:
            # WIND DIRECTION GUIDE IMAGE
            with st.expander("View Wind Direction guide"):
                st.caption("Degree to Direction")
                colA, colB, colC = st.columns([2.7,3,2.7])
                with colB:
                    st.image("images/compass.png", width=275)
                
                st.caption("Ex- 350° means Wind is coming from 350° and going towards opposite to that.")
            wind_dir = st.slider("Wind Direction (°)", 0, 360, 90)
            wind = st.slider(" Wind Speed (km/h)", 0, 20, 6)


        # DATE INPUTS
        st.divider()
        st.subheader("Date Parameters")
        st.caption("Select Date")
        



        with st.expander("View Detailed Seasonal Patterns by Region"):
    

            styled_df = df.style.map(color_map)
            st.dataframe(styled_df, use_container_width=True)
            st.caption("Note: This matrix helps align predictions with India's specific meteorological cycles.")

        col3, col4, col5 = st.columns(3)

        with col3:
            month = st.slider("Month", 1, 12, 5)

        with col4:
            day = st.slider("Day", 1, 30, 15)

        with col5:
            dow = st.slider("Day (0=Mon)", 0, 6, 2)

        st.divider()

        # PREDICTION BUTTON
        if st.button("🚀 Predict AQI", use_container_width=True):

            input_data = {
                "city": city,
                'temperature_2m': temp,
                'relative_humidity_2m': humidity,
                'wind_speed_10m': wind,
                'precipitation': precip,
                'surface_pressure': pressure,
                'month': month,
                'day': day,
                'day_of_week': dow,
                'wind_direction_10m': wind_dir
            }

            df25, df10 = build_features(input_data, cols25, cols10)

            pm25 = model_pm25.predict(df25)[0]
            ratio = model_pm10.predict(df10)[0]
            pm10 = pm25 * ratio

            cpcb = get_cpcb_aqi(pm25, pm10)
            who  = get_who_aqi(pm25, pm10)


            # RESULTS
            st.subheader("📊 Results")

            r1, r2 = st.columns(2)

            with r1:
                st.metric("PM2.5 (µg/m³)", f"{pm25:.2f}")
                st.metric("CPCB AQI 🇮🇳", f"{cpcb:.2f}")
                st.metric("CPCB Verdict",get_cpcb_verdict_emoji(cpcb))

            with r2:
                st.metric("PM10 (µg/m³)", f"{pm10:.2f}")
                st.metric("WHO AQI 🌍", f"{who:.2f}")
                st.metric("WHO Verdict",get_who_verdict_emoji(who))
    with left:
        city_coords = {
    "Amaravati": {"lat": 16.5412, "lon": 80.5154},
    "Itanagar": {"lat": 27.1004, "lon": 93.6166},
    "Dispur": {"lat": 26.1445, "lon": 91.7362},
    "Patna": {"lat": 25.5941, "lon": 85.1376},
    "Raipur": {"lat": 21.2444, "lon": 81.6306},
    "Panaji": {"lat": 15.4909, "lon": 73.8278},
    "Gandhinagar": {"lat": 23.2156, "lon": 72.6369},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794},
    "Shimla": {"lat": 31.1048, "lon": 77.1734},
    "Ranchi": {"lat": 23.3600, "lon": 85.3300},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Thiruvananthapuram": {"lat": 8.5241, "lon": 76.9366},
    "Bhopal": {"lat": 23.2599, "lon": 77.4126},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Imphal": {"lat": 24.8170, "lon": 93.9368},
    "Shillong": {"lat": 25.5788, "lon": 91.8933},
    "Aizawl": {"lat": 23.7271, "lon": 92.7176},
    "Kohima": {"lat": 25.6701, "lon": 94.1077},
    "Bhubaneswar": {"lat": 20.2961, "lon": 85.8245},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Gangtok": {"lat": 27.3389, "lon": 88.6065},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Agartala": {"lat": 23.8315, "lon": 91.2868},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    "Dehradun": {"lat": 30.3165, "lon": 78.0322},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639},

    # NCR Cities
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Gurugram": {"lat": 28.4595, "lon": 77.0266},
    "Noida": {"lat": 28.5355, "lon": 77.3910},
    "Faridabad": {"lat": 28.4089, "lon": 77.3178},
    "Ghaziabad": {"lat": 28.6692, "lon": 77.4538}
}
        lat=city_coords[city]["lat"]
        lon=city_coords[city]["lon"]
        map_df = pd.DataFrame({
        "lat": [lat],
        "lon": [lon]
    })



        st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=22.5,      # India center
        longitude=78.9,
        zoom=3.2
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"lat": lat, "lon": lon}],
            get_position='[lon, lat]',
            get_radius=40000,
            get_fill_color=[255, 0, 0],
        )
    ]
))