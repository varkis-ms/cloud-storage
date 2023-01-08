from cloud_storage.endpoints.health_check import api_router as health_check_router
from cloud_storage.endpoints.output_file import api_router as file_check_router
from cloud_storage.endpoints.upload_file import api_router as file_upload_router


list_of_routes = [
    health_check_router,
    file_check_router,
    file_upload_router,
]


__all__ = [
    "list_of_routes",
]
