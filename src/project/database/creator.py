import asyncio
import logging
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from project.database.models import Base

log = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = "/".join(BASE_DIR.split("/")[:-1])
DB_DIR = "/database"
db_path = os.path.join(BASE_DIR + DB_DIR, "db.db")
async_engine = create_async_engine("sqlite+aiosqlite:///" + db_path)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())
