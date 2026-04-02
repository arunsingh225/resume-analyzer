"""
utils/roadmap.py  –  AI-powered, field-agnostic roadmap & course generator
Replaces hardcoded engineering roadmap with dynamic AI generation.
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


def generate_roadmap(resume_text: str) -> dict:
    """
    Generate a 3-phase skill improvement roadmap tailored to the person's
    actual field and current skill level.
    Returns dict with keys "Phase 1 – Quick Wins", "Phase 2 – Core Skills",
    "Phase 3 – Advanced" for compatibility with app.py rendering.
    """
    prompt = f"""You are a career coach. Analyze this resume and create a 3-phase skill improvement roadmap.

IMPORTANT:
- Detect the person's field FIRST.
- ALL suggested skills must be relevant to THEIR field.
- Do NOT suggest programming/tech skills for non-tech people.
- Phase 1 = quick wins (1-4 weeks), easy skills with immediate impact.
- Phase 2 = core skills (1-3 months), essential skills for their target roles.
- Phase 3 = advanced (3-6 months), skills that unlock senior/specialist roles.

Return ONLY valid JSON, no explanation:
{{
  "Phase 1 – Quick Wins": {{
    "duration": "1–4 weeks",
    "description": "Low-effort skills with immediate impact",
    "skills": ["skill1", "skill2", "skill3", "skill4"]
  }},
  "Phase 2 – Core Skills": {{
    "duration": "1–3 months",
    "description": "Core skills for your target roles",
    "skills": ["skill1", "skill2", "skill3", "skill4"]
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
        return {
            "Phase 1 – Quick Wins": {
                "duration": "1–4 weeks",
                "description": "Start with these high-impact skills",
                "skills": ["Communication", "Time Management"]
            },
            "Phase 2 – Core Skills": {
                "duration": "1–3 months",
                "description": "Build your core skill set",
                "skills": ["Domain Knowledge", "Industry Tools"]
            },
            "Phase 3 – Advanced": {
                "duration": "3–6 months",
                "description": "Advanced expertise for senior roles",
                "skills": ["Leadership", "Strategic Thinking"]
            }
        }


def get_course_recommendations(missing_skills: list) -> list:
    """
    Recommend real online courses for the missing skills.
    Returns list of course dicts with keys: skill, course, platform, duration, url.
    """
    if not missing_skills:
        return []

    skill_names = [s["skill"] if isinstance(s, dict) else s for s in missing_skills[:6]]

    prompt = f"""Recommend one real online course for each of these skills.
Only use real platforms: Coursera, Udemy, edX, LinkedIn Learning, Google, NPTEL, YouTube.
Only use real course URLs that actually exist.

Skills: {json.dumps(skill_names)}

Return ONLY valid JSON, no explanation:
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
        return []


def get_company_suggestions(resume_text: str) -> list:
    """
    Suggest real companies to apply to based on the person's field and skills.
    Returns list of company dicts — field-aware.
    """
    prompt = f"""You are a career advisor. Analyze this resume and suggest 6 real companies
where this person should apply based on their field, skills, and experience level.

IMPORTANT:
- Suggest companies relevant to THEIR ACTUAL FIELD.
- If they are in finance/accounting, suggest banks, CA firms, fintech companies.
- If they are in marketing, suggest agencies, brands with strong marketing teams.
- If they are in healthcare, suggest hospitals, pharma companies, healthtech startups.
- Include Indian companies if context suggests India, international if otherwise.
- Mix of startup, mid-size, and large companies.

Return ONLY valid JSON, no explanation:
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
        return []
