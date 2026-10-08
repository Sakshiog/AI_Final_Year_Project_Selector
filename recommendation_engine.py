from models.content_based import ContentBasedRecommender
from models.student_profile import StudentProfile


class ProjectRecommendationEngine:

    def __init__(self, project_data_path):

        self.recommender = ContentBasedRecommender(
            project_data_path
        )

    # --------------------------------------------------
    # Get Recommendations
    # --------------------------------------------------

    def get_recommendations(
        self,
        student,
        top_n=5,
        domain=None,
        difficulty=None
    ):

        student_data = student.to_dict()

        return self.recommender.recommend(
            student_data,
            top_n=top_n,
            domain=domain,
            difficulty=difficulty
        )

   
    # Trend Analysis
    # --------------------------------------------------

    def get_trend_analysis(self):

        projects = self.recommender.projects.copy()

        if "trend_score" not in projects.columns:
            projects["trend_score"] = 0

        projects["trend_score"] = (
            pd.to_numeric(
                projects["trend_score"],
                errors="coerce"
            )
            .fillna(0)
        )

        analysis = {
            "total_projects": len(projects),
            "average_trend_score": round(
                projects["trend_score"].mean(), 2
            ),
            "highest_trend_score": round(
                projects["trend_score"].max(), 2
            ),
            "lowest_trend_score": round(
                projects["trend_score"].min(), 2
            )
        }

        top_trending = projects.sort_values(
            "trend_score",
            ascending=False
        ).head(10)

        return analysis, top_trending

    # --------------------------------------------------
    # Export Recommendations
    # --------------------------------------------------

    def export_recommendations(
        self,
        recommendations,
        filename="recommendations.csv"
    ):

        recommendations.to_csv(
            filename,
            index=False
        )

        return filename


# ------------------------------------------------------
# TEST
# ------------------------------------------------------

if __name__ == "__main__":

    import pandas as pd

    engine = ProjectRecommendationEngine(
        "data/projects.csv"
    )

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

    recommendations = engine.get_recommendations(
        student,
        top_n=5,
        domain="Any",
        difficulty="Any"
    )

    print("\n========================================")
    print("     AI FINAL YEAR PROJECT SELECTOR")
    print("========================================")

    print(f"\nStudent: {student.name}")
    print(f"Branch: {student.branch}")
    print(f"Domain: {student.preferred_domain}")
    print(f"Difficulty: {student.difficulty}")

    print("\nRecommended Projects:")
    print("----------------------------------------")

    for _, row in recommendations.iterrows():

        print(f"\nProject: {row['title']}")
        print(f"Domain: {row['domain']}")
        print(f"Difficulty: {row['difficulty']}")
        print(f"Trend Score: {row['trend_score']}")
        print(f"Match Score: {row['match_score']:.2f}%")

    # Trend Analysis

    analysis, top_trending = (
        engine.get_trend_analysis()
    )

    print("\n========================================")
    print("          TREND ANALYSIS")
    print("========================================")

    print(
        f"Total Projects: "
        f"{analysis['total_projects']}"
    )

    print(
        f"Average Trend Score: "
        f"{analysis['average_trend_score']}"
    )

    print(
        f"Highest Trend Score: "
        f"{analysis['highest_trend_score']}"
    )

    print("\nTop Trending Projects:")
    print("----------------------------------------")

    for _, row in top_trending.iterrows():

        print(
            f"{row['title']} "
            f"→ {row['trend_score']}"
        )

    # Export

    filename = engine.export_recommendations(
        recommendations
    )

    print(
        f"\nRecommendations exported to: "
        f"{filename}"
    )