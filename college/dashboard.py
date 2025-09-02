import streamlit as st
from college import features

def college_dashboard():
    st.sidebar.title(f"🎓College Dashboard")

    menu = st.sidebar.radio(
        "Select an option",
        [
            "View Profile",
            "Manage Placement Schedule",
            "View All Students",
            "View All Companies",
            "Notifications",
            "Activity Log",
            "Logout"
        ]
    )

    # st.title("📘 College Dashboard")

    if menu == "View Profile":
        features.view_profile()

    elif menu == "Manage Placement Schedule":
        features.manage_schedule()

    elif menu == "View All Students":
        features.view_all_students()

    elif menu == "View All Companies":
        features.view_all_companies()

    elif menu == "Notifications":
        features.view_notifications()

    elif menu == "Activity Log":
        features.activity_log()

    elif menu == "Logout":
        st.success("You have been logged out.")
        st.session_state.logged_in = False
        st.session_state.clear()
