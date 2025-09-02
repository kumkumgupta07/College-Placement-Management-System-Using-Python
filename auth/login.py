# login.py

import streamlit as st
from auth.auth_utils import login_user, register_user

def login_page(active_tab="login"):
    if active_tab == "login":
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        role = st.radio("Login as", ["Student", "Company", "College"], horizontal=True, key="login_role")

        if st.button("Login Now", key="login_btn_real"):
            user = login_user(email, password)
            if user and user["role"] == role:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user_id = str(user["_id"])
                st.session_state.role = user["role"]
                st.session_state.email = user["email"]
                st.session_state.name = user["name"]
                st.session_state.show_dashboard_btn = True
            else:
                st.error("Invalid credentials or role mismatch.")

        # 🔘 Show "Go to Dashboard" button only after successful login
        if st.session_state.get("show_dashboard_btn"):
            if st.button("➡️ Go to Dashboard", key="go_to_dash_btn"):
                st.session_state.auth_tab = None  # clear form view
                st.session_state.show_dashboard_btn = False  # hide this button
                # simulate redirect by showing dashboard next run

    elif active_tab == "register":
        st.subheader("Register")
        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        role = st.radio("Register as", ["Student", "Company", "College"], horizontal=True, key="reg_role")

        if st.button("Register Now", key="register_btn_real"):
            success = register_user(name, email, password, role)
            if success:
                st.success("Registration successful. Please login.")
            else:
                st.error("User already exists or registration failed.")
