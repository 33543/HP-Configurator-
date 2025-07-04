
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

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

gas_emission_option = st.selectbox(
    "Select Gas Emission Factor Source",
    (
        "Default - 0.183",
        "Custom value"
    )
)

if gas_emission_option == "Default - 0.183":
    gas_emission_factor = 0.183
else:
    gas_emission_factor = st.number_input("Enter Custom Gas Emission Factor (kg CO2e/kWh)", key="custom_gas_emission", value=0.183)


emission_option = st.selectbox(
    "Select Electricity Emission Factor Source",
    (
        "Full system (generation + T&D) - 0.225",
        "Generation only - 0.124",
        "Custom value"
    )
)

if emission_option == "Full system (generation + T&D) - 0.225":
    electricity_emission_factor = 0.225
elif emission_option == "Generation only - 0.124":
    electricity_emission_factor = 0.124
else:
    electricity_emission_factor = st.number_input("Enter Custom Electricity Emission Factor (kg CO2e/kWh)", key="custom_elec_emission", value=0.220)

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

st.subheader("Generate and Download Report")

if st.button("Generate PDF Report"):
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='PNG')
    img_buffer.seek(0)
    chart_image = ImageReader(img_buffer)

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4    logo_path = "logo.jpg"

    if os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, 40, height - 100, width=150, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            st.warning("Logo found but could not be loaded into PDF.")
    else:
        st.warning("Logo not found for PDF.")

    y = height - 140 
   

    

    # Write wrapped lines
    text_lines = [
        "Renewable Energy Analysis",
        "",
        "System Sizing",
        f"- Estimated Peak Gas Input Required: {peak_gas_input_kw:.2f} kW",
        f"- Required Heat Pump Size: {required_heat_pump_kw:.2f} kW",
        f"- Annual Electricity Needed: {electricity_needed:.0f} kWh",
        "",
        "Cost Comparison",
        f"- Annual Heating Cost (Gas): £{cost_gas:.2f}",
        f"- Annual Heating Cost (Heat Pump): £{cost_electric:.2f}",
        f"- Annual Savings: £{savings:.2f}",
        f"- CAPEX: £{capex:.2f}",
        "",
        "Carbon Savings",
        f"- Annual Emissions (Gas): {carbon_gas:.1f} kg CO₂e",
        f"- Annual Emissions (Heat Pump): {carbon_hp:.1f} kg CO₂e",
        f"- Carbon Saved per Year: {carbon_savings:.1f} kg CO₂e",
        "",
        "Payback Period",
        f"- {'Estimated Payback Period: {:.1f} years'.format(payback_years) if savings > 0 else 'No payback possible with current settings'}"
    ]

    y = height - 120
    for line in text_lines:
        if y < 100:
            c.showPage()
            y = height - 50
        c.drawString(40, y, line)
        y -= 20

    # Add chart on a new page
    c.showPage()
    c.drawImage(chart_image, 40, height / 2 - 150, width=500, preserveAspectRatio=True, mask='auto')

    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    st.download_button("Download PDF Report", data=pdf_buffer, file_name="renewable_energy_report.pdf", mime="application/pdf")
