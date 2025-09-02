import streamlit as st
from datetime import datetime
import re
import random
import json
import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from PyPDF2 import PdfReader

from utils.database import get_db, get_collection
from utils.file_utils import create_log_entry

# Ensure NLTK stopwords are downloaded
nltk.download("stopwords")

# --- MongoDB Collections ---
db = get_db()
companies = db["companies"]
jobs = db["jobs"]
applications = db["applications"]
notifications = db["notifications"]
logs = db["logs"]

# --- Feature: View Company Profile ---
def view_profile():
    st.subheader("👤 My Profile")
    st.write("**Name:**", st.session_state.name)
    st.write("**Email:**", st.session_state.email)
    st.write("**Role:**", st.session_state.role)

# --- Feature: Post Job ---
def post_job():
    st.subheader("📢 Post a Job")
    title = st.text_input("Job Title")
    description = st.text_area("Job Description")
    location = st.text_input("Location")

    if st.button("Post Job"):
        jobs.insert_one({
            "company_id": st.session_state.user_id,
            "title": title,
            "description": description,
            "location": location
        })
        st.success("✅ Job posted successfully!")
        logs.insert_one(create_log_entry(st.session_state.user_id, f"Posted job: {title}"))

# --- Feature: View Posted Jobs ---
def view_posted_jobs():
    st.subheader("Posted Jobs")
    posted = list(jobs.find({"company_id": st.session_state.user_id}))
    for job in posted:
        title = job.get("title", "Untitled")
        location = job.get("location", "Location not specified")
        description = job.get("description", "No description provided")

        st.markdown(f"**{title}** - {location}")
        st.caption(description)


# --- Feature: View Applicants ---
def view_applicants():
    st.subheader("📋 Applicants for Your Jobs")
    job_list = list(jobs.find({"company_id": st.session_state.user_id}))
    for job in job_list:
        st.markdown(f"### {job['title']}")
        applicants = list(applications.find({"job_id": str(job['_id'])}))
        if applicants:
            for app in applicants:
                st.write(f"- Applicant ID: {app['student_id']}")
        else:
            st.caption("No applicants yet.")

# --- Feature: View Notifications ---
def view_notifications():
    st.subheader("🔔 Company Notifications")
    notes = list(notifications.find({"user_id": st.session_state.user_id}))
    for note in notes:
        st.success(note.get("message", "No message"))

# --- Feature: Activity Log ---
def activity_log():
    st.subheader("📜 Activity Log")
    user_logs = list(logs.find({"user_id": st.session_state.user_id}))
    for entry in user_logs:
        st.markdown(f"🕒 **{entry['timestamp']}** - {entry['action']}")

# --- Utility: Extract and Clean Resume ---
def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def clean_and_tokenize(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word not in stopwords.words("english")]

def calculate_ats_score(jd_tokens, resume_tokens):
    jd_keywords = set(jd_tokens)
    resume_keywords = set(resume_tokens)
    matched = jd_keywords.intersection(resume_keywords)
    score = len(matched) / len(jd_keywords) * 10 if jd_keywords else 0
    return round(score, 2), matched

# --- Feature: Resume Analyzer ---
def resume_analyzer(user_id):
    st.subheader("📄 Resume Analyzer with ATS Score")

    jd_text = st.text_area("🧠 Enter Job Description or Generate It", height=200, placeholder="Enter your job description here...")

    if jd_text:
        st.info("✅ Now upload or select a resume to compare.")

        option = st.radio("Choose Resume Source", ["Upload Resume", "Select from Applicants"])

        resume_text = ""
        resume_name = ""

        if option == "Upload Resume":
            uploaded_file = st.file_uploader("📎 Upload Resume (PDF only)", type=["pdf"])
            if uploaded_file and uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
                resume_name = uploaded_file.name

        elif option == "Select from Applicants":
            applicant_db = get_collection("applicants")
            resumes = list(applicant_db.find({"company_id": user_id}))

            if resumes:
                selected_app = st.selectbox("📋 Choose Applicant", [f"{app.get('name', 'Unnamed')} - {app.get('email', '')}" for app in resumes])
                if selected_app:
                    email = selected_app.split(" - ")[-1]
                    resume_doc = applicant_db.find_one({"email": email})
                    if resume_doc and "resume_text" in resume_doc:
                        resume_text = resume_doc["resume_text"]
                        resume_name = resume_doc.get("name", "Selected Resume")
            else:
                st.warning("No applicants found for this company.")

        if resume_text:
            st.success(f"📄 Analyzing resume: {resume_name}")

            jd_tokens = clean_and_tokenize(jd_text)
            resume_tokens = clean_and_tokenize(resume_text)

            ats_score, matched = calculate_ats_score(jd_tokens, resume_tokens)

            st.metric("📊 ATS Score", f"{ats_score} / 10")

            if ats_score >= 7:
                st.success("🎯 Great fit! Highly suitable for the job.")
            elif ats_score >= 4:
                st.warning("⚠️ Partial match. May need improvements.")
            else:
                st.error("❌ Not a match for this job description.")

            st.markdown(f"**Matched Keywords:** {', '.join(matched)}")

            # --- ✅ Save to MongoDB ---
            analyzed_collection = get_collection("analyzed_resumes")
            analysis_record = {
                "company_id": user_id,
                "resume_name": resume_name,
                "job_description": jd_text,
                "ats_score": ats_score,
                "matched_keywords": list(matched),
                "eligible": ats_score >= 4,
                "timestamp": datetime.now()
            }
            analyzed_collection.insert_one(analysis_record)
            st.success("✅ Analysis result saved.")
