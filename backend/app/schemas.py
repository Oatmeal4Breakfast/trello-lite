from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class UserRead(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BoardBase(BaseModel):
    title: str
    description: str | None = None

class BoardCreate(BoardBase):
    owner_id: int

class BoardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class BoardRead(BoardBase):
    id: int
    owner_id: int

    model_config = {
        "from_attributes": True
    }

class ListBase(BaseModel):
    title: str
    board_id: int

class ListCreate(ListBase):
    pass

class ListUpdate(BaseModel):
    title: str | None = None

class ListRead(ListBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class CardBase(BaseModel):
    title: str
    description: str | None = None
    list_id: int
    position: int
    due_date: datetime | None = None

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    position: int | None = None
    due_date: datetime | None = None

class CardRead(CardBase):
    id: int

    model_config = {
        "from_attributes": True
    }