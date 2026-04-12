import streamlit as st
import pandas as pd
import joblib
import pydeck as pdk

from modules.feature_builder import build_features
from modules.aqi_utils import get_cpcb_aqi


st.set_page_config(layout="wide")

#SEASON DATAFRAME
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

df = season_matrix.copy()

# COLOR MAPPING OF DATAFRAME
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

# MAIN 
def run():
    resources = st.session_state.resources

    model_pm25 = resources["pm25_model"]
    model_pm10 = resources["pm10_model"]
    cols25 = resources["pm25_cols"]
    cols10 = resources["pm10_cols"]
    def predict_aqi(input_data):
        df25, df10 = build_features(input_data, cols25, cols10)

        pm25 = model_pm25.predict(df25)[0]
        ratio = model_pm10.predict(df10)[0]
        pm10 = pm25 * ratio
        aqi = get_cpcb_aqi(pm25, pm10)
        return pm25, pm10, aqi


    st.header(" Scenario Simulator")
    st.caption("See how environmental changes impact AQI")
    st.divider()

    left, icenter, right = st.columns([2,6,2])

    with icenter:
        #CITY
        city = st.selectbox("📍 Select City", [
            'Agartala','Aizawl','Amaravati','Bengaluru','Bhopal','Bhubaneswar',
            'Chandigarh','Chennai','Dehradun','Delhi','Dispur','Faridabad',
            'Gandhinagar','Gangtok','Gurugram','Hyderabad','Imphal','Itanagar',
            'Jaipur','Kohima','Kolkata','Lucknow','Mumbai','Noida','Panaji',
            'Patna','Raipur','Ranchi','Shillong','Shimla','Thiruvananthapuram'
        ])
        #PARAMETER HELP SECTION
        st.subheader("Parameter help")
        st.caption("Required for Parameter Understanding")
        colA,colB = st.columns([1,1])
        with colA:
                with st.expander("View Weather Verdict Guide"):
                    st.image("images/weather_verdict.png")
        with colB:
            with st.expander("View Wind Direction guide"):
                col1,coly, col3 = st.columns([1,3,1])
                with coly:
                    st.image("images/compass.png",width=280)
                st.caption("Ex- 350° means Wind is coming from 350° and going towards opposite to that.")

        with st.expander("View Detailed Seasonal Patterns by Region"):
    

            styled_df = df.style.map(color_map)
            st.dataframe(styled_df, use_container_width=True)
            st.caption("Note: This matrix helps align predictions with India's specific meteorological cycles.")
        st.divider()
        ileft,iright = st.columns([3,3])


        # BASE CONDITIONS
        with ileft:
            st.subheader("🟢 Current Conditions")
            st.caption("Select Base Parameters")
            st.divider()
            st.caption("Weather Parameters")

            col1, col2 = st.columns(2)

            with col1:
                temp = st.slider("Temperature (°C)", 0, 50, 30,key="base_temp")
                humidity = st.slider("Humidity (%)", 0, 100, 60,key="base_humidity")


            with col2:
                precip = st.slider("Precipitation (mm)", 0, 10, 0,key="base_precip")
                pressure = st.slider("Pressure (hPa)", 980, 1050, 1000,key="base_pressure")
            st.caption("Wind Parameters")
            wind_speed = st.slider("Wind Speed (km/h)", 0, 20, 6,key="base_speed")
            wind_dir = st.slider("Wind Direction (°)", 0, 360, 90,key="base_wind_dir")
        # DATE INPUTS
            st.divider()
            st.caption("Date")

            col3, col4, col5 = st.columns(3)

            with col3:
                month = st.slider("Month", 1, 12, 5,key="base_month")

            with col4:
                day = st.slider("Day", 1, 30, 15,key="base_day")

            with col5:
                dow = st.slider("Day (0=Mon)", 0, 6, 2,key="base_dow")




        # MODIFICATIONS
        with iright:
            st.subheader("🔧 Modify Conditions")
            st.caption("Select New Parameters")
            st.divider()
            st.caption("Weather Parameters")


            col6, col7 = st.columns(2)

            with col6:
                new_temp = st.slider("Temperature (°C)", 0, 50, 30,key="new_temp")
                new_humidity = st.slider("Humidity (%)", 0, 100, 60,key="new_humidity")
                

            with col7:
                new_precip = st.slider("Precipitation (mm)", 0, 10, 0,key="new_precip")
                new_pressure = st.slider("Pressure (hPa)", 980, 1050, 1000,key="new_pressure")
            
            st.caption("Wind Parameters")
            new_wind_speed = st.slider("Wind Speed (km/h)", 0, 20, 6,key="new_speed")
            new_wind_dir = st.slider("Wind Direction(°)", 0, 360, 90,key="new_wind_dir")

            # DATE INPUTS
            st.divider()
            st.caption("Date")
            col8, col9, col10 = st.columns(3)

            with col8:
                new_month = st.slider("Month", 1, 12, 5,key="new_month")

            with col9:
                new_day = st.slider("Day", 1, 30, 15,key="new_day")

            with col10:
                new_dow = st.slider("Day (0=Mon)", 0, 6, 2,key="new_dow")
        st.divider()

        # RUN SIMULATION
        if st.button("🚀 Simulate Impact", use_container_width=True):

            base_input = {
                "city": city,
                'temperature_2m': temp,
                'relative_humidity_2m': humidity,
                'wind_speed_10m': wind_speed,
                'precipitation': precip,
                'surface_pressure': pressure,
                'month': month,
                'day': day,
                'day_of_week': dow,
                'wind_direction_10m': wind_dir
            }

            modified_input = base_input.copy()

            modified_input['temperature_2m'] = new_temp
            modified_input['relative_humidity_2m'] = new_humidity
            modified_input['wind_speed_10m'] = new_wind_speed
            modified_input['precipitation'] = new_precip
            modified_input['surface_pressure'] = new_pressure
            modified_input['month'] = new_month
            modified_input['day'] = new_day
            modified_input['day_of_week'] = new_dow
            modified_input['wind_direction_10m'] = new_wind_dir



            # PREDICT

            base_pm25, base_pm10, base_aqi = predict_aqi(base_input)
            new_pm25, new_pm10, new_aqi = predict_aqi(modified_input)

            pm25_delta = new_pm25 - base_pm25
            pm10_delta = new_pm10 - base_pm10
            aqi_delta = new_aqi - base_aqi


            # OUTPUT

            st.subheader("📊 Simulation Result")
            st.markdown("Note: AQI values are reported using CPCB standards.")

            c1, c2, c3 = st.columns([1,1,1])

            with c1:
                with st.container(border=True):
                    st.metric("Baseline PM2.5 (µg/m³)",round(base_pm25),2)
                    st.metric("Simulated PM2.5 (µg/m³)", round(new_pm25, 2), delta=round(pm25_delta, 2))
                    st.metric("PM2.5 Impact", "Smog Risk ↑" if pm25_delta > 0 else "Smog Risk ↓")

            with c2:
                    with st.container(border=True):
                        st.metric("Baseline PM10 (µg/m³)",round(base_pm10),2)
                        st.metric("Simulated PM10 (µg/m³)", round(new_pm10, 2), delta=round(pm10_delta, 2))
                        st.metric("PM10 Impact", "Dust Load ↑" if pm10_delta > 0 else "Dust Load ↓")

            with c3:
                with st.container(border=True):
                    st.metric("Baseline AQI", round(base_aqi,2))
                    st.metric("Simulated AQI", round(new_aqi, 2), delta=round(aqi_delta, 2))
                    st.metric("Overall Air Quality", "Improved" if aqi_delta < 0 else "Deteriorated")
    #MAP
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
