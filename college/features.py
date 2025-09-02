import streamlit as st
from utils.database import get_db
from utils.file_utils import create_log_entry

db = get_db()

def view_profile():
    st.subheader("👤 My Profile")
    st.write("**Name:**", st.session_state.name)
    st.write("**Email:**", st.session_state.email)
    st.write("**Role:**", st.session_state.role)



def manage_schedule():
    st.subheader("📅 Manage Placement Schedule")
    with st.form("schedule_form"):
        company = st.text_input("Company Name")
        date = st.date_input("Placement Date")
        time = st.time_input("Placement Time")
        location = st.text_input("Location / Mode")
        remarks = st.text_area("Remarks")

        submit = st.form_submit_button("Add Schedule")
        if submit:
            db.placement_schedule.insert_one({
                "company": company,
                "date": str(date),
                "time": str(time),
                "location": location,
                "remarks": remarks,
                "created_by": st.session_state.get("email")
            })
            st.success("Schedule added successfully.")

def view_all_students():
    st.subheader("🎓 All Registered Students")
    students = list(db.students.find({}, {"password": 0, "password_hash": 0}))
    if students:
        for s in students:
            st.write(f"**Name:** {s.get('name')} | **Email:** {s.get('email')} | **Branch:** {s.get('branch', 'N/A')}")
    else:
        st.info("No students found.")

def view_all_companies():
    st.subheader("🏢 All Registered Companies")
    companies = list(db.companies.find({}, {"password": 0, "password_hash": 0}))
    if companies:
        for c in companies:
            st.write(f"**Name:** {c.get('name')} | **Email:** {c.get('email')} | **Location:** {c.get('location', 'N/A')}")
    else:
        st.info("No companies found.")

def view_notifications():
    st.subheader("🔔 Notifications")
    notifs = db.notifications.find({"for": "College"})
    for n in notifs:
        st.info(f"📢 {n.get('message')}")

def activity_log():
    st.subheader("📜 Activity Log")
    logs = db.logs.find({"user_id": st.session_state.get("user_id")}).sort("timestamp", -1)
    for log in logs:
        st.write(f"{log['timestamp']}: {log['action']}")
