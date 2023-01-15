from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import TEXT, FLOAT, ENUM

from .base import BaseTable


class FileInfo(BaseTable):
    __tablename__ = "file_info"

    name = Column(
        "name",
        TEXT,
        nullable=False,
        doc="Name of file",
    )
    path = Column(
        "path",
        TEXT,
        nullable=False,
        doc="Path to file",
    )
    owner_id = Column(
        "owner_id",
        ForeignKey("user.id", ondelete="SET NULL", onupdate="SET NULL"),
        nullable=True,
        doc="Identifier of user, who own file",
    )
    extension = Column(
        "extension",
        TEXT,  # ENUM
        nullable=True,
        doc="Extension of file (file type)",
    )
    size = Column(
        "size",
        FLOAT,
        nullable=True,
        server_default=text("null"),
        doc="Size of file",
    )
