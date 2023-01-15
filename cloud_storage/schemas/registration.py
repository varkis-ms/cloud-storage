from pydantic import BaseModel, EmailStr, root_validator


class RegistrationForm(BaseModel):
    email: EmailStr
    password1: str
    password2: str

    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password1'), values.get('password2')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match')
        return values


class RegistrationFormInDb(RegistrationForm):
    email: EmailStr
    hashed_password: str


class RegistrationResponse(BaseModel):
    message: str
