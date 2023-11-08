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
    badge_number: str | None = None


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


class EmployeeBase(BaseModel):
    avatar_url: str | None = None
    phone: str | None = None
    job_position: str | None = None
    department: str | None = None
    work_location: str | None = None
    summary: str | None = None


class EmployeeCreate(EmployeeBase):
    managers: list[UUID] = []


class Employee(EmployeeBase):
    id: UUID
    user_id: UUID
    managers: list[User] = []
