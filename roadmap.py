"""
utils/roadmap.py  –  AI-powered, field-aware roadmap, course, and company generator.
Works with dynamic detected fields from app.py.
"""

import json
import os
import re
from anthropic import Anthropic

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY") or _st_secret()
        _client = Anthropic(api_key=api_key)
    return _client

def _st_secret():
    try:
        import streamlit as st
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None

def _ask_claude(prompt: str, max_tokens: int = 1500) -> str:
    client = _get_client()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()

def _parse_json(text: str):
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return json.loads(text)


def generate_roadmap(resume_text: str, detected_field: str = "general", missing=None) -> dict:
    """
    Generate a 3-phase skill improvement roadmap tailored to field and missing skills.
    Compatible with app.py.
    """
    missing_skills = []
    if missing:
        for item in missing[:8]:
            if isinstance(item, dict) and "skill" in item:
                missing_skills.append(item["skill"])
            elif isinstance(item, str):
                missing_skills.append(item)

    prompt = f"""You are a career coach. Analyze this resume and create a 3-phase skill improvement roadmap.

IMPORTANT:
- Detected field: {detected_field}
- ALL suggested skills must be relevant to THIS field.
- Do NOT suggest programming/tech skills for non-tech people unless clearly relevant.
- Use missing skills when useful: {json.dumps(missing_skills)}
- Phase 1 = quick wins (1-4 weeks), easy skills with immediate impact.
- Phase 2 = core skills (1-3 months), essential skills for target roles.
- Phase 3 = advanced (3-6 months), skills that unlock specialist/senior roles.

Return ONLY valid JSON, no explanation:
{{
  "Phase 1 – Quick Wins": {{
    "duration": "1–4 weeks",
    "description": "Low-effort skills with immediate impact",
    "skills": ["skill1", "skill2", "skill3"]
  }},
  "Phase 2 – Core Skills": {{
    "duration": "1–3 months",
    "description": "Core skills for your target roles",
    "skills": ["skill1", "skill2", "skill3"]
  }},
  "Phase 3 – Advanced": {{
    "duration": "3–6 months",
    "description": "Advanced skills that unlock senior roles",
    "skills": ["skill1", "skill2", "skill3"]
  }}
}}

Resume:
\"\"\"
{resume_text[:3500]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt, max_tokens=1000)
        return _parse_json(raw)
    except Exception:
        return _fallback_roadmap(detected_field, missing_skills)


def get_course_recommendations(missing_skills: list, detected_field: str = "general") -> list:
    """
    Recommend online courses for missing skills.
    Compatible with app.py.
    """
    if not missing_skills:
        return []

    skill_names = []
    for s in missing_skills[:6]:
        if isinstance(s, dict) and "skill" in s:
            skill_names.append(s["skill"])
        elif isinstance(s, str):
            skill_names.append(s)

    if not skill_names:
        return []

    prompt = f"""Recommend one real online course for each of these skills.

Detected field: {detected_field}

Rules:
- Use only relevant courses for the detected field.
- Prefer real platforms: Coursera, Udemy, edX, LinkedIn Learning, Google, NPTEL, YouTube.
- Return only valid JSON.

Skills: {json.dumps(skill_names)}

Return ONLY valid JSON:
[
  {{
    "skill": "Skill Name",
    "course": "Course Title",
    "platform": "Platform Name",
    "duration": "X hours / X weeks",
    "url": "https://real-url.com"
  }}
]
"""
    try:
        raw = _ask_claude(prompt, max_tokens=1200)
        return _parse_json(raw)
    except Exception:
        return _fallback_courses(skill_names, detected_field)


def get_company_suggestions(resume_text: str, detected_field: str = "general", job_matches=None) -> list:
    """
    Suggest companies based on detected field and top job matches.
    Compatible with app.py.
    """
    top_roles = []
    if job_matches:
        for role in job_matches[:5]:
            if isinstance(role, dict) and "role" in role:
                top_roles.append(role["role"])

    prompt = f"""You are a career advisor. Analyze this resume and suggest 6 real companies
where this person should apply based on their field, skills, and top matched roles.

Detected field: {detected_field}
Top matched roles: {json.dumps(top_roles)}

IMPORTANT:
- Suggest companies relevant to THIS field.
- If they are in finance/accounting, suggest banks, CA firms, fintech companies.
- If they are in marketing, suggest agencies, consumer brands, startups.
- If they are in HR, suggest companies with strong HR/recruitment teams.
- If they are in design, suggest product companies, agencies, creative firms.
- If they are in engineering, suggest tech companies, startups, IT firms.
- Include Indian companies if context suggests India.
- Mix startup, mid-size, and large companies.

Return ONLY valid JSON:
[
  {{
    "name": "Company Name",
    "type": "MNC / Startup / SME / Firm",
    "size": "50-200",
    "match_pct": 78,
    "matched_role": "Role they should apply for",
    "url": "https://company-careers-page.com"
  }}
]

Resume:
\"\"\"
{resume_text[:3000]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt, max_tokens=1200)
        return _parse_json(raw)
    except Exception:
        return _fallback_companies(detected_field, top_roles)


