from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# User Schemas

# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base schema for user."""
    email: EmailStr = Field(..., description="The email address of the user.")

# PUBLIC_INTERFACE
class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, description="Password of the user.")

# PUBLIC_INTERFACE
class UserRead(UserBase):
    """Schema for reading user info."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Note Schemas

# PUBLIC_INTERFACE
class NoteBase(BaseModel):
    """Base schema for a note."""
    title: str = Field(..., max_length=255, description="The note's title.")
    content: Optional[str] = Field("", description="Content of the note.")

# PUBLIC_INTERFACE
class NoteCreate(NoteBase):
    """Schema for creating a note."""

# PUBLIC_INTERFACE
class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, max_length=255, description="The note's title.")
    content: Optional[str] = Field(None, description="Content of the note.")

# PUBLIC_INTERFACE
class NoteRead(NoteBase):
    """Schema for reading a note."""
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str

# PUBLIC_INTERFACE
class TokenData(BaseModel):
    """Schema for token data."""
    email: Optional[str] = None
