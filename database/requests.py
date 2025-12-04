from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import getenv

engine = create_async_engine(getenv('.env', 'DATABASE'))

async_session = async_sessionmaker()

