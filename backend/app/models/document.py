from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.base import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    filename = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
