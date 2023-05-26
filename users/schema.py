import enum

from uuid import uuid4
from sqlalchemy import Column, Integer
from sqlalchemy_utils import ChoiceType
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class LoginForm(SQLModel):
    username: str
    password: str


class UserRoleEnum(enum.Enum):
    admin = 'ADMIN'
    user  = 'USER'


class UserBase(SQLModel):
    username: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(default=None, unique=True, index=True)
    password: Optional[str] = Field(default=None)
    email: str = Field(default=None, unique=True, index=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    active: bool = Field(default=True)
    verified: bool = Field(default=False)
    verify_code: str = Field(default=uuid4().__str__())

    """ Enum, вместо нормализованной таблицы. TODO: Нормализовать """
    role: UserRoleEnum = Field(default= UserRoleEnum.user,
                               sa_column=Column(ChoiceType(UserRoleEnum), nullable=False))

    journals: list["Journal"] = Relationship(back_populates='owner')


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int






