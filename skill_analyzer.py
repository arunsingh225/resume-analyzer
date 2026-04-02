import re
from collections import Counter

# -------------------------------
# FIELD DATABASE
# -------------------------------
FIELD_KEYWORDS = {
    "engineering": [
        "python", "java", "c++", "c", "javascript", "react", "node", "sql",
        "machine learning", "data science", "api", "django", "flask", "git",
        "html", "css", "mongodb", "mysql", "pandas", "numpy", "tensorflow",
        "scikit-learn", "power bi", "excel", "data analysis"
    ],
    "commerce": [
        "accounting", "tally", "gst", "taxation", "auditing", "bookkeeping",
        "financial reporting", "balance sheet", "ledger", "invoice", "payroll",
        "bank reconciliation", "cost accounting", "commerce", "finance", "excel"
    ],
    "management": [
        "sales", "marketing", "business development", "crm", "lead generation",
        "market research", "branding", "customer relationship", "negotiation",
        "strategy", "management", "operations", "communication", "advertising"
    ],
    "hr": [
        "recruitment", "talent acquisition", "onboarding", "payroll", "employee engagement",
        "performance management", "hr", "human resources", "training", "compliance"
    ],
    "design": [
        "photoshop", "illustrator", "figma", "ui", "ux", "wireframe", "prototype",
        "graphic design", "canva", "adobe xd", "design thinking"
    ],
    "general": []
}

SKILLS_DB = {
    "engineering": {
        "Programming Languages": ["python", "java", "c++", "c", "javascript", "sql"],
        "Web & App": ["html", "css", "react", "node", "flask", "django", "api"],
        "Data & AI": ["machine learning", "data science", "pandas", "numpy", "tensorflow", "scikit-learn"],
        "Tools": ["git", "github", "mongodb", "mysql", "power bi", "excel"]
    },
    "commerce": {
        "Accounting": ["accounting", "bookkeeping", "ledger", "balance sheet", "auditing"],
        "Tax & Finance": ["gst", "taxation", "finance", "financial reporting", "cost accounting"],
        "Tools": ["tally", "excel", "payroll", "bank reconciliation", "invoice"]
    },
    "management": {
        "Sales": ["sales", "lead generation", "negotiation", "business development"],
        "Marketing": ["marketing", "branding", "advertising", "market research"],
        "Business": ["strategy", "operations", "crm", "communication"]
    },
    "hr": {
        "HR Operations": ["recruitment", "talent acquisition", "onboarding", "payroll"],
        "People Management": ["employee engagement", "training", "performance management", "compliance"]
    },
    "design": {
        "Design Tools": ["figma", "photoshop", "illustrator", "canva", "adobe xd"],
        "Design Skills": ["ui", "ux", "wireframe", "prototype", "graphic design", "design thinking"]
    },
    "general": {
        "General Skills": ["communication", "excel", "management", "teamwork", "leadership"]
    }
}

ROLE_DB = {
    "engineering": [
        {
            "role": "Backend Developer",
            "required": ["python", "sql", "api", "flask"],
            "optional": ["django", "mongodb", "git"],
            "avg_salary": "₹5-12 LPA",
            "demand": "High"
        },
        {
            "role": "Frontend Developer",
            "required": ["html", "css", "javascript", "react"],
            "optional": ["git", "api"],
            "avg_salary": "₹4-10 LPA",
            "demand": "High"
        },
        {
            "role": "Data Analyst",
            "required": ["excel", "sql", "power bi", "data analysis"],
            "optional": ["python", "pandas"],
            "avg_salary": "₹4-9 LPA",
            "demand": "High"
        },
        {
            "role": "ML Engineer",
            "required": ["python", "machine learning", "pandas", "numpy"],
            "optional": ["tensorflow", "scikit-learn", "sql"],
            "avg_salary": "₹6-15 LPA",
            "demand": "Medium"
        },
        {
            "role": "Full Stack Developer",
            "required": ["html", "css", "javascript", "react", "python", "sql"],
            "optional": ["node", "mongodb", "git"],
            "avg_salary": "₹6-14 LPA",
            "demand": "High"
        }
    ],
    "commerce": [
        {
            "role": "Accountant",
            "required": ["accounting", "tally", "gst", "excel"],
            "optional": ["auditing", "taxation", "finance"],
            "avg_salary": "₹3-7 LPA",
            "demand": "High"
        },
        {
            "role": "Financial Analyst",
            "required": ["finance", "excel", "financial reporting"],
            "optional": ["accounting", "cost accounting"],
            "avg_salary": "₹4-10 LPA",
            "demand": "Medium"
        },
        {
            "role": "Auditor",
            "required": ["auditing", "accounting", "balance sheet"],
            "optional": ["gst", "taxation"],
            "avg_salary": "₹4-8 LPA",
            "demand": "Medium"
        }
    ],
    "management": [
        {
            "role": "Sales Executive",
            "required": ["sales", "communication", "negotiation"],
            "optional": ["crm", "lead generation"],
            "avg_salary": "₹3-8 LPA",
            "demand": "High"
        },
        {
            "role": "Marketing Executive",
            "required": ["marketing", "branding", "communication"],
            "optional": ["market research", "advertising"],
            "avg_salary": "₹3-8 LPA",
            "demand": "High"
        },
        {
            "role": "Business Development Executive",
            "required": ["business development", "lead generation", "communication"],
            "optional": ["crm", "strategy"],
            "avg_salary": "₹4-9 LPA",
            "demand": "High"
        }
    ],
    "hr": [
        {
            "role": "HR Executive",
            "required": ["recruitment", "onboarding", "communication"],
            "optional": ["payroll", "employee engagement"],
            "avg_salary": "₹3-7 LPA",
            "demand": "Medium"
        },
        {
            "role": "Talent Acquisition Specialist",
            "required": ["talent acquisition", "recruitment", "communication"],
            "optional": ["training", "compliance"],
            "avg_salary": "₹4-8 LPA",
            "demand": "Medium"
        }
    ],
    "design": [
        {
            "role": "UI/UX Designer",
            "required": ["figma", "ui", "ux", "wireframe"],
            "optional": ["prototype", "design thinking"],
            "avg_salary": "₹4-10 LPA",
            "demand": "Medium"
        },
        {
            "role": "Graphic Designer",
            "required": ["photoshop", "illustrator", "graphic design"],
            "optional": ["canva", "branding"],
            "avg_salary": "₹3-7 LPA",
            "demand": "Medium"
        }
    ],
    "general": [
        {
            "role": "Office Executive",
            "required": ["communication", "excel"],
            "optional": ["management", "leadership"],
            "avg_salary": "₹2-5 LPA",
            "demand": "Medium"
        }
    ]
}


