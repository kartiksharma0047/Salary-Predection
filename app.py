import streamlit as st
import pandas as pd

# Load your data ONCE — reusable
data = pd.read_csv("./Employee_Salary_Data.csv")
data["YearsExperience"] = data["YearsExperience"].round(1)
data["Salary (in INR)"] = data["Salary (in INR)"].round(1)
data["YearsExperience_Display"] = data["YearsExperience"].map(
    lambda x: f"{x:.1f}".rstrip('0').rstrip('.') if '.' in str(x) else str(x)
)
data["Salary (in INR)"] = data["Salary (in INR)"].apply(
    lambda x: str(x).rstrip('0').rstrip('.') if '.' in str(x) else x
)

# Navigation
nav = st.sidebar.radio("Navigation", ["Home", "Prediction", "Contribute"])

# Import pages
from routes import home, prediction, contribute

if nav == "Home":
    home.show(data)
elif nav == "Prediction":
    prediction.show(data)
elif nav == "Contribute":
    contribute.show(data)
