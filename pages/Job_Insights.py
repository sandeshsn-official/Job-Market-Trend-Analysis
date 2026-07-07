import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Insights", page_icon="📈", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/final_jobs.csv")

df = load_data()

st.title("📈 Job Market Insights")

# -----------------------------
# Top Hiring Companies
# -----------------------------

st.subheader("🏢 Top Hiring Companies")

top_companies = (
    df["companyname"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_companies.columns = ["Company", "Jobs"]

fig = px.bar(
    top_companies,
    x="Jobs",
    y="Company",
    orientation="h",
    color="Jobs",
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top Hiring Cities
# -----------------------------

st.subheader("🏙️ Top Hiring Cities")

top_locations = (
    df["location"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_locations.columns = ["City", "Jobs"]

fig = px.bar(
    top_locations,
    x="Jobs",
    y="City",
    orientation="h",
    color="Jobs",
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Salary Band
# -----------------------------

st.subheader("💰 Salary Band Distribution")

fig = px.histogram(
    df,
    x="salary_band",
    color="salary_band"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Experience
# -----------------------------

st.subheader("👨‍💻 Experience Category")

fig = px.pie(
    df,
    names="experience_category"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Ratings
# -----------------------------

st.subheader("⭐ Company Ratings")

ratings = df[df["aggregaterating"] > 0]

fig = px.histogram(
    ratings,
    x="aggregaterating",
    nbins=20
)

st.plotly_chart(fig, use_container_width=True)