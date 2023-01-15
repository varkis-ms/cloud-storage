from logging import getLogger

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn import run

from cloud_storage.config import DefaultSettings
from cloud_storage.config.utils import get_settings
from cloud_storage.endpoints import list_of_routes
from cloud_storage.utils.common import get_hostname


logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: DefaultSettings) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "Напишу тут что-то, но попозже"

    tags_metadata = [
        {
            "name": "Health check",
            "description": "Health check ручка",
        },
        {
            "name": "Work with files",
            "description": "Ручки для работы с файлами",
        },
    ]

    application = FastAPI(
        title="cloud-storage",
        description=description,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )
    settings = get_settings()
    bind_routes(application, settings)
    application.state.settings = settings
    application["info"]["x-logo"] = {
        "url": "https://www.google.com/url?sa=i&url=https%3A%2F%2Frutube.ru%2Fchannel%2F27218067%2F&psig=AOvVaw06pZkJm0xjwXCcipQhe7Q_&ust=1673834028761000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCPidpue7yPwCFQAAAAAdAAAAABAE"
    }
    return application


app = get_app()

app.mount("/", StaticFiles(directory="/Users/sergeymarkin/Desktop/Project/OpenSource/cloud-storage/front",
                           html=True))

if __name__ == "__main__":  # pragma: no cover
    settings_for_application = get_settings()
    run(
        "cloud_storage.__main__:app",
        host=get_hostname(settings_for_application.APP_HOST),
        port=settings_for_application.APP_PORT,
        reload=True,
        reload_dirs=["cloud_storage", "tests"],
        log_level="debug",
    )
