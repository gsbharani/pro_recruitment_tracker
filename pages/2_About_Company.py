import streamlit as st
from database import execute_query

user = st.session_state.get("user")
if not user:
    st.warning("Login first on Home page")
    st.stop()

client_id = user[1]

st.header("About Company")
st.image("client_logo.png", width=150)
st.write(f"Client ID: {client_id}")

# fetch company info from DB
company = execute_query("SELECT name, ceo, total_employees FROM clients WHERE client_id=%s", (client_id,), fetch=True)
if company:
    st.write(f"Company Name: {company[0][0]}")
    st.write(f"CEO: {company[0][1]}")
    st.write(f"Total Employees: {company[0][2]}")

# Dashboard counts
selected = execute_query("SELECT COUNT(*) FROM candidates WHERE client_id=%s AND status='selected'", (client_id,), fetch=True)
rejected = execute_query("SELECT COUNT(*) FROM candidates WHERE client_id=%s AND status='rejected'", (client_id,), fetch=True)
st.write(f"Selected Candidates: {selected[0][0]}")
st.write(f"Rejected Candidates: {rejected[0][0]}")
