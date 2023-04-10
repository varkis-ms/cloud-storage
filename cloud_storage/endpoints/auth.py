from fastapi import Depends, APIRouter, Form, Body, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from cloud_storage.schemas import RegistrationForm, RegistrationResponse, RegistrationFormInDb
from cloud_storage.config import get_settings
from cloud_storage.utils.user.business_logic import *
from cloud_storage.utils.user.auth_db import *
from cloud_storage.db.models import User
from cloud_storage.schemas import *
from cloud_storage.schemas import User as UserSchema
from cloud_storage.utils.files import create_directory, file_in_db
from cloud_storage.schemas import FileInfoSchema


user_router = APIRouter(tags=["auth"],
                        prefix="/user")


@user_router.post(
    "/auth",
    response_model=Token,
)
async def auth(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"},
                            )
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get(
    "/me",
    response_model=UserSchema,
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserSchema.from_orm(current_user)


@user_router.post(
    "/registration",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters for registration",
        },
    },
)
async def registration(
        registration_form: RegistrationForm = Body(),
        session: AsyncSession = Depends(get_session),
):
    user_data = RegistrationFormInDb(**registration_form.dict())
    check_user = await register_user(session, user_data)
    if check_user:
        create_directory(f"{get_settings().STORAGE_PATH}/", user_data.email)
        root_folder = FileInfoSchema(file_name=user_data.email, owner_id=check_user.id)
        check_root = await file_in_db(session, root_folder)
        if check_root:
            return {"message": "Successful registration!"}
        return {"message": "Successful registration, but root file doesn't create("}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already exists.",
    )
