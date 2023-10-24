import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()


engine = create_engine(os.getenv('DSN'))

Session = sessionmaker(bind=engine)

