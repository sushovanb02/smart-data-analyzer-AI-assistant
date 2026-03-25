from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from app.services.data_service import analyze_data

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        os.makedirs("data", exist_ok=True)
        file_location = f"data/{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        analysis = analyze_data(file_location)

        return {
            "filename": file.filename,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))