from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.constants.strings import ConstStrings
from app.core.config import settings
from app.database.connection import get_db
from app.model.token import BlacklistedToken

security = HTTPBearer(auto_error=False)

revoked_tokens = set()


def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ConstStrings.TOKEN_REQUIRED
        )

    token = credentials.credentials
    blacklisted = db.query(BlacklistedToken).filter(
        BlacklistedToken.token == token
    ).first()

    if blacklisted:
        raise HTTPException(
            status_code=401,
            detail=ConstStrings.TOKEN_EXPIRED
        )
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        payload["raw_token"] = token
        return payload


    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ConstStrings.INVALID_TOKEN
        )


# verify refresh token
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail=ConstStrings.REFRESH_TOKEN_EXPIRED
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail=ConstStrings.INVALID_REFRESH_TOKEN
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail=ConstStrings.INVALID_REFRESH_TOKEN
        )

    return payload