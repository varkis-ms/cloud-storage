from pydantic import BaseModel, EmailStr, constr, validator


class RegistrationForm(BaseModel):
    username: str
    # password: constr(min_length=8)
    password: str
    email: EmailStr | None
