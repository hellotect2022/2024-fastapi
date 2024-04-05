import asyncio
import aiomysql
from ..setting.Settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

setting = Settings()

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'username',
    'password': 'password',
    'db': 'dbname',
    'autocommit': True
}


# SQLAlchemy 비동기 엔진 생성
DATABASE_URL = "mysql+aiomysql://{user}:{password}@{host}:{port}/{db}"
engine = create_async_engine(DATABASE_URL.format(**DATABASE_CONFIG))

# 비동기 세션 생성
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_user(username):
    async with aiomysql.create_pool(**DATABASE_CONFIG) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
                user_data = await cur.fetchone()
                if user_data:
                    user = User(id=user_data[0], username=user_data[1], email=user_data[2], password=user_data[3])
                    return user
                else:
                    return None