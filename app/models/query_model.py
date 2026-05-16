from sqlalchemy import Column, Integer, Text, String

from app.db.database import Base

class Query(Base):
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    raw_query = Column(String, nullable=False)
    extracted_data = Column(Text,nullable=False)
    