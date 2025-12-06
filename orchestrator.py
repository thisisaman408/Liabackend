import uuid
import os
from datetime import datetime
from models import Message, ChatResponse
from engine import SentimentEngine
from storage import Storage
from groq import Groq

class ChatbotOrchestrator:
    def __init__(self, sentiment_engine: SentimentEngine, storage: Storage):
        self.sentiment_engine = sentiment_engine
        self.storage = storage
        self.groq_client = None
        api_key = os.getenv("GROQ_API_KEY")
        print(f"DEBUG: API Key loaded: {bool(api_key)}") # not printing the actual key for security logs
        if api_key:
            try:
                self.groq_client = Groq(api_key=api_key)
                print("DEBUG: Groq client initialized successfully")
            except Exception as e:
                print(f"ERROR: Failed to initialize Groq client: {e}")
        else:
            print("ERROR: GROQ_API_KEY not found in environment variables")

    def handle_message(self, text: str, conversation_id: str = None) -> ChatResponse:
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
       
        label, score = self.sentiment_engine.analyze_message(text)
        
       
        user_msg = Message(
            id=str(uuid.uuid4()),
            text=text,
            sender="user",
            sentiment_label=label,
            sentiment_score=score,
            timestamp=datetime.now()
        )
        
       
        self.storage.add_message(conversation_id, user_msg)
        
     
        bot_text = self._generate_bot_response(text, label, conversation_id)
        
      
        bot_msg = Message(
            id=str(uuid.uuid4()),
            text=bot_text,
            sender="bot",
            timestamp=datetime.now()
        )
        
       
        self.storage.add_message(conversation_id, bot_msg)
        
       
        conversation = self.storage.get_conversation(conversation_id)
        messages_dicts = [msg.dict() for msg in conversation.messages]
        analysis = self.sentiment_engine.analyze_conversation(messages_dicts)
        self.storage.update_analysis(conversation_id, analysis)
        
        return ChatResponse(
            reply=bot_text,
            sentiment_label=label,
            sentiment_score=score,
            conversation_id=conversation_id
        )

    def _generate_bot_response(self, text: str, sentiment: str, conversation_id: str) -> str:
        if self.groq_client:
            try:
               
                history = self.storage.get_conversation(conversation_id)
                messages = [
                    {"role": "system", "content": "You are a helpful and empathetic customer support chatbot. Respond to the user based on their latest message and the sentiment."}
                ]
                
                if history and history.messages:
                    for msg in history.messages[-10:]:
                        role = "user" if msg.sender == "user" else "system" 
                        if msg.sender == "bot": role = "assistant"
                        
                        content = msg.text
                        if role == "user" and msg.sentiment_label:
                            content += f" [Sentiment: {msg.sentiment_label}]"
                            
                        messages.append({"role": role, "content": content})
                
                
                messages.append({"role": "user", "content": f"{text} [Sentiment: {sentiment}]"})

                completion = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=100
                )
                return completion.choices[0].message.content
            except Exception as e:
                print(f"Groq generation failed: {e}")
                
      
        if sentiment == "Negative":
            import random
            options = [
                "I'm sorry to hear that. I'm here to listen if you want to vent.",
                "That sounds tough. Is there anything specific bothering you?",
                "I understand this might be frustrating. How can I support you?"
            ]
            return random.choice(options)
        elif sentiment == "Positive":
            import random
            options = [
                "That's wonderful! I'd love to hear more details.",
                "It's great to see you in high spirits! What made it so good?",
                "Positive vibes! Tell me more about it."
            ]
            return random.choice(options)
        else:
            import random
            options = [
                "I see. Please go on, I'm listening.",
                "Interesting. Tell me more about that.",
                "I'm following. What else is on your mind?"
            ]
            return random.choice(options)

    def get_history(self, conversation_id: str):
        return self.storage.get_conversation(conversation_id)
