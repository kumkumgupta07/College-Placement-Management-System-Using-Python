import streamlit as st

class SessionState:
    def __init__(self):
        self.state = st.session_state

    def set(self, key, value):
        self.state[key] = value

    def get(self, key, default=None):
        return self.state.get(key, default)

    def clear(self):
        for key in list(self.state.keys()):
            del self.state[key]

session = SessionState()
