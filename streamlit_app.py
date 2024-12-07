import streamlit as st

# Session state for tracking login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login form
st.title("Login to Streamlit App")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "password123":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid credentials")

# Display content if logged in
if st.session_state.logged_in:
    st.write("Welcome to the admin dashboard!")
