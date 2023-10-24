import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()


engine = create_async_engine(os.getenv('DSN'))

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
