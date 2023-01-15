from cloud_storage.endpoints.health_check import api_router as health_check_router
from cloud_storage.endpoints.output_file import files_router
from .auth import user_router


list_of_routes = [
    health_check_router,
    files_router,
    user_router,
]


__all__ = [
    "list_of_routes",
]
