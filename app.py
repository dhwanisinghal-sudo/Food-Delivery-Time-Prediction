import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Ultimate Food Delivery Simulator", layout="wide")

st.title("🚀 Ultimate Food Delivery Simulator")
st.write("Simulate delivery times under realistic and extreme conditions. Adjust sliders, dropdowns, and checkboxes to see the effects!")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Delivery Inputs")

distance = st.sidebar.slider("Distance (km)", 0, 1000, 50, step=10, help="Distance from restaurant to customer")
traffic = st.sidebar.selectbox("Traffic Condition", ["Low", "Medium", "High"], help="Current traffic level")
weather = st.sidebar.selectbox("Weather Condition", ["Clear", "Cloudy", "Rainy", "Stormy"], help="Current weather")
vehicle = st.sidebar.selectbox("Vehicle Type", ["Bike", "Car", "Truck", "Drone"], help="Type of delivery vehicle")
festival = st.sidebar.checkbox("Festival / Rush Hour", help="Increase delivery time during busy periods")
urgency = st.sidebar.selectbox("Delivery Urgency", ["Normal", "Express", "Priority"], help="Speed requirements for delivery")
extreme = st.sidebar.checkbox("Extreme Mode", help="Enable unrealistic extreme scenario simulation")

# ---------------- Base Calculation ----------------
base_time = 20 + (distance * 2)

# Traffic modifier
traffic_dict = {"Low": 0, "Medium": distance * 0.05, "High": distance * 0.1}
traffic_effect = traffic_dict[traffic]

# Weather modifier
weather_dict = {"Clear": 0, "Cloudy": distance * 0.02, "Rainy": distance * 0.05, "Stormy": distance * 0.15}
weather_effect = weather_dict[weather]

# Vehicle modifier
vehicle_dict = {"Bike": 0, "Car": -distance*0.02, "Truck": distance*0.05, "Drone": -distance*0.05}
vehicle_effect = vehicle_dict[vehicle]

# Festival modifier
festival_effect = 30 if festival else 0

# Urgency modifier
urgency_multiplier = {"Normal":1, "Express":0.85, "Priority":0.7}
urgency_effect = urgency_multiplier[urgency]

# Extreme mode modifier
extreme_effect = 0
if extreme:
    extreme_effect = distance * 0.2 + np.random.randint(0,50)

# Total time
total_time = (base_time + traffic_effect + weather_effect + vehicle_effect + festival_effect + extreme_effect) * urgency_effect

# Max cap 2000 minutes
if total_time > 2000:
    total_time = 2000

# ---------------- Color-coded output ----------------
if total_time <= 60:
    color = 'green'
elif total_time <= 300:
    color = 'orange'
else:
    color = 'red'

st.markdown(f"### ⏱ Estimated Delivery Time: <span style='color:{color}'>{int(total_time)} minutes</span>", unsafe_allow_html=True)

# ---------------- Bar Chart of Factors ----------------
effect_df = pd.DataFrame({
    'Factor': ['Base Time', 'Traffic', 'Weather', 'Vehicle', 'Festival', 'Extreme Mode'],
    'Minutes': [base_time, traffic_effect, weather_effect, vehicle_effect, festival_effect, extreme_effect]
})

st.subheader("Factor Contribution")
st.bar_chart(effect_df.set_index('Factor'))

# ---------------- Line Chart Simulation ----------------
st.subheader("Delivery Time vs Distance Simulation")
sim_distance = np.arange(0, 1001, 10)
sim_times = (20 + sim_distance*2 + 
             np.array([traffic_dict[traffic]]*len(sim_distance)) +
             np.array([weather_dict[weather]]*len(sim_distance)) +
             np.array([vehicle_dict[vehicle]]*len(sim_distance)) +
             np.array([festival_effect]*len(sim_distance)) +
             np.array([extreme_effect]*len(sim_distance))) * urgency_effect

sim_df = pd.DataFrame({"Distance (km)": sim_distance, "Predicted Time (min)": sim_times})
st.line_chart(sim_df.set_index("Distance (km)"))

# ---------------- Random Scenario Generator ----------------
st.subheader("Random Scenario Example")
if st.button("Generate Random Scenario"):
    rand_distance = np.random.randint(1,1000)
    rand_traffic = np.random.choice(["Low","Medium","High"])
    rand_weather = np.random.choice(["Clear","Cloudy","Rainy","Stormy"])
    rand_vehicle = np.random.choice(["Bike","Car","Truck","Drone"])
    rand_festival = np.random.choice([True,False])
    
    rand_base = 20 + rand_distance*2
    rand_total = (rand_base + traffic_dict[rand_traffic] + weather_dict[rand_weather] +
                  vehicle_dict[rand_vehicle] + (30 if rand_festival else 0))*urgency_effect
    if rand_total>2000: rand_total=2000
    st.write(f"Distance: {rand_distance} km, Traffic: {rand_traffic}, Weather: {rand_weather}, Vehicle: {rand_vehicle}, Festival: {rand_festival}")
    st.success(f"Predicted Delivery Time: {int(rand_total)} minutes")
