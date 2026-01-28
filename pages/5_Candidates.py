import streamlit as st
import tempfile
from resume_parser import parse_resume
from text_utils import extract_text
from database import execute_query

user = st.session_state["user"]
client_id = user[1]

st.header("Upload Candidate Resumes")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])

job_options = execute_query("SELECT job_id, title FROM jobs WHERE client_id=%s", (client_id,), fetch=True)
job_dict = {str(j[0]): j[1] for j in job_options}
selected_job = st.selectbox("Select Job", options=list(job_dict.keys()), format_func=lambda x: job_dict[x])

if st.button("Upload Resume"):
    if resume_file and selected_job:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(resume_file.read())
            resume_text = extract_text(tmp.name)

        parsed = parse_resume(tmp.name, [])

        execute_query(
            "INSERT INTO candidates (job_id, name, email, mobile, dob, experience, resume_text) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (selected_job, parsed.get("name"), parsed.get("email"), parsed.get("mobile"), parsed.get("dob"), parsed.get("experience"), resume_text)
        )
        st.success("Resume Uploaded Successfully!")
