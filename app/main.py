import uvicorn
from fastapi import FastAPI

from app.routes.queries import router as query_router
from app.models.query_model import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI powered research platform")

app.include_router(query_router)

@app.get("/")
def root():
    return {
        "message":"AI research backend running"
    }
    
if __name__ == '__main__':
    uvicorn.run(app)