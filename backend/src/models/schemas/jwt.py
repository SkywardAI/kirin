from pydantic import BaseModel, EmailStr, Field
import datetime


class JWToken(BaseModel):
    exp: datetime.datetime = Field(..., title="exp", description="exp")
    sub: str = Field(..., title="sub", description="sub")


class JWTAccount(BaseModel):
    username: str = Field(..., title="username", description="username")
    email: EmailStr = Field(..., title="email", description="email")
