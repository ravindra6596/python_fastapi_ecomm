from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.constants.strings import ConstStrings
from app.model.token import BlacklistedToken
from app.repository import auth_repository
from app.schemas.auth_schema import UserCreate
from app.schemas.response_schema import CustomResponse
from app.utils.auth_utils import hash_password, create_access_token, verify_password, create_refresh_token
from app.utils.auth_dependency import verify_refresh_token



def register_service(
    db: Session,
    emp: UserCreate
):
    existing_user = (
        auth_repository.get_user_by_email_repo(
            db,
            emp.email
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail=ConstStrings.USER_EXISTS
        )

    hashed_password = hash_password(emp.password)

    return auth_repository.register_repo(
        db,
        emp,
        hashed_password
    )
#login
def login_service(
    db: Session,
    email: str,
    password: str
):
    user = (
        auth_repository.get_user_by_email_repo(db, email)
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail=ConstStrings.NO_USER
        )

    if not verify_password(
        password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail=ConstStrings.INVALID_PASSWORD
        )
        # optional active check
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail=ConstStrings.ACCOUNT_INACTIVE
        )
    token_data = {
        "email": user.email,
        "user_id": user.id,
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    }

# refresh token
def refresh_access_token(refresh_token: str):
    payload = verify_refresh_token(refresh_token)

    new_access_token = create_access_token({
        "user_id": payload["user_id"],
        "email": payload["email"],
    })

    return CustomResponse.success_response(
        statusCode=200,
        message=ConstStrings.NEW_ACCESS_TOKEN,
        data={
            "user_id": payload["user_id"],
            "email": payload["email"],
            "access_token": new_access_token
        }
    )

# logout
def logout_service(db, token: str):
    blacklisted = BlacklistedToken(token=token)

    db.add(blacklisted)
    db.commit()

    return True