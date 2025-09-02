import streamlit as st
from session import init_session
from auth.login import login_page
from student.dashboard import student_dashboard
from company.dashboard import company_dashboard
from college.dashboard import college_dashboard
from utils.session import session
import pymongo

init_session()
st.set_page_config(page_title="🎓 College Placement System", layout="wide")

# ---- STYLES ----
st.markdown("""
    <style>
        .main-title {
            font-size: 55px;
            text-align: center;
            font-weight: bold;    
            margin-bottom: 10px;
            margin-top: 10px;
        }
        .sub-info {
            text-align: center;
            font-size: 20px;
            color: gray;
            margin-bottom: 20px;
        }
        .top-buttons {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
        }
        .top-buttons button {
            font-size: 16px !important;
            padding: 0.5em 1.5em;
            border-radius: 8px;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .stAlert {
            position: relative;
            top: -20px;
            margin-bottom: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("<div class='main-title'>🎓 College Placement System</div>", unsafe_allow_html=True)

# ---- SHOW SUCCESS MESSAGES IF ANY ----
if "success_msg" in st.session_state:
    st.success(st.session_state.success_msg)
    del st.session_state.success_msg

# ---- DASHBOARD REDIRECT IF LOGGED IN ----
if st.session_state.get("logged_in") and st.session_state.get("role"):
    role = st.session_state["role"]
    if role == "Student":
        student_dashboard()
    elif role == "Company":
        company_dashboard()
    elif role == "College":
        college_dashboard()
    else:
        st.warning("Unknown role. Please login again.")
else:
    # ---- TOP RIGHT REGISTER BUTTON AND LOGIN ----
    col1, col2 = st.columns([6, 1])  # Wider left column, register on far right
    with col1:
        if st.button("🔐 Login", key="top_login"):
            st.session_state.auth_tab = "login"
    with col2:
        if st.button("📝 Register", key="top_register"):
            st.session_state.auth_tab = "register"

    # ---- SET LOGIN / REGISTER FORM TAB STATE ----
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    # ---- LOGIN/REGISTER PAGE ----
    login_page(st.session_state.auth_tab)