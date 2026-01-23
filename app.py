import streamlit as st

st.set_page_config(page_title="Food Delivery Time Prediction")

st.title("🍔 Food Delivery Time Prediction")

st.write("Streamlit GUI for Food Delivery Time Prediction project")

distance = st.number_input("Distance (km)", min_value=0.0, value=5.0)
traffic = st.selectbox("Traffic Condition", ["Low", "Medium", "High"])
weather = st.selectbox("Weather Condition", ["Clear", "Cloudy", "Rainy"])

if st.button("Predict"):
    st.success("⏱ Estimated Delivery Time: 35 minutes (Demo)")
