import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Food Delivery Time Prediction", layout="wide")
st.title("🍔 Food Delivery Time Prediction")
st.write("Predict estimated food delivery time based on distance, traffic, weather, vehicle type, urgency, and more.")

# ---------------- Sidebar Inputs ----------------
st.sidebar.header("Delivery Inputs")

# Distance input (float)
distance = st.sidebar.number_input(
    "Distance (km)", min_value=0.1, max_value=100.0, value=5.0, step=0.01, format="%.2f"
)

# Restaurant selection (optional, affects prep time)
restaurant = st.sidebar.selectbox(
    "Restaurant", ["Pizza Palace", "Burger Hub", "Sushi World", "Dessert Cafe"]
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

# Extreme Mode (optional demo)
extreme = st.sidebar.checkbox("Extreme Mode (optional)")

# ---------------- Base Time Calculation ----------------
# Base prep time per restaurant
prep_time_dict = {"Pizza Palace": 10, "Burger Hub": 8, "Sushi World": 12, "Dessert Cafe": 6}
base_time = prep_time_dict[restaurant] + (distance * 3)  # prep + distance

# Traffic effect
traffic_dict = {"Low": 0, "Medium": distance * 0.05, "High": distance * 0.1}
traffic_effect = traffic_dict[traffic]

# Weather effect
weather_dict = {"Clear": 0, "Cloudy": distance * 0.02, "Rainy": distance * 0.05, "Stormy": distance * 0.15}
weather_effect = weather_dict[weather]

# Vehicle effect
vehicle_dict = {"Bike": 0, "EV": -distance * 0.03, "Drone": -distance * 0.06}
vehicle_effect = vehicle_dict[vehicle]

# Festival / Rush hour
festival_effect = 20 if festival else 0

# Time of Day effect
time_dict = {"Morning": 0, "Lunch": 10, "Evening": 15, "Night": 5}
time_effect = time_dict[time_of_day]

# Urgency multiplier
urgency_multiplier = {"Normal":1, "Express":0.85, "Priority":0.7}

# Extreme mode effect
extreme_effect = distance*0.2 + np.random.randint(0,30) if extreme else 0

# Total predicted time
total_time = (base_time + traffic_effect + weather_effect + vehicle_effect +
              festival_effect + time_effect + extreme_effect) * urgency_multiplier[urgency]

# Cap maximum time to 2000 minutes (~33 hours)
if total_time > 2000:
    total_time = 2000

# ---------------- Color-coded Output ----------------
if total_time <= 30:
    color = 'green'
elif total_time <= 120:
    color = 'orange'
else:
    color = 'red'

st.markdown(
    f"### ⏱ Estimated Delivery Time from {restaurant}: "
    f"<span style='color:{color}'>{total_time:.2f} minutes</span>",
    unsafe_allow_html=True
)

# ---------------- Factor Contribution Bar Chart ----------------
effect_df = pd.DataFrame({
    'Factor': ['Base Time', 'Traffic', 'Weather', 'Vehicle', 'Festival', 'Time of Day', 'Extreme Mode'],
    'Minutes': [base_time, traffic_effect, weather_effect, vehicle_effect, festival_effect, time_effect, extreme_effect]
})
st.subheader("Factor Contribution to Delivery Time")
st.bar_chart(effect_df.set_index('Factor'))

# ---------------- Delivery Time vs Distance Line Chart ----------------
st.subheader("Delivery Time vs Distance Simulation")
sim_distance = np.arange(0.1, 100.1, 0.5)
sim_times = (prep_time_dict[restaurant] + sim_distance*3 +
             np.array([traffic_dict[traffic]]*len(sim_distance)) +
             np.array([weather_dict[weather]]*len(sim_distance)) +
             np.array([vehicle_dict[vehicle]]*len(sim_distance)) +
             np.array([festival_effect]*len(sim_distance)) +
             np.array([time_effect]*len(sim_distance)) +
             np.array([extreme_effect]*len(sim_distance))
            ) * urgency_multiplier[urgency]

sim_df = pd.DataFrame({"Distance (km)": sim_distance, "Predicted Time (min)": sim_times})
st.line_chart(sim_df.set_index("Distance (km)"))

# ---------------- Random Scenario Generator ----------------
st.subheader("Random Scenario Analysis")
num_scenarios = st.slider("Number of Random Scenarios", 1, 20, 5)

if st.button("Generate Random Scenarios"):
    results = []
    for _ in range(num_scenarios):
        rand_distance = round(np.random.uniform(0.1, 100.0), 2)
        rand_restaurant = np.random.choice(list(prep_time_dict.keys()))
        rand_traffic = np.random.choice(["Low","Medium","High"])
        rand_weather = np.random.choice(["Clear","Cloudy","Rainy","Stormy"])
        rand_vehicle = np.random.choice(["Bike","EV","Drone"])
        rand_festival = np.random.choice([True,False])
        rand_time = np.random.choice(["Morning","Lunch","Evening","Night"])

        rand_base = prep_time_dict[rand_restaurant] + rand_distance*3
        rand_total = (rand_base +
                      traffic_dict[rand_traffic] +
                      weather_dict[rand_weather] +
                      vehicle_dict[rand_vehicle] +
                      (20 if rand_festival else 0) +
                      time_dict[rand_time] +
                      (rand_distance*0.2 + np.random.randint(0,30) if extreme else 0)
                     ) * urgency_multiplier[urgency]
        if rand_total > 2000: rand_total = 2000

        results.append([rand_restaurant, rand_distance, rand_traffic, rand_weather, rand_vehicle,
                        rand_festival, rand_time, round(rand_total,2)])

    result_df = pd.DataFrame(results, columns=['Restaurant','Distance (km)','Traffic','Weather','Vehicle',
                                               'Festival','Time of Day','Predicted Time (min)'])
    st.dataframe(result_df)

    st.write("**Summary:**")
    st.write(f"Minimum Time: {result_df['Predicted Time (min)'].min():.2f} min")
    st.write(f"Maximum Time: {result_df['Predicted Time (min)'].max():.2f} min")
    st.write(f"Average Time: {result_df['Predicted Time (min)'].mean():.2f} min")
