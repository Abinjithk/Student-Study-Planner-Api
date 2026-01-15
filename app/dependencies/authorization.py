from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy.future import select
from app.models.user import User


settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
#         user: int = payload.get("sub")
#         role: str = payload.get("role")
#         if user is None or role is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token",
#             )
#         return {"id": user, "role": role}
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#         )



async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: int = payload.get("sub")
        role: str = payload.get("role")

        if not user_id or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid user id in token")
        # 🔍 CHECK USER STILL EXISTS
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            # User was deleted by admin
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists",
            )

        return {
            "id": user.id,
            "role": user.role,
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )