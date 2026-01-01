from fastapi import Cookie, HTTPException
from jose import jwt, JWTError
from app.config import get_settings

settings = get_settings()

def get_current_user(access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(
            access_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401)


