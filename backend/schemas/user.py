from pydantic import BaseModel, EmailStr
from typing import List, Optional

# User Schemas
class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(UserBaseSchema):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    

class UserResponseSchema(UserBaseSchema):
    id: int

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None