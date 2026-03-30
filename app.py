import streamlit as st
import joblib
import os
import gdown
import zipfile

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="AQI System", layout="wide")


@st.cache_resource
def load_all_resources():
    if not os.path.exists("models"):
        FILE_ID = "1ja_FHxj2I-lHJHjgbaOSDIljq5nrnCMP"

        gdown.download(
            id=FILE_ID,
            output="models.zip",
            quiet=False,
            fuzzy=True
        )

        with zipfile.ZipFile("models.zip", "r") as zip_ref:
            zip_ref.extractall("models")

    resources = {
        "pm10_metrics": joblib.load("models/pm10_model_metrics.pkl"),
        "pm25_metrics": joblib.load("models/pm25_model_metrics.pkl"),
        "pm10_model": joblib.load("models/weather_pm10_model.pkl"),
        "pm25_model": joblib.load("models/weather_pm25_model.pkl"),
        "pm10_cols": joblib.load("models/weather_pm10_cols.pkl"),
        "pm25_cols": joblib.load("models/weather_pm25_cols.pkl")
    }

    return resources


# IMPORT MODULES AFTER LOADING
# LOAD FIRST
if "resources" not in st.session_state:
    st.session_state["resources"] = load_all_resources()


# IMPORT AFTER LOADING
import modules.predictor as predictor
import modules.simulator as simulator
import modules.feature as feature
import modules.metrics as metrics


# HEADER
colA, colB = st.columns([9, 1])

with colA:
    st.title("🌍 AQI Prediction System")
    st.caption("⚠️ Note: This system is specifically designed for Indian AQI patterns and conditions.")

with colB:
    st.markdown("### 🔗 Connect")
    st.link_button(
        "LinkedIn",
        "https://www.linkedin.com/in/milind-singh-880a41314/",
        use_container_width=True
    )
    st.link_button(
        "Power BI Dashboard",
        "https://shorturl.at/UxeFd",
        use_container_width=True
    )

st.divider()


# PAGE INIT
if "page" not in st.session_state:
    st.session_state.page = "Predictor"


# NAV BUTTONS
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔮 Predictor", use_container_width=True):
        st.session_state.page = "Predictor"

with col2:
    if st.button("⚙️ Simulator", use_container_width=True):
        st.session_state.page = "Simulator"

with col3:
    if st.button("📊 Feature Importance", use_container_width=True):
        st.session_state.page = "Feature"

with col4:
    if st.button("📈 Model Metrics", use_container_width=True):
        st.session_state.page = "Metrics"

st.divider()


# PAGE ROUTING
page_map = {
    "Predictor": predictor.run,
    "Simulator": simulator.run,
    "Feature": feature.run,
    "Metrics": metrics.run
}

page_map[st.session_state.page]()
