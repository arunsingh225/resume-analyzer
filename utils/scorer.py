"""
utils/scorer.py
ATS resume scoring engine — returns a score 0–100 and breakdown
"""

import re
from .skills_data import ATS_KEYWORDS, SKILL_CATEGORIES


def score_resume(text: str) -> dict:
    """
    Score a resume on 5 dimensions:
    1. Section completeness   (20 pts)
    2. Action verbs           (20 pts)
    3. Quantifiable metrics   (20 pts)
    4. Keyword density        (20 pts)
    5. Formatting hints       (20 pts)
    Returns dict with total score and breakdown.
    """
    text_lower = text.lower()
    results = {}

    # 1. Section completeness ────────────────────────────────────────────────
    found_sections = [s for s in ATS_KEYWORDS["sections"] if s in text_lower]
    section_score = min(20, int(len(found_sections) / len(ATS_KEYWORDS["sections"]) * 20))
    results["sections"] = {
        "score": section_score,
        "max": 20,
        "found": found_sections,
        "label": "Section completeness"
    }

    # 2. Action verbs ────────────────────────────────────────────────────────
    found_verbs = [v for v in ATS_KEYWORDS["action_verbs"] if v in text_lower]
    verb_score = min(20, len(found_verbs) * 2)
    results["action_verbs"] = {
        "score": verb_score,
        "max": 20,
        "found": found_verbs[:8],
        "label": "Action verbs"
    }

    # 3. Quantifiable metrics ────────────────────────────────────────────────
    metrics_found = []
    for pattern in ATS_KEYWORDS["metrics_patterns"]:
        matches = re.findall(pattern, text, re.IGNORECASE)
        metrics_found.extend(matches)
    metric_score = min(20, len(metrics_found) * 4)
    results["metrics"] = {
        "score": metric_score,
        "max": 20,
        "found": metrics_found[:6],
        "label": "Quantifiable metrics"
    }

    # 4. Keyword density (skills found) ──────────────────────────────────────
    all_skills = [s for cat in SKILL_CATEGORIES.values() for s in cat]
    found_skills = [s for s in all_skills if s in text_lower]
    keyword_score = min(20, len(found_skills) * 2)
    results["keywords"] = {
        "score": keyword_score,
        "max": 20,
        "found": found_skills[:10],
        "label": "Technical keywords"
    }

    # 5. Formatting hints ────────────────────────────────────────────────────
    fmt_score = 0
    # Contact info present
    if re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', text):
        fmt_score += 5
    # Phone present
    if re.search(r'(\+?\d[\d\s\-().]{7,}\d)', text):
        fmt_score += 3
    # LinkedIn or GitHub URL
    if re.search(r'linkedin\.com|github\.com', text_lower):
        fmt_score += 4
    # Reasonable length (300–1500 words)
    word_count = len(text.split())
    if 300 <= word_count <= 1500:
        fmt_score += 5
    elif word_count > 100:
        fmt_score += 2
    # Avoid photos / tables hint (proxy: check word density)
    if word_count > 200:
        fmt_score += 3
    results["formatting"] = {
        "score": min(20, fmt_score),
        "max": 20,
        "found": [],
        "label": "Formatting & contact info"
    }

    total = sum(v["score"] for v in results.values())
    grade = _grade(total)

    return {
        "total": total,
        "grade": grade,
        "breakdown": results,
        "word_count": len(text.split()),
        "char_count": len(text)
    }


def _grade(score: int) -> str:
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 55:
        return "Fair"
    else:
        return "Needs Work"
