# 🎓 AI Final Year Project Selector
An AI-powered recommendation system that helps students find suitable final-year project ideas based on their **academic background, skills, interests, preferred domain, difficulty level, and project trends**.

The system uses **Natural Language Processing (NLP), TF-IDF, Content-Based Filtering, and similarity-based recommendation techniques** to generate personalized project recommendations.

## 🚀 Features
* 👤 Student Registration and Login
* 📝 Student Profile Management
* 🎯 Personalized Project Recommendations
* 🤖 AI-based Matching Score
* 🧠 NLP-based Profile and Project Processing
* 📊 TF-IDF and Cosine Similarity
* 💡 Skill and Interest Matching
* 🎓 Branch-based Matching
* 📌 Domain-based Filtering
* ⚡ Difficulty-based Filtering
* 🔥 Project Trend Score
* 🔢 Top-N Project Recommendations
* 📥 Export Recommendations to CSV
* 📊 Export Recommendations to Excel
* 📈 Project Analytics Dashboard
* 🧪 Recommendation Testing with Multiple Student Profiles

## 🧠 How the System Works

The recommendation process follows these steps:

```text
Student Registration
        ↓
Student Profile Creation
        ↓
Profile Data Processing
        ↓
NLP Preprocessing
        ↓
Project Feature Extraction
        ↓
TF-IDF Vectorization
        ↓
Similarity Calculation
        ↓
Skill + Interest + Domain + Branch Matching
        ↓
AI Match Score
        ↓
Personalized Project Recommendations
```
## 🎯 Recommendation Factors

The recommendation engine considers multiple factors while ranking projects:

| Factor             | Purpose                                                      |
| ------------------ | ------------------------------------------------------------ |
| Branch             | Matches the student's academic branch                        |
| Skills             | Matches student's technical skills with project requirements |
| Interests          | Matches student's areas of interest                          |
| Domain             | Matches preferred project domain                             |
| Difficulty         | Matches preferred project difficulty                         |
| Profile Similarity | Measures similarity between student profile and project      |
| Trend Score        | Indicates project relevance/trend                            |

The final result is a ranked list of projects with an **AI Match Score**.

## 🛠️ Technologies Used
### Programming Language
* Python
### Machine Learning & NLP
* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity
* Natural Language Processing (NLP)
* NLTK
### Data Processing
* Pandas
* NumPy
### Frontend
* Streamlit
### Data Storage
* CSV
* JSON
### Export
* CSV
* Excel

## 📂 Project Structure

```text
AI_Final_Year_Project_Selector/
│
├── data/
│   ├── projects.csv
│   └── students.json
│
├── models/
│   ├── content_based.py
│   ├── nlp_processor.py
│   └── student_profile.py
│
├── utils/
│   └── data_loader.py
│
├── app.py
├── dashboard.py
├── recommendation_engine.py
├── test_profiles.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 📊 Project Dataset
The system contains a collection of **150 final-year project ideas** covering multiple technical domains.
Projects include domains such as:
* Artificial Intelligence
* Machine Learning
* Data Science
* Web Development
* Cybersecurity
* IoT
* Healthcare
* Agriculture
* Software Development
* Data Analytics
  
Each project contains information such as:
* Project Title
* Domain
* Branch
* Difficulty
* Technologies
* Skills
* Interests
* Trend Information
  
## 🤖 Recommendation Engine
The recommendation engine uses a combination of the following techniques:
### 1. Content-Based Filtering
Projects are recommended according to the similarity between the student's profile and project information.
### 2. NLP Processing
Text data such as skills, interests, project descriptions, and technologies are processed using NLP techniques.
### 3. TF-IDF
TF-IDF converts textual information into numerical vectors for similarity analysis.
### 4. Cosine Similarity
Cosine similarity measures the similarity between the student profile and project representations.
### 5. Multi-Factor Matching
The system combines multiple matching factors to generate the final project ranking.

## 📈 Example Recommendation
### AI Resume Screening System
**AI Match Score:** 34.1%
**Trend Score:** High
**Why Recommended:**
* Skills match
* Preferred domain matches
* Difficulty matches
* Profile similarity

## 🧪 Testing
The project includes a testing script:

```bash
python test_profiles.py
```

The testing process evaluates recommendations for different student profiles, such as:

* AI Student
* Web Development Student
* IoT Student
* Cybersecurity Student
* Healthcare Student

This helps verify that the recommendation engine produces different project rankings according to different student profiles.

---

## 📥 Export Results
Students can export their personalized recommendations in:
* CSV format
* Excel format
This allows recommended projects to be saved for future reference.

## 🎓 Use Case
This system can help:
* B.Tech students
* Final-year students
* Project coordinators
* Faculty members
* Students looking for suitable academic projects
Instead of manually searching through hundreds of project ideas, students can create a profile and receive personalized project recommendations.

## 🙏 Thank You
Thank you for visiting and exploring the **AI Final Year Project Selector**.


