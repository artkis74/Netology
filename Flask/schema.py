import pydantic
from typing import Optional


class CreateUser(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError('password is too short')
        return value


class PatchUser(pydantic.BaseModel):
    email: Optional[str]
    password: Optional[str]

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError('password is too short')
        return value


class CreateAds(pydantic.BaseModel):
    title: str
    description: str

    @pydantic.validator('title')
    def validate_password(cls, value):
        if len(value) < 3:
            raise ValueError('title is too short')
        return value


class PatchAds(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]

    @pydantic.validator('title')
    def validate_password(cls, value):
        if len(value) < 3:
            raise ValueError('title is too short')
        return value
