import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from dotenv import load_dotenv

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = Chroma(
    collection_name="agent_memory",
    embedding_function=embedding_model,
    persist_directory="./chroma_memory"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

class MemoryTool:
    def __init__(self):
        self.vectorstore = vectorstore
        self.retriever = retriever

    def store_memory(self, content: str, metadata: dict = None):
        doc = Document(page_content=content, metadata=metadata or {})
        self.vectorstore.add_documents([doc])
        print(f"[MemoryTool] Stored: {content}")

    def retrieve_memory(self, query: str) -> list:
        results = self.retriever.invoke(query)
        print(f"[MemoryTool] Retrieved {len(results)} items for query: '{query}'")
        return [doc.page_content for doc in results]
