from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User.id, User.name, User.email, User.role, User.created_at)
    result = await db.execute(stmt)
    users = result.all()  # returns list of tuples
    return [
        {"id": u[0], "name": u[1], "email": u[2], "role": u[3], "created_at": u[4]}
        for u in users
    ]
