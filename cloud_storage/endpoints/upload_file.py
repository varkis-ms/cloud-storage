from fastapi import APIRouter, UploadFile, File, Depends, status, Request, Body, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

import shutil

from cloud_storage.db.connection import get_session
from cloud_storage.schemas import RegistrationForm
from cloud_storage.db.models import FileInfo

api_router = APIRouter(
    tags=["Work with files"],
    prefix="/file", )


@api_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    summary="Upload files",
)
async def upload_files(files: list[UploadFile] = File(...)):
    for file in files:
        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"Status": "All files upload"}
