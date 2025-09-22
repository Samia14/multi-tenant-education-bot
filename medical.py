"""File that will run on local machine for testing."""
import streamlit as st
import random
from phi.agent import Agent
from gtts import gTTS
from assistent import medical_agent
from io import BytesIO
from io import StringIO
from pylatexenc.latexwalker import get_default_latex_context_db, LatexWalker, LatexCharsNode
from pathlib import Path
import random
import psycopg2
from interesting_facts import interesting_fun_fact,suggestions

from assistent import agent_response_call_physics,agent_response_call_computer,agent_response_call_chemistry
import os,tempfile
output = StringIO()
from streamlit import config
def intro_information(subject='Physics',grade='9'):
    col1, col2 = st.columns([1, 5])
    col1.image(r"assets/ConvoBridgeImage_WithText.png", width=500)
    col2.title(f"Medical Bot ")
    st.divider()

intro_information()
def show_chat_messages(session_data):
    runs = session_data.get("runs", [])
    intro_information()
    if not runs:
        st.info("No stored messages for this session.")

    for chat in session_data['runs']:
        st.markdown(f"🧑‍🎓 **You**: {chat['message']['content']}")
        st.markdown(f"🤖 **Bot**: {chat['response']['content']}")
def get_chat_history():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="HelloWorld1!",
            host="localhost",  # e.g., 'localhost' or an IP address
            port="5432"    # default is 5432
        )
        print("Connection to PostgreSQL successful!")
        cur = conn.cursor()
        # cur.execute("select memory from ai.llm_default where session_id='645a431e-0aab-4f46-90bb-7d41a6f95d51'")
        cur.execute("select session_id,memory,updated_at,created_at from ai.llm_default order by updated_at  ") 

        db_version = cur.fetchall()
        # print(db_version)
        with st.sidebar:
            import datetime
            st.header("🗂️ Chat history")
            for button in db_version:#TODO: need to use enumerate to add label of chat 1 ,chat 2 etc 
                if button[2] is not None:
                    dt_utc   = datetime.datetime.utcfromtimestamp(button[2])          # 2025-05-22 19:11:46
                    dt_pk    = dt_utc + datetime.timedelta(hours=5)            # 2025-05-23 00:11:46
                    print(dt_utc.isoformat(" ", "seconds"))
                    print(dt_pk.isoformat(" ", "seconds"))
                else:
                    dt_utc   = datetime.datetime.utcfromtimestamp(button[3])          # 2025-05-22 19:11:46
                    dt_pk    = dt_utc + datetime.timedelta(hours=5)            # 2025-05-23 00:11:46
                    print(dt_utc.isoformat(" ", "seconds"))
                    print(dt_pk.isoformat(" ", "seconds"))
                st.button(label=dt_pk.isoformat(" ", "seconds"),on_click=show_chat_messages,args=(button[1],)    )
            st.divider()
     
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


def set_theme(theme_name):
    """Set the Streamlit theme based on user selection."""
    if theme_name == "dark":
        config.set_option("theme.base", "dark")
    elif theme_name == "light":
        config.set_option("theme.base", "light")
    else:  # system
        config.set_option("theme.base", "auto")


                           

    

def initailize_session(subject:str=None,grade:str=None):
    """Initialize the chat history based on the subject and grade selected."""
    # if "last_subject" in st.session_state and st.session_state["last_subject"]!=subject:
    st.session_state.pop("rag_assistant",None)
    st.session_state.pop("rag_assistant_agent_id",None)
    st.session_state.pop("messages",None)
    # else:
    # st.session_state["last_subject"]=subject
    print("session state:",st.session_state)
    rag_assistent:Agent
    if  st.session_state.get("rag_assistant") == None:
        rag_assistent = medical_agent()
        st.session_state["rag_assistant"] = rag_assistent
        # print("-------------------",rag_assistent)
    else:
        rag_assistent = st.session_state["rag_assistant"]
    try:
        st.session_state["rag_assistant_agent_id"] = rag_assistent.agent_id
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
    rag_assistant:Agent = medical_agent()
    if st.session_state.get('rag_assistant_agent_id'):
        del st.session_state['rag_assistant_agent_id']
    st.session_state["rag_assistant"] =rag_assistant
    try:
        st.session_state["rag_assistant_agent_id"] = rag_assistant.agent_id
        if "messages" not in st.session_state:
            st.session_state.messages=[]
    except Exception :
        st.warning("Could not create the Agent, please try again !")

  
st.sidebar.title("**Helping Platform**")

# Initialize session state for theme if it doesn't exist
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Sidebar theme selector
theme = st.sidebar.selectbox(
    "Choose a Theme",
    ["light", "dark"],
    index=["light", "dark"].index(st.session_state.theme),
    key="theme_selector"
)

# Apply theme if it changed
if theme != st.session_state.theme:
    st.session_state.theme = theme
    set_theme(theme)
    st.rerun()
st.session_state,rag_assistant = initailize_session()
if st.sidebar.button(f'Start New Chat ',on_click=clear_cache):
    if "messages" in st.session_state:
            # st.session_state,rag_assistant = initailize_session(subject)
            st.session_state.messages=[]
            st.success("Cleared Chat successfully!")
st.sidebar.divider()
# get_chat_history()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Ask me anything related to the Drs information provided !"}]

# Apply theme
if theme:
        st.session_state.theme = theme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        processed_msg = message.get("processed_content", message["content"])
        st.markdown(processed_msg,unsafe_allow_html=True)




def show_suggestive_prompts():
    # Initialize session state for 'question' if not set
    if 'question' not in st.session_state:
        st.session_state['question'] = ''

    # Create dynamic columns based on number of suggestions (max 4 per row for readability)
    num_cols = min(len(suggestions), 4)
    cols = st.columns(num_cols)

    # Display buttons for each suggestion
    for i, suggestion_msg in enumerate(suggestions):
        col_idx = i % num_cols  # Map suggestion to column
        if cols[col_idx].button(suggestion_msg, key=f"prompt_{i}", use_container_width=True):
            st.session_state['question'] = suggestion_msg

    # Display selected suggestion with visual feedback
    if not st.session_state['question']:
        st.info("Click a suggestion to select it.")

if 'question' not in st.session_state:
    st.session_state['question'] = ''

# Display suggestive prompts
# show_suggestive_prompts()

# Get user input from chat_input
user_input = st.chat_input(f"Ask me anything about given list of dr!")

# Determine the prompt to use
prompt = None
if user_input:
    prompt = user_input
    st.session_state['question'] = ''  
elif st.session_state.get('question'):
    prompt = st.session_state['question']

if prompt!=None:    
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container

    with st.chat_message("user"):
        st.markdown(prompt)
     

    with st.spinner("Thinking...  "):
        # st.warning("💡 FUN FACT !  \n"+random.choice(interesting_fun_fact))
        st.warning("Please Waiting...It can take some time")

    # Display assistant response in chat message container
        with st.chat_message("assistant",avatar=r'assets/ConvoBridgeImage_WithoutText.png'):
            message_placeholder = st.empty()

            full_response = ""
            try:
                assistant_response= rag_assistant.run(prompt,stream=True)
                for chunk in assistant_response:
                    if chunk:
                        full_response+=chunk.content  
                # mix_response = contains_latex(full_response)
            except Exception as E:
                print("Error in running agent",E)
                st.error("No Internet! Check your internet connection and try again. ")

            message_placeholder.markdown(full_response,unsafe_allow_html=True)
            message_placeholder.session_state.processed_output = full_response
           
            # image_extraction_regex(full_response)
            st.session_state['question']=''
            #     # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response,'processed_content':full_response})



