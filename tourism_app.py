import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Tourism Experience Analytics",
    layout="wide"
)

# -----------------------------
# Load Cleaned Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv(
        "Notebooks/processed/cleaned_tourism_experience_data.csv"
    )

try:
    rec_df = load_data()
    st.success("Cleaned dataset loaded successfully")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -----------------------------
# Title
# -----------------------------
st.title("Tourism Experience Analytics")

st.write("""
This Streamlit application provides:
- Popular destination recommendations
- Preference-based tourism suggestions
- Visit mode prediction
- Key insights from tourism experience data
""")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs([
    "Destination Recommendation",
    "Visit Mode Prediction",
    "Insights & Trends"
])

# =====================================================
# TAB 1: DESTINATION RECOMMENDATION
# =====================================================
with tab1:
    st.header("Destination Recommendation System")

    st.sidebar.header("Recommendation Preferences")

    visit_mode = st.sidebar.selectbox(
        "Select Visit Mode",
        sorted(rec_df["VisitMode"].dropna().unique())
    )

    attraction_type = st.sidebar.selectbox(
        "Select Attraction Type",
        sorted(rec_df["AttractionType"].dropna().unique())
    )

    region = st.sidebar.selectbox(
        "Select Region",
        ["All"] + sorted(rec_df["Region"].dropna().unique())
    )

    top_n = st.sidebar.slider(
        "Number of Recommendations",
        min_value=1,
        max_value=10,
        value=5
    )

    filtered_df = rec_df[
        (rec_df["VisitMode"] == visit_mode) &
        (rec_df["AttractionType"] == attraction_type)
    ]

    if region != "All":
        filtered_df = filtered_df[filtered_df["Region"] == region]

    recommendations = (
        filtered_df
        .groupby(["City", "Country"], as_index=False)
        .agg(avg_rating=("Rating", "mean"))
        .sort_values("avg_rating", ascending=False)
        .head(top_n)
    )

    st.subheader("Recommended Destinations")

    if recommendations.empty:
        st.warning("No matching destinations found for selected preferences.")
    else:
        st.dataframe(recommendations, use_container_width=True)

# =====================================================
# TAB 2: VISIT MODE PREDICTION
# =====================================================
with tab2:
    st.header("Visit Mode Prediction")

    st.write("""
This module predicts the most likely visit mode based on
traveler profile inputs.
    """)

    age_group = st.selectbox(
        "Select Age Group",
        ["18-25", "26-35", "36-50", "50+"]
    )

    travel_budget = st.selectbox(
        "Select Travel Budget",
        ["Low", "Medium", "High"]
    )

    group_size = st.slider(
        "Group Size",
        min_value=1,
        max_value=10,
        value=2
    )

    def predict_visit_mode(age, budget, group):
        if group >= 4:
            return "Family"
        elif budget == "High":
            return "Business"
        elif age == "18-25":
            return "Solo"
        else:
            return "Friends"

    if st.button("Predict Visit Mode"):
        prediction = predict_visit_mode(age_group, travel_budget, group_size)
        st.success(f"Predicted Visit Mode: **{prediction}**")

# =====================================================
# TAB 3: INSIGHTS & TRENDS
# =====================================================
with tab3:
    st.header("Tourism Insights & Trends")

    st.subheader("Most Popular Visit Modes")
    visit_mode_counts = rec_df["VisitMode"].value_counts()
    st.bar_chart(visit_mode_counts)

    st.subheader("Average Rating by Region")
    region_rating = (
        rec_df.groupby("Region")["Rating"]
        .mean()
        .sort_values(ascending=False)
    )
    st.bar_chart(region_rating)

    st.info("""
These insights help tourism boards and businesses understand
traveler behavior and regional performance.
    """)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Tourism Experience Analytics | Streamlit Demo")
