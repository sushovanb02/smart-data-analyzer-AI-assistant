from fastapi import FastAPI, APIRouter, UploadFile, File
import shutil
from app.routes.upload import router

app = FastAPI()

app.include_router(router)