def _fallback_roadmap(detected_field: str, missing_skills: list) -> dict:
    defaults = {
        "engineering": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Start with practical tools and fundamentals",
                "skills": missing_skills[:3] if missing_skills else ["SQL", "Git", "Problem Solving"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Build strong technical depth",
                "skills": ["Python", "APIs", "Data Structures"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Move toward advanced roles",
                "skills": ["System Design", "Cloud", "Machine Learning"]
            }
        },
        "commerce": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Improve job-ready business tools",
                "skills": missing_skills[:3] if missing_skills else ["Excel", "Tally", "GST Basics"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Strengthen accounting and finance fundamentals",
                "skills": ["Accounting", "Financial Reporting", "Taxation"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Move toward analyst and specialist roles",
                "skills": ["Financial Analysis", "Auditing", "Forecasting"]
            }
        },
        "management": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Build immediate workplace impact",
                "skills": missing_skills[:3] if missing_skills else ["Communication", "Excel", "CRM Basics"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Develop strong business execution skills",
                "skills": ["Sales", "Marketing", "Lead Generation"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Prepare for growth-focused roles",
                "skills": ["Strategy", "Negotiation", "Business Analytics"]
            }
        },
        "hr": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Build essential people-ops basics",
                "skills": missing_skills[:3] if missing_skills else ["Recruitment", "Communication", "Onboarding"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Strengthen core HR skills",
                "skills": ["Talent Acquisition", "Payroll", "Compliance"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Prepare for specialist HR roles",
                "skills": ["Performance Management", "HR Analytics", "Employee Engagement"]
            }
        },
        "design": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Improve design workflow quickly",
                "skills": missing_skills[:3] if missing_skills else ["Figma", "Canva", "Design Basics"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Build strong design foundations",
                "skills": ["UI Design", "UX Research", "Wireframing"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Move toward high-value design roles",
                "skills": ["Prototyping", "Design Systems", "User Research"]
            }
        },
        "general": {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Start with foundational workplace skills",
                "skills": missing_skills[:3] if missing_skills else ["Communication", "Excel", "Time Management"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Build role-relevant capabilities",
                "skills": ["Domain Knowledge", "Professional Writing", "Problem Solving"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Prepare for better roles and responsibilities",
                "skills": ["Leadership", "Planning", "Strategic Thinking"]
            }
        }
    }
    return defaults.get(detected_field, defaults["general"])


def _fallback_courses(skill_names: list, detected_field: str) -> list:
    base_url = {
        "engineering": "https://www.coursera.org",
        "commerce": "https://www.udemy.com",
        "management": "https://www.coursera.org",
        "hr": "https://www.linkedin.com/learning",
        "design": "https://www.youtube.com",
        "general": "https://www.coursera.org"
    }.get(detected_field, "https://www.coursera.org")

    results = []
    for skill in skill_names[:6]:
        results.append({
            "skill": skill,
            "course": f"Introduction to {skill.title()}",
            "platform": "Recommended Platform",
            "duration": "4-8 weeks",
            "url": base_url
        })
    return results


def _fallback_companies(detected_field: str, top_roles: list) -> list:
    company_map = {
        "engineering": [
            ("TCS", "MNC", "10000+", "Software Engineer"),
            ("Infosys", "MNC", "10000+", "Developer"),
            ("Wipro", "MNC", "10000+", "Backend Developer"),
            ("HCLTech", "MNC", "10000+", "Analyst"),
            ("Zoho", "Product Company", "1000-5000", "Software Developer"),
            ("Accenture", "MNC", "10000+", "Associate Engineer"),
        ],
        "commerce": [
            ("HDFC Bank", "MNC", "10000+", "Accountant"),
            ("ICICI Bank", "MNC", "10000+", "Finance Associate"),
            ("Deloitte", "Firm", "10000+", "Analyst"),
            ("KPMG", "Firm", "10000+", "Audit Associate"),
            ("EY", "Firm", "10000+", "Finance Analyst"),
            ("Grant Thornton", "Firm", "1000-5000", "Account Executive"),
        ],
        "management": [
            ("BYJU'S", "Startup", "1000-5000", "Business Development Executive"),
            ("Hindustan Unilever", "MNC", "10000+", "Sales Executive"),
            ("Zomato", "Startup", "5000-10000", "Growth Associate"),
            ("Swiggy", "Startup", "5000-10000", "Operations Executive"),
            ("Flipkart", "MNC", "10000+", "Category Executive"),
            ("Reliance Retail", "Enterprise", "10000+", "Sales Associate"),
        ],
        "hr": [
            ("TeamLease", "Firm", "5000-10000", "HR Executive"),
            ("Randstad", "Firm", "10000+", "Recruiter"),
            ("Infosys", "MNC", "10000+", "HR Associate"),
            ("Wipro", "MNC", "10000+", "Talent Acquisition Specialist"),
            ("Accenture", "MNC", "10000+", "HR Operations"),
            ("TCS", "MNC", "10000+", "HR Executive"),
        ],
        "design": [
            ("CRED", "Startup", "1000-5000", "UI/UX Designer"),
            ("Zerodha", "Product Company", "1000-5000", "Product Designer"),
            ("PhonePe", "Startup", "5000-10000", "Visual Designer"),
            ("Swiggy", "Startup", "5000-10000", "Graphic Designer"),
            ("Adobe", "MNC", "10000+", "Designer"),
            ("Canva", "Product Company", "10000+", "Design Associate"),
        ],
        "general": [
            ("Infosys", "MNC", "10000+", "Associate"),
            ("Wipro", "MNC", "10000+", "Executive"),
            ("TCS", "MNC", "10000+", "Analyst"),
            ("Accenture", "MNC", "10000+", "Associate"),
            ("Concentrix", "Enterprise", "10000+", "Operations Executive"),
            ("Teleperformance", "Enterprise", "10000+", "Support Executive"),
        ]
    }

    fallback = company_map.get(detected_field, company_map["general"])
    matched_role = top_roles[0] if top_roles else fallback[0][3]

    results = []
    for i, (name, ctype, size, role) in enumerate(fallback):
        results.append({
            "name": name,
            "type": ctype,
            "size": size,
            "match_pct": max(55, 82 - i * 4),
            "matched_role": matched_role if i < 3 else role,
            "url": "https://www.linkedin.com/jobs/"
        })
    return results
