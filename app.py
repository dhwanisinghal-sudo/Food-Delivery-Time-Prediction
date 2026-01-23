import streamlit as st

st.set_page_config(page_title="Food Delivery Time Prediction")

st.title("🍔 Food Delivery Time Prediction")
st.write("Enter the details below to get an estimated delivery time.")

# --- User Inputs ---
distance = st.number_input("Distance (km)", min_value=0.0, value=5.0)
traffic = st.selectbox("Traffic Condition", ["Low", "Medium", "High"])
weather = st.selectbox("Weather Condition", ["Clear", "Cloudy", "Rainy"])

# --- Predict Button ---
if st.button("Predict Delivery Time"):
    # Base delivery time formula
    time = 20 + (distance * 2)  # base time + distance factor
    
    # Traffic effect
    if traffic == "Medium":
        time += 5
    elif traffic == "High":
        time += 10
    
    # Weather effect
    if weather == "Rainy":
        time += 5
    elif weather == "Cloudy":
        time += 2  # optional small effect
    
    # Display result
    st.success(f"⏱ Estimated Delivery Time: {int(time)} minutes")

