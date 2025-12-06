from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
from models import ChatRequest, ChatResponse
from engine import ContentAwareLinguisticEngine, VaderSentimentEngine
from storage import Storage
from orchestrator import ChatbotOrchestrator
from database import init_db


# Initialize Database (SRP: Delegated to database module)
init_db()

app = FastAPI(title="Conversational Sentiment Chatbot")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://liafrontend-five.vercel.app", 
        "https://liabackend.onrender.com",
        "http://localhost:5173", 
        "*"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from engine import ContentAwareLinguisticEngine, VaderSentimentEngine
sentiment_engine = ContentAwareLinguisticEngine()
print("Using Content-Aware Linguistic Engine (Hybrid VADER + PhD Heuristics)")

storage = Storage()
orchestrator = ChatbotOrchestrator(sentiment_engine, storage)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = orchestrator.handle_message(request.message, request.conversation_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    conversation = orchestrator.get_history(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.get("/conversations")
async def list_conversations():
   
    return storage.get_recent_conversations()

class FeedbackRequest(BaseModel):
    message_id: str
    corrected_label: str

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
  
    storage.update_message_feedback(feedback.message_id, feedback.corrected_label)
    return {"status": "success", "message": "Feedback received and learning updated"}


@app.get("/")
async def root():
    return {"message": "Sentiment Chatbot API is running"}
