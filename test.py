from typing import cast
from app.core.security import get_password_hash, verify_password
from sqlalchemy import CursorResult, update


async def test_password_hashing():
    password = "string"
    hash_pwd = "$2b$12$UpdhrLAf8nmy3j48Nm1ZqOS67RtWQYhV0S8PpSsIRFl7RrWx6E/T6"
    # hashed = get_password_hash(password)
    # print(hashed)
    x = verify_password(password, hash_pwd)
    print(x)

async def test_result():
    from app.user.models import User
    from sqlalchemy import select
    from app.core.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        stmt = select(User)
        # print(dir(stmt))
        # print(stmt.columns)
        result = await db.execute(stmt)
        print(result)
        
        print("all",result.all())

        result = await db.execute(stmt)
        print("first",result.first())
        
        stmt1 = select(User).where(User.id == 4)
        result = await db.execute(stmt1)
        print("scalar_one_or_none",result.scalar_one_or_none())

        result = await db.execute(stmt)
        print("scalars",result.scalars())
        result = await db.execute(stmt)
        print("scalars all",result.scalars().all())
        result = await db.execute(stmt)
        print("scalars first",result.scalars().first())

        stmt2 = select(User).where(User.id == 4)
        result = await db.execute(stmt2)
        print("scalars one_or_none",result.scalars().one_or_none())
        
        # user = result.scalar_one_or_none()
        # print(user)

        stmt = update(User).where(User.id>1).values()
        result = await db.execute(stmt)
        print(result.rowcount)

    

if __name__ == "__main__":
    import asyncio
    # asyncio.run(test_password_hashing())
    # 测试分页查询
    asyncio.run(test_result())
