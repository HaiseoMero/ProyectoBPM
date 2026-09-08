import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session_maker
from app.services.auth_service import authenticate_user
from app.utils.security import verify_password
from app.models import Usuario
from sqlalchemy import select

async def main():
    async with async_session_maker() as db:
        user = await authenticate_user(db, "estudiante@vocalis.cl", "vocalis123")
        if user:
            print(f"Success! User {user.email} authenticated successfully. Role: {user.rol}")
        else:
            print("Authentication failed!")

if __name__ == "__main__":
    asyncio.run(main())
