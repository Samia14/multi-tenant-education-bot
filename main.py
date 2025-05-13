"""File that will run on local machine for testing."""
import streamlit as st
import random
from io import StringIO
from pylatexenc.latexwalker import get_default_latex_context_db, LatexWalker, LatexCharsNode, LatexGroupNode, LatexSpecialsNode, LatexMacroNode, LatexEnvironmentNode
import time
from assistent import agent_response_call
import os,tempfile
output = StringIO()
st.title('Educational ChatBot')
st.write("Your Personal Tutor for STEM subjects of (BISE Lahore) Pakistan")
def clean_latex(text):
    return (
        text.replace('⍺rac', r'\frac')  # Fix mis-encoded '\frac'
            .replace('ext{', r'\text{')  # Fix mis-encoded '\text{'
            .replace('ext(', r'\text(')
            .replace('\\,', r'\,')       # Ensure proper spacing command
    )

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
        agent =agent_response_call()
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

            # Render everything at once as markdown
            st.markdown(output.getvalue())
                 
        # Detection and rendering
        contains_latex(full_response)
  


     #    Combined regex pattern for LaTeX
        # parts = re.split(r'(\\\[.*?\\\])|', full_response, flags=re.DOTALL)
     
    # Split content, keeping the delimiters (captured groups)
    

        
    #     r"""
    #     # Match LaTeX environments (e.g., equation, align)
    #     \\begin\{.*?\}.*?\\end\{.*?\}  
    #     |
    #     # Match display math blocks: $$...$$ or $...$
    #     (\$\$.*?\$\$|\\$.*?\\$)       
    #     |
    #     # Match inline math: $...$ or $...$
    #     (\$.*?\$|\\$.*?\\$)            
    #     |
    #     # Match standalone LaTeX commands with arguments (e.g., \frac{}{}, \text{})
    #     (\$a-zA-Z]+\*?\s*\{[^{}]*\}(?:\{[^{}]*\})*)  
    #     |
    #     # Match simple LaTeX commands (e.g., \times, \approx)
    #     (\\[a-zA-Z]+\*?)                              
    # """

        # for part in parts:
        # # Check if the part is a display math block
        #     if part.startswith('\[') and part.endswith('\]'):
        #         # Extract the LaTeX code by removing \[ and \] and any surrounding whitespace
        #         latex_code = part[2:-2].strip()
        #         st.latex(latex_code)
        #     else:
        #         # Render text (which may include inline math) with st.markdown
        #         st.markdown(part)

#         # Split the text into LaTeX and non-LaTeX parts
        # result = []
        # last_pos = 0
        # for match in re.finditer(pattern, full_response, flags=re.DOTALL):
        #     if last_pos < match.start():
        #         result.append(('text', full_response[last_pos:match.start()]))
        #     result.append(('latex', match.group(0)))
        #     last_pos = match.end()
        # if last_pos < len(full_response):
        #     result.append(('text', full_response[last_pos:]))

        # for chunk_type, chunk in result:
        #     if chunk_type == 'latex':
        #         st.latex(clean_latex(chunk.strip()))
        #     else:
        #         st.markdown(chunk)            

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


