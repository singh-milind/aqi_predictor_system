import streamlit as st
import pandas as pd


from modules.feature_builder import build_features



# =========================
# MAIN
# =========================
def run():

    resources = st.session_state.resources

    model_pm25 = resources["pm25_model"]
    model_pm10 = resources["pm10_model"]
    cols25 = resources["pm25_cols"]
    cols10 = resources["pm10_cols"]
    def predict(input_data):
        df25, df10 = build_features(input_data, cols25, cols10)

        pm25 = model_pm25.predict(df25)[0]
        ratio = model_pm10.predict(df10)[0]
        pm10 = pm25 * ratio

        return pm25, pm10

    st.header("Feature Impact (Sensitivity Analysis)")
    st.caption("See how each parameter affects PM2.5 & PM10")
    st.divider()
    left, icenter, right = st.columns([1.5, 5, 1.5])
    # st.caption("Weather Parameters")

    with icenter:

        ileft,iright = st.columns([3,3])

        # CITY

        with ileft:    
            with st.expander("View Weather Verdict Guide"):
                st.caption(" ")
                st.image("images/weather_verdict.png")

        # INPUTS
            col1, col2 = st.columns(2)

            with col1:
                temp = st.slider(" Temperature (°C)", 0, 50, 25)
                humidity = st.slider(" Humidity (%)", 0, 100, 65)

            with col2:
                precip = st.slider(" Precipitation (mm)", 0, 10, 1)
                pressure = st.slider(" Pressure (hPa)", 950, 1050, 1000)
        
        
        with iright:
            # WIND DIRECTION GUIDE IMAGE
            with st.expander("View Wind Direction guide"):
                col1,coly, col3 = st.columns([1,3,1])
                with coly:
                    st.image("images/compass.png",width=280)
                st.caption("Ex- 350° means Wind is coming from 350° and going towards opposite to that.")
            wind_dir = st.slider("Wind Direction (°)", 0, 360, 90)
            wind_speed = st.slider(" Wind Speed (km/h)", 0, 20, 6)


        # DATE INPUTS
        st.divider()
        st.subheader("Date Parameters")
        st.caption("Can change Base Parameters")
        
        col3, col4, col5 = st.columns(3)

        with col3:
            month = st.slider("Month", 1, 12, 5)

        with col4:
            day = st.slider("Day", 1, 30, 15)

        with col5:
            dow = st.slider("Day (0=Mon)", 0, 6, 2)

        st.divider()


# =========================
# BASE (HARD CODED)
# =========================
    base_input = {
        'temperature_2m': 25,
        'relative_humidity_2m': 65,
        'wind_speed_10m': 6,
        'precipitation': 1,
        'surface_pressure': 1000,
        'month': month,
        'day': day,
        'day_of_week': dow,
        'wind_direction_10m': 90
        }

# BASE PREDICTION
    base_pm25, base_pm10 = predict(base_input)
    colA,colB,colC,colD,colE =st.columns([3,1,1,1,3])
    with colB:
                        st.metric("Base PM2.5 (µg/m³)",round(base_pm25,2))
    with colD:
                        st.metric("Base PM10 (µg/m³)",round(base_pm10,2))

    # =========================
    # BASE PREDICTION
    # =========================

    def modify_and_predict(key, new_value):
        modified = base_input.copy()
        modified[key] = new_value
        return predict(modified)


    t25,t10 =modify_and_predict('temperature_2m', temp)
    h25,h10 =modify_and_predict('relative_humidity_2m', humidity)
    w25,w10=modify_and_predict('wind_speed_10m', wind_speed)
    pre25,pre10=modify_and_predict('precipitation', precip,)
    pres25,pres10=modify_and_predict('surface_pressure', pressure,)
    wd25,wd10=modify_and_predict('wind_direction_10m', wind_dir)

    # =========================
    # FEATURES TO TEST
    # =========================
    features = {
        "Temperature": (t25,t10),
        "Humidity": (h25,h10),
        "Wind Speed": (w25,w10),
        "Precipitation": (pre25,pre10),
        "Pressure": (pres25,pres10),
        "Wind Direction":(wd25,wd10)
    }

    results = []

    for name, (new_pm25,new_pm10) in features.items():

        delta25=new_pm25-base_pm25
        delta10=new_pm10-base_pm10

        pm25_change = ((delta25) / base_pm25) * 100
        pm10_change = ((delta10) / base_pm10) * 100

        results.append({
            "Feature": name,
            "PM2.5 % Change": round(pm25_change, 2),
            "PM10 % Change": round(pm10_change, 2)
        })

    df = pd.DataFrame(results)

    # =========================
    # DISPLAY
    # =========================
    # =========================
    # BAR CHART
    # =========================
    colX,colY,colZ=st.columns([1,4,1])

    with colY:
        st.subheader("📈 Impact (%)")
        st.dataframe(df)
        st.divider()
        st.line_chart(
        df.set_index("Feature"),
    )
