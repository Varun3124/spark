import json

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.llm_service import extract_structured_data
from app.schemas.query_schema import QueryRequest
from app.models.query_model import Query

router = APIRouter(prefix="/queries", tags=["Queries"])

@router.post("/")
def create_query(payload: QueryRequest, db: Session = Depends(get_db)):
    llm_response = extract_structured_data(payload.query)
    
    provider = llm_response["provider"]
    extracted_data = llm_response["data"]
    
    db_query = Query(
        raw_query=payload.query,
        llm_provider=provider,
        extracted_data=json.dumps(extracted_data)
    )
    
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    
    return {
        "id": db_query.id,
        "query": db_query.raw_query,
        "llm_provider": provider,
        "extracted_data": extracted_data
    }

@router.get("/{query_id}")
def get_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(Query).filter(Query.id == query_id).first()
    
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    return {
        "id": query.id,
        "query": query.raw_query,
        "llm_provider": query.llm_provider,
        "extracted_data": json.loads(query.extracted_data)
    }