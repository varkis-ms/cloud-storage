from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from cloud_storage.db.models import User
from cloud_storage.schemas import RegistrationForm


async def get_user(session: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    return await session.scalar(query)


async def register_user(session: AsyncSession, possible_user: RegistrationForm) -> bool:
    user = User(email=possible_user["email"], password=possible_user["password"])
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True
