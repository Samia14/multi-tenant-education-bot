"""File that will run on local machine for testing."""
import streamlit as st
import random
from io import StringIO
from pylatexenc.latexwalker import get_default_latex_context_db, LatexWalker, LatexCharsNode, LatexGroupNode, LatexSpecialsNode, LatexMacroNode, LatexEnvironmentNode
import time
from pathlib import Path
from assistent import agent_response_call_physics,agent_response_call_computer,agent_response_call_chemistry
import os,tempfile
output = StringIO()
st.title('Educational ChatBot')
st.write("Your Personal Tutor for STEM subjects of (BISE Lahore) Pakistan")
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

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]
# uploaded_files= st.file_uploader(label='Upload files on which you want to train your tutor',accept_multiple_files=True,type=['pdf'])
# if uploaded_files is not None:
#     for uploaded_file in uploaded_files:
#         tmp_dir = tempfile.mkdtemp()
#         file_path = os.path.join(tmp_dir, uploaded_file.name)
#         with open(uploaded_file.name, "wb") as f:
#             f.write(uploaded_file.getbuffer())

# Display chat messages from history on app rerun
with st.sidebar:
    subject = st.selectbox(
        "Choose your Subject",
        ("Physics", "Chemistry", "Computer","Biology")
    )
    grade = st.selectbox(
        "Choose your grade",
        ("9th", "10th", "11th","12th")
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your text here."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    



        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        agent=None
        if subject=='Physics':

            agent =agent_response_call_physics()
        elif subject =='Chemistry':
            agent =agent_response_call_chemistry()
        else:
            agent =agent_response_call_computer()


        assistant_response= agent.run(prompt,stream=True)
        for chunk in assistant_response:
            if chunk:
                full_response+=chunk.content
    
        
      
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
            # Render everything at once as markdown
           
        # print("fdklj jfl kjf",full_response)      
        # Detection and rendering
        mix_response = contains_latex(full_response)
        message_placeholder.markdown(mix_response.getvalue())

        image_extraction_regex(full_response)
        # st.image("C:\\Users\\mysel\\Pictures\\Screenshots\\Physics\\Book9_1\\Figure 1.9.png")
   
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


