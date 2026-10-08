import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from recommendation_engine import (
    ProjectRecommendationEngine
)

from models.student_profile import StudentProfile


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Final Year Project Selector",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 AI Final Year Project Selector")

st.write(
    "AI-powered project recommendations "
    "based on your skills, interests and academic profile."
)


# --------------------------------------------------
# LOAD ENGINE
# --------------------------------------------------

engine = ProjectRecommendationEngine(
    "data/projects.csv"
)

projects = engine.recommender.projects.copy()


# --------------------------------------------------
# SIDEBAR - STUDENT PROFILE
# --------------------------------------------------

st.sidebar.header("👤 Student Profile")

student_id = st.sidebar.text_input(
    "Student ID",
    "S001"
)

name = st.sidebar.text_input(
    "Name",
    "Sakshi"
)

education = st.sidebar.text_input(
    "Education",
    "B.Tech Computer Science"
)

branch = st.sidebar.text_input(
    "Branch",
    "CSE"
)

skills = st.sidebar.text_input(
    "Skills",
    "Python Machine Learning Pandas Scikit-learn NLP"
)

interests = st.sidebar.text_input(
    "Interests",
    "Artificial Intelligence Natural Language Processing"
)

domain = st.sidebar.selectbox(
    "Preferred Domain",
    ["Any"] +
    sorted(
        projects["domain"]
        .dropna()
        .unique()
        .tolist()
    )
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Any"] +
    sorted(
        projects["difficulty"]
        .dropna()
        .unique()
        .tolist()
    )
)

top_n = st.sidebar.slider(
    "Number of Recommendations",
    1,
    10,
    5
)


# --------------------------------------------------
# CREATE STUDENT
# --------------------------------------------------

student = StudentProfile(
    student_id=student_id,
    name=name,
    education=education,
    branch=branch,
    skills=skills,
    interests=interests,
    preferred_domain=domain,
    difficulty=difficulty
)


# --------------------------------------------------
# RECOMMENDATION
# --------------------------------------------------

if st.sidebar.button("🔍 Get Recommendations"):

    recommendations = engine.get_recommendations(
        student,
        top_n=top_n,
        domain=domain,
        difficulty=difficulty
    )

    st.session_state["recommendations"] = (
        recommendations
    )


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

if "recommendations" in st.session_state:

    recommendations = st.session_state[
        "recommendations"
    ]

    st.header("🎯 Recommended Projects")

    if recommendations.empty:

        st.warning(
            "No matching projects found."
        )

    else:

        for i, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            with st.container():

                st.subheader(
                    f"{i}. {row['title']}"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Match",
                    f"{row['match_score']:.1f}%"
                )

                col2.metric(
                    "Trend",
                    f"{row['trend_score']}"
                )

                col3.metric(
                    "Domain",
                    row["domain"]
                )

                col4.metric(
                    "Difficulty",
                    row["difficulty"]
                )

                st.write(
                    f"**Technologies:** "
                    f"{row['technologies']}"
                )

                st.divider()


        # --------------------------------------------------
        # EXPORT
        # --------------------------------------------------

        csv = recommendations.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Export Recommendations",
            data=csv,
            file_name="project_recommendations.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.header("📊 Project Analytics")


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Projects",
    len(projects)
)

col2.metric(
    "Average Trend",
    f"{projects['trend_score'].mean():.1f}"
)

col3.metric(
    "Highest Trend",
    f"{projects['trend_score'].max():.1f}"
)

col4.metric(
    "Domains",
    projects["domain"].nunique()
)


# --------------------------------------------------
# TREND CHART
# --------------------------------------------------

st.subheader("📈 Top Trending Projects")

top_trending = projects.sort_values(
    "trend_score",
    ascending=False
).head(10)

fig, ax = plt.subplots()

ax.barh(
    top_trending["title"],
    top_trending["trend_score"]
)

ax.set_xlabel("Trend Score")

ax.set_ylabel("Project")

ax.invert_yaxis()

st.pyplot(fig)


# --------------------------------------------------
# DOMAIN DISTRIBUTION
# --------------------------------------------------

st.subheader("🔍 Projects by Domain")

domain_counts = projects[
    "domain"
].value_counts()

fig2, ax2 = plt.subplots()

domain_counts.plot(
    kind="bar",
    ax=ax2
)

ax2.set_xlabel("Domain")

ax2.set_ylabel("Number of Projects")

plt.xticks(rotation=45)

st.pyplot(fig2)


# --------------------------------------------------
# DIFFICULTY DISTRIBUTION
# --------------------------------------------------

st.subheader("⚡ Difficulty Distribution")

difficulty_counts = projects[
    "difficulty"
].value_counts()

fig3, ax3 = plt.subplots()

difficulty_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax3
)

ax3.set_ylabel("")

st.pyplot(fig3)