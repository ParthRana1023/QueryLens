import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from huggingface_hub import login  # Add this import

load_dotenv()

login(token=os.getenv("HUGGINGFACEHUB_API_TOKEN"))

def get_answer(question: str) -> str:
    # Use updated embeddings
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
    
    index_name = "pdf-chatbot"
    
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
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