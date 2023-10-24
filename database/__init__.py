import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
from asyncio import run

dotenv_path = join(dirname(__file__), 'database.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, autoflush=False, autocommit=False)

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    run(create_database())