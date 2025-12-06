from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class DBConversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True) 
    overall_sentiment = Column(String, nullable=True)
    trend = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("DBMessage", back_populates="conversation", cascade="all, delete-orphan")

class DBMessage(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    text = Column(Text)
    sender = Column(String)  # "user" or "bot"
    sentiment_label = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    corrected_label = Column(String, nullable=True) # For RL Feedback
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("DBConversation", back_populates="messages")



class Message(BaseModel):
    id: str
    text: str
    sender: str
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None
    corrected_label: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class Conversation(BaseModel):
    id: str
    title: Optional[str] = None
    messages: List[Message] = []
    overall_sentiment: Optional[str] = None

    trend: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    sentiment_label: str
    sentiment_score: float
    conversation_id: str

