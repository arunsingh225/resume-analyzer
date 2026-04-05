import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9,+#/.\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_processed_jobs(file_path="processed_jobs.csv"):
    df = pd.read_csv(file_path)
    df = df.fillna("")
    return df


def build_job_text(row):
    parts = [
        row.get("job_title", ""),
        row.get("role", ""),
        row.get("skills", ""),
        row.get("job_description", ""),
        row.get("qualifications", ""),
        row.get("responsibilities", ""),
    ]
    return " ".join([str(p) for p in parts])


def match_resume_to_jobs(resume_text, jobs_df, top_n=10):
    resume_text = clean_text(resume_text)

    jobs_df = jobs_df.copy()
    jobs_df["combined_text"] = jobs_df.apply(build_job_text, axis=1)
    jobs_df["combined_text"] = jobs_df["combined_text"].apply(clean_text)

    corpus = jobs_df["combined_text"].tolist() + [resume_text]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(corpus)

    resume_vector = vectors[-1]
    job_vectors = vectors[:-1]

    similarities = cosine_similarity(resume_vector, job_vectors)[0]
    jobs_df["match_score"] = similarities

    top_matches = jobs_df.sort_values("match_score", ascending=False).head(top_n).copy()
    top_matches["match_percent"] = (top_matches["match_score"] * 100).round(2)

    return top_matches


def extract_resume_skills(resume_text, skills_master=None):
    resume_text = clean_text(resume_text)

    if skills_master is None:
        skills_master = [
            "python", "sql", "excel", "advanced excel", "power bi", "tableau",
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "html", "css", "javascript", "react", "node.js", "django", "flask",
            "accounting", "tally", "gst", "ledger", "bookkeeping", "billing",
            "erp", "bank reconciliation", "recruitment", "onboarding", "payroll",
            "sales", "crm", "lead generation", "marketing", "seo", "social media"
        ]

    found = []
    for skill in skills_master:
        pattern = rf'(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])'
        if re.search(pattern, resume_text):
            found.append(skill)

    return sorted(list(set(found)))


def get_missing_skills_from_top_jobs(resume_text, top_matches, top_k=10):
    resume_skills = set(extract_resume_skills(resume_text))
    job_skill_counter = {}

    for _, row in top_matches.iterrows():
        skills_text = str(row.get("skills", ""))
        job_skills = [s.strip().lower() for s in skills_text.split(",") if s.strip()]

        for skill in job_skills:
            if skill not in resume_skills:
                job_skill_counter[skill] = job_skill_counter.get(skill, 0) + 1

    sorted_missing = sorted(job_skill_counter.items(), key=lambda x: x[1], reverse=True)
    return [{"skill": skill, "frequency": freq} for skill, freq in sorted_missing[:top_k]]


def get_top_role_summary(top_matches, top_n=5):
    role_scores = {}

    for _, row in top_matches.head(top_n).iterrows():
        role = row.get("role", "unknown")
        score = float(row.get("match_percent", 0))
        role_scores[role] = max(role_scores.get(role, 0), score)

    result = [{"role": role, "match_percent": round(score, 2)} for role, score in role_scores.items()]
    result = sorted(result, key=lambda x: x["match_percent"], reverse=True)
    return result


def calculate_confidence(top_matches):
    if top_matches.empty:
        return {"label": "Low", "score": 0}

    best_score = float(top_matches.iloc[0]["match_percent"])

    if best_score >= 75:
        return {"label": "High", "score": round(best_score, 2)}
    elif best_score >= 45:
        return {"label": "Medium", "score": round(best_score, 2)}
    else:
        return {"label": "Low", "score": round(best_score, 2)}
   
