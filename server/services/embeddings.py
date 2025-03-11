import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from huggingface_hub import login  # Add this import

load_dotenv()

login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def process_pdfs(pdf_path: str):
    # Use correct embedding initialization
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  # Add device configuration
        encode_kwargs={'normalize_embeddings': True}

    )
    
    # Configure Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "pdf-chatbot"
    
    # Create index with correct dimensions
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # Dimension for 'all-mpnet-base-v2'
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region=os.getenv("PINECONE_ENV")
            )
        )
    
    # Load and process PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    PineconeVectorStore.from_documents(
        chunks,
        embeddings,
        index_name=index_name
    )
    print(f"Processed {os.path.basename(pdf_path)}")

if __name__ == "__main__":
    pdf_directory = "services/pdf"

    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
        
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            process_pdfs(pdf_path)