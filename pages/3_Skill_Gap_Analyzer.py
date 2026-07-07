import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/final_jobs.csv")

df = load_data()

# ----------------------------------------------------
# Build Skill Dictionary
# ----------------------------------------------------

skill_dictionary = {}

for _, row in df.iterrows():

    job = str(row["title"]).strip()

    skills = str(row["tagsandskills"]).split(",")

    skills = [
        s.strip().lower()
        for s in skills
        if s.strip()
    ]

    if job not in skill_dictionary:
        skill_dictionary[job] = Counter()

    skill_dictionary[job].update(skills)

for job in skill_dictionary:

    skill_dictionary[job] = [

        skill

        for skill, count

        in skill_dictionary[job].most_common(20)

    ]

# ----------------------------------------------------
# UI
# ----------------------------------------------------

st.title("🧠 AI Career & Skill Gap Analyzer")

st.markdown("""
Compare your current skills with the skills required for your dream job and receive personalized recommendations.
""")

job = st.selectbox(
    "🎯 Select Target Job",
    sorted(skill_dictionary.keys())
)

user_input = st.text_area(
    "📝 Enter Your Skills (comma separated)",
    placeholder="Python, SQL, Excel"
)

# ----------------------------------------------------
# Analyze
# ----------------------------------------------------

if st.button("🚀 Analyze"):

    current = [

        s.strip().lower()

        for s in user_input.split(",")

        if s.strip()

    ]

    required = skill_dictionary[job]

    matched = [

        s

        for s in required

        if s in current

    ]

    missing = [

        s

        for s in required

        if s not in current

    ]

    match = round(

        len(matched)/max(len(required),1)*100,

        2

    )

    employability = min(

        100,

        match + 10

    )

    # ----------------------------

    st.header("📊 Analysis")

    st.progress(match/100)

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Skill Match",
            f"{match}%"
        )

    with c2:

        st.metric(
            "Employability Score",
            f"{employability}%"
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.success("✅ Skills You Already Have")

        if matched:

            for skill in matched:

                st.write("✔", skill.title())

        else:

            st.write("No matching skills found.")

    with col2:

        st.error("❌ Missing Skills")

        for skill in missing:

            st.write("•", skill.title())

    st.divider()

    st.subheader("🔥 Recommended Learning Path")

    for i, skill in enumerate(missing[:5], start=1):

        st.write(f"**Step {i}:** Learn **{skill.title()}**")

    st.divider()

    st.subheader("⏳ Estimated Learning Time")

    weeks = max(4, len(missing) * 2)

    st.info(f"Estimated time to acquire these skills: **{weeks} weeks**")

    st.subheader("💼 Career Advice")

    if match >= 80:

        st.success(
            "Excellent! You are already well prepared for this role."
        )

    elif match >= 60:

        st.warning(
            "You are close. Learning a few additional skills will significantly improve your profile."
        )

    else:

        st.error(
            "Your current profile has significant skill gaps. Focus on the recommended learning path before applying."
        )