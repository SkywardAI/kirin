import datetime
from typing import Optional
from pydantic import Field, EmailStr

from src.models.schemas.base import BaseSchemaModel


class AccountInCreate(BaseSchemaModel):
    username: str = Field(..., title="username", description="username")
    email: EmailStr = Field(..., title="email", description="email")
    password: str = Field(..., title="user password", description="Password length 6-20 characters")


class AccountInUpdate(BaseSchemaModel):
    email: Optional[EmailStr] = Field(default=None, title="email", description="email")
    password: Optional[str] = Field(default=None, title="user password", description="Password length 6-20 characters")


class AccountInLogin(BaseSchemaModel):
    username: str = Field(..., title="username", description="username")
    password: str = Field(..., title="user password", description="Password length 6-20 characters")


class AccountWithToken(BaseSchemaModel):
    token: str = Field(..., title="token", description="Auth token")
    username: str = Field(..., title="username", description="username")
    email: EmailStr = Field(..., title="email", description="email")
    is_verified: bool = Field(..., title="Verify", description="Verify true or false")
    is_active: bool = Field(..., title="Active", description="Active true or false")
    is_logged_in: bool = Field(..., title="Logged", description="Logged true or false")
    created_at: datetime.datetime = Field(..., title="Creation time", description="Creation time")
    updated_at: datetime.datetime | None = Field(..., title="Update  time", description="Update time")


class AccountInResponse(BaseSchemaModel):
    id: int
    authorized_account: AccountWithToken

class Account(BaseSchemaModel):
    id: int
    username: str
    email: EmailStr
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_logged_in: Optional[bool] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    _hash_salt: Optional[str] = None
    _hashed_password: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)