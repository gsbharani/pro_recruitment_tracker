import streamlit as st

st.header("Login")
client_id = st.text_input("Client ID")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Enter"):
    # dummy authentication
    if client_id and username and password:
        st.session_state["client_id"] = client_id
        st.session_state["user"] = (username, client_id)
        st.success("Login successful! Go to About Company page")
    else:
        st.error("Enter all details")
