from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass

class ItemUpdate(BaseModel):
    """Schema for updating an existing item"""
    name: Optional[str] = None
    description: Optional[str] = None

class ItemResponse(ItemBase):
    """Schema for returning item data in responses"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Chat-related schemas for OpenRouter integration
class ChatRequest(BaseModel):
    """Schema for chat requests to the LLM"""
    prompt: str
    system_message: Optional[str] = "You are a helpful assistant."
    model: Optional[str] = None
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    """Schema for chat responses from the LLM"""
    response: str
    model_used: str

# User-related schemas for Social OS
class UserBase(BaseModel):
    """Base schema for user data"""
    name: str
    bio: Optional[str] = None
    wiki_content: Optional[str] = None

class UserCreate(BaseModel):
    """Schema for creating a new user"""
    user_id: str
    name: str
    bio: Optional[str] = None
    wiki_content: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    name: Optional[str] = None
    bio: Optional[str] = None
    wiki_content: Optional[str] = None

class UserSummary(BaseModel):
    """Schema for user list summary view"""
    user_id: str = Field(serialization_alias="userId")
    name: str
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserResponse(BaseModel):
    """Schema for full user profile response"""
    user_id: str = Field(serialization_alias="userId")
    name: str
    bio: Optional[str] = None
    wiki_content: Optional[str] = Field(default=None, serialization_alias="wikiContent")
    created_at: datetime = Field(serialization_alias="createdAt")
    updated_at: datetime = Field(serialization_alias="updatedAt")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True) 