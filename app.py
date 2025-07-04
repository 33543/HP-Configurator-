
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Energy Dashboard: Solar & Heat Pump Sizing")

st.subheader("Heat Pump Sizing and Savings Calculator")

# User Inputs
heating_demand = st.number_input("Annual Heating Demand (kWh)", value=12000)
building_size = st.number_input("Building Size (m²)", value=150)
cop = st.slider("Heat Pump Efficiency (COP)", 2.0, 5.0, 3.0, step=0.1)
gas_price = st.number_input("Gas Price (pence/kWh)", value=8.0)
elec_price = st.number_input("Electricity Price (pence/kWh)", value=24.0)

# Calculations
heat_pump_size_kw = heating_demand / 1500  # Rough rule of thumb: 1500 full load hours/year
electricity_needed = heating_demand / cop
cost_gas = heating_demand * gas_price / 100
cost_electric = electricity_needed * elec_price / 100
savings = cost_gas - cost_electric

# Outputs
st.write(f"**Required Heat Pump Size:** {heat_pump_size_kw:.2f} kW")
st.write(f"**Annual Electricity Needed:** {electricity_needed:.0f} kWh")
st.write(f"**Annual Heating Cost (Gas):** £{cost_gas:.2f}")
st.write(f"**Annual Heating Cost (Heat Pump):** £{cost_electric:.2f}")
st.write(f"**Estimated Annual Savings:** £{savings:.2f}")

# Plot comparison
fig, ax = plt.subplots()
labels = ['Gas Heating', 'Heat Pump']
costs = [cost_gas, cost_electric]
ax.bar(labels, costs)
ax.set_ylabel('Annual Cost (£)')
ax.set_title('Heating Cost Comparison')
st.pyplot(fig)
