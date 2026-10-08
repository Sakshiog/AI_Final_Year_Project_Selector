import json
import os
import io
import hashlib

import pandas as pd
import streamlit as st

from recommendation_engine import ProjectRecommendationEngine
from models.student_profile import StudentProfile


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Final Year Project Selector",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

STUDENT_FILE = "data/students.json"
PROJECT_FILE = "data/projects.csv"


# =========================================================
# CREATE DATA FOLDER / STUDENT FILE
# =========================================================

os.makedirs("data", exist_ok=True)

if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w") as file:
        json.dump({}, file, indent=4)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APP ---------- */

    .stApp {
        background-color: #FFFFFF;
        color: #111111;
    }

    /* ---------- TITLES ---------- */

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #111111;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .main-subtitle {
        text-align: center;
        font-size: 22px;
        color: #666666;
        margin-top: 10px;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 800;
        color: #111111;
        margin-top: 28px;
        margin-bottom: 18px;
    }

    p, h1, h2, h3, h4, li {
        color: #111111;
    }

    /* ---------- LABELS ---------- */

    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label,
    .stMultiSelect label,
    [data-testid="stWidgetLabel"] p {
        font-weight: 700 !important;
        color: #111111 !important;
        font-size: 15px !important;
    }

    /* ---------- ALL INPUTS: WHITE ---------- */

    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        border: 1px solid #111111 !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] svg {
        color: #111111 !important;
        fill: #111111 !important;
    }

    /* Password eye button */
    div[data-baseweb="input"] button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    /* Selectbox dropdown list */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: #F3F4F6 !important;
    }

    /* ---------- FORCE WHITE (works on newer Streamlit too) ---------- */

    :root {
        color-scheme: light !important;
    }

    input, textarea {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
    }

    input::placeholder, textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }

    [data-testid="stTextInput"] *,
    [data-testid="stTextArea"] *,
    [data-testid="stNumberInput"] *,
    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stTextInputRootElement"],
    [data-testid="stTextInputRootElement"] > div,
    [data-testid="stTextAreaRootElement"],
    [data-testid="stTextAreaRootElement"] > div {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }

    [data-testid="stTextInputRootElement"],
    [data-testid="stTextAreaRootElement"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border: 1px solid #111111 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSelectbox"] svg {
        fill: #111111 !important;
    }

    /* ---------- DARK BORDER ON ALL INPUTS ---------- */

    [data-testid="stTextInputRootElement"],
    [data-testid="stTextAreaRootElement"],
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stTextInput"] [data-baseweb="input"],
    [data-testid="stNumberInput"] [data-baseweb="input"],
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        border: 1px solid #111111 !important;
        border-radius: 8px !important;
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        border: none !important;
    }

    [data-testid="stTextInput"] *,
    [data-testid="stTextArea"] *,
    [data-testid="stNumberInput"] * {
        border-color: #111111 !important;
    }

    /* ---------- TEXT AREA: SAME LOOK AS OTHER BOXES ---------- */

    /* wrappers: no border of their own */
    [data-testid="stTextArea"] [data-baseweb="textarea"],
    [data-testid="stTextArea"] [data-baseweb="base-input"],
    [data-testid="stTextAreaRootElement"] {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background-color: transparent !important;
    }

    /* the textarea itself carries the border */
    [data-testid="stTextArea"] textarea {
        border: 1px solid #111111 !important;
        border-radius: 8px !important;
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        padding: 10px 12px !important;
        box-sizing: border-box !important;
        width: 100% !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: #60A5FA !important;
        box-shadow: 0 0 0 1px #60A5FA !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
    }

    /* ---------- FOCUS ---------- */

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #60A5FA !important;
        box-shadow: 0 0 0 1px #60A5FA !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button,
    .stDownloadButton > button {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: 1px solid #4F46E5 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        min-height: 42px;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #4338CA !important;
        color: #FFFFFF !important;
        border-color: #4338CA !important;
    }

    .stButton > button p,
    .stDownloadButton > button p {
        color: #FFFFFF !important;
    }

       /* ---------- BORDERED CONTAINER (cards / login box) ---------- */

    [data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"]) > div[data-testid="stVerticalBlockBorderWrapper"],
    div.st-key-login_box,
    div.st-key-register_box {
        background-color: #FFFFFF !important;
        border: 2px solid #111111 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
    }

    .project-title {
        font-size: 21px;
        font-weight: 800;
        color: #111111;
    }

    .project-info {
        color: #666666;
        font-size: 14px;
        margin-top: 6px;
        margin-bottom: 8px;
    }

    .match-score {
        font-size: 28px;
        font-weight: 800;
        color: #111111;
    }

    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #111111 !important;
    }

    [data-testid="stMetricLabel"] p {
        color: #666666 !important;
    }

    /* ---------- EXPANDER ---------- */

    [data-testid="stExpander"] {
        background-color: #4F46E5 !important;
        border: 1px solid #4F46E5 !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary {
        padding: 16px 20px !important;
        min-height: 56px;
        background-color: #4F46E5 !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: #4338CA !important;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* andar ka content white background pe readable rahe */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #FFFFFF !important;
        padding: 16px 20px !important;
    }

        /* ---------- SPINNER ---------- */

    [data-testid="stSpinner"] p {
        color: #4F46E5 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }

    /* ---------- ALERTS ---------- */

    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PASSWORD FUNCTIONS
# =========================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash


# =========================================================
# STUDENT JSON FUNCTIONS
# =========================================================

def load_students():
    try:
        with open(STUDENT_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {}


def save_students(students):
    with open(STUDENT_FILE, "w") as file:
        json.dump(students, file, indent=4)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_id" not in st.session_state:
    st.session_state.student_id = None

if "account_created" not in st.session_state:
    st.session_state.account_created = False


# =========================================================
# LOAD RECOMMENDATION ENGINE
# =========================================================

@st.cache_resource(show_spinner=False)
def load_engine():
    return ProjectRecommendationEngine(PROJECT_FILE)


with st.spinner("🎓 Loading AI Project Selector... please wait"):
    engine = load_engine()


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    st.markdown(
        '<div class="main-title">🎓 AI Final Year Project Selector</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Find the right final-year project using AI-powered recommendations'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.15, 1])

    with center:

        if st.session_state.account_created:
            st.success("Account created successfully! Please login.")
            st.session_state.account_created = False

        with st.container(border=True, key="login_box"):

            st.subheader("🔐 Student Login")

            student_id = st.text_input(
                "Student ID",
                placeholder="Enter your Student ID"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login = st.button("Login", use_container_width=True)

            if login:

                students = load_students()

                if not student_id.strip():
                    st.error("Please enter your Student ID.")

                elif not password:
                    st.error("Please enter your password.")

                elif student_id not in students:
                    st.error("Student ID not found. Please create an account first.")

                elif not verify_password(password.strip(), students[student_id]["password"]):
                    st.error("Incorrect password.")

                else:
                    st.session_state.logged_in = True
                    st.session_state.student_id = student_id
                    st.session_state.page = "dashboard"
                    st.rerun()

            if st.button("Create New Account", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()


# =========================================================
# CREATE ACCOUNT PAGE
# =========================================================

def register_page():

    st.markdown(
        '<div class="main-title">🧑‍🎓 Create Student Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Create your profile before getting AI project recommendations'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([0.7, 1.6, 0.7])

    with center:
        with st.container(border=True, key="register_box"):
            st.subheader("👤 Student Details")

            student_id = st.text_input(
                "Student ID",
                placeholder="Example: S001"
            )

            name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            education = st.text_input(
                "Education",
                value="B.Tech Computer Science"
            )

            branch = st.selectbox(
                "Branch",
                [
                    "Computer Science",
                    "Computer Science & Engineering (CSE)",
                    "Information Technology",
                    "Artificial Intelligence & Data Science",
                    "Artificial Intelligence & Machine Learning",
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Data Science",
                    "Data Analytics",
                    "Cyber Security",
                    "Cloud Computing",
                    "Internet of Things (IoT)",
                    "Blockchain Technology",
                    "Software Engineering",
                    "Computer Applications (BCA)",
                    "Computer Applications (MCA)",
                    "Computer Science & Business Systems",
                    "Computer Science & Design",
                    "Computer Engineering",
                    "Information Science & Engineering",
                    "Robotics & Automation",
                    "Mechatronics",
                    "Game Technology",
                    "Networking & Telecommunications",
                    "Electronics & Communication",
                    "Electronics & Computer Engineering",
                    "Electronics & Instrumentation",
                    "Electronics & Telecommunication",
                    "VLSI Design",
                    "Embedded Systems",
                    "Electrical",
                    "Electrical & Electronics",
                    "Instrumentation & Control",
                    "Power Systems",
                    "Telecommunication Engineering",
                    "Mechanical",
                    "Automobile",
                    "Aerospace",
                    "Aeronautical",
                    "Production Engineering",
                    "Industrial Engineering",
                    "Manufacturing Engineering",
                    "Marine Engineering",
                    "Mining Engineering",
                    "Metallurgical Engineering",
                    "Materials Science",
                    "Civil",
                    "Structural Engineering",
                    "Environmental Engineering",
                    "Construction Technology",
                    "Architecture",
                    "Geoinformatics",
                    "Chemical",
                    "Petroleum Engineering",
                    "Biotechnology",
                    "Biomedical Engineering",
                    "Bioinformatics",
                    "Food Technology",
                    "Agricultural Engineering",
                    "Textile Engineering",
                    "Polymer Science",
                    "Nanotechnology",
                    "Pharmacy",
                    "Mathematics & Computing",
                    "Physics",
                    "Statistics",
                    "Business Analytics",
                    "Management (MBA)",
                    "Other"
                ]
            )

            skills = st.text_area(
                "Skills",
                placeholder="Example: Python, Machine Learning, Pandas, SQL"
            )

            interests = st.text_area(
                "Interests",
                placeholder="Example: Artificial Intelligence, NLP, Data Science"
            )

            preferred_domain = st.selectbox(
                "Preferred Domain",
                [
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Deep Learning",
                    "Generative AI",
                    "Natural Language Processing",
                    "Computer Vision",
                    "Reinforcement Learning",
                    "Speech Recognition",
                    "Recommendation Systems",
                    "Data Science",
                    "Big Data & Analytics",
                    "Data Visualization",
                    "Data Engineering",
                    "Business Intelligence",
                    "Predictive Analytics",
                    "Web Development",
                    "Full Stack Development",
                    "Frontend Development",
                    "Backend Development",
                    "Mobile App Development",
                    "Cross-Platform Apps",
                    "E-Commerce Systems",
                    "Progressive Web Apps",
                    "Cyber Security",
                    "Ethical Hacking",
                    "Network Security",
                    "Digital Forensics",
                    "Cryptography",
                    "Malware Analysis",
                    "Cloud Computing",
                    "DevOps",
                    "Serverless Computing",
                    "Edge Computing",
                    "Internet of Things",
                    "Embedded Systems",
                    "Robotics",
                    "Drones & UAV",
                    "Automation",
                    "Smart Home",
                    "Smart City",
                    "Industrial IoT",
                    "Wearable Technology",
                    "Blockchain",
                    "Smart Contracts",
                    "Cryptocurrency & DeFi",
                    "AR / VR",
                    "Metaverse",
                    "Game Development",
                    "3D Modeling & Animation",
                    "Healthcare Technology",
                    "Medical Image Analysis",
                    "Bioinformatics",
                    "Agriculture Technology",
                    "Education Technology",
                    "Fintech",
                    "Social Media Analytics",
                    "Sentiment Analysis",
                    "Chatbots & Virtual Assistants",
                    "Image Processing",
                    "Signal Processing",
                    "VLSI & Chip Design",
                    "Wireless Communication",
                    "5G & Networking",
                    "Renewable Energy",
                    "Smart Grid",
                    "Electric Vehicles",
                    "Autonomous Vehicles",
                    "Transportation Systems",
                    "Environmental Monitoring",
                    "Disaster Management",
                    "Geospatial / GIS",
                    "Quantum Computing",
                    "Operating Systems",
                    "Database Systems",
                    "Compiler Design",
                    "Software Testing",
                    "Software Development",
                    "Other"
                ]
            )

            difficulty = st.selectbox(
                "Preferred Difficulty",
                ["Any", "Easy", "Medium", "Hard"]
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )

            create_account = st.button(
                "Create Account",
                use_container_width=True
            )

        if create_account:
            students = load_students()

            if not student_id.strip():
                st.error("Please enter Student ID.")

            elif not name.strip():
                st.error("Please enter your name.")

            elif not skills.strip():
                st.error("Please enter your skills.")

            elif not interests.strip():
                st.error("Please enter your interests.")

            elif not password:
                st.error("Please create a password.")

            elif password.strip() != confirm_password.strip():
                st.error("Passwords do not match. Check spelling, capital letters and extra spaces.")

            elif student_id in students:
                st.error("This Student ID already exists.")

            else:
                students[student_id] = {
                    "student_id": student_id,
                    "name": name,
                    "education": education,
                    "branch": branch,
                    "skills": skills,
                    "interests": interests,
                    "preferred_domain": preferred_domain,
                    "difficulty": difficulty,
                    "password": hash_password(password.strip())
                }

                save_students(students)

                st.session_state.account_created = True
                st.session_state.page = "login"
                st.rerun()

        st.write("")

        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

def show_chart(data, height=420, horizontal=False):
    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        st.bar_chart(
            data,
            height=height,
            horizontal=horizontal,
            use_container_width=True
        )

# =========================================================
# DASHBOARD
# =========================================================

def dashboard():

    students = load_students()
    student_id = st.session_state.student_id
    student_data = students[student_id]

    student = StudentProfile(
        student_id=student_data["student_id"],
        name=student_data["name"],
        education=student_data["education"],
        branch=student_data["branch"],
        skills=student_data["skills"],
        interests=student_data["interests"],
        preferred_domain=student_data["preferred_domain"],
        difficulty=student_data["difficulty"]
    )

    # ---------- HEADER ----------

    top1, top2 = st.columns([4, 1])

    with top1:
        st.markdown(
            '<div class="main-title"> 🎓 AI Final Year Project Selector</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="main-subtitle">'
            'Personalized project recommendations powered by AI'
            '</div>',
            unsafe_allow_html=True
        )

    with top2:
        st.write("")
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.session_state.page = "login"
            st.rerun()

    # ---------- STUDENT PROFILE ----------

    st.markdown(
        '<div class="section-title">👤 Student Profile</div>',
        unsafe_allow_html=True
    )

    p1, p2, p3, p4 = st.columns(4)

    p1.metric("Student ID", student.student_id)
    p2.metric("Branch", student.branch)
    p3.metric("Domain", student.preferred_domain)
    p4.metric("Difficulty", student.difficulty)

    with st.expander("👤 View Candidate Profile"):
        c1, c2 = st.columns(2)

        with c1:
            st.write(f"**Name:** {student.name}")
            st.write(f"**Education:** {student.education}")
            st.write(f"**Branch:** {student.branch}")

        with c2:
            st.write(f"**Skills:** {student.skills}")
            st.write(f"**Interests:** {student.interests}")
            st.write(f"**Preferred Domain:** {student.preferred_domain}")

    # ---------- LOAD PROJECTS ----------

    projects = pd.read_csv(PROJECT_FILE)

    # ---------- ANALYTICS ----------

    st.markdown(
        '<div class="section-title">📊 Project Analytics</div>',
        unsafe_allow_html=True
    )

    a1, a2, a3, a4 = st.columns(4)

    a1.metric("Total Projects", len(projects))
    a2.metric("Domains", projects["domain"].nunique())
    a3.metric("Branches", projects["branch"].nunique())
    a4.metric(
        "Trending Projects",
        len(projects[projects["trend_score"] >= 70])
    )

    # ---------- INSIGHTS ----------

    st.markdown(
        '<div class="section-title">📈 Project Insights</div>',
        unsafe_allow_html=True
    )


    # ---------- 1. TOP TRENDING PROJECTS ----------

    st.subheader("🔥 Top Trending Projects")

    trending = (
        projects
        .sort_values("trend_score", ascending=False)
        .head(8)
    )

    show_chart(
    trending.set_index("title")["trend_score"],
    height=450,
    horizontal=True
)


    # ---------- 2. PROJECTS BY DOMAIN ----------

    st.subheader("📂 Projects by Domain")

    show_chart(
        projects["domain"].value_counts(),
        height=800,
        horizontal=True
    )


    # ---------- 3. DIFFICULTY DISTRIBUTION ----------

    st.subheader("🎯 Difficulty Distribution")

    show_chart(
    projects["difficulty"].value_counts(),
    height=350
)


    # ---------- 4. TOP PROJECT DOMAINS ----------

    st.subheader("🏆 Top Project Domains")

    show_chart(
projects["domain"].value_counts().head(5),
    height=350
)

    # ---------- FILTERS ----------

    st.markdown(
        '<div class="section-title">🎯 Find Your Projects</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        selected_domain = st.selectbox(
            "Domain Filter",
            ["Any"] + sorted(projects["domain"].dropna().unique().tolist())
        )

    with f2:
        selected_difficulty = st.selectbox(
            "Difficulty Filter",
            ["Any", "Easy", "Medium", "Hard"]
        )

    with f3:
        top_n = st.selectbox(
            "Number of Recommendations",
            list(range(1, 11)),
            index=4
        )

    # ---------- RECOMMENDATIONS ----------

        recommendations = engine.get_recommendations(
        student,
        top_n=top_n,
        domain=None if selected_domain == "Any" else selected_domain,
        difficulty=None if selected_difficulty == "Any" else selected_difficulty
    )
       

    st.markdown(
        '<div class="section-title">🤖 Personalized AI Recommendations</div>',
        unsafe_allow_html=True
    )

    if recommendations.empty:

        st.warning("No projects match the selected filters.")

    else:

        for _, row in recommendations.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.markdown(
                        f'<div class="project-title">{row["title"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f'<div class="project-info">'
                        f'📌 Domain: {row["domain"]}'
                        f' &nbsp; | &nbsp; '
                        f'🎓 Branch: {row["branch"]}'
                        f' &nbsp; | &nbsp; '
                        f'⚡ Difficulty: {row["difficulty"]}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.write(f"**Technologies:** {row['technologies']}")

                    reasons = []

                    if row["branch_score"] > 0:
                        reasons.append("Branch matches")

                    if row["skills_score"] > 0:
                        reasons.append("Skills match")

                    if row["interest_score"] > 0:
                        reasons.append("Interests match")

                    if row["domain_score"] > 0:
                        reasons.append("Preferred domain matches")

                    if row["difficulty_score"] > 0:
                        reasons.append("Difficulty matches")

                    if row["tfidf_score"] > 0:
                        reasons.append("Profile similarity")

                    if reasons:
                        st.write("**Why Recommended:** " + " • ".join(reasons))

                with col2:

                    st.markdown(
                        f'<div class="match-score">{row["match_score"]:.1f}%</div>',
                        unsafe_allow_html=True
                    )

                    st.caption("AI Match Score")

                    st.write(f"🔥 Trend: {row['trend_score']}")

    # ---------- EXPORT ----------

    st.markdown(
        '<div class="section-title">📥 Export Results</div>',
        unsafe_allow_html=True
    )

    if not recommendations.empty:

        export_cols = [
            "title", "domain", "branch", "difficulty",
            "technologies", "trend_score", "match_score"
        ]

        export_df = recommendations[export_cols].copy()
        export_df["match_score"] = export_df["match_score"].round(2)

        st.download_button(
            label="Download Recommendations CSV",
            data=export_df.to_csv(index=False),
            file_name="my_project_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )

        buffer = io.BytesIO()
        export_df.to_excel(buffer, index=False, sheet_name="Recommendations")

        st.download_button(
            label="Download Recommendations Excel",
            data=buffer.getvalue(),
            file_name="my_project_recommendations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# =========================================================
# PAGE ROUTING
# =========================================================

if st.session_state.logged_in:
    dashboard()
else:
    if st.session_state.page == "register":
        register_page()
    else:
        login_page()