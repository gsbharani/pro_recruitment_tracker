import streamlit as st
import tempfile
from text_utils import extract_text
from database import execute_query

user = st.session_state["user"]
client_id = user[1]

st.header("Post a New Job")

title = st.text_input("Job Title")
required_skills = st.text_input("Required Skills (comma separated)")
positions = st.number_input("Number of Positions", min_value=1, value=1)
jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

if st.button("Post Job"):
    if title and jd_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(jd_file.read())
            jd_text = extract_text(tmp.name)

        execute_query(
            "INSERT INTO jobs (client_id, title, jd, required_skills, positions) VALUES (%s,%s,%s,%s,%s)",
            (client_id, title, jd_text, required_skills, positions)
        )
        st.success("Job Posted Successfully!")
