import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.services.auth_service import authenticate_user

async def main():
    async with async_session_maker() as db:
        user = await authenticate_user(db, "estudiante@vocalis.cl", "vocalis123")
        if user:
            print(f"Login successful: {user.email}, role: {user.rol}")
        else:
            print("Login failed")

if __name__ == "__main__":
    asyncio.run(main())
