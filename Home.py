import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

st.set_page_config(
    page_title="AI-Powered Job Market Trend Analysis",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/final_jobs.csv")

df = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("🔍 Filters")

company = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(df["companyname"].dropna().unique())
)

location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(df["location"].dropna().unique())
)

experience = st.sidebar.selectbox(
    "Experience",
    ["All"] + sorted(df["experience_category"].dropna().unique())
)

filtered_df = df.copy()

if company != "All":
    filtered_df = filtered_df[
        filtered_df["companyname"] == company
    ]

if location != "All":
    filtered_df = filtered_df[
        filtered_df["location"] == location
    ]

if experience != "All":
    filtered_df = filtered_df[
        filtered_df["experience_category"] == experience
    ]

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("📊 AI-Powered Job Market Trend Analysis & Skill Gap Analyzer")

st.markdown("""
Welcome to the **AI-Powered Job Market Trend Analysis & Skill Gap Analyzer**.

This application analyzes **97,000+ Indian job postings** to identify hiring trends,
top companies, high-demand skills, experience requirements, and provides an AI-based
Skill Gap Analyzer for career guidance.
""")

st.divider()

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------

st.subheader("📈 Job Market Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Jobs", len(filtered_df))

with c2:
    st.metric("Companies", filtered_df["companyname"].nunique())

with c3:
    st.metric("Locations", filtered_df["location"].nunique())

with c4:
    st.metric(
        "Avg Experience",
        f"{filtered_df['avg_experience'].mean():.1f} Years"
    )

st.divider()

# ---------------------------------------------------
# Charts
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🏢 Top Hiring Companies")

    companies = (
        filtered_df["companyname"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8,4))

    sns.barplot(
        x=companies.values,
        y=companies.index,
        ax=ax
    )

    st.pyplot(fig)

with right:

    st.subheader("🏙️ Top Hiring Cities")

    cities = (
        filtered_df["location"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(8,4))

    sns.barplot(
        x=cities.values,
        y=cities.index,
        ax=ax
    )

    st.pyplot(fig)

# ---------------------------------------------------
# Experience
# ---------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("👨‍💻 Experience Categories")

    st.bar_chart(
        filtered_df["experience_category"].value_counts()
    )

with right:

    st.subheader("⭐ Company Ratings")

    ratings = filtered_df["aggregaterating"]

    ratings = ratings[ratings > 0]

    fig, ax = plt.subplots(figsize=(8,4))

    ax.hist(ratings, bins=20)

    st.pyplot(fig)

# ---------------------------------------------------
# Top Skills
# ---------------------------------------------------

st.subheader("🔥 Top Skills")

skills = []

for row in filtered_df["tagsandskills"].dropna():

    skills.extend(
        [
            s.strip()
            for s in str(row).split(",")
        ]
    )

top = Counter(skills).most_common(15)

skill_df = pd.DataFrame(
    top,
    columns=["Skill","Count"]
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    data=skill_df,
    x="Count",
    y="Skill",
    ax=ax
)

st.pyplot(fig)

# ---------------------------------------------------
# Dataset Preview
# ---------------------------------------------------

st.divider()

st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.info("""
**Technologies Used:** Python • Pandas • NumPy • Scikit-learn • Streamlit • Matplotlib • Seaborn

**Dataset:** Indian Job Market Dataset (2025)

Use the sidebar to explore **Job Insights** and the **AI Skill Gap Analyzer**.
""")