import streamlit as st
from streamlit import config
from main import set_theme,clear_cache
st.sidebar.title("**Learning Platform**")

grade = st.sidebar.selectbox(
    "Choose Your Grade",
    ("11th")
)

subject = st.sidebar.selectbox(
    "Choose Your Subject",
    ("Physics", "Chemistry", "Computer")
)


if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Sidebar theme selector
theme = st.sidebar.selectbox(
    "Choose a Theme",
    ["light", "dark"],
    index=["light", "dark"].index(st.session_state.theme),
    key="theme_selector"
)
col1, col2 = st.columns([1, 5])
col1.image(r"C:\Users\mysel\Downloads\Forman_Christian_College_logo.png", width=500)
col2.title(f"FC {subject} Bot — Grade {grade}")
st.divider()
st.write(f"Aligned with BISE Lahore - Interactive Learning Assistant")
st.divider()

st.title("Quiz Time!")

# Apply theme if it changed
if theme != st.session_state.theme:
    st.session_state.theme = theme
    set_theme(theme)
    st.rerun()
if st.sidebar.button(f'Start New {subject} Quiz ',on_click=clear_cache):
        if "messages" in st.session_state:
            # st.session_state,rag_assistant = initailize_session(subject)
            st.session_state.messages=[]
            st.success("Cleared Chat successfully!")
# Apply theme
if theme:
        st.session_state.theme = theme