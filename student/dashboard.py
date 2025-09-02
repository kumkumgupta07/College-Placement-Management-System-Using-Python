import streamlit as st
from student import features

def student_dashboard():
    st.sidebar.title("Student Dashboard")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio("📚 Features", [
        "View Profile",
        "Upload Resume",
        "Notifications",
        "Placement Schedule",
        "Activity Log",
        "Logout",
    ])

    st.markdown(f"<h3 style='color:green;'>Welcome, {st.session_state.name} 🎓</h3>", unsafe_allow_html=True)

    if menu == "View Profile":
        features.view_profile()

    elif menu == "Upload Resume":
        features.resume_upload()

    elif menu == "Notifications":
        features.view_notifications()

    elif menu == "Placement Schedule":
        features.view_schedule()

    elif menu == "Activity Log":
        features.activity_log()

    elif menu == "Logout":
        st.success("You have been logged out.")
        st.session_state.clear()
        st.rerun()

    st.sidebar.markdown("---")
