"""Information regarding all asistents and agents."""
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.document.chunking.agentic import AgenticChunking
from phi.document.reader.pdf import PDFReader
from config import POSTGRES_URL,OPENAI_EMBEDDING_MODEL_NAME,BOOK_PATH,PHYSICS_BOOK,CHEMISTRY_BOOK,COMPUTER_BOOK
from phi.vectordb.pgvector import PgVector
import os
from phi.embedder.openai import OpenAIEmbedder
from phi.storage.agent.postgres import PgAgentStorage

from config import POSTGRES_URL,OPENAI_KEY,OPENAI_MODEL_NAME


def agent_response_call_chemistry()->Agent:

    return Agent(
        model=OpenAIChat(id=OPENAI_MODEL_NAME,api_key=OPENAI_KEY),
        storage=PgAgentStorage(table_name="llm_default",db_url=POSTGRES_URL),
        # Enable RAG by adding references from AgentKnowledge to the user prompt.
        add_context=True,
        # Set as False because Agents default to `search_knowledge=True`
        search_knowledge=True,
        markdown=True,
        debug_mode=True,
        instructions=['If you do not find any relavant information, avoid fabricating response.',
                      'Give data based on the selected chunk from the knowledge base.',
                      ' If you could not find any answer just simply apologize .',
                      'If the user`s question is unclear and does not make any sense with the previous data then ask for clarification.',
                      'You are only limited to the data provided to you.',
                      'if the response have reference to the image or figure, always add images or figures to help in better explanation.',
                      'Always mention the source information from where you get the data like chaper number and page number.',
                      'answer only from the material given in the book.',
                      "Do not add any image link reference from any source just provide information from the data source like figure 1.2 nothing more ",
                      "While answering questions, make sure to answer only that question, with the answer containing only relevant data.Do not mix up similar information with different context.",
                      "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
                      'If the user asked for summary make the response easy to understand based on the selected data from knowledge base no additional search '],
        guidelines=['Your scope is only limited to Chemistry of 9th grade from your knowledge base. No need to respond on questions if user asked about other filed or general knowledge question. ',
                    'Use the topic number to cite its title—for example, 6.5 → “Forms of Energy.”'],
        description='You are expert in Chemistry for 9th grade. Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.'

    )
def agent_response_call_computer()->Agent:

    return Agent(
        model=OpenAIChat(id=OPENAI_MODEL_NAME,api_key=OPENAI_KEY),
        storage=PgAgentStorage(table_name="llm_default",db_url=POSTGRES_URL),
        add_history_to_messages=True,
    # Number of historical responses to add to the messages.
        num_history_responses=5,
        # Enable RAG by adding references from AgentKnowledge to the user prompt.
        add_context=True,
        # Set as False because Agents default to `search_knowledge=True`
        search_knowledge=True,
        markdown=True,
        debug_mode=True,
        instructions=['If you do not find any relavant information, avoid fabricating response.',
                      'Give data based on the selected chunk from the knowledge base.',
                      'All questions are supposed to answered from the knowledge, do not force user to specifically write in question.',
                      ' If you could not find any answer just simply apologize .',
                      'If the user`s question is unclear and does not make any sense with the previous data then ask for clarification.',
                      'You are only limited to the data provided to you.',
                      'if the response have reference to the image or figure, always add images or figures to help in better explanation.',
                      'Always mention the source information from where you get the data like chaper number.',
                      'answer only from the material given in the book.',
                      "Do not add any image link reference from any source just provide information from the data source like figure 1.2 nothing more. Dont render images like :![Figure 3.10: Rocket](Figure 3.10),just simply mention figure 3.10. ",
                      "While answering questions, make sure to answer only that question, with the answer containing only relevant data.Do not mix up similar information with different context.",
                      "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
                      'If the user asked for summary make the response easy to understand based on the selected data from knowledge base no additional search '],

        guidelines=['Your scope is only limited to Computer of 9th grade from your knowledge base. No need to respond on questions if user asked about other filed or general knowledge question. ',
                    'Use the topic number to cite its title—for example, 6.5 → “Forms of Energy.”'],
        description='You are expert in Computer for 9th grade. Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.'

    )

