import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or input("Please enter your OpenAI API key: ")

def get_answer(question: str) -> str:
    # Initialize components
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    index_name = "pdf-chatbot"
    
    # Connect to Pinecone
    vector_store = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    
    # Create QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    # Get answer
    result = qa.invoke(question)
    return result['result']

if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        answer = get_answer(query)
        print(f"\nAnswer: {answer}")