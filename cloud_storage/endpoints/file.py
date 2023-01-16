import os.path

from fastapi import APIRouter, UploadFile, File, Depends, status, Request, Body, HTTPException, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from uuid import UUID
import shutil

from cloud_storage.db.connection import get_session
from cloud_storage.schemas import FileInfoSchema
from cloud_storage.db.models import FileInfo, User
from cloud_storage.utils.files import create_directory, delete_directory, files_in_directory,\
    zip_files, get_file, file_in_db, get_file_size, get_mime_type
from cloud_storage.config import get_settings
from cloud_storage.utils.user import get_current_user

settings = get_settings()

files_router = APIRouter(tags=["Work with files"],
                         prefix="/file")


@files_router.get(
    "/download",
    status_code=status.HTTP_200_OK,
    summary="Download files",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Could not validate credentials",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "File with this id and this owner not found",
        },
    },
)
async def download_files(
        file_id: UUID,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    file_db = await get_file(session, file_id)
    if not file_db or current_user.id != file_db.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File doesn't exists.",
        )
    path_file = f"{settings.STORAGE_PATH}{file_db.path}{file_db.file_name}"
    if os.path.isfile(path_file):
        return FileResponse(path_file,
                            filename=f"{file_db.file_name}",
                            media_type="application/octet-stream")
    elif os.path.isdir(path_file):
        return StreamingResponse(
            zip_files(path_file, file_db.file_name),
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": f"attachment;filename={file_db.file_name}.zip"}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="File doesn't exists.",
    )


@files_router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    summary="Upload files",
)
async def upload_files(
        folder_id: UUID,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
):
    file_db = await get_file(session, folder_id)
    if not file_db or current_user.id != file_db.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Folder doesn't exists.",
        )
    path_file = f"{settings.STORAGE_PATH}{file_db.path}{file_db.file_name}"
    with open(f"{path_file}/{file.filename}", "wb") as buffer:
        file_content = await file.read()
        buffer.write(file_content)
        mime_type = get_mime_type(file_content)
        buffer.close()
    file_size = get_file_size(f"{file_db.path}{file_db.file_name}/{file.filename}")
    file_info = FileInfoSchema(file_name=file.filename,
                               owner_id=current_user.id,
                               path=f"{file_db.path}{file_db.file_name}/",
                               mime_type=mime_type,
                               size=file_size,
                               path_id=file_db.id)
    if await file_in_db(session, file_info):
        return {"Status": f"File {file.filename} uploaded!"}
    # todo: Доделать откат при ошибке
    return {"Status": f"File {file.filename} doesn't upload.\nTry again!"}
