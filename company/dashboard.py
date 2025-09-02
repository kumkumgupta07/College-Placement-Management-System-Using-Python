import streamlit as st
from company import features
from datetime import datetime


def company_dashboard():
    st.sidebar.title(f"Company Dashboard")
    options = [
        "View Profile", "Post Job", "View Posted Jobs", "View Applicants",
        "Notifications", "Activity Log", "Resume Analyzer", "Logout"
    ]
    choice = st.sidebar.radio("Dashboard", options)

    if choice == "View Profile":
        features.view_profile()

    elif choice == "Post Job":
        features.post_job()

    elif choice == "View Posted Jobs":
        features.view_posted_jobs()

    elif choice == "View Applicants":
        features.view_applicants()

    elif choice == "Notifications":
        features.view_notifications()

    elif choice == "Activity Log":
        features.activity_log()

    elif choice == "Resume Analyzer":
        features.resume_analyzer(st.session_state.user_id)

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.clear()
        st.success("You have been logged out. Please refresh the page.")
