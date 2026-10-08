from recommendation_engine import ProjectRecommendationEngine
from models.student_profile import StudentProfile

engine = ProjectRecommendationEngine("data/projects.csv")

test_students = [
    StudentProfile(
        student_id="T1", name="AI Student",
        education="B.Tech Computer Science",
        branch="Artificial Intelligence & Data Science",
        skills="Python, Machine Learning, TensorFlow, Pandas",
        interests="Artificial Intelligence, Deep Learning, NLP",
        preferred_domain="Artificial Intelligence",
        difficulty="Medium"
    ),
    StudentProfile(
        student_id="T2", name="Web Student",
        education="B.Tech Computer Science",
        branch="Computer Science",
        skills="HTML, CSS, JavaScript, React, Node.js, MongoDB",
        interests="Web Development, E-Commerce",
        preferred_domain="Web Development",
        difficulty="Easy"
    ),
    StudentProfile(
        student_id="T3", name="IoT Student",
        education="B.Tech Electronics",
        branch="Electronics & Communication",
        skills="Arduino, Raspberry Pi, Sensors, C++, MQTT",
        interests="IoT, Smart City, Embedded Systems",
        preferred_domain="Internet of Things",
        difficulty="Medium"
    ),
    StudentProfile(
        student_id="T4", name="Cyber Student",
        education="B.Tech Computer Science",
        branch="Cyber Security",
        skills="Python, Networking, Linux, Cryptography",
        interests="Cyber Security, Network Security, Ethical Hacking",
        preferred_domain="Cyber Security",
        difficulty="Hard"
    ),
    StudentProfile(
        student_id="T5", name="Healthcare Student",
        education="B.Tech Biomedical",
        branch="Biomedical Engineering",
        skills="Python, OpenCV, Deep Learning, Keras",
        interests="Medical Image Analysis, Healthcare AI",
        preferred_domain="Healthcare Technology",
        difficulty="Medium"
    ),
]

for s in test_students:
    print("\n" + "=" * 60)
    print(f"{s.name} | Domain: {s.preferred_domain} | Difficulty: {s.difficulty}")
    print("=" * 60)

    recs = engine.get_recommendations(s, top_n=5)

    for i, (_, row) in enumerate(recs.iterrows(), 1):
        print(f"{i}. {row['title']}")
        print(f"   Domain: {row['domain']} | {row['difficulty']} | Match: {row['match_score']:.1f}%")