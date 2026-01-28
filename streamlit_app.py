import streamlit as st
import tempfile
import uuid
import pandas as pd

from supabase_client import execute_query
from resume_parser import parse_resume, extract_text
from matcher import semantic_score, skill_score

st.set_page_config("Recruiter JD Matcher", layout="wide")
st.title("🧑‍💼✅ Recruiter JD ↔ Resume Matcher")

# ---------------- Recruiter ----------------
st.header("Recruiter Login")
client_id = st.text_input("Client ID")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Enter"):
    # Here you could validate client_id/username/password from DB
    st.session_state["client_id"] = client_id
    st.session_state["username"] = username
    st.success("Login successful! Redirecting to About Company page...")
    st.experimental_rerun()

if "client_id" not in st.session_state:
    st.stop()

# ---------------- JD Upload ----------------
st.header("Upload Job Description")
jd_file = st.file_uploader("Upload JD (PDF)", type=["pdf"])
if jd_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(jd_file.read())
        jd_text = extract_text(tmp.name)
    st.session_state["jd_text"] = jd_text
    st.success("JD uploaded")

if "jd_text" not in st.session_state:
    st.stop()

# ---------------- Skills ---------------
st.subheader("Required Skills")
skills_input = st.text_input("Enter skills (comma separated)", placeholder="Python, SQL, AWS")
skills = []
if skills_input:
    skills = [s.strip().lower() for s in skills_input.split(",")]
    st.session_state["skills"] = skills

# ---------------- Resume Upload ----------------
st.header("Upload Resumes")
resume_files = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"], accept_multiple_files=True)

results = []

if "uploaded_resumes" not in st.session_state:
    st.session_state["uploaded_resumes"] = set()

if resume_files:
    for resume_file in resume_files:
        if resume_file.name in st.session_state["uploaded_resumes"]:
            continue
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(resume_file.read())
            resume_text = extract_text(tmp.name)
        parsed = parse_resume(tmp.name)

        jd_score = semantic_score(st.session_state["jd_text"], resume_text)
        skill_match = skill_score(resume_text, skills)
        final_score = round((jd_score * 0.7) + (skill_match * 0.3), 2)

        results.append({
            "resume_name": resume_file.name,
            "score": final_score
        })

        # Insert candidate into Neon/Postgres
        query = """
        INSERT INTO candidates (id, client_id, resume_name, email, mobile, experience, score, skills)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        execute_query(query, (
            str(uuid.uuid4()),
            st.session_state["client_id"],
            resume_file.name,
            parsed["email"],
            parsed["mobile"],
            parsed["experience"],
            final_score,
            skills
        ))

        st.session_state["uploaded_resumes"].add(resume_file.name)
        st.markdown(f"""
        **📄 {resume_file.name}**
        - 🧠 JD Match: **{jd_score}%**
        - 🛠 Skill Match: **{skill_match}%**
        - 🎯 Final Score: **{final_score}%**
        """)

# ---------------- Ranking ----------------
st.header("📊 Ranked Candidates")
ranked_results = sorted(results, key=lambda x: x["score"], reverse=True)
df = pd.DataFrame(ranked_results)
st.dataframe(df)

# ---------------- Download Shortlisted ----------------
df["shortlist"] = df["score"] >= 70
shortlisted = df[df["shortlist"]]

st.download_button(
    "Download Shortlisted (CSV)",
    shortlisted.to_csv(index=False),
    file_name="shortlisted_resumes.csv"
)
