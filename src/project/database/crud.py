from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from project.database.creator import async_session


async def select_entry(model, pk_value):
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            entry = await session.get(model, pk_value)
            return entry


async def update_entry(entry, **kwargs):
    async with async_session() as session:
        async with session.begin():
            for column, value in kwargs.items():
                setattr(entry, column, value)
            current_db_sessions = session.object_session(entry)
            if current_db_sessions:
                current_db_sessions.add(entry)
            else:
                session.add(entry)
            await session.commit()
            return entry


async def insert_entry(db_model, **kwargs):
    async with async_session() as session:
        async with session.begin():
            entry = db_model(**kwargs)
            session.add(entry)
            await session.commit()
            return entry


async def delete_entry(entry):
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            await session.delete(entry)


async def select_entries(model):
    async with async_session() as session:
        async with session.begin():
            entries = await session.execute(select(model))
            return entries.scalars().all()
