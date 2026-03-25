from fastapi import FastAPI, APIRouter, UploadFile, File
import shutil
from app.routes.upload import router
from app.routes.query import router as query_router

app = FastAPI()

app.include_router(router, prefix="/api", tags=["Upload"])
app.include_router(query_router, prefix="/api", tags=["Query"])