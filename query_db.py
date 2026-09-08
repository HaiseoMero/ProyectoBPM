import asyncio
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Usuario

async def main():
    async with async_session_maker() as db:
        result = await db.execute(select(Usuario))
        users = result.scalars().all()
        for u in users:
            print(f"User: {u.email}, Role: {u.rol}, Hash: {u.hashed_password}")

if __name__ == "__main__":
    asyncio.run(main())
