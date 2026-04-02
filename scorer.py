"""
utils/scorer.py  –  AI-powered, field-neutral ATS resume scorer.
Scores based on resume QUALITY (formatting, structure, completeness, impact)
NOT on tech-specific keywords. Works for any field.
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


def score_resume(resume_text: str) -> dict:
    """
    Score a resume on ATS-relevant dimensions.
    Field-neutral: scores structure, clarity, impact — NOT domain keywords.
    Returns dict matching app.py's expected structure.
    """
    word_count = len(resume_text.split())
    char_count = len(resume_text)

    prompt = f"""You are an ATS (Applicant Tracking System) expert. Score this resume on 5 dimensions.

Score STRICTLY based on resume quality — NOT on which field or technology is used.
Any field (accounting, medicine, marketing, engineering, law) can score 100/100.

Scoring dimensions:
1. Formatting & contact info (max 20): Has name, email, phone, LinkedIn/portfolio? Clean structure?
2. Technical keywords (max 20): Has field-relevant technical terms and domain keywords for THEIR field?
3. Quantifiable metrics (max 20): Uses numbers, percentages, measurable achievements?
4. Action verbs (max 20): Uses strong action verbs (managed, led, developed, achieved, etc.)?
5. Section completeness (max 20): Has all key sections (summary/objective, experience, education, skills, projects/achievements)?

For each section, list what you FOUND in the resume (specific words/phrases, up to 6 examples).

Return ONLY valid JSON, no explanation:
{{
  "breakdown": {{
    "formatting": {{
      "label": "Formatting & contact info",
      "score": 14,
      "max": 20,
      "found": ["email found", "phone found", "LinkedIn found"]
    }},
    "keywords": {{
      "label": "Technical keywords",
      "score": 16,
      "max": 20,
      "found": ["keyword1", "keyword2", "keyword3"]
    }},
    "metrics": {{
      "label": "Quantifiable metrics",
      "score": 10,
      "max": 20,
      "found": ["30% increase", "team of 5"]
    }},
    "action_verbs": {{
      "label": "Action verbs",
      "score": 12,
      "max": 20,
      "found": ["managed", "developed", "led"]
    }},
    "sections": {{
      "label": "Section completeness",
      "score": 15,
      "max": 20,
      "found": ["experience", "education", "skills", "projects"]
    }}
  }}
}}

Resume:
\"\"\"
{resume_text[:4000]}
\"\"\"
"""
    try:
        raw = _ask_claude(prompt, max_tokens=1200)
        data = _parse_json(raw)
        breakdown = data["breakdown"]

        total = sum(v["score"] for v in breakdown.values())
        if total >= 80:
            grade = "Excellent"
        elif total >= 65:
            grade = "Good"
        elif total >= 50:
            grade = "Fair"
        else:
            grade = "Needs Work"

        return {
            "total": total,
            "grade": grade,
            "breakdown": breakdown,
            "word_count": word_count,
            "char_count": char_count,
        }

    except Exception:
        # Fallback: simple rule-based scoring so app doesn't crash
        return _fallback_score(resume_text, word_count, char_count)


def _fallback_score(text: str, word_count: int, char_count: int) -> dict:
    """Simple rule-based fallback if AI call fails."""
    text_lower = text.lower()

    has_email = "@" in text
    has_phone = any(c.isdigit() for c in text)
    has_linkedin = "linkedin" in text_lower
    fmt_score = (8 if has_email else 0) + (6 if has_phone else 0) + (6 if has_linkedin else 0)

    sections = ["experience", "education", "skills", "projects", "summary", "objective", "achievements"]
    found_sections = [s for s in sections if s in text_lower]
    sec_score = min(20, len(found_sections) * 4)

    numbers = re.findall(r'\d+%|\d+ years|\d+\+', text)
    metric_score = min(20, len(numbers) * 4)

    action_words = ["managed", "led", "developed", "built", "designed", "achieved",
                    "improved", "created", "implemented", "launched", "increased",
                    "reduced", "coordinated", "analyzed", "delivered"]
    found_verbs = [w for w in action_words if w in text_lower]
    verb_score = min(20, len(found_verbs) * 4)

    keyword_score = 12  # neutral default

    total = fmt_score + sec_score + metric_score + verb_score + keyword_score
    grade = "Good" if total >= 65 else "Fair" if total >= 50 else "Needs Work"

    return {
        "total": total,
        "grade": grade,
        "breakdown": {
            "formatting": {"label": "Formatting & contact info", "score": fmt_score, "max": 20,
                           "found": (["email"] if has_email else []) + (["phone"] if has_phone else []) + (["linkedin"] if has_linkedin else [])},
            "keywords":   {"label": "Technical keywords", "score": keyword_score, "max": 20, "found": []},
            "metrics":    {"label": "Quantifiable metrics", "score": metric_score, "max": 20, "found": numbers[:6]},
            "action_verbs": {"label": "Action verbs", "score": verb_score, "max": 20, "found": found_verbs[:6]},
            "sections":   {"label": "Section completeness", "score": sec_score, "max": 20, "found": found_sections},
        },
        "word_count": word_count,
        "char_count": char_count,
    }
