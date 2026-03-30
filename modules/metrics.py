import streamlit as st
import joblib
import os
import requests
import zipfile
# import gdown

# @st.cache_resource
# def load_metrics():
#     # if not os.path.exists("models"):

#     #     FILE_ID = "1ja_FHxj2I-lHJHjgbaOSDIljq5nrnCMP"
#     #     url = f"https://drive.google.com/uc?id={FILE_ID}"

#     #     # download zip
#     #     gdown.download(url, "models.zip", quiet=False)

#     #     # unzip
#     #     with zipfile.ZipFile("models.zip", "r") as zip_ref:
#     #         zip_ref.extractall("models")


#     #     # unzip
#     #     with zipfile.ZipFile("models.zip", "r") as zip_ref:
#     #         zip_ref.extractall("models")
#     pm10_metrics=joblib.load("models/pm10_model_metrics.pkl")
#     pm25_metrics=joblib.load("models/pm25_model_metrics.pkl")
#     return pm25_metrics,pm10_metrics

# pm25,pm10 = load_metrics()


def run():

    resources = st.session_state.resources

    pm25 = resources["pm25_metrics"]
    pm10 = resources["pm10_metrics"]

    st.header("Model Evaluation")
    st.caption("Performance metrics for PM2.5 and PM10 models")
    st.divider()
    st.subheader("🔁 Model Workflow")

    st.markdown("""
1. 🌫️ **PM2.5 Model** predicts particulate concentration  
2. 🔗 **Ratio Model** estimates PM10/PM2.5 relationship  
3. 🌪️ **Final PM10 = PM2.5 × Ratio**  
4. 📊 AQI calculated using CPCB & WHO formulas  
""")
    st.info(
    "⚠️ **Model Design Note:** PM2.5 and Ratio models are trained independently to avoid leakage. "
    "The ratio model does NOT use predicted PM2.5 as an input feature. "
)
    st.divider()

    # =========================
    # PM2.5
    # =========================
    st.subheader("PM2.5 Model")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("MAE", round(pm25["MAE"], 2))
    col2.metric("MSE", round(pm25["MSE"], 2))
    col3.metric("RMSE", round(pm25["RMSE"], 2))
    col4.metric("R² Score", round(pm25["R2"], 3))
    st.divider()
    colA,colB,colC = st.columns(3)
    colA.metric("Train R² Score",(round(pm25["Train_R2"], 3)))
    colB.metric("Test R² Score",(round(pm25["Test_r2"], 3)))
    diff25=round(pm25["Train_R2"], 3)-round(pm25["Test_r2"], 3)
    colC.metric("Difference",round(diff25,3))



    st.divider()
    st.divider()

    # =========================
    # PM10
    # =========================
    st.subheader("PM10 Ratio Model")
    st.markdown("Ratio = (PM10 / PM2.5)")
    st.caption(
    "⚠️ PM10 is derived as: PM10 = PM2.5 × predicted ratio. "
    "This model predicts the ratio, not absolute PM10."
)

    col5, col6, col7,col8 = st.columns(4)

    col5.metric("MAE", round(pm10["MAE"], 2))
    col6.metric("MSE", round(pm10["MSE"], 2))
    col7.metric("RMSE", round(pm10["RMSE"], 2))
    col8.metric("R² Score", round(pm10["R2"], 3))


    st.divider()
    colA,colB,colC = st.columns(3)
    colA.metric("Train R² Score",(round(pm10["Train_R2"], 3)))
    colB.metric("Test R² Score",(round(pm10["Test_r2"], 3)))
    diff10=round(pm10["Train_R2"], 3)-round(pm10["Test_r2"], 3)
    colC.metric("Difference",round(diff10,3))
    st.divider()
