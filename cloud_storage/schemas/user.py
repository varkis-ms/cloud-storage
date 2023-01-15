from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    username: str | None
    email: EmailStr
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True
