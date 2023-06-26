import pydantic
from typing import Optional, Type, Union


class CreateUser(pydantic.BaseModel):
    username: str
    password: str

    @pydantic.validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is too short")
        return value


class PatchUser(pydantic.BaseModel):
    username: Optional[str]
    password: Optional[str]

    @pydantic.validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password is too short")
        return value


VALIDATION_CLASS = Union[Type[CreateUser], Type[PatchUser]]
