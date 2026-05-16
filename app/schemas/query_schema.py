from pydantic import BaseModel
from typing import Any, Optional

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):    
    id: int
    query: str
    llm_provider: Optional[str] = None
    extracted_data: Any
    
    class Config:
        from_attributes=True