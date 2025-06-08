"""Data ingestion script for postgress."""
from phi.knowledge.pdf import PDFKnowledgeBase
from phi.document.chunking.agentic import AgenticChunking
from phi.document.reader.pdf import PDFReader
from config import POSTGRES_URL,OPENAI_EMBEDDING_MODEL_NAME,BOOK_PATH,PHYSICS_BOOK,CHEMISTRY_BOOK,COMPUTER_BOOK
from phi.vectordb.pgvector import PgVector
import os
from phi.embedder.openai import OpenAIEmbedder

def load_pd_files_physics():
    """read any pdf file provided by the user."""
    pdf_path = BOOK_PATH+'\\Physics\\Book9\\Modified and Extracted Chp\\Modified_Chp\\Physics9_2.pdf'
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
        num_documents=10,
        vector_db=PgVector(table_name="physics", db_url=POSTGRES_URL,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model=OPENAI_EMBEDDING_MODEL_NAME)),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'
def load_pd_files_chemistry():
    """read any pdf file provided by the user."""
    pdf_path = BOOK_PATH+CHEMISTRY_BOOK
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="chemistry", db_url=POSTGRES_URL,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model=OPENAI_EMBEDDING_MODEL_NAME)),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'


def load_pd_files_computer():
    """read any pdf file provided by the user."""
    pdf_path = BOOK_PATH+COMPUTER_BOOK
    pdf_reader = PDFReader(chunking_strategy=AgenticChunking())
    knowledge_base = PDFKnowledgeBase(
        reader=pdf_reader,
        path=pdf_path,  
         num_documents=10,
        # Store embeddings in the `ai.recipes` table
        vector_db=PgVector(table_name="computer", db_url=POSTGRES_URL,  embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model=OPENAI_EMBEDDING_MODEL_NAME)),
    )
    # Load the knowledge base: Comment after first run
    knowledge_base.load(recreate=True,upsert=True)
    return 'all done'
if __name__=="__main__":
    print(load_pd_files_physics())
    # print(load_pd_files_chemistry())

    # print(load_pd_files_computer())
