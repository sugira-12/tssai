from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from ..db.base import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    questions = Column(JSON)  # store quiz as JSON
