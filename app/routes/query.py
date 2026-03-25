from fastapi import APIRouter
from pydantic import BaseModel
from app.services.data_service import ask_question

router = APIRouter()

class QueryRequest(BaseModel):
    file_path: str
    question: str

@router.post("/query")
async def query_data(request: QueryRequest):
    answer = ask_question(request.file_path, request.question)

    return {
        "question": request.question,
        "answer": answer
    }