from phi.tools.youtube_tools import YouTubeTools

def agent_response_call_physics()->Agent: 
    # physic_agent = Agent(
    #     role="Find answers for questions related to physics, numericals, concept, concepts with images, exmaples and problems.",
    #     name="Physics Expert of 9th grade of BISE Lahore.",
    #     knowledge_base=
    # )
    
    pdf_path = BOOK_PATH+'\\Physics\\Book9\\Modified and Extracted Chp\\Modified_Chp\\Physics9_2.pdf'
    reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=reader,
        chunking_strategy=AgenticChunking(),
        path=pdf_path,
        num_documents=3,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="physics", db_url=POSTGRES_URL,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model=OPENAI_EMBEDDING_MODEL_NAME)),
    )
    study_guide = Agent(
    name="Study planner",  # Fixed typo in name
    model=OpenAIChat(id=OPENAI_MODEL_NAME,api_key=OPENAI_KEY,temperature=0.3),
    markdown=True,
    description="You are a study partner who assists users in planning the given topic under limited time.",
    instructions=[
        "Create personalized study plans with clear milestones, deadlines, and progress tracking.",
        "Provide tips for effective learning techniques, time management, and maintaining motivation.",
        "Recommend relevant communities, forums, and study groups for peer learning and networking.",
    ],
)
    return Agent(
        model=OpenAIChat(id=OPENAI_MODEL_NAME,api_key=OPENAI_KEY,temperature=0.3),
        storage=PgAgentStorage(table_name="llm_default",db_url=POSTGRES_URL),
          guidelines=['Your scope is only limited to Physics of 9th grade from your knowledge base. You have team named `Study planner`, assign the task related to planning your study to that team member. If user asked any question other than greeting,simpling apolozie.Always avoid questions that are not techncial apart from greetings. '],
        description='You are  conversational based expert in Physics for 9th grade chatbot . Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.You have team named `Study planner`, assign the task related to planning your study to that team member.',
        team= [study_guide],
        # Enable RAG by adding references from AgentKnowledge to the user prompt.
        add_context=True,
        knowledge_base=knowledge_base,
        add_chat_history_to_messages=True,
        # team=[physic_agent],
        # Set as False because Agents default to `search_knowledge=True`
        search_knowledge=True,
        num_history_responses=3,
        
        read_chat_history=True,
        markdown=True,
        prevent_hallucinations=True,
        debug_mode=True,
        instructions=["IMPORTANT:No need to answer questions like how to cheat, regarding teachers or anything ethically or non ethically. Simply refuse to answer.Avoid sharing your team member details."
            'To answer any technical information always use knowledge base as a reference.',
            'If you do not find any relavant information, Always avoid fabricating response and just simply apologize .',
            
            'If the user`s question is unclear and does not make any sense with the previous data then ask for clarification.',
            'Always respond based on the knwoledgebase provided to you',
            'if the response from the knowledge base have reference to the image or figure / video always add them in the response',
            'Always mention the source information from where you get the data like chapter number and  be concise and correct.',
            "Generate the expression using proper KaTeX/LaTeX that works inside Streamlit's st.markdown() with unsafe_allow_html=True or directly as string Follow these rules strictly",
            # 'If a user question is related to creating table, use html instead of markdown',
            'When user ask about video/figrue referring to a topic, look for the Figure or Video reference present in the revalent chunk of text.',
            'If user ask information related to video or image, always refer to the knowledge_base and return it from the .',
            "Do not add any image or video link reference from any source just provide information from the knowledge base with the relavent chunk like Figure 1.2 for image and Video 1.2 nothing more ",
            "While answering questions, make sure to answer only that question .Avoid mix up similar information with different context.",
            'All examples are referred as EXAMPLE 1.2 where 1 refers as chapter 1.So, select all chunks from chapter 1 only.',
            "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
            'create summaries or steps for different topics to make it more easy to understaqnd or rephrase them without lossing the context of the data .'],
      
    )


