from fastapi import APIRouter
from starlette import status
from fastapi.responses import FileResponse

# from cloud_storage.schemas import PingResponse


api_router = APIRouter(tags=["Work with files"])


@api_router.get(
    "/file/download",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return FileResponse("/Users/sergeymarkin/Desktop/Project/OpenSource/cloud-storage/env.sample",
                        filename="test.txt",
                        media_type="application/octet-stream")
