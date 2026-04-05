"""
app.py  –  Resume Analyzer  |  Streamlit Dashboard
Run:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
import csv

# Make sure local modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from utils.parser import extract_text, extract_email, extract_phone, extract_name
from utils.scorer import score_resume
from utils.skill_analyzer import extract_skills, match_job_roles, suggest_skills_to_learn
from utils.roadmap import generate_roadmap, get_course_recommendations, get_company_suggestions
from utils.feedback import generate_feedback

from job_matcher import (
    load_processed_jobs,
    match_resume_to_jobs,
    get_missing_skills_from_top_jobs,
    calculate_confidence
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stSidebar"] { background-color: #0f172a; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  .metric-card {
    background: #f8fafc; border-radius: 12px; padding: 1rem 1.25rem;
    border: 1px solid #e2e8f0; margin-bottom: 0.75rem;
  }
  .score-circle { text-align: center; padding: 1.5rem; }
  .badge {
    display: inline-block; padding: 3px 10px; border-radius: 99px;
    font-size: 12px; font-weight: 600; margin: 2px;
  }
  .badge-blue  { background:#dbeafe; color:#1e40af; }
  .badge-green { background:#dcfce7; color:#166534; }
  .badge-amber { background:#fef9c3; color:#854d0e; }
  .badge-red   { background:#fee2e2; color:#991b1b; }
  .badge-purple{ background:#ede9fe; color:#5b21b6; }
  .company-card {
    background:#fff; border:1px solid #e2e8f0; border-radius:10px;
    padding:0.85rem 1rem; margin-bottom:0.5rem;
  }
  .section-title {
    font-size:1.1rem; font-weight:700; color:#0f172a;
    margin: 1.5rem 0 0.75rem; padding-bottom:4px;
    border-bottom: 2px solid #6366f1;
    display: inline-block;
  }
  stTabs [data-baseweb="tab"] { font-size: 0.95rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 Resume Analyzer")
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
        help="Supports PDF, DOCX, and TXT formats"
    )
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool analyzes your resume and provides:
    - ✅ ATS compatibility score
    - 🎯 Job role matching
    - 📚 Skill gap analysis
    - 🗺️ Learning roadmap
    - 💼 Company recommendations
    """)
    st.markdown("---")
    st.caption("Built with Streamlit + Python")


# ── Landing state ────────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("# 📊 Resume Analyzer Dashboard")
    st.markdown("**Upload your resume in the sidebar to get started.**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🎯 ATS Score\nGet your resume's ATS compatibility score")
    with col2:
        st.success("🔍 Skill Analysis\nSee which skills you have and which you're missing")
    with col3:
        st.warning("📚 Learning Roadmap\nGet a personalized skill improvement plan")
    with col4:
        st.error("💼 Job Matching\nFind the best-fit roles and companies for your profile")
    st.stop()


# ── Parse resume ─────────────────────────────────────────────────────────────
with st.spinner("Parsing resume..."):
    resume_text = extract_text(uploaded_file)

if resume_text.startswith("PDF parsing error") or resume_text.startswith("DOCX parsing error"):
    st.error(f"Could not parse file: {resume_text}")
    st.stop()

if len(resume_text.strip()) < 50:
    st.error("Resume appears to be empty or unreadable. Please try a different file.")
    st.stop()


# ── Run analysis ─────────────────────────────────────────────────────────────
with st.spinner("Analyzing resume..."):
    name        = extract_name(resume_text)
    email       = extract_email(resume_text)
    phone       = extract_phone(resume_text)
    ats         = score_resume(resume_text)
    skills_map  = extract_skills(resume_text)
    job_matches = match_job_roles(resume_text)
    missing     = suggest_skills_to_learn(resume_text)
    roadmap     = generate_roadmap(resume_text)
    courses     = get_course_recommendations(missing)
    companies   = get_company_suggestions(resume_text)
    feedback = generate_feedback(resume_text, skills_map, ats["total"])
    jobs_df = load_processed_jobs("processed_jobs.csv")
    top_matches = match_resume_to_jobs(resume_text, jobs_df, top_n=10)
    missing_skills_real = get_missing_skills_from_top_jobs(resume_text, top_matches, top_k=10)
    confidence = calculate_confidence(top_matches)


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"# 👤 {name}")
col_e, col_p, col_f = st.columns(3)
col_e.metric("Email", email)
col_p.metric("Phone", phone)
col_f.metric("File", uploaded_file.name)
st.markdown("---")
st.subheader("AI Job Match Summary")
c1, c2 = st.columns(2)
c1.metric("Confidence Score", f"{confidence['score']}%")
c2.metric("Confidence Level", confidence["label"])

st.markdown("---")


# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ATS Score",
    "🎯 Job Matching",
    "🛠️ Skills",
    "🗺️ Roadmap & Courses",
    "💼 Companies"
])


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1 — ATS Score
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    score_col, detail_col = st.columns([1, 2])

    with score_col:
        total = ats["total"]
        color = "#22c55e" if total >= 70 else "#f59e0b" if total >= 50 else "#ef4444"

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total,
            number={"suffix": "/100", "font": {"size": 36}},
            title={"text": f"ATS Score — {ats['grade']}", "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": color},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 50],  "color": "#fee2e2"},
                    {"range": [50, 70], "color": "#fef9c3"},
                    {"range": [70, 85], "color": "#dcfce7"},
                    {"range": [85, 100],"color": "#bbf7d0"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 2},
                    "thickness": 0.75,
                    "value": total
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(t=40, b=0, l=20, r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.metric("Word count", ats["word_count"])
        st.metric("Characters", ats["char_count"])

    with detail_col:
        st.markdown('<div class="section-title">Score Breakdown</div>', unsafe_allow_html=True)

        breakdown = ats["breakdown"]
        labels = [v["label"] for v in breakdown.values()]
        scores = [v["score"] for v in breakdown.values()]
        maxes  = [v["max"]   for v in breakdown.values()]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=scores, y=labels, orientation='h',
            marker_color="#6366f1", name="Your score",
            text=[f"{s}/{m}" for s, m in zip(scores, maxes)],
            textposition="outside"
        ))
        fig_bar.add_trace(go.Bar(
            x=[m - s for s, m in zip(scores, maxes)],
            y=labels, orientation='h',
            marker_color="#e2e8f0", name="Remaining",
            showlegend=False
        ))
        fig_bar.update_layout(
            barmode='stack', height=280,
            margin=dict(t=10, b=10, l=10, r=60),
            legend=dict(orientation="h", y=-0.15),
            xaxis_title="Points"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Details
        for key, val in breakdown.items():
            if val["found"]:
                badges = " ".join([f'<span class="badge badge-blue">{s}</span>' for s in val["found"][:6]])
                st.markdown(
                    f"**{val['label']}** ({val['score']}/{val['max']}): {badges}",
                    unsafe_allow_html=True
                )

    # Tips
    st.markdown("---")
    st.markdown('<div class="section-title">💡 Improvement Tips</div>', unsafe_allow_html=True)
    tip_col1, tip_col2 = st.columns(2)
    with tip_col1:
        if breakdown["sections"]["score"] < 15:
            st.warning("Add missing sections: " + ", ".join(
                s for s in ["summary", "experience", "education", "skills", "projects"]
                if s not in breakdown["sections"]["found"]
            ))
        if breakdown["metrics"]["score"] < 12:
            st.warning("Add quantifiable achievements (e.g. 'increased revenue by 30%', 'led team of 5')")
    with tip_col2:
        if breakdown["action_verbs"]["score"] < 12:
            st.info("Use stronger action verbs: Built, Developed, Led, Optimized, Deployed...")
        if breakdown["formatting"]["score"] < 15:
            st.info("Add LinkedIn/GitHub URL and ensure contact info is clearly visible")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2 — Job Matching
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("Top Real Job Matches")

if not top_matches.empty:
    cols_to_show = ["job_title", "role", "match_percent"]

if "company" in top_matches.columns:
    cols_to_show.append("company")

if "location" in top_matches.columns:
    cols_to_show.append("location")

    show_df = top_matches[cols_to_show].head(10)

    st.dataframe(show_df, use_container_width=True)
else:
    st.warning("No matching jobs found.")
with tab2:
    st.markdown('<div class="section-title">Top Job Role Matches</div>', unsafe_allow_html=True)

    top5 = job_matches[:5]
    df_roles = pd.DataFrame([{
        "Role": r["role"],
        "Match %": r["match_pct"],
        "Avg Salary": r["avg_salary"],
        "Market Demand": r["demand"]
    } for r in top5])

    # Bar chart
    fig_roles = px.bar(
        df_roles, x="Match %", y="Role", orientation='h',
        color="Match %", color_continuous_scale=["#fee2e2","#fef9c3","#dcfce7","#22c55e"],
        range_color=[0, 100], text="Match %"
    )
    fig_roles.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_roles.update_layout(
        height=320, margin=dict(t=10, b=10, l=10, r=60),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_roles, use_container_width=True)

    # Cards
    for i, role in enumerate(top5):
        pct = role["match_pct"]
        color = "green" if pct >= 70 else "amber" if pct >= 40 else "red"
        with st.expander(f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else '🔹'} {role['role']} — {pct}% match"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Match", f"{pct}%")
            c2.metric("Salary", role["avg_salary"])
            c3.metric("Demand", role["demand"])

            if role["required_matched"]:
                st.markdown("**✅ Skills you have:**")
                st.markdown(" ".join([f'<span class="badge badge-green">{s}</span>' for s in role["required_matched"]]), unsafe_allow_html=True)
            if role["missing_required"]:
                st.markdown("**❌ Missing required skills:**")
                st.markdown(" ".join([f'<span class="badge badge-red">{s}</span>' for s in role["missing_required"]]), unsafe_allow_html=True)
            if role["optional_matched"]:
                st.markdown("**⭐ Bonus skills you have:**")
                st.markdown(" ".join([f'<span class="badge badge-purple">{s}</span>' for s in role["optional_matched"]]), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3 — Skills
# ═══════════════════════════════════════════════════════════════════════════
st.subheader("Missing Skills (Based on Real Jobs)")

if missing_skills_real:
    for skill in missing_skills_real:
        st.write(f"{skill['skill']} (demand: {skill['frequency']})")
else:
    st.success("No major missing skills found")
with tab3:
    present_col, missing_col = st.columns(2)

    with present_col:
        st.markdown('<div class="section-title">Skills Found in Resume</div>', unsafe_allow_html=True)
        if skills_map:
            for category, skills_list in skills_map.items():
                st.markdown(f"**{category}**")
                badges = " ".join([f'<span class="badge badge-blue">{s}</span>' for s in skills_list])
                st.markdown(badges, unsafe_allow_html=True)
                st.markdown("")
            # Radar chart
            categories = list(skills_map.keys())
            values = [len(v) for v in skills_map.values()]
            fig_radar = go.Figure(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself', fillcolor='rgba(99,102,241,0.2)',
                line=dict(color='#6366f1')
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(values)+1])),
                height=300, margin=dict(t=10, b=10)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("No recognizable skills found. Make sure your resume uses standard skill names.")

    with missing_col:
        st.markdown('<div class="section-title">Skills to Learn (Priority)</div>', unsafe_allow_html=True)
        if missing:
            for item in missing:
                freq = item["frequency"]
                bar_pct = min(100, freq * 20)
                color_class = "badge-red" if freq >= 4 else "badge-amber" if freq >= 2 else "badge-blue"
                st.markdown(
                    f'<span class="badge {color_class}">{item["skill"]}</span> '
                    f'<small style="color:#64748b">needed in {freq} top role(s)</small>',
                    unsafe_allow_html=True
                )
                st.progress(bar_pct / 100)
        else:
            st.success("Great! You seem to have the key skills for your matched roles.")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4 — Roadmap & Courses
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Skill Improvement Roadmap</div>', unsafe_allow_html=True)

    phase_colors = {
        "Phase 1 – Quick Wins": "#22c55e",
        "Phase 2 – Core Skills": "#6366f1",
        "Phase 3 – Advanced":   "#f59e0b"
    }

    for phase, info in roadmap.items():
        color = phase_colors.get(phase, "#64748b")
        st.markdown(f"""
        <div style="border-left:4px solid {color}; padding:0.75rem 1rem;
                    background:#f8fafc; border-radius:0 8px 8px 0; margin-bottom:1rem;">
            <strong style="color:{color};">{phase}</strong>
            <span style="color:#64748b; font-size:13px; margin-left:8px;">⏱ {info['duration']}</span><br>
            <small style="color:#475569;">{info['description']}</small><br><br>
            {"".join([f'<span class="badge badge-blue" style="margin:2px;">{s}</span>' for s in info['skills']])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">📚 Recommended Courses</div>', unsafe_allow_html=True)

    if courses:
        df_courses = pd.DataFrame(courses)
        df_courses.columns = [c.title() for c in df_courses.columns]
        df_courses["Url"] = df_courses["Url"].apply(
            lambda u: f'<a href="{u}" target="_blank">Open →</a>'
        )
        st.write(df_courses.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("Add more skills to your resume for personalized course recommendations.")
        
st.markdown("---")
st.markdown('<div class="section-title">📢 Resume Feedback</div>', unsafe_allow_html=True)

for f in feedback:
    st.warning(f)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 5 — Companies
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Companies Where You Can Apply</div>', unsafe_allow_html=True)
    st.caption("Based on your top matched roles and current skill set")

    if companies:
        for i, company in enumerate(companies):
            pct = company["match_pct"]
            color = "#22c55e" if pct >= 70 else "#f59e0b" if pct >= 50 else "#6366f1"
            st.markdown(f"""
            <div class="company-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <strong style="font-size:1rem;">{company['name']}</strong>
                        <span class="badge badge-blue" style="margin-left:8px;">{company['type']}</span>
                        <span class="badge badge-purple" style="margin-left:4px;">{company['size']} employees</span>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-weight:700; color:{color};">{pct}% profile match</span><br>
                        <small style="color:#64748b;">for {company['matched_role']}</small>
                    </div>
                </div>
                <div style="margin-top:8px;">
                    <a href="{company['url']}" target="_blank"
                       style="color:#6366f1; font-size:13px; text-decoration:none;">
                        🔗 View open positions →
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Upload a resume with more skills to get personalized company suggestions.")

    st.markdown("---")
    st.caption("💡 Tip: Tailor your resume for each company. Keyword-match the job description to increase your ATS score.")

st.markdown("---")

st.markdown("## 💬 User Feedback")

with st.form("feedback_form"):
    rating = st.slider("⭐ Rate your experience", 1, 5, 4)
    message = st.text_area("📝 Write your feedback")

    submit = st.form_submit_button("Submit")

    if submit:
        with open("feedback.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([rating, message])

        st.success("✅ Thank you for your feedback!")
