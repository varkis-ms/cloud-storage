from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from cloud_storage.db.models import User
from cloud_storage.schemas import RegistrationFormInDb


async def get_user(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    return await session.scalar(query)


async def register_user(session: AsyncSession, possible_user: RegistrationFormInDb) -> bool | User:
    user = User(**possible_user.dict())
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return user
