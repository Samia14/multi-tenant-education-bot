"""The code file that will be deployed on virtual machine."""
import streamlit as st
chat_page = st.Page("main.py", title="Conversational Bot", icon=":material/chat_bubble:")
quiz_page = st.Page("quiz.py", title="Create Quiz", icon=":material/assignment:")
voice_page = st.Page("voice_chat.py", title="Listen Voice Response", icon=":material/voice_chat:")


pg = st.navigation([chat_page, voice_page])
st.set_page_config(page_title="Beaconhouse ChatBot", page_icon=":material/robot_2:")
pg.run()