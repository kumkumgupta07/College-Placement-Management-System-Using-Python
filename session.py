# session.py

def init_session():
    if 'logged_in' not in session_state:
        session_state.logged_in = False
        session_state.user_id = None
        session_state.role = None
        session_state.email = None
        session_state.name = None

# For short alias
import streamlit as st
session_state = st.session_state
