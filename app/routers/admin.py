from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User
from app.dependencies.authorization import get_current_user
from fastapi import HTTPException,status

router = APIRouter(prefix="/admin", tags=["Admin"])



@router.get("/get_all_users")
async def get_all_users(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    stmt = select(User.id, User.name, User.email, User.role, User.created_at)
    result = await db.execute(stmt)
    users = result.all()
    return [
        {
            "id": u[0],
            "name": u[1],
            "email": u[2],
            "role": u[3],
            "created_at": u[4].isoformat(),
        }
        for u in users
    ]
