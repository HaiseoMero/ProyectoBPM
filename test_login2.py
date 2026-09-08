import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.services.auth_service import authenticate_user
from app.utils.security import verify_password, pwd_context
from app.models import Usuario
from sqlalchemy import select

async def main():
    async with async_session_maker() as db:
        user = await authenticate_user(db, "estudiante@vocalis.cl", "vocalis123")
        if user:
            print("Authenticate function returned User!")
        else:
            print("Authenticate function returned None!")
            
        result = await db.execute(select(Usuario).where(Usuario.email == "estudiante@vocalis.cl"))
        u = result.scalar_one_or_none()
        if u:
            print("User found by email:", u.email)
            print("Verifying password manually:", verify_password("vocalis123", u.hashed_password))
        else:
            print("User not found by email in DB!")

if __name__ == "__main__":
    asyncio.run(main())
