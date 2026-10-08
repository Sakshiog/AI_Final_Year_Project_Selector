class StudentProfile:

    def __init__(
        self,
        student_id,
        name,
        education,
        branch,
        skills,
        interests,
        preferred_domain,
        difficulty="Any"
    ):

        self.student_id = student_id
        self.name = name
        self.education = education
        self.branch = branch
        self.skills = skills
        self.interests = interests
        self.preferred_domain = preferred_domain
        self.difficulty = difficulty

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "name": self.name,
            "education": self.education,
            "branch": self.branch,
            "skills": self.skills,
            "interests": self.interests,
            "preferred_domain": self.preferred_domain,
            "difficulty": self.difficulty
        }


if __name__ == "__main__":

    student = StudentProfile(
        student_id="S001",
        name="Sakshi",
        education="B.Tech Computer Science",
        branch="CSE",
        skills="Python Machine Learning Pandas Scikit-learn NLP",
        interests="Artificial Intelligence Natural Language Processing",
        preferred_domain="Artificial Intelligence",
        difficulty="Medium"
    )

    print("\nStudent Profile")
    print("================")

    for key, value in student.to_dict().items():
        print(f"{key}: {value}")