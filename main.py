from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.model import User

app = FastAPI()



@app.get("/")
def root():
    return {"message": "Hello, FastAPI with PostgreSQL is ready!"}

@app.post("/users")
async def create_user(name: str, email: str, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    await db.commit()
    return {"message": "User created"}

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()