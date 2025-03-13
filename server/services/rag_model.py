import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from huggingface_hub import login

load_dotenv()

login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def get_answer(question: str) -> str:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Configure Groq
    llm = ChatGroq(
        temperature=0.7,
        model_name="mixtral-8x7b-32768",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Connect to ChromaDB
    vector_store = Chroma(
        collection_name="querylens",
        embedding_function=embeddings,
        persist_directory="./database/chroma_db"
    )
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    result = qa.invoke(question)
    return result['result']

if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        answer = get_answer(query)
        print(f"\nAnswer: {answer}")