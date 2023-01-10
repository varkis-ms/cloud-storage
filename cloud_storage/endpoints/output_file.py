from fastapi import APIRouter
from fastapi import status
from fastapi.responses import FileResponse


api_router = APIRouter(tags=["Work with files"])


@api_router.get(
    "/file/download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    summary="Download files",
)
async def download_files():
    return FileResponse("cloud_storage/__init__.py",
                        filename="test.py",
                        media_type="application/octet-stream", )
