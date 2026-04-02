"""
utils/feedback.py  –  AI-powered, field-aware resume feedback generator.
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


def generate_feedback(resume_text: str, skills_map: dict, ats_score: int) -> list:
    """
    Generate 4-6 actionable, field-specific feedback points for the resume.
    Returns list of strings.
    """
    try:
        client = _get_client()
        prompt = f"""You are a professional resume coach. Analyze this resume and give 5 specific, 
actionable feedback points to improve it.

Rules:
- Feedback must be relevant to THEIR FIELD (not generic tech advice for non-tech people).
- Each point should be a single clear sentence starting with an action word.
- Focus on: missing sections, weak phrasing, missing metrics, formatting issues, 
  missing contact info, skills gaps for their specific field.
- ATS Score so far: {ats_score}/100.

Return ONLY a JSON array of strings, no explanation:
["Feedback point 1", "Feedback point 2", "Feedback point 3", "Feedback point 4", "Feedback point 5"]

Resume:
\"\"\"
{resume_text[:3000]}
\"\"\"
"""
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = msg.content[0].text.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
        return json.loads(raw)
    except Exception:
        tips = []
        if ats_score < 50:
            tips.append("Add quantifiable achievements (e.g. 'Increased sales by 30%', 'Managed a team of 5')")
        if "@" not in resume_text:
            tips.append("Add your email address to the contact section")
        if "linkedin" not in resume_text.lower():
            tips.append("Add your LinkedIn profile URL to improve ATS compatibility")
        tips.append("Use stronger action verbs at the start of each bullet point")
        tips.append("Add a professional summary at the top of your resume")
        return tips
