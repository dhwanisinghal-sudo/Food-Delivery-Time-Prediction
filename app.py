import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Food Delivery Time Prediction", layout="wide")
st.title("🍔 Food Delivery Time Prediction (Pro Version)")

st.write("""
Predict estimated food delivery time based on distance, traffic, weather, vehicle type, urgency, festival, time of day, and more.  
Random scenario simulation and visual analytics included!
""")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Delivery Inputs")

# Manual restaurant input
restaurants_input = st.sidebar.text_input(
    "Enter Restaurant Name (single)", "Pizza Palace"
)
restaurant = restaurants_input.strip()  # single restaurant

# Distance input (float)
distance = st.sidebar.number_input(
    "Distance (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.01, format="%.2f"
)

# Traffic & Weather
traffic = st.sidebar.selectbox("Traffic Condition", ["Low", "Medium", "High"])
weather = st.sidebar.selectbox("Weather Condition", ["Clear", "Cloudy", "Rainy", "Stormy"])

# Vehicle & Urgency
vehicle = st.sidebar.selectbox("Vehicle Type", ["Bike", "EV", "Drone"])
urgency = st.sidebar.selectbox("Delivery Urgency", ["Normal", "Express", "Priority"])

# Festival / Rush hour
festival = st.sidebar.checkbox("Festival / Rush Hour")

# Time of Day
time_of_day = st.sidebar.selectbox("Time of Day", ["Morning", "Lunch", "Evening", "Night"])

# Extreme Mode
extreme = st.sidebar.checkbox("Extreme Mode (optional)")

# ---------------- Prep time ----------------
default_prep_time = 10
prep_time_dict = {"Pizza Palace": 10, "Burger Hub": 8, "Sushi World": 12, "Dessert Cafe": 6}
prep_time = prep_time_dict.get(restaurant, default_prep_time)

# ---------------- Base time ----------------
base_time = prep_time + distance * 3

# Traffic effect
traffic_effect = {"Low":0, "Medium":distance*0.05, "High":distance*0.1}[traffic]

# Weather effect
weather_effect = {"Clear":0, "Cloudy":distance*0.02, "Rainy":distance*0.05, "Stormy":distance*0.15}[weather]

# Vehicle effect
vehicle_effect = {"Bike":0, "EV":-distance*0.03, "Drone":-distance*0.06}[vehicle]

# Festival effect
festival_effect = 20 if festival else 0

# Time of Day effect
time_effect = {"Morning":0, "Lunch":10, "Evening":15, "Night":5}[time_of_day]

# Urgency multiplier
urgency_multiplier = {"Normal":1, "Express":0.85, "Priority":0.7}[urgency]

# Extreme mode
extreme_effect = distance*0.2 + np.random.randint(0,30) if extreme else 0

# ---------------- Predicted Time ----------------
predicted_time = (base_time + traffic_effect + weather_effect + vehicle_effect +
                  festival_effect + time_effect + extreme_effect) * urgency_multiplier

# Cap at 2000 minutes
predicted_time = min(predicted_time, 2000)

# ---------------- Display Predicted Time ----------------
st.subheader(f"Estimated Delivery Time for {restaurant}")
if predicted_time <= 30:
    color = 'green'
elif predicted_time <= 120:
    color = 'orange'
else:
    color = 'red'
st.markdown(f"<span style='color:{color}; font-size:24px'>{predicted_time:.2f} minutes</span>", unsafe_allow_html=True)

# ---------------- Factor Contribution ----------------
st.subheader("Factor Contribution (Minutes)")
factor_df = pd.DataFrame({
    'Factor': ['Base Time', 'Traffic', 'Weather', 'Vehicle', 'Festival', 'Time of Day', 'Extreme Mode'],
    'Minutes': [base_time, traffic_effect, weather_effect, vehicle_effect, festival_effect, time_effect, extreme_effect]
})
st.bar_chart(factor_df.set_index('Factor'))

# ---------------- Random Scenario Simulation ----------------
st.subheader("Random Scenario Analysis")
num_scenarios = st.slider("Number of Random Scenarios", 1, 20, 5)

if st.button("Generate Random Scenarios"):
    results = []
    for _ in range(num_scenarios):
        rand_distance = round(np.random.uniform(0.1, 100.0),2)
        rand_traffic = np.random.choice(["Low","Medium","High"])
        rand_weather = np.random.choice(["Clear","Cloudy","Rainy","Stormy"])
        rand_vehicle = np.random.choice(["Bike","EV","Drone"])
        rand_festival = np.random.choice([True,False])
        rand_time = np.random.choice(["Morning","Lunch","Evening","Night"])

        rand_base = prep_time_dict.get(restaurant, default_prep_time) + rand_distance*3
        rand_total = (rand_base +
                      {"Low":0, "Medium":rand_distance*0.05, "High":rand_distance*0.1}[rand_traffic] +
                      {"Clear":0, "Cloudy":rand_distance*0.02, "Rainy":rand_distance*0.05, "Stormy":rand_distance*0.15}[rand_weather] +
                      {"Bike":0, "EV":-rand_distance*0.03, "Drone":-rand_distance*0.06}[rand_vehicle] +
                      (20 if rand_festival else 0) +
                      {"Morning":0,"Lunch":10,"Evening":15,"Night":5}[rand_time] +
                      (rand_distance*0.2 + np.random.randint(0,30) if extreme else 0)
                     ) * urgency_multiplier
        rand_total = min(rand_total,2000)
        results.append([rand_distance, rand_traffic, rand_weather, rand_vehicle, rand_festival, rand_time, round(rand_total,2)])

    scenario_df = pd.DataFrame(results, columns=['Distance (km)','Traffic','Weather','Vehicle','Festival','Time of Day','Predicted Time (min)'])
    st.dataframe(scenario_df)

    st.write("**Summary:**")
    st.write(f"Minimum Time: {scenario_df['Predicted Time (min)'].min():.2f} min")
    st.write(f"Maximum Time: {scenario_df['Predicted Time (min)'].max():.2f} min")
    st.write(f"Average Time: {scenario_df['Predicted Time (min)'].mean():.2f} min")

# ---------------- Line Chart: Delivery Time vs Distance ----------------
st.subheader(f"Delivery Time vs Distance Simulation for {restaurant}")
distance_sim = np.linspace(0.5,50,50)
sim_times = []
for d in distance_sim:
    sim_time = (prep_time + d*3 +
                traffic_effect + weather_effect + vehicle_effect +
                festival_effect + time_effect + extreme_effect) * urgency_multiplier
    sim_times.append(sim_time)
line_df = pd.DataFrame({'Distance (km)': distance_sim, 'Predicted Time (min)': sim_times})
st.line_chart(line_df.set_index('Distance (km)'))
