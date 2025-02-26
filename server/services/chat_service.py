from typing import List, Dict
from services.rag_model import get_answer
import logging

class ChatService:
    def __init__(self):
        self.conversation_history: Dict[str, List[Dict]] = {}
        
    def process_message(self, session_id: str, message: str) -> str:
        try:
            if not message.strip():
                raise ValueError("Empty message")

            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].append({
                "role": "user",
                "content": message
            })
            
            # Remove await since get_answer is not async
            response = get_answer(message)
            
            if not response:
                raise ValueError("Empty response from RAG model")
                
            self.conversation_history[session_id].append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            logging.error(f"Error in process_message: {str(e)}")
            raise
    def get_conversation_history(self, session_id: str) -> List[Dict]:
        return self.conversation_history.get(session_id, [])