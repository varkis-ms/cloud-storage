from datetime import datetime
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, TIMESTAMP, UUID
from sqlalchemy.sql import func

from cloud_storage.db import DeclarativeBase


class UrlStorage(DeclarativeBase):
    __tablename__ = "_storage"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the string in table",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
