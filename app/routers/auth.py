from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import *
from app.dependencies.auth import *
from app import  schemas, database
from sqlalchemy.future import select


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(
    user: schemas.LoginSchema,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # Use async select
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
    "sub": str(db_user.id),     # ✅ REQUIRED (immutable)
    "role": db_user.role,       # ✅ authorization
    "email": db_user.email,     # ✅ display only
    "name": db_user.name,       # ✅ display only
})


    # Set cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(user_email: str = Depends(get_current_user)):
    return {"email": user_email}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}


@router.post("/register", response_model=schemas.Token)
async def register(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(database.get_db)
):
    # Check if user exists
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    token = create_access_token({
    "sub": str(db_user.id),     # ✅ REQUIRED (immutable)
    "role": db_user.role,       # ✅ authorization
    "email": db_user.email,     # ✅ display only
    "name": db_user.name,       # ✅ display only
})


    return {
        "access_token": token,
        "token_type": "bearer"
    }