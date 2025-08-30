import json
import os
from phi.model.openai import OpenAIChat
from phi.embedder.openai import OpenAIEmbedder
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector
def medical_agent():
    knowledge_base = JSONKnowledgeBase(
        path="C:\\Users\\mysel\\Downloads\\restaurant_embeddings_25.json",
        # Table name: ai.json_documents
        vector_db=PgVector(
            table_name="resturant_json",
            db_url="postgresql+psycopg://postgres:HelloWorld1!@4.240.100.54:5432/postgres",embedder=OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"),model='text-embedding-3-large')
        ),
    )
    from phi.agent import Agent
    os.environ["OPENAI_API_KEY"]='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'
    return Agent(model=
        OpenAIChat(id='gpt-4o-mini',api_key=os.getenv("OPENAI_API_KEY"),temperature=0.3),
        knowledge=knowledge_base,
        search_knowledge=True,
    )


if __name__ == "__main__":
    agent =medical_agent()
    agent.knowledge.load(recreate=True)

    while 1:
        input_data = input()
        if input_data=='end':
            break     
        else: 
            agent.print_response(input_data)
    