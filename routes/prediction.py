import streamlit as st
import pandas as pd
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")
GEMINI_MODEL=os.getenv("GEMINI_MODEL")

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)

# 🔮 AI call function
def call_gemini(prompt: str):
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(prompt)
    return response.text.strip()

def show(data: pd.DataFrame):
    st.title("Know Your Salary (AI Estimation)")

    st.markdown("""
    Use AI to estimate your expected salary.  
    Fill in details like your job title, industry, education, and years of experience.  
    Get an approximate prediction even if no exact dataset match is found.
    """)

    st.markdown("""<br/>""", unsafe_allow_html=True)

    # 👉 Extract dropdowns
    job_titles = sorted(set(data["Job Title"].dropna()))
    industries = sorted(set(data["Industry"].dropna()))
    education_levels = sorted(set(data["Education Level"].dropna()))
    locations = sorted(set(data["Location"].dropna()))
    employment_types = sorted(set(data["Employment Type"].dropna()))
    company_sizes = sorted(set(data["Company Size"].dropna()))
    remote_options = sorted(set(data["Remote"].dropna()))

    with st.form(key="prediction_form"):
        # Row 1
        col1, col2, col3 = st.columns(3)
        with col1:
            job_title = st.selectbox("Job Title", job_titles)
        with col2:
            employment_type = st.selectbox("Employment Type", employment_types)
        with col3:
            industry = st.selectbox("Industry", industries)

        # Row 2
        col4, col5, col6 = st.columns(3)
        with col4:
            company_size = st.selectbox("Company Size", company_sizes)
        with col5:
            max_exp = round(data["YearsExperience"].astype(float).max(), 1)
            years_exp = st.number_input(
                "Years of Experience",
                min_value=0.0,
                max_value=max_exp,
                value=min(max_exp, 1.0),
                step=0.5
            )
        with col6:
            remote = st.selectbox("Remote", remote_options)

        _, col7, col8, _ = st.columns([1, 1, 1, 1])
        with col7:
            location = st.selectbox("Location", locations)
        with col8:
            education_level = st.selectbox("Education Level", education_levels)

        col_reset, _, col_predict = st.columns([1, 5, 1])
        with col_reset:
            reset = st.form_submit_button("Reset")
        with col_predict:
            predict = st.form_submit_button("Predict")

    if reset:
        st.session_state.clear()
        st.rerun()

    if predict:
        # ✅ Dynamic progress bar
        progress_bar = st.progress(0.0)
        prediction_done = False

        # 📝 Build prompt
        prompt = f"""
        You are an expert salary estimator.
        Estimate a fair salary in INR for the following:
        - Job Title: {job_title}
        - Industry: {industry}
        - Employment Type: {employment_type}
        - Company Size: {company_size}
        - Years of Experience: {years_exp}
        - Remote: {remote}
        - Location: {location}
        - Education Level: {education_level}

        ONLY return the estimated annual salary range in INR, 
        like "₹6,00,000 - ₹8,50,000 per annum" and nothing else.
        Do not add explanations, factors, or any extra text.
        """


        # 🪄 Start AI call in background
        import threading

        ai_result = {"response": None}

        def get_ai_response():
            ai_result["response"] = call_gemini(prompt)

        t = threading.Thread(target=get_ai_response)
        t.start()

        # 👉 Slider simulation
        steps = [0.0, 0.25, 0.50, 0.75, 0.99, 1.0]
        delays = [0.5, 1.5, 2.0, 3.0]  # seconds between ranges

        for i in range(1, len(steps)):
            progress_bar.progress(steps[i - 1])
            step_start = time.time()
            while time.time() - step_start < delays[i - 1]:
                if ai_result["response"]:
                    break
                time.sleep(0.1)
            if ai_result["response"]:
                break

        # If AI not done yet, wait until finished
        while ai_result["response"] is None:
            time.sleep(0.2)

        # Finish progress bar
        progress_bar.progress(1.0)

        # ✅ Save in session
        st.session_state["ai_salary_estimate"] = ai_result["response"]
        st.session_state["prediction_done"] = True

    # 👉 Show result
    if st.session_state.get("prediction_done", False):
        response = st.session_state.get("ai_salary_estimate", "").strip()
        st.success(f"💰 **AI Estimated Salary:**\n\n{response}")
        st.caption("_This is an AI generated estimate for informational purposes only._")
