import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from huggingface_hub import login

load_dotenv()

login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def process_pdfs(pdf_path: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Load and process PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Add PDF name metadata to all documents
    pdf_name = os.path.basename(pdf_path)
    for doc in documents:
        doc.metadata["pdf_name"] = pdf_name
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    
    # Store in ChromaDB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="querylens",
        persist_directory="./database/chroma_db"
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