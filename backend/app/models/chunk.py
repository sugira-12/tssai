from sqlalchemy import Column, Integer, String, ForeignKey
from ..db.base import Base

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    text = Column(String)
    chunk_index = Column(Integer)
