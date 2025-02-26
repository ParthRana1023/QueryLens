from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_service import ChatService
import logging

chat_router = APIRouter()
chat_service = ChatService()

class ChatMessage(BaseModel):
    session_id: str
    message: str

@chat_router.post("/send")
def send_message(chat_message: ChatMessage):
    try:
        if not chat_message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
            
        response = chat_service.process_message(
            chat_message.session_id,
            chat_message.message
        )
        return {"response": response}
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )

@chat_router.get("/history/{session_id}")
def get_history(session_id: str):
    try:
        history = chat_service.get_conversation_history(session_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))