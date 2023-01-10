from pydantic import BaseModel, Field

from datetime import datetime


class BaseFile(BaseModel):
    name: str
    extension: str
    dt_create: datetime
    time_create: datetime
    dt_change: datetime
    time_change: datetime
    size: float
