from pydantic import BaseModel
from typing import Any

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):    
    id: int
    query: str
    extracted_data: Any
    
    class Config:
        from_attributes=True