# -------------------------------
# HELPERS
# -------------------------------
def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_resume_keywords(text):
    text = normalize_text(text)
    found = set()

    all_keywords = set()
    for field_data in SKILLS_DB.values():
        for skill_list in field_data.values():
            all_keywords.update(skill_list)

    for field_roles in ROLE_DB.values():
        for role in field_roles:
            all_keywords.update(role["required"])
            all_keywords.update(role["optional"])

    for kw in all_keywords:
        if kw in text:
            found.add(kw)

    return found


# -------------------------------
# FIELD DETECTION
# -------------------------------
def detect_field(resume_text):
    text = normalize_text(resume_text)
    scores = {}

    for field, keywords in FIELD_KEYWORDS.items():
        scores[field] = sum(1 for kw in keywords if kw in text)

    best_field = max(scores, key=scores.get)
    if scores[best_field] == 0:
        return "general"

    return best_field


# -------------------------------
# SKILL EXTRACTION
# -------------------------------
def extract_skills(resume_text, detected_field="general"):
    text = normalize_text(resume_text)

    if detected_field not in SKILLS_DB:
        detected_field = "general"

    categorized_skills = {}
    for category, skills in SKILLS_DB[detected_field].items():
        found = [skill for skill in skills if skill in text]
        if found:
            categorized_skills[category] = found

    return categorized_skills


# -------------------------------
# JOB MATCHING
# -------------------------------
def match_job_roles(resume_text, detected_field="general"):
    text = normalize_text(resume_text)
    resume_skills = extract_resume_keywords(text)

    if detected_field not in ROLE_DB:
        detected_field = "general"

    matches = []

    for role_data in ROLE_DB[detected_field]:
        required = set(role_data["required"])
        optional = set(role_data["optional"])

        required_matched = sorted(list(required.intersection(resume_skills)))
        missing_required = sorted(list(required - resume_skills))
        optional_matched = sorted(list(optional.intersection(resume_skills)))

        if len(required) > 0:
            required_score = (len(required_matched) / len(required)) * 70
        else:
            required_score = 0

        if len(optional) > 0:
            optional_score = (len(optional_matched) / len(optional)) * 30
        else:
            optional_score = 0

        match_pct = round(required_score + optional_score)

        matches.append({
            "role": role_data["role"],
            "match_pct": match_pct,
            "avg_salary": role_data["avg_salary"],
            "demand": role_data["demand"],
            "required_matched": required_matched,
            "missing_required": missing_required,
            "optional_matched": optional_matched
        })

    matches = sorted(matches, key=lambda x: x["match_pct"], reverse=True)
    return matches


# -------------------------------
# MISSING / PRIORITY SKILLS
# -------------------------------
def suggest_skills_to_learn(resume_text, detected_field="general", job_matches=None):
    text = normalize_text(resume_text)
    resume_skills = extract_resume_keywords(text)

    if detected_field not in ROLE_DB:
        detected_field = "general"

    if job_matches is None:
        job_matches = match_job_roles(resume_text, detected_field)

    top_roles = job_matches[:5]
    counter = Counter()

    for role in top_roles:
        for skill in role.get("missing_required", []):
            counter[skill] += 1

    suggestions = []
    for skill, freq in counter.most_common():
        suggestions.append({
            "skill": skill,
            "frequency": freq
        })

    return suggestions
