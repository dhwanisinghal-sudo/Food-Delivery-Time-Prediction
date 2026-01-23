import streamlit as st
import pandas as pd

st.set_page_config(page_title="Food Delivery Time Prediction", layout="centered")

st.title("🍔 Food Delivery Time Prediction")
st.write("Adjust the inputs and see the estimated delivery time. Time updates dynamically based on conditions.")

# --- User Inputs ---
distance = st.slider("Distance (km)", min_value=0, max_value=20, value=5)
traffic = st.selectbox("Traffic Condition", ["Low", "Medium", "High"])
weather = st.selectbox("Weather Condition", ["Clear", "Cloudy", "Rainy"])

# --- Predict Logic ---
base_time = 20 + (distance * 2)

traffic_effect = 0
if traffic == "Medium":
    traffic_effect = 5
elif traffic == "High":
    traffic_effect = 10

weather_effect = 0
if weather == "Cloudy":
    weather_effect = 2
elif weather == "Rainy":
    weather_effect = 5

total_time = base_time + traffic_effect + weather_effect

# Optional max cap
if total_time > 120:
    total_time = 120

# Color-coded output
if total_time <= 30:
    color = 'green'
elif total_time <= 60:
    color = 'orange'
else:
    color = 'red'

st.markdown(f"### ⏱ Estimated Delivery Time: <span style='color:{color}'>{int(total_time)} minutes</span>", unsafe_allow_html=True)

# --- Optional: Bar chart of effects ---
effect_df = pd.DataFrame({
    'Factor': ['Base Time', 'Traffic Effect', 'Weather Effect'],
    'Minutes': [base_time, traffic_effect, weather_effect]
})

st.bar_chart(effect_df.set_index('Factor'))

