
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Heat Pump Sizing, Cost & Carbon Savings Calculator")

# User Inputs
heating_demand = st.number_input("Annual Heating Demand (kWh)", value=12000)
building_size = st.number_input("Building Size (m²)", value=150)
cop = st.slider("Heat Pump Efficiency (COP)", 2.0, 5.0, 3.0, step=0.1)
gas_price = st.number_input("Gas Price (pence/kWh)", value=8.0)
elec_price = st.number_input("Electricity Price (pence/kWh)", value=24.0)
capex = st.number_input("Capital Cost of Heat Pump System (£)", value=12000)

# Emission Factors (kg CO₂e per kWh)
gas_emission_factor = 0.183
electricity_emission_factor = 0.074  # based on UK's grid average

# Calculations
heat_pump_size_kw = heating_demand / 1500  # Rough estimate
electricity_needed = heating_demand / cop

cost_gas = heating_demand * gas_price / 100
cost_electric = electricity_needed * elec_price / 100
savings = cost_gas - cost_electric

carbon_gas = heating_demand * gas_emission_factor
carbon_hp = electricity_needed * electricity_emission_factor
carbon_savings = carbon_gas - carbon_hp

# Outputs
st.markdown(f"### 🔧 Heat Pump Sizing")
st.write(f"**Required Heat Pump Size:** {heat_pump_size_kw:.2f} kW")
st.write(f"**Annual Electricity Needed:** {electricity_needed:.0f} kWh")

st.markdown(f"### 💷 Cost Comparison")
st.write(f"**Annual Heating Cost (Gas):** £{cost_gas:.2f}")
st.write(f"**Annual Heating Cost (Heat Pump):** £{cost_electric:.2f}")
st.write(f"**Annual Savings:** £{savings:.2f}")
st.write(f"**CAPEX:** £{capex:.2f}")

st.markdown(f"### 🌍 Carbon Savings")
st.write(f"**Annual Emissions (Gas):** {carbon_gas:.1f} kg CO₂e")
st.write(f"**Annual Emissions (Heat Pump):** {carbon_hp:.1f} kg CO₂e")
st.write(f"**Carbon Saved per Year:** {carbon_savings:.1f} kg CO₂e")

# Chart
fig, ax = plt.subplots()
labels = ['Gas Heating', 'Heat Pump']
costs = [cost_gas, cost_electric]
ax.bar(labels, costs, color=["grey", "green"])
ax.set_ylabel('Annual Cost (£)')
ax.set_title('Heating Cost Comparison')
st.pyplot(fig)
