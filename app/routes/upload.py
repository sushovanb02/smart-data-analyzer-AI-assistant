from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

from app.services.data_service import analyze_data

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Step 1: Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")

        # Step 2: Ensure data directory exists
        os.makedirs("data", exist_ok=True)

        # Step 3: Save file locally
        file_location = f"data/{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 4: Call analysis service
        analysis = analyze_data(file_location)

        # Step 5: Return response
        return {
            "filename": file.filename,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))