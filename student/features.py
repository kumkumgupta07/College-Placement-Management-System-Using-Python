import streamlit as st
from utils.file_utils import is_valid_file, generate_filename, save_file_to_mongodb, create_log_entry
from utils.database import get_db
from datetime import datetime
from bson import ObjectId

# ✅ 1. View Profile
def view_profile():
    st.subheader("👤 My Profile")
    st.write("**Name:**", st.session_state.name)
    st.write("**Email:**", st.session_state.email)
    st.write("**Role:**", st.session_state.role)

# ✅ 2. Upload Resume (PDF)
def resume_upload():
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF resume", type=["pdf"])

    if uploaded_file:
        if is_valid_file(uploaded_file):
            file_id = save_file_to_mongodb(
                uploaded_file,
                metadata={
                    "user_id": st.session_state.user_id,
                    "name": st.session_state.name,
                    "uploaded_at": datetime.utcnow()
                }
            )
            st.success("✅ Resume uploaded successfully!")
        else:
            st.error("❌ Invalid file type. Please upload a PDF.")

# ✅ 3. Notifications Panel
def view_notifications():
    st.subheader("🔔 Notifications")
    db = get_db()
    notifications = db.notifications.find({"user_role": "Student"})

    has_data = False
    for note in notifications:
        has_data = True
        st.markdown(f"**{note['title']}**  \n{note['message']}  \n*Date:* {note['date']}")
        st.markdown("---")

    if not has_data:
        st.info("No new notifications.")

# ✅ 4. Placement Schedule
def view_schedule():
    st.subheader("📅 Placement Schedule")
    db = get_db()
    schedule = db.schedule.find({"target": "Student"})

    has_data = False
    for event in schedule:
        has_data = True
        st.markdown(f"**{event['title']}**  \n🕒 {event['date']}  \n📍 {event['location']}")
        st.markdown("---")

    if not has_data:
        st.info("No placement events scheduled.")

# ✅ 5. View Activity Log
def activity_log():
    st.subheader("🗂️ Activity Log")
    db = get_db()
    logs = db.logs.find({"user_id": st.session_state.user_id}).sort("timestamp", -1)

    has_logs = False
    for log in logs:
        has_logs = True
        st.markdown(f"- **{log['action']}** — *{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}*")

    if not has_logs:
        st.info("No activity logged yet.")
