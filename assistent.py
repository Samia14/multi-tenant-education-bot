"""Information regarding all asistents and agents."""
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.document.chunking.agentic import AgenticChunking
from phi.document.reader.pdf import PDFImageReader,PDFReader

from phi.vectordb.pgvector import PgVector, SearchType
import os
from phi.embedder.openai import OpenAIEmbedder

db_url = "postgresql+psycopg://postgres:HelloWorld1!@localhost:5432/postgres"
os.environ["OPENAI_API_KEY"]='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'

def load_pd_files_physics():
    """read any pdf file provided by the user."""
    pdf_path = "C:\\Education Project Data\\Physics_9.pdf"
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="physics", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'
def load_pd_files_chemistry():
    """read any pdf file provided by the user."""
    pdf_path = "C:\\Education Project Data\\Chemistry_9.pdf"
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="chemistry", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'


def load_pd_files_computer():
    """read any pdf file provided by the user."""
    pdf_path = "C:\\Education Project Data\\Computer_9.pdf"
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="computer", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'

def agent_response_call_chemistry()->Agent:
    
    pdf_path = "C:\\Education Project Data\\Chemistry_9.pdf"
    reader = PDFImageReader(
        
    )
    knowledge_base = PDFKnowledgeBase(
        reader=reader,
        path=pdf_path,
  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="chemistry", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini",api_key='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'),
        knowledge=knowledge_base,
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
                      "Do not add any image link reference from any source just provide information from the data source like fig 1.2 nothing more ",
                      "While answering questions, make sure to answer only that question, with the answer containing only relevant data.Do not mix up similar information with different context.",
                      "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
                      'If the user asked for summary make the response easy to understand based on the selected data from knowledge base no additional search '],
        guidelines=['Your scope is only limited to Physics of 9th grade from your knowledge base. No need to respond on questions if user asked about other filed or general knowledge question. ',
                    'Use the topic number to cite its title—for example, 6.5 → “Forms of Energy.”'],
        description='You are expert in Physics for 9th grade. Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.'

    )
def agent_response_call_computer()->Agent:
    
    pdf_path = "C:\\Education Project Data\\Computer_9.pdf"
    reader = PDFImageReader(
        
    )
    knowledge_base = PDFKnowledgeBase(
        reader=reader,
        path=pdf_path,
  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="computer", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini",api_key='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'),
        knowledge=knowledge_base,
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
                      "Do not add any image link reference from any source just provide information from the data source like fig 1.2 nothing more ",
                      "While answering questions, make sure to answer only that question, with the answer containing only relevant data.Do not mix up similar information with different context.",
                      "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
                      'If the user asked for summary make the response easy to understand based on the selected data from knowledge base no additional search '],
        guidelines=['Your scope is only limited to Physics of 9th grade from your knowledge base. No need to respond on questions if user asked about other filed or general knowledge question. ',
                    'Use the topic number to cite its title—for example, 6.5 → “Forms of Energy.”'],
        description='You are expert in Physics for 9th grade. Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.'

    )
def agent_response_call_physics()->Agent:
    
    pdf_path = "C:\\Education Project Data\\Physics_9.pdf"
    reader = PDFImageReader(
        
    )
    knowledge_base = PDFKnowledgeBase(
        reader=reader,
        path=pdf_path,
  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="physics", db_url=db_url,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model="text-embedding-3-large")),
    )
    return Agent(
        model=OpenAIChat(id="gpt-4o-mini",api_key='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'),
        knowledge=knowledge_base,
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
                      "Do not add any image link reference from any source just provide information from the data source like fig 1.2 nothing more ",
                      "While answering questions, make sure to answer only that question, with the answer containing only relevant data.Do not mix up similar information with different context.",
                      "When the user`s question contains a numeric reference (e.g., 'Explain topic 2.5' or 'What does example 4 cover?'), identify the source from the book that matches that number. If it is example it will be like Example 6.5, If it is topic it will be like : 6.5 abc and use it to construct your answer",
                      'If the user asked for summary make the response easy to understand based on the selected data from knowledge base no additional search '],
        guidelines=['Your scope is only limited to Physics of 9th grade from your knowledge base. No need to respond on questions if user asked about other filed or general knowledge question. ',
                    'Use the topic number to cite its title—for example, 6.5 → “Forms of Energy.”'],
        description='You are expert in Physics for 9th grade. Your task is to answer based on user`s query. Please follow the instructions and guidelines provided to you.'

    )
if __name__=="__main__":
    # print(load_pd_files_physics())
    print(load_pd_files_chemistry())

    print(load_pd_files_computer())


