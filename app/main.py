from fastapi import FastAPI, APIRouter, UploadFile, File
import shutil
from app.services.data_service import analyze_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Data Analyzer running"}

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    analysis = analyze_data(file_location)

    return {
        "filename": file.filename,
        "analysis": analysis
    }