"""
utils/skill_analyzer.py  –  AI-powered, field-agnostic skill extraction
Replaces the old hardcoded SKILL_CATEGORIES / JOB_ROLES approach.
Requires:  pip install anthropic
Set env var ANTHROPIC_API_KEY in your Streamlit secrets or .env file.
"""

import json
import os
import re
from anthropic import Anthropic

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY") or st_secret()
        _client = Anthropic(api_key=api_key)
    return _client

def st_secret():
    """Try to get key from Streamlit secrets."""
    try:
        import streamlit as st
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        return None


def _ask_claude(prompt: str, max_tokens: int = 1500) -> str:
    """Send a prompt to Claude and return the text response."""
    client = _get_client()
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def _parse_json(text: str):
    """Extract JSON from Claude's response robustly."""
    # Strip markdown code fences if present
    text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
    return json.loads(text)


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API — same function signatures as before so app.py needs NO changes
# ─────────────────────────────────────────────────────────────────────────────

def extract_skills(resume_text: str) -> dict:
    """
    Dynamically detect the person's field and extract skills grouped by category.
    Returns dict: { "Category Name": ["skill1", "skill2", ...], ... }
    Works for ANY field: engineering, finance, medicine, law, marketing, arts, etc.
    """
    prompt = f"""You are a professional resume parser. Analyze the resume below.

1. Detect the person's professional field (e.g. Software Engineering, Accounting, Marketing, Medicine, Law, Sales, Design, etc.)
2. Extract ALL skills mentioned or strongly implied in the resume.
3. Group them into relevant categories FOR THAT FIELD.
   - For a software engineer: Programming Languages, Frameworks, Databases, Cloud, Tools, etc.
   - For an accountant: Accounting Software, Financial Skills, Tax Knowledge, Compliance, etc.
   - For a marketer: Digital Marketing, SEO/SEM, Analytics Tools, CRM, Content, etc.
   - For a doctor: Clinical Skills, Medical Specialties, Equipment, Research, etc.
   - Use whatever categories make sense for their actual field.

Return ONLY valid JSON in this exact format, no explanation:
{{
  "field": "detected field name",
  "skills": {{
    "Category Name": ["skill1", "skill2"],
    "Another Category": ["skill3", "skill4"]
  }}
}}

Resume:
\"\"\"
{resume_text[:4000]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt)
        data = _parse_json(raw)
        return data.get("skills", {})
    except Exception as e:
        # Fallback: return a minimal result so app doesn't crash
        return {"General Skills": ["Communication", "Teamwork"]}


def detect_field(resume_text: str) -> str:
    """Detect the person's professional field from their resume."""
    prompt = f"""Read this resume and return ONLY the professional field in 2-4 words.
Examples: "Software Engineering", "Financial Accounting", "Digital Marketing", "Clinical Medicine", "Graphic Design", "Civil Engineering", "Human Resources", "Sales & Business Development"

Resume:
\"\"\"
{resume_text[:2000]}
\"\"\"

Return ONLY the field name, nothing else."""
    try:
        return _ask_claude(prompt, max_tokens=20)
    except Exception:
        return "Professional"


def match_job_roles(resume_text: str) -> list:
    """
    Match resume to relevant job roles IN THE PERSON'S FIELD.
    Returns list of role dicts sorted by match %, same structure as before.
    Works for any field — not just tech.
    """
    prompt = f"""You are an expert career counselor. Analyze this resume.

1. Identify the person's professional field.
2. List the 5 most relevant job roles for this person IN THEIR FIELD.
   - If they are an accountant, suggest accounting/finance roles (not software roles).
   - If they are a nurse, suggest healthcare roles.
   - If they are a marketer, suggest marketing/growth roles.
   - Match to their ACTUAL background, not generic tech roles.

For each role provide:
- Role name
- Match percentage (0-100) based on their skills and experience
- Required skills for this role (list of 6-8 skills)
- Which required skills they already have (from the resume)
- Which required skills they are missing
- Nice-to-have skills they already have
- Average salary range (in INR per annum if Indian context, USD if international)
- Market demand: High / Medium / Low

Return ONLY valid JSON, no explanation:
[
  {{
    "role": "Role Name",
    "match_pct": 75,
    "required_matched": ["skill1", "skill2"],
    "missing_required": ["skill3"],
    "optional_matched": ["skill4"],
    "avg_salary": "₹6-10 LPA",
    "demand": "High"
  }}
]

Resume:
\"\"\"
{resume_text[:4000]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt, max_tokens=2000)
        roles = _parse_json(raw)
        # Sort by match_pct descending
        return sorted(roles, key=lambda x: x.get("match_pct", 0), reverse=True)
    except Exception:
        return [{
            "role": "Professional",
            "match_pct": 50,
            "required_matched": [],
            "missing_required": [],
            "optional_matched": [],
            "avg_salary": "Varies",
            "demand": "Medium"
        }]


def suggest_skills_to_learn(resume_text: str) -> list:
    """
    Suggest missing skills to learn, relevant to the person's actual field.
    Returns list of {"skill": str, "frequency": int} sorted by priority.
    """
    prompt = f"""You are a career advisor. Analyze this resume.

Identify the top 8 skills this person should learn to advance IN THEIR SPECIFIC FIELD.
- Base this on their current skills, experience level, and field.
- Do NOT suggest generic tech skills if they are not in tech.
- Prioritize skills that appear across multiple relevant job roles.
- Assign a frequency score (1-5) indicating how critical the skill is.

Return ONLY valid JSON, no explanation:
[
  {{"skill": "Skill Name", "frequency": 4}},
  {{"skill": "Another Skill", "frequency": 3}}
]

Resume:
\"\"\"
{resume_text[:3000]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt, max_tokens=800)
        return _parse_json(raw)
    except Exception:
        return []


def get_all_skills_flat(resume_text: str) -> list:
    """Return flat list of all matched skills."""
    skills_by_cat = extract_skills(resume_text)
    return [s for skills in skills_by_cat.values() for s in skills]


def identify_missing_skills(resume_text: str, top_roles: int = 3) -> dict:
    """For the top N matched roles, list which skills are missing."""
    matches = match_job_roles(resume_text)[:top_roles]
    missing = {}
    for m in matches:
        if m.get("missing_required"):
            missing[m["role"]] = m["missing_required"]
    return missing
