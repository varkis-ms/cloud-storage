from datetime import datetime

from pydantic import BaseModel, EmailStr, constr


class User(BaseModel):
    username: str | None = None
    email: EmailStr
    # disabled: bool | None = None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True
