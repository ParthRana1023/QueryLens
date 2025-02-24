# models/embeddings.py
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

def process_pdfs(pdf_path):
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Manually set the dimensions attribute
    embeddings.dimensions = 1536
    
    # Configure Pinecone
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )
    index_name = "pdf-chatbot"
    
    # Check if the index exists, create if it does not
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=embeddings.dimensions,
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region=os.getenv("PINECONE_ENV")
            )
        )
    
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # Store embeddings in Pinecone
    PineconeVectorStore.from_documents(
        chunks,
        embeddings,
        index_name=index_name
    )
    print(f"Processed {os.path.basename(pdf_path)}")

if __name__ == "__main__":
    pdf_directory = "models/pdf"
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            process_pdfs(pdf_path)