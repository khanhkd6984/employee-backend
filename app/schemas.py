from uuid import UUID
from pydantic import BaseModel


class RoleBase(BaseModel):
    role: str


class Role(RoleBase):
    id: UUID


class UserBase(BaseModel):
    name: str
    email: str
    role_id: UUID


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
