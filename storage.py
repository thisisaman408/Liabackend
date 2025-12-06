from typing import Dict, List, Optional
from models import Conversation, Message, DBConversation, DBMessage
from database import SessionLocal

class Storage:
    def __init__(self):
        pass

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        db = SessionLocal()
        try:
            db_conv = db.query(DBConversation).filter(DBConversation.id == conversation_id).first()
            if db_conv:
               
                return Conversation.from_orm(db_conv)
            return None
        finally:
            db.close()

    def create_conversation(self, conversation_id: str) -> Conversation:
        db = SessionLocal()
        try:
            db_conv = DBConversation(id=conversation_id)
            db.add(db_conv)
            db.commit()
            db.refresh(db_conv)
            return Conversation.from_orm(db_conv)
        except Exception as e:
            db.rollback()
            print(f"Error creating conversation: {e}")
            raise e
        finally:
            db.close()

    def add_message(self, conversation_id: str, message: Message):
        db = SessionLocal()
        try:
          
            db_conv = db.query(DBConversation).filter(DBConversation.id == conversation_id).first()
            if not db_conv:
                db_conv = DBConversation(id=conversation_id)
                db.add(db_conv)
                db.commit()
            
            db_msg = DBMessage(
                id=message.id,
                conversation_id=conversation_id,
                text=message.text,
                sender=message.sender,
                sentiment_label=message.sentiment_label,
                sentiment_score=message.sentiment_score,
                timestamp=message.timestamp
            )
            db.add(db_msg)
            
           
            if not db_conv.title and message.sender == 'user':
               
                db_conv.title = message.text[:30] + "..." if len(message.text) > 30 else message.text
                
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error adding message: {e}")
            raise e
        finally:
            db.close()

    def update_analysis(self, conversation_id: str, analysis: Dict):
        db = SessionLocal()
        try:
            db_conv = db.query(DBConversation).filter(DBConversation.id == conversation_id).first()
            if db_conv:
                db_conv.overall_sentiment = analysis.get("overall_sentiment")
                db_conv.trend = analysis.get("trend")
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating analysis: {e}")
        finally:
            db.close()

    def get_recent_conversations(self, limit: int = 20) -> List[Conversation]:
        db = SessionLocal()
        try:
           
            db_convs = db.query(DBConversation).order_by(DBConversation.created_at.desc()).limit(limit).all()
            return [Conversation.from_orm(c) for c in db_convs]
        finally:
            db.close()

    def update_message_feedback(self, message_id: str, corrected_label: str):
        db = SessionLocal()
        try:
            msg = db.query(DBMessage).filter(DBMessage.id == message_id).first()
            if msg:
                msg.corrected_label = corrected_label
                db.commit()
               
                print(f"Reinforcement Learning: Updated msg {message_id} with label {corrected_label}")
        except Exception as e:
            db.rollback()
            print(f"Error updating feedback: {e}")
        finally:
            db.close()
            
    def set_title(self, conversation_id: str, title: str):
        db = SessionLocal()
        try:
            db_conv = db.query(DBConversation).filter(DBConversation.id == conversation_id).first()
            if db_conv:
                db_conv.title = title
                db.commit()
        finally:
            db.close()
