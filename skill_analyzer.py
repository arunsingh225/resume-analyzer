"""
utils/skill_analyzer.py
Extract skills from resume text and identify gaps vs. job roles
"""

from utils.skills_data import SKILL_CATEGORIES, JOB_ROLES


def extract_skills(text: str) -> dict:
    """
    Return dict: {category_name: [matched_skills]}
    """
    text_lower = text.lower()
    found = {}
    for category, skills in SKILL_CATEGORIES.items():
        matched = [s for s in skills if s in text_lower]
        if matched:
            found[category] = matched
    return found


def get_all_skills_flat(text: str) -> list:
    """Return flat list of all matched skills."""
    skills_by_cat = extract_skills(text)
    return [s for skills in skills_by_cat.values() for s in skills]


def match_job_roles(text: str) -> list:
    """
    Score each job role 0–100 based on required + nice-to-have skills.
    Returns list of dicts sorted by match %.
    """
    user_skills = set(get_all_skills_flat(text))
    results = []

    for role, data in JOB_ROLES.items():
        required = data["required"]
        optional = data.get("good_to_have", [])

        req_matched = [s for s in required if s in user_skills]
        opt_matched = [s for s in optional if s in user_skills]
        req_missing = [s for s in required if s not in user_skills]

        # Weighted: required = 70%, optional = 30%
        req_pct = len(req_matched) / len(required) if required else 0
        opt_pct = len(opt_matched) / len(optional) if optional else 0
        match_pct = round((req_pct * 0.70 + opt_pct * 0.30) * 100)

        results.append({
            "role": role,
            "match_pct": match_pct,
            "required_matched": req_matched,
            "optional_matched": opt_matched,
            "missing_required": req_missing,
            "avg_salary": data["avg_salary"],
            "demand": data["demand"],
        })

    return sorted(results, key=lambda x: x["match_pct"], reverse=True)


def identify_missing_skills(text: str, top_roles: int = 3) -> dict:
    """
    For the top N matched roles, list which skills are missing.
    """
    matches = match_job_roles(text)[:top_roles]
    missing = {}
    for m in matches:
        if m["missing_required"]:
            missing[m["role"]] = m["missing_required"]
    return missing


def suggest_skills_to_learn(text: str) -> list:
    """
    Aggregate missing skills from top 5 roles, ranked by frequency.
    """
    from collections import Counter
    matches = match_job_roles(text)[:5]
    counter = Counter()
    for m in matches:
        for skill in m["missing_required"]:
            counter[skill] += 1
    return [{"skill": s, "frequency": f} for s, f in counter.most_common(10)]
