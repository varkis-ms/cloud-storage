from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from cloud_storage.db.models import FileInfo
from cloud_storage.schemas import FileInfoSchema


async def get_file(session: AsyncSession, file_id: UUID) -> FileInfo | None:
    query = select(FileInfo).where(FileInfo.id == file_id)
    return await session.scalar(query)


async def file_in_db(session: AsyncSession, file_info: FileInfoSchema):
    file = FileInfo(**file_info.dict())
    session.add(file)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True
