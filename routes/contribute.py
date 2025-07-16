import streamlit as st
import pandas as pd
import os

CSV_FILE = "Employee_Salary_Data.csv"

def show(data: pd.DataFrame):
    st.title("Contribute Data")

    st.markdown("""
    Use this form to contribute your real salary data.
    This helps improve future salary predictions!
    """)

    st.sidebar.markdown("<hr/>",unsafe_allow_html=True)
    mode = st.sidebar.radio(
        "Change Inputs",
        ("Existing Values", "Custom Values")
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    # Dropdown options
    job_titles = sorted(set(data["Job Title"].dropna()))
    industries = sorted(set(data["Industry"].dropna()))
    education_levels = sorted(set(data["Education Level"].dropna()))
    locations = sorted(set(data["Location"].dropna()))
    employment_types = sorted(set(data["Employment Type"].dropna()))
    company_sizes = sorted(set(data["Company Size"].dropna()))
    remote_options = sorted(set(data["Remote"].dropna()))

    with st.form(key="contribute_form"):
        # Row 1: Job Title, Industry, Education
        col1, col2, col3 = st.columns(3)
        with col1:
            if mode == "Existing Values":
                job_title = st.selectbox("Job Title", job_titles)
            else:
                job_title = st.text_input("Job Title")

        with col2:
            if mode == "Existing Values":
                industry = st.selectbox("Industry", industries)
            else:
                industry = st.text_input("Industry")

        with col3:
            education_level = st.selectbox("Education Level", education_levels)

        # Row 2: Location, Employment Type, Company Size
        col4, col5, col6 = st.columns(3)
        with col4:
            if mode == "Existing Values":
                location = st.selectbox("Location", locations)
            else:
                location = st.text_input("Location")

        with col5:
            employment_type = st.selectbox("Employment Type", employment_types)

        with col6:
            company_size = st.selectbox("Company Size", company_sizes)

        # Row 3: Remote, YearsExperience, Salary
        col7, col8, col9 = st.columns(3)
        with col7:
            remote = st.selectbox("Remote", remote_options)

        with col8:
            years_exp = st.number_input(
                "Years of Experience",
                min_value=0.0,
                max_value=50.0,
                value=1.0,
                step=0.5
            )

        with col9:
            salary_inr = st.number_input(
                "Salary (INR per annum)",
                min_value=0.0,
                max_value=10_00_00_000.0,
                value=5_00_000.0,
                step=1_000.0
            )

        col_reset, _, col_submit = st.columns([1, 5, 1])
        with col_reset:
            reset = st.form_submit_button("Reset")
        with col_submit:
            submit = st.form_submit_button("Add Data")

    if reset:
        st.session_state.clear()
        st.rerun()

    if submit:
        new_row = {
            "Job Title": job_title.strip(),
            "Industry": industry.strip(),
            "Education Level": education_level.strip(),
            "Location": location.strip(),
            "Employment Type": employment_type.strip(),
            "Company Size": company_size.strip(),
            "Remote": remote.strip(),
            "YearsExperience": years_exp,
            "Salary (in INR)": salary_inr
        }

        try:
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([new_row])

        df.to_csv(CSV_FILE, index=False)
        st.success("Your data has been added. Thank you for contributing!")