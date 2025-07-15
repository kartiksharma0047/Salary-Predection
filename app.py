import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go

# --- Load CSV ---
data = pd.read_csv("./Employee_Salary_Data.csv")

# --- Format decimals ---
data["YearsExperience"] = data["YearsExperience"].round(1)
data["Salary (in INR)"] = data["Salary (in INR)"].round(1)

# Only make a display column for pretty output:
data["YearsExperience_Display"] = data["YearsExperience"].map(
    lambda x: f"{x:.1f}".rstrip('0').rstrip('.') if '.' in str(x) else str(x)
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

    st.markdown("## 📊 Salary vs. Experience Graph")
    st.markdown("Visualize how years of experience relate to salary.")

    graph_type = st.radio(
        "Select Graph Type:",
        ["Non-Interactive (Matplotlib)", "Interactive (Plotly)"],
        horizontal=True
    )

    with st.expander("📈 Show Graph"):
        if graph_type == "Non-Interactive (Matplotlib)":
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(
                data["YearsExperience"].astype(float),
                data["Salary (in INR)"].astype(float),
                color='royalblue',
                edgecolor='k',
                alpha=0.7
            )
            ax.set_xlim(left=0)
            ax.set_xlabel("Years of Experience")
            ax.set_ylabel("Salary Million (INR)")
            ax.set_title("Scatter Plot: Experience vs. Salary")
            ax.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            st.pyplot(fig)

        elif graph_type == "Interactive (Plotly)":
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=data["YearsExperience"].astype(float),
                    y=data["Salary (in INR)"].astype(float),
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=data["YearsExperience"].astype(float),
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Years Exp")
                    ),
                    hovertemplate="<b>Experience:</b> %{x} years<br><b>Salary:</b> ₹%{y}<extra></extra>"
                )
            )

            fig.update_layout(
                title="Interactive Scatter Plot: Experience vs. Salary",
                xaxis=dict(title="Years of Experience", range=[0, 16]),
                yaxis=dict(title="Salary (INR)", range=[0, 2100000]),
                template="plotly_white",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)
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
            # ✅ 1️⃣ Convert experience to float for bucketing
            data["YearsExperience_Float"] = pd.to_numeric(data["YearsExperience"], errors="coerce")

            # ✅ 2️⃣ Add slider to set bucket size
            max_years = int(data["YearsExperience_Float"].max()) + 1
            bucket_size = st.sidebar.slider("Experience Range (in years)", min_value=1, max_value=max_years, value=1, step=1)

            # ✅ 3️⃣ Define bucket range function
            def get_dynamic_range(x, bucket):
                if pd.isna(x):
                    return "Unknown"
                lower = int((x // bucket) * bucket)
                upper = lower + bucket
                return f"{lower}-{upper} Years"

            def get_dynamic_sort_key(x):
                if x == "Unknown":
                    return -1
                return int(x.split("-")[0])

            # ✅ 4️⃣ Apply dynamic bucketing
            data["Experience_Range"] = data["YearsExperience_Float"].apply(lambda x: get_dynamic_range(x, bucket_size))
            data["Experience_Range_Sort"] = data["Experience_Range"].apply(get_dynamic_sort_key)

            # ✅ 5️⃣ Grouping Options
            st.sidebar.markdown("###### Grouping Options")
            optional_fields = ["Education Level", "Location", "Employment Type", "Company Size", "Remote"]

            group_selections = []
            cols = st.sidebar.columns(2)
            for idx, field in enumerate(optional_fields):
                col = cols[idx % 2]
                if col.checkbox(field, value=True):
                    group_selections.append(field)

            group_cols = ["Experience_Range", "Job Title", "Industry"] + group_selections

            # ✅ 6️⃣ Group by
            grouped = data.groupby(group_cols).agg(
                Avg_Salary=pd.NamedAgg(column="Salary (in INR)", aggfunc=lambda x: round(x.astype(float).mean(), 1)),
                Grouped=pd.NamedAgg(column="Salary (in INR)", aggfunc="count"),
                Sort_Key=pd.NamedAgg(column="Experience_Range_Sort", aggfunc="first")
            ).reset_index()

            # ✅ 7️⃣ Sort & Display
            grouped = grouped[grouped["Experience_Range"] != "Unknown"]
            grouped = grouped.sort_values(by="Sort_Key").drop(columns=["Sort_Key"])

            grouped.index += 1
            grouped.index.name = "S. No."
            st.dataframe(grouped, use_container_width=True, height=500)
