"""
utils/roadmap.py
Generate skill improvement roadmap + course recommendations
"""

from utils.skills_data import COURSES
from utils.skill_analyzer import suggest_skills_to_learn, match_job_roles


def get_course_recommendations(missing_skills: list) -> list:
    """Map missing skills to course recommendations."""
    recommendations = []
    seen_titles = set()
    for skill_info in missing_skills:
        skill = skill_info["skill"].lower()
        # Try exact match first, then partial
        courses = COURSES.get(skill)
        if not courses:
            for key in COURSES:
                if key in skill or skill in key:
                    courses = COURSES[key]
                    break
        if not courses:
            courses = COURSES["default"]

        for course in courses:
            if course["title"] not in seen_titles:
                recommendations.append({
                    "skill": skill,
                    "course": course["title"],
                    "platform": course["platform"],
                    "level": course["level"],
                    "url": course["url"]
                })
                seen_titles.add(course["title"])

    return recommendations[:12]  # Cap at 12


def generate_roadmap(text: str) -> dict:
    """
    Generate a 3-phase roadmap:
    Phase 1: Quick wins (easy skills, 1-2 weeks each)
    Phase 2: Core skills (medium, 1 month each)
    Phase 3: Advanced (2+ months each)
    """
    missing = suggest_skills_to_learn(text)

    # Simple heuristic: tag each skill with effort
    easy_skills = ["git", "sql", "html", "css", "bash", "excel", "tableau",
                   "rest api", "postman", "linux", "agile", "scrum"]
    hard_skills = ["kubernetes", "terraform", "deep learning", "nlp",
                   "machine learning", "kubernetes", "spark", "distributed systems"]

    phase1, phase2, phase3 = [], [], []

    for item in missing:
        skill = item["skill"]
        if skill in easy_skills:
            phase1.append(skill)
        elif skill in hard_skills:
            phase3.append(skill)
        else:
            phase2.append(skill)

    # Fill phases if empty
    if not phase1 and missing:
        phase1 = [missing[0]["skill"]] if missing else []
    if not phase2 and len(missing) > 1:
        phase2 = [missing[1]["skill"]] if len(missing) > 1 else []

    return {
        "Phase 1 – Quick Wins": {
            "duration": "1–4 weeks",
            "description": "Low-effort skills with immediate impact",
            "skills": phase1[:4] or ["Polish LinkedIn profile", "Update GitHub", "SQL basics"]
        },
        "Phase 2 – Core Skills": {
            "duration": "1–3 months",
            "description": "Core technical skills for your target roles",
            "skills": phase2[:4] or ["Build 2 portfolio projects", "Contribute to open source"]
        },
        "Phase 3 – Advanced": {
            "duration": "3–6 months",
            "description": "Advanced skills that unlock senior roles",
            "skills": phase3[:4] or ["System design", "Cloud certification", "Leadership experience"]
        }
    }


def get_company_suggestions(text: str) -> list:
    """Suggest companies based on top matched roles."""
    from utils.skills_data import COMPANIES
    roles = match_job_roles(text)[:3]
    suggestions = []
    seen = set()

    role_to_domain = {
        "Data Scientist": "Data Science / AI",
        "ML Engineer": "Data Science / AI",
        "AI/LLM Engineer": "Data Science / AI",
        "Full Stack Developer": "Full Stack / Web",
        "Frontend Developer": "Full Stack / Web",
        "Backend Developer": "Full Stack / Web",
        "DevOps Engineer": "Cloud / DevOps",
        "Cloud Architect": "Cloud / DevOps",
        "Data Analyst": "Data Science / AI",
        "Mobile Developer": "General Tech",
    }

    for role_info in roles:
        domain = role_to_domain.get(role_info["role"], "General Tech")
        companies = COMPANIES.get(domain, COMPANIES["General Tech"])
        for company in companies[:3]:
            if company["name"] not in seen:
                suggestions.append({
                    **company,
                    "matched_role": role_info["role"],
                    "match_pct": role_info["match_pct"]
                })
                seen.add(company["name"])

    # Always add some big tech
    for company in COMPANIES["General Tech"]:
        if company["name"] not in seen and len(suggestions) < 10:
            suggestions.append({**company, "matched_role": "General", "match_pct": 50})
            seen.add(company["name"])

    return suggestions[:10]
