from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, unique=True)
    email = Column(String(60), unique=True, index=True, nullable=False)
    password = Column(String(60), nullable=False)
    registered_at = Column(DateTime, server_default=func.now())


class Ads(Base):

    __tablename__ = 'ads'
    ads_id = Column(Integer, unique=True, primary_key=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(String(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    owner = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    user = relationship(User, backref="user", cascade="all, delete")
