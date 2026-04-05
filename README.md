# 🌍 AQI Prediction System | End-to-End Air Quality Intelligence Platform

## 📌 Project Overview

This project is an **end-to-end Air Quality Index (AQI) Prediction System** built to predict **PM2.5**, **PM10**, and **AQI values** using **Random Forest Regressor** models.

The system analyzes environmental and meteorological parameters to generate accurate air quality predictions along with **95% confidence intervals**, **health risk categorization**, and **scenario-based simulation outputs**.

It combines:

* **Machine Learning Prediction**
* **Interactive Streamlit Dashboard**
* **Sensitivity / What-if Analysis**
* **Confidence Interval Estimation**
* **Power BI Analytics Dashboard**
* **Real-time API Data Pipeline**

This project is designed as a **real-world decision-support system for air quality monitoring**.

---

## 🎯 Objective

The main objectives of this project are:

* Predict **PM2.5 concentration levels**
* Predict **PM10 levels** using a **ratio-based model**
* Estimate **AQI values** using **CPCB & WHO formulas**
* Classify air quality into categories such as:

  * Good
  * Moderate
  * Poor
  * Very Poor
  * Severe
* Provide a **user-friendly interactive dashboard**
* Support **scenario simulation & feature impact analysis**

---

## 📂 Dataset

Due to GitHub file size limitations, the dataset is hosted externally.

🔗 **Dataset Link:**
https://drive.google.com/file/d/1Fd141VJ2burkhNXBTLwAhM5hAM0Jr6Oi/view?usp=sharing

---

## 🛠️ Tech Stack

* **Python**
* **Pandas**
* **NumPy**
* **Scikit-learn**
* **Matplotlib**
* **Seaborn**
* **Streamlit**
* **Power BI**
* **API Integration**

---

## 📊 Features Used

The model uses environmental and weather-based parameters such as:

* Temperature
* Humidity
* Pressure
* Precipitation
* Wind Speed
* Wind Direction
* Date Features

  * Month
  * Day
  * Weekday

---

## 🤖 Model Workflow

1. Data collection from APIs
2. Data preprocessing & cleaning
3. Missing value handling
4. Feature engineering
5. PM2.5 prediction using Random Forest
6. PM10 estimation using ratio model
7. AQI calculation using CPCB & WHO standards
8. Confidence interval generation
9. Dashboard deployment in Streamlit
10. Reporting dashboard in Power BI

---

## 🔄 Prediction Architecture

### PM2.5 Model

Predicts particulate concentration directly.

### PM10 Ratio Model

PM10 is estimated using:

$$
PM10 = PM2.5 \times Ratio
$$

PM10 = PM2.5 \times Ratio

This separate ratio model helps avoid **data leakage** and improves robustness.

---

## 📈 Model Performance

### PM2.5 Model

* **MAE:** `9.74`
* **MSE:** `239.16`
* **RMSE:** `15.46`
* **R² Score:** `0.794`
* **Train R²:** `0.928`
* **Test R²:** `0.794`

### PM10 Ratio Model

* **MAE:** `0.22`
* **MSE:** `0.17`
* **RMSE:** `0.41`
* **R² Score:** `0.763`
* **Train R²:** `0.916`
* **Test R²:** `0.763`

---

## 🖥️ Dashboard Features

The Streamlit dashboard includes:

* Real-time AQI prediction
* Weather parameter sliders
* Seasonal insights
* Region-wise pattern guide
* What-if simulation
* Sensitivity analysis
* Confidence interval prediction
* AQI severity categorization

---

## 🔍 Sample Prediction Output

Example output from deployed dashboard:

* **Predicted PM2.5:** `69.39 µg/m³`
* **Predicted PM10:** `101.52 µg/m³`
* **Estimated CPCB AQI:** `131.30`
* **AQI Category:** `Moderate`
* **95% CI AQI Range:** `65 – 232`
* **WHO PM2.5 Limit Exceeded By:** `4.63x`
* **WHO PM10 Limit Exceeded By:** `2.26x`

This helps users quickly interpret pollution severity and health risks.

---

## 📊 Power BI Dashboard

🔗 **Power BI Dashboard Link:**
https://shorturl.at/UxeFd

Do check the **Power BI dashboard for visual insights and analysis based on the same dataset used in this project.**


---

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Future Improvements

Several future enhancements are still in the pipeline, including the integration of government prevention measures impact analysis using NLP to evaluate how policies and public advisories influence AQI trends.

---

## 👤 Author

**Milind Singh**

Data Analyst | Machine Learning | Power BI | Streamlit
