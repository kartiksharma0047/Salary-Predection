import streamlit as st
import pandas as pd

# --- Load CSV ---
data = pd.read_csv("./Employee_Salary_Data.csv")

# --- Format decimals ---
data["YearsExperience"] = data["YearsExperience"].round(1)
data["Salary (in INR)"] = data["Salary (in INR)"].round(1)

data["YearsExperience"] = data["YearsExperience"].apply(
    lambda x: str(x).rstrip('0').rstrip('.') if '.' in str(x) else x
)
data["Salary (in INR)"] = data["Salary (in INR)"].apply(
    lambda x: str(x).rstrip('0').rstrip('.') if '.' in str(x) else x
)

# --- Streamlit app ---
st.title("Salary Predictor")

nav = st.sidebar.radio("Navigation", ["Home", "Prediction", "Contribute"])

if nav == "Home":
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("user-astronaut-solid.svg", width=300)

    show_data = st.checkbox("Show Data")

    if show_data:
        st.sidebar.markdown("---")  # Line separator below navigation
        st.sidebar.markdown("## View Mode")
        view_mode = st.sidebar.radio("", ["Default", "Range"])
        st.sidebar.markdown("<hr/>", unsafe_allow_html=True)

        if view_mode == "Default":
            # ✅ Filters for Default view
            st.sidebar.markdown("### Filters")
            filter_fields = [
                "Job Title",
                "Industry",
                "Education Level",
                "Location",
                "Employment Type",
                "Company Size",
                "Remote"
            ]

            # Initialize session state for filters
            if "filters" not in st.session_state:
                st.session_state.filters = {field: "All" for field in filter_fields}

            # Render dropdowns vertically
            for field in filter_fields:
                options = ["All"] + sorted(data[field].dropna().unique().tolist())
                selected = st.sidebar.selectbox(f"{field}", options, index=options.index(st.session_state.filters[field]))
                st.session_state.filters[field] = selected

            # Reset button
            if st.sidebar.button("Reset Filters"):
                for field in filter_fields:
                    st.session_state.filters[field] = "All"
                st.rerun()

            # Apply filters
            filtered_data = data.copy()
            for field, selected in st.session_state.filters.items():
                if selected != "All":
                    filtered_data = filtered_data[filtered_data[field] == selected]

            filtered_data = filtered_data.reset_index(drop=True)
            filtered_data.index += 1
            filtered_data.index.name = "S. No."

            if not filtered_data.empty:
                st.dataframe(filtered_data, use_container_width=True, height=500)
            else:
                st.dataframe(filtered_data, use_container_width=True, height=500)
                st.warning("No Data Available for the selected filters.")

        elif view_mode == "Range":
            # ✅ 1️⃣ Convert experience back to float for bucketing
            data["YearsExperience_Float"] = pd.to_numeric(data["YearsExperience"], errors="coerce")

            def get_exp_range(x):
                if pd.isna(x):
                    return "Unknown"
                lower = int(x)
                upper = lower + 1
                return f"{lower}-{upper} Years"

            # ✅ 2️⃣ Create the Experience_Range column BEFORE grouping
            data["Experience_Range"] = data["YearsExperience_Float"].apply(get_exp_range)

            # ✅ 3️⃣ Show dynamic grouping checkboxes AFTER
            st.sidebar.markdown("###### Grouping Options")

            optional_fields = ["Education Level", "Location", "Employment Type", "Company Size", "Remote"]

            group_selections = []
            cols = st.sidebar.columns(2)

            for idx, field in enumerate(optional_fields):
                col = cols[idx % 2]
                is_checked = col.checkbox(field, value=True)
                if is_checked:
                    group_selections.append(field)

            # ✅ 4️⃣ Always include Experience_Range & Job Title & Industry
            group_cols = ["Experience_Range", "Job Title", "Industry"] + group_selections

            # ✅ 5️⃣ Group by updated columns
            grouped = data.groupby(group_cols).agg(
                Avg_Salary=pd.NamedAgg(column="Salary (in INR)", aggfunc=lambda x: round(x.astype(float).mean(), 1)),
                Grouped=pd.NamedAgg(column="Salary (in INR)", aggfunc="count")
            ).reset_index()

            grouped = grouped[grouped["Experience_Range"] != "Unknown"]
            grouped = grouped.sort_values(by=["Experience_Range"])

            grouped.index += 1
            grouped.index.name = "S. No."

            st.dataframe(grouped, use_container_width=True, height=500)