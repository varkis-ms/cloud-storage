from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, validator


class FileInfoSchema(BaseModel):
    file_name: str
    path: str = Field(default="/")
    owner_id: UUID
    path_id: UUID | None
    mime_type: str | None
    size: float | None

    class Config:
        orm_mode = True
