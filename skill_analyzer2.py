# utils/skill_analyzer.py

import re
from collections import Counter

# ---------------- FIELD KEYWORDS ----------------
FIELD_KEYWORDS = {
    "engineering": ["python", "java", "c++", "sql", "react", "ml", "api"],
    "commerce": ["accounting", "tally", "gst", "finance", "audit"],
    "management": ["sales", "marketing", "business", "crm"],
    "general": []
}

# ---------------- SKILLS DB ----------------
SKILLS_DB = {
    "engineering": ["python", "java", "sql", "react", "api", "ml"],
    "commerce": ["accounting", "tally", "gst", "excel"],
    "management": ["sales", "marketing", "crm", "communication"],
    "general": ["communication", "excel"]
}

# ---------------- ROLES ----------------
ROLE_DB = {
    "engineering": [
        {"role": "Backend Developer", "skills": ["python", "sql", "api"]},
        {"role": "Frontend Developer", "skills": ["html", "css", "react"]},
    ],
    "commerce": [
        {"role": "Accountant", "skills": ["accounting", "tally", "gst"]},
        {"role": "Financial Analyst", "skills": ["finance", "excel"]},
    ],
    "management": [
        {"role": "Sales Executive", "skills": ["sales", "communication"]},
        {"role": "Marketing Executive", "skills": ["marketing", "branding"]},
    ],
    "general": [
        {"role": "Office Executive", "skills": ["communication", "excel"]}
    ]
}


# ---------------- FIELD DETECTION ----------------
def detect_field(text):
    text = text.lower()
    scores = {}

    for field, keywords in FIELD_KEYWORDS.items():
        scores[field] = sum(1 for k in keywords if k in text)

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text, field="general"):
    text = text.lower()
    skills = SKILLS_DB.get(field, SKILLS_DB["general"])

    found = [s for s in skills if s in text]

    return {"Skills": found}


# ---------------- JOB MATCHING ----------------
def match_job_roles(text, field="general"):
    text = text.lower()
    roles = ROLE_DB.get(field, ROLE_DB["general"])

    results = []

    for role in roles:
        match = sum(1 for s in role["skills"] if s in text)
        pct = int((match / len(role["skills"])) * 100)

        results.append({
            "role": role["role"],
            "match_pct": pct,
            "avg_salary": "₹3-10 LPA",
            "demand": "High",
            "required_matched": [s for s in role["skills"] if s in text],
            "missing_required": [s for s in role["skills"] if s not in text],
            "optional_matched": []
        })

    return sorted(results, key=lambda x: x["match_pct"], reverse=True)


# ---------------- MISSING SKILLS ----------------
def suggest_skills_to_learn(text, field="general", job_matches=None):
    text = text.lower()

    skills = SKILLS_DB.get(field, SKILLS_DB["general"])
    missing = [s for s in skills if s not in text]

    return [{"skill": s, "frequency": 1} for s in missing]
