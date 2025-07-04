
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Display the logo
st.image("logo.jpg", width=300)

st.title("Renewable Energy Analysis")

# User Inputs
heating_demand = st.number_input("Annual Heating Demand (kWh)", value=12000)
building_size = st.number_input("Building Size (m²)", value=150)
cop = st.slider("Heat Pump Efficiency (COP)", 2.0, 5.0, 3.0, step=0.1)
boiler_efficiency = st.slider("Boiler Efficiency (%)", 60, 100, 85, step=1)
gas_price = st.number_input("Gas Price (pence/kWh)", value=8.0)
elec_price = st.number_input("Electricity Price (pence/kWh)", value=24.0)
capex = st.number_input("Capital Cost of Heat Pump System (£)", value=12000)

# Emission Factors (kg CO₂e per kWh)
gas_emission_factor = 0.183
electricity_emission_factor = 0.074

# Adjust heating demand for boiler inefficiency
adjusted_gas_demand = heating_demand / (boiler_efficiency / 100)

# Sizing logic based on peak demand
full_load_hours = 1500
peak_gas_input_kw = adjusted_gas_demand / full_load_hours
required_heat_pump_kw = heating_demand / full_load_hours
electricity_needed = heating_demand / cop

# Cost and emissions calculations
cost_gas = adjusted_gas_demand * gas_price / 100
cost_electric = electricity_needed * elec_price / 100
savings = cost_gas - cost_electric

carbon_gas = adjusted_gas_demand * gas_emission_factor
carbon_hp = electricity_needed * electricity_emission_factor
carbon_savings = carbon_gas - carbon_hp

# Outputs
st.subheader("System Sizing")
st.write(f"Estimated Peak Gas Input Required: {peak_gas_input_kw:.2f} kW")
st.write(f"Required Heat Pump Size: {required_heat_pump_kw:.2f} kW")
st.write(f"Annual Electricity Needed: {electricity_needed:.0f} kWh")

st.subheader("Cost Comparison")
st.write(f"Annual Heating Cost (Gas): £{cost_gas:.2f}")
st.write(f"Annual Heating Cost (Heat Pump): £{cost_electric:.2f}")
st.write(f"Annual Savings: £{savings:.2f}")
st.write(f"CAPEX: £{capex:.2f}")

st.subheader("Carbon Savings")
st.write(f"Annual Emissions (Gas): {carbon_gas:.1f} kg CO₂e")
st.write(f"Annual Emissions (Heat Pump): {carbon_hp:.1f} kg CO₂e")
st.write(f"Carbon Saved per Year: {carbon_savings:.1f} kg CO₂e")

st.subheader("Payback Period")
if savings > 0:
    payback_years = capex / savings
    st.write(f"Estimated Payback Period: {payback_years:.1f} years")
else:
    st.write("No payback possible with current settings (savings are zero or negative).")

# Chart
fig, ax = plt.subplots()
labels = ['Gas Heating', 'Heat Pump']
costs = [cost_gas, cost_electric]
ax.bar(labels, costs, color=["grey", "green"])
ax.set_ylabel('Annual Cost (£)')
ax.set_title('Heating Cost Comparison')
st.pyplot(fig)
