from fastapi import APIRouter, UploadFile, File
from starlette import status
from fastapi.responses import FileResponse

import shutil


api_router = APIRouter(tags=["Work with files"])


@api_router.post(
    "/file/upload",
    status_code=status.HTTP_200_OK,
)
async def health_check(files: list[UploadFile] = File(...)):
    for file in files:
        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return {"Status": "All files upload"}
