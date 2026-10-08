import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.nlp_processor import NLPProcessor


class ContentBasedRecommender:

    def __init__(self, data_path):

        self.projects = pd.read_csv(data_path)

        self.nlp = NLPProcessor()

        # ----------------------------------------------
        # Prepare project text
        # ----------------------------------------------

        self.projects["processed_text"] = (
            self.projects["title"].fillna("") + " " +
            self.projects["description"].fillna("") + " " +
            self.projects["branch"].fillna("") + " " +
            self.projects["domain"].fillna("") + " " +
            self.projects["technologies"].fillna("")
        ).apply(self.nlp.preprocess)

        # ----------------------------------------------
        # TF-IDF
        # ----------------------------------------------

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000
        )

        self.project_vectors = self.vectorizer.fit_transform(
            self.projects["processed_text"]
        )

    # --------------------------------------------------
    # Normalize text
    # --------------------------------------------------

    def normalize(self, text):

        text = str(text).lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        return text.strip()

    # --------------------------------------------------
    # Get terms
    # --------------------------------------------------

    def get_terms(self, text):

        text = self.normalize(text)

        return {
            word
            for word in text.split()
            if len(word) > 1
        }

    # --------------------------------------------------
    # Skill Matching
    # --------------------------------------------------

    def calculate_skill_match(
        self,
        student_skills,
        project_technologies
    ):

        student_terms = self.get_terms(
            student_skills
        )

        project_terms = self.get_terms(
            project_technologies
        )

        if not student_terms:
            return 0

        matched = student_terms.intersection(
            project_terms
        )

        return (
            len(matched) /
            len(student_terms)
        ) * 100

    # --------------------------------------------------
    # Interest Matching
    # --------------------------------------------------

    def calculate_interest_match(
        self,
        student_interests,
        project_text
    ):

        student_terms = self.get_terms(
            student_interests
        )

        project_terms = self.get_terms(
            project_text
        )

        if not student_terms:
            return 0

        matched = student_terms.intersection(
            project_terms
        )

        return (
            len(matched) /
            len(student_terms)
        ) * 100

    # --------------------------------------------------
    # Branch Matching
    # --------------------------------------------------

    def calculate_branch_match(
        self,
        student_branch,
        project_branch
    ):

        student_branch = self.normalize(
            student_branch
        )

        project_branch = self.normalize(
            project_branch
        )

        if not student_branch:
            return 0

        if student_branch == project_branch:
            return 100

        return 0

    # --------------------------------------------------
    # Domain Matching
    # --------------------------------------------------

    def calculate_domain_match(
        self,
        preferred_domain,
        project_domain
    ):

        preferred_domain = self.normalize(
            preferred_domain
        )

        project_domain = self.normalize(
            project_domain
        )

        if not preferred_domain:
            return 0

        if preferred_domain == project_domain:
            return 100

        # Partial domain matching
        if (
            preferred_domain in project_domain
            or project_domain in preferred_domain
        ):
            return 70

        return 0

    # --------------------------------------------------
    # Difficulty Matching
    # --------------------------------------------------

    def calculate_difficulty_match(
        self,
        preferred_difficulty,
        project_difficulty
    ):

        if (
            not preferred_difficulty
            or preferred_difficulty.lower() == "any"
        ):
            return 100

        if (
            preferred_difficulty.lower()
            == str(project_difficulty).lower()
        ):
            return 100

        return 0

    # --------------------------------------------------
    # Main Recommendation
    # --------------------------------------------------

    def recommend(
        self,
        student_profile,
        top_n=5,
        domain=None,
        difficulty=None
    ):

        skills = student_profile.get(
            "skills",
            ""
        )

        interests = student_profile.get(
            "interests",
            ""
        )

        education = student_profile.get(
            "education",
            ""
        )

        branch = student_profile.get(
            "branch",
            ""
        )

        preferred_domain = student_profile.get(
            "preferred_domain",
            ""
        )

        preferred_difficulty = student_profile.get(
            "difficulty",
            "Any"
        )

        # ----------------------------------------------
        # Student Profile Text
        # ----------------------------------------------

        profile_text = (
            skills + " " +
            interests + " " +
            education + " " +
            branch + " " +
            preferred_domain
        )

        processed_profile = self.nlp.preprocess(
            profile_text
        )

        # ----------------------------------------------
        # TF-IDF Similarity
        # ----------------------------------------------

        student_vector = self.vectorizer.transform(
            [processed_profile]
        )

        tfidf_scores = cosine_similarity(
            student_vector,
            self.project_vectors
        ).flatten() * 100

        results = self.projects.copy()

        results["tfidf_score"] = tfidf_scores

        # ----------------------------------------------
        # Skills Score
        # ----------------------------------------------

        results["skills_score"] = results[
            "technologies"
        ].apply(
            lambda x:
            self.calculate_skill_match(
                skills,
                x
            )
        )

        # ----------------------------------------------
        # Interest Score
        # ----------------------------------------------

        results["interest_score"] = results.apply(
            lambda row:
            self.calculate_interest_match(
                interests,
                (
                    str(row["title"]) + " " +
                    str(row["description"]) + " " +
                    str(row["domain"]) + " " +
                    str(row["technologies"])
                )
            ),
            axis=1
        )

        # ----------------------------------------------
        # Branch Score
        # ----------------------------------------------

        results["branch_score"] = results[
            "branch"
        ].apply(
            lambda x:
            self.calculate_branch_match(
                branch,
                x
            )
        )

        # ----------------------------------------------
        # Domain Score
        # ----------------------------------------------

        results["domain_score"] = results[
            "domain"
        ].apply(
            lambda x:
            self.calculate_domain_match(
                preferred_domain,
                x
            )
        )

        # ----------------------------------------------
        # Difficulty Score
        # ----------------------------------------------

        results["difficulty_score"] = results[
            "difficulty"
        ].apply(
            lambda x:
            self.calculate_difficulty_match(
                preferred_difficulty,
                x
            )
        )

        # ----------------------------------------------
        # Final Weighted Score
        #
        # Branch       = 30%
        # Skills       = 25%
        # Interests    = 20%
        # Domain       = 15%
        # TF-IDF       = 5%
        # Difficulty   = 5%
        # ----------------------------------------------

        # ----------------------------------------------
        # Trend Score
        # ----------------------------------------------

        if "trend_score" not in results.columns:
            results["trend_score"] = 0

        results["trend_score_normalized"] = (
            results["trend_score"].fillna(0).clip(0, 100)
        )

        # ----------------------------------------------
        # Final Weighted Score
        #
        # Branch       = 28%
        # Skills       = 24%
        # Interests    = 18%
        # Domain       = 14%
        # Difficulty   = 6%
        # TF-IDF       = 5%
        # Trend        = 5%
        # ----------------------------------------------

        results["match_score"] = (
            results["branch_score"] * 0.28 +
            results["skills_score"] * 0.24 +
            results["interest_score"] * 0.18 +
            results["domain_score"] * 0.14 +
            results["difficulty_score"] * 0.06 +
            results["tfidf_score"] * 0.05 +
            results["trend_score_normalized"] * 0.05
        )

        # ----------------------------------------------
        # Domain Filter
        # ----------------------------------------------

        if domain and domain != "Any":

            results = results[
                results["domain"].str.lower()
                == domain.lower()
            ]

        # ----------------------------------------------
        # Difficulty Filter
        # ----------------------------------------------

        if difficulty and difficulty != "Any":

            results = results[
                results["difficulty"].str.lower()
                == difficulty.lower()
            ]

        # ----------------------------------------------
        # Sort Results
        # ----------------------------------------------

        results = results.sort_values(
            by="match_score",
            ascending=False
        )

        return results.head(top_n)[
    [
        "project_id",
        "title",
        "branch",
        "domain",
        "technologies",
        "difficulty",
        "trend_score",
        "branch_score",
        "skills_score",
        "interest_score",
        "domain_score",
        "tfidf_score",
        "difficulty_score",
        "match_score"
    ]
]