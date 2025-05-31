"""File that will run on local machine for testing."""
import streamlit as st
import random
from phi.agent import Agent

from io import StringIO
from pylatexenc.latexwalker import get_default_latex_context_db, LatexWalker, LatexCharsNode
import time
from pathlib import Path


from assistent import agent_response_call_physics,agent_response_call_computer,agent_response_call_chemistry
import os,tempfile
output = StringIO()
from streamlit import config

def set_theme(theme_name):
    """Set the Streamlit theme based on user selection."""
    if theme_name == "dark":
        config.set_option("theme.base", "dark")
    elif theme_name == "light":
        config.set_option("theme.base", "light")
    else:  # system
        config.set_option("theme.base", "auto")


def image_extraction_regex(text:str):
        """extract image form the code."""
        import re
        image_str = r'C:\Users\mysel\Pictures\Screenshots\Physics\test'
        image_folder =Path('C:\\Users\\mysel\\Pictures\\Screenshots\\Physics\\test')
        matches = re.findall(r'\b[Ff]igure\s+\d+(?:\.\d+)?\b', text)
        
        if len(matches)>0:
            for image in matches:
                for file in image_folder.iterdir():
                    if file.is_file() :
                       
                        if file.name.lower().replace(' ','')==image.lower().replace(' ','')+'.png':
                            image_path = image_str+"\\"+file.name
                            st.image(image_path)

def subject_selection(subject:str):
    if subject=='Physics':
        return agent_response_call_physics()
    elif subject =='Chemistry':
        return agent_response_call_chemistry()
    else:
        return agent_response_call_computer()
    

def initailize_session(subject:str,grade:str=None):
    """Initialize the chat history based on the subject and grade selected."""
    if "last_subject" in st.session_state and st.session_state["last_subject"]!=subject:
        st.session_state.pop("rag_assistant",None)
        st.session_state.pop("rag_assistant_run_id",None)
        st.session_state.pop("messages",None)
    # else:
        st.session_state["last_subject"]=subject
        print("session state:",st.session_state)
    rag_assistent:Agent
    if  st.session_state.get("rag_assistant") == None:
        rag_assistent = subject_selection(subject)
        st.session_state["rag_assistant"] = rag_assistent
        # print("-------------------",rag_assistent)
    else:
        rag_assistent = st.session_state["rag_assistant"]
    try:
        st.session_state["rag_assistant_run_id"] = rag_assistent.run_id
    except Exception:
        st.warning("Could not create the Assistant! Please check if database is running ? ")
        return st.session_state, None
    if "messages" not in st.session_state:
        st.session_state.messages=[]
    return st.session_state, rag_assistent

# Display chat messages from history on app rerun
def clear_cache():
    """Clear cache based on the agent id of the session."""
    if st.session_state.get('rag_assistant'):
        del st.session_state['rag_assistant']
    rag_assistant:Agent = subject_selection(subject)
    if st.session_state.get('rag_assistant_run_id'):
        del st.session_state['rag_assistant_run_id']
    st.session_state["rag_assistant"] =rag_assistant
    try:
        st.session_state["rag_assistant_run_id"] = rag_assistant.run_id
        if "messages" not in st.session_state:
            st.session_state.messages=[]
    except Exception :
        st.warning("Could not create the Agent, please try again !")

def contains_latex(latex_text: str) -> bool:
                latex_context = get_default_latex_context_db()
                walker = LatexWalker(latex_text, latex_context=latex_context)
                walker = LatexWalker(latex_text, latex_context=latex_context)
                nodes, _, _ = walker.get_latex_nodes()

                for node in nodes:
                    if not isinstance(node, LatexCharsNode):
                        latex_content = node.latex_verbatim()
                        if latex_content.startswith(r"\(") and latex_content.endswith(r"\)"):
                            # For inline math, use single $ directly (no backslashes)
                            output.write(f"${latex_content[2:-2]}$")  
                        elif latex_content.startswith(r"\[") and latex_content.endswith(r"\]"):
                            # For display math, use double $$ with newlines
                            output.write(f"$$\n{latex_content[2:-2]}\n$$")  
                        else:
                            # For other LaTeX, use display math
                            output.write(f"$$\n{latex_content}\n$$")  
                    else:
                        # Escape any dollar signs in the text that aren't part of math
                        text = node.latex_verbatim().replace('$', r'\$')
                        output.write(text)
                return output

        
grade = st.sidebar.selectbox(
    "Choose your grade",
    ("9th")
)

subject = st.sidebar.selectbox(
    "Choose your Subject",
    ("Physics", "Chemistry", "Computer")
)


# font_size = st.sidebar.slider(
#     "Font Size", 
#     min_value=12, 
#     max_value=24, 
#     value=16,
#     key="font_size_slider"
# )
# Initialize session state for theme if it doesn't exist
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Sidebar theme selector
theme = st.sidebar.selectbox(
    "Select Theme",
    ["light", "dark"],
    index=["light", "dark"].index(st.session_state.theme),
    key="theme_selector"
)
st.title(f'Class {grade} {subject} Helper')
st.divider()
st.write("Your Personal Tutor for STEM subjects of (BISE Lahore) Pakistan")
# Apply theme if it changed
if theme != st.session_state.theme:
    st.session_state.theme = theme
    set_theme(theme)
    st.rerun()
st.session_state,rag_assistant = initailize_session(subject)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]
if st.sidebar.button('Start New Chat ',on_click=clear_cache):
        if "messages" in st.session_state:
            # st.session_state,rag_assistant = initailize_session(subject)
            st.session_state.messages=[]
            st.success("Cleared Chat successfully!")
# Apply theme
if theme:
        st.session_state.theme = theme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        processed_msg = message.get("processed_content", message["content"])
        st.markdown(processed_msg,unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("Enter your question here."):
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Thinking...", show_time=True):
        # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                try:
                    assistant_response= rag_assistant.run(prompt,stream=True)
                    for chunk in assistant_response:
                        if chunk:
                            full_response+=chunk.content  
                    # Detection and rendering
              
                    mix_response = contains_latex(full_response)
                except Exception as E:
                    print("Error in running agent",E)
                    st.error("No Internet! Check your internet connection and try again. ")
            
            message_placeholder.markdown(mix_response.getvalue(),unsafe_allow_html=True)
            # message_placeholder.session_state.processed_output = mix_response.getvalue()
    
          
            image_extraction_regex(full_response)

             # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response,'processed_content':mix_response.getvalue()})
       