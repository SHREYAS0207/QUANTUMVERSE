from sqlalchemy import Column,String,Integer,Float,Boolean,DateTime,Text,JSON,ForeignKey
from sqlalchemy.sql import func
try:
    from app.database.connection import Base
except Exception:
    from app.database.session import Base
class QLearnTopic(Base):
    __tablename__='qlearn_topics'; id=Column(String,primary_key=True); title=Column(String,nullable=False); category=Column(String); theory=Column(Text); mathematics=Column(Text); created_at=Column(DateTime,server_default=func.now())
class QLearnSimulation(Base):
    __tablename__='qlearn_simulations'; id=Column(String,primary_key=True); topic_id=Column(String); title=Column(String); status=Column(String); config_json=Column(JSON); validation_json=Column(JSON); created_at=Column(DateTime,server_default=func.now())
class QLearnSolverHistory(Base):
    __tablename__='qlearn_solver_history'; id=Column(String,primary_key=True); user_id=Column(String); original_question=Column(Text); final_answer=Column(Text); verification_status=Column(String); calculation_json=Column(JSON); created_at=Column(DateTime,server_default=func.now())
class QLearnConversation(Base):
    __tablename__='qlearn_conversations'; id=Column(String,primary_key=True); user_id=Column(String); title=Column(String); context_json=Column(JSON); created_at=Column(DateTime,server_default=func.now())
class QLearnConversationMessage(Base):
    __tablename__='qlearn_conversation_messages'; id=Column(String,primary_key=True); conversation_id=Column(ForeignKey('qlearn_conversations.id')); role=Column(String); content=Column(Text); context_json=Column(JSON); created_at=Column(DateTime,server_default=func.now())
class QLearnExperiment(Base):
    __tablename__='qlearn_experiments'; id=Column(String,primary_key=True); user_id=Column(String); name=Column(String); topic=Column(String); circuit_json=Column(JSON); parameters_json=Column(JSON); results_json=Column(JSON); notes=Column(Text); created_at=Column(DateTime,server_default=func.now())
