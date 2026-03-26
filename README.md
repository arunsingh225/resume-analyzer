
# 📄 Resume Analyzer — Complete Setup Guide

A full-featured resume analysis dashboard built with Python + Streamlit.

## Features
- ✅ ATS/Resume Score (0–100) with breakdown
- 🔍 Skill extraction by category
- 🎯 Job role matching with % scores
- ❌ Missing skill identification
- 🗺️ 3-phase learning roadmap
- 📚 Course recommendations
- 💼 Company suggestions with apply links

---

## 📁 Project Structure

```
resume_analyzer/
├── app.py                  ← Main Streamlit dashboard
├── requirements.txt        ← Python dependencies
├── data/
│   ├── __init__.py
│   └── skills_data.py      ← Skills, roles, companies, courses data
└── utils/
    ├── __init__.py
    ├── parser.py           ← PDF/DOCX text extraction
    ├── scorer.py           ← ATS scoring engine
    ├── skill_analyzer.py   ← Skill extraction + job matching
    └── roadmap.py          ← Roadmap + course recommendations
```

---

## 🚀 Step-by-Step Setup

### Step 1 — Install Python
Make sure you have Python 3.9+ installed.
```bash
python --version
```

### Step 2 — Create a virtual environment
```bash
cd resume_analyzer
python -m venv venv

# Activate it:
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Download spaCy model (optional, for better NLP)
```bash
python -m spacy download en_core_web_sm
```

### Step 5 — Run the app locally
```bash
streamlit run app.py
```
Your browser will open at http://localhost:8501

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Click "New app" → select your repo and branch
4. Set main file path: `app.py`
5. Click Deploy — your app gets a public URL instantly!

### Alternative: Deploy to Hugging Face Spaces
1. Create a Space at https://huggingface.co/spaces
2. Choose "Streamlit" as the SDK
3. Upload all files
4. The app auto-deploys!

---

## 🔧 Optional: Add OpenAI for smarter analysis

In `utils/skill_analyzer.py`, you can add an OpenAI-powered analysis function:

```python
import openai

def ai_analyze_resume(text: str, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional resume coach."},
            {"role": "user", "content": f"Analyze this resume and give top 5 improvements:\n\n{text[:3000]}"}
        ]
    )
    return response.choices[0].message.content
```

Then add an "AI Analysis" tab in `app.py` and call this function with a user-provided API key via `st.text_input("OpenAI API Key", type="password")`.

---

## 📦 Dependencies explained

| Package | Purpose |
|---|---|
| streamlit | Dashboard UI |
| pdfplumber | Extract text from PDFs |
| python-docx | Extract text from Word files |
| plotly | Interactive charts |
| pandas | Data tables |
| scikit-learn | TF-IDF for future improvements |
| spacy | NLP (optional, for entity extraction) |

---

## 🛠️ Customize

- **Add more job roles**: Edit `data/skills_data.py` → `JOB_ROLES` dict
- **Add more companies**: Edit `data/skills_data.py` → `COMPANIES` dict
- **Add more courses**: Edit `data/skills_data.py` → `COURSES` dict
- **Change scoring weights**: Edit `utils/scorer.py` → `score_resume()`
- **Change roadmap phases**: Edit `utils/roadmap.py` → `generate_roadmap()`
=======
# resume-analyzer
AI Resume Analyzer using Streamlit
>>>>>>> 75002d3eade13292b1ada7d8f77a97acca092e54
