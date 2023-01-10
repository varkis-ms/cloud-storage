from fastapi import APIRouter
from fastapi import status
from fastapi.responses import HTMLResponse


api_router = APIRouter(tags=["Not found"])


@api_router.get(
    "/404",
    # response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse
)
async def health_check():
    return "<h2>Такого запроса не существует</h2>"
