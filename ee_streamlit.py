import streamlit as st
import numpy as np

# Constants
gas_c = 8.314462
j2kcal = 0.000239006
kelvin = 273.15

def ee2ddg(ee, temp):
    global gas_c, j2kcal, kelvin
    if ee < 0:
        raise NotImplementedError("Negative EE")
    else:
        r_ee = (ee + 100) / (100 - ee)
        k_tp = temp + kelvin
        ddg = gas_c * k_tp * np.log(r_ee) * j2kcal
        return ddg

def ddg2ee(ddg, temp):
    global gas_c, j2kcal, kelvin
    k_tp = temp + kelvin
    r_ee = np.exp(ddg / (gas_c * k_tp * j2kcal))
    ee = (100 * (r_ee - 1)) / (r_ee + 1)
    return ee

def er2ddg(er, temp):
    global gas_c, j2kcal, kelvin
    k_tp = temp + kelvin
    ddg = gas_c * k_tp * np.log(er) * j2kcal
    return ddg

def ee2er(ee):
    r_ee = (ee + 100) / (100 - ee)
    return r_ee

def er2ee(er):
    ee = (100 * (er - 1)) / (er + 1)
    return ee

def recover_temp(ee, ddg):
    global gas_c, j2kcal, kelvin
    r_ee = (ee + 100) / (100 - ee)
    return  (kelvin - ddg / ((gas_c * j2kcal) * np.log(r_ee))) * -1

# Streamlit app
st.title("Enantiomeric Calculations")
st.text("Also works for Diastereomeric calculations")

option = st.selectbox("Select an option", ["EE to ΔΔG", "ΔΔG to EE", "ER to ΔΔG", "EE to ER", "ER to EE", "Recover Temperature"])

if option == "EE to ΔΔG":
    ee = st.number_input("Enter Enantiomeric Excess (EE) in %", value=0.0)
    temp = st.number_input("Enter Temperature in Celsius", value=25.0)
    if st.button("Calculate ΔΔG"):
        result = ee2ddg(ee, temp)
        st.write(f"ΔΔG: {result} kcal/mol")

elif option == "ΔΔG to EE":
    ddg = st.number_input("Enter Free Energy Difference (ΔΔG) in kcal/mol", value=0.0)
    temp = st.number_input("Enter Temperature in Celsius", value=25.0)
    if st.button("Calculate EE"):
        result = ddg2ee(ddg, temp)
        st.write(f"EE: {result} %")

elif option == "ER to ΔΔG":
    er = st.number_input("Enter Enantiomeric Ratio (ER)", value=1.0)
    temp = st.number_input("Enter Temperature in Celsius", value=25.0)
    if st.button("Calculate ΔΔG"):
        result = er2ddg(er, temp)
        st.write(f"ΔΔG: {result} kcal/mol")

elif option == "EE to ER":
    ee = st.number_input("Enter Enantiomeric Excess (EE) in %", value=0.0)
    if st.button("Calculate ER"):
        result = ee2er(ee)
        st.write(f"ER: {result}")

elif option == "ER to EE":
    er = st.number_input("Enter Enantiomeric Ratio (ER)", value=1.0)
    if st.button("Calculate EE"):
        result = er2ee(er)
        st.write(f"EE: {result} %")

elif option == "Recover Temperature":
    ee = st.number_input("Enter Enantiomeric Excess (EE) in %", value=0.0)
    ddg = st.number_input("Enter Free Energy Difference (ΔΔG) in kcal/mol", value=0.0)
    if st.button("Recover Temperature"):
        result = recover_temp(ee, ddg)
        st.write(f"Temperature: {result} Celsius")