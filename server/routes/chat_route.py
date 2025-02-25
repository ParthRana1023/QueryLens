from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_model import get_answer

chat_router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@chat_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    try:
        answer = get_answer(request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer: {str(e)}")