"""
Data models for the Simple Social Media API using SQLModel.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


# Database Models (Tables)
class Post(SQLModel, table=True):
    """Post table model."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    username: str = Field(min_length=1, max_length=50, index=True)
    content: str = Field(min_length=1, max_length=2000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    likes_count: int = Field(default=0, ge=0)
    comments_count: int = Field(default=0, ge=0)


class Comment(SQLModel, table=True):
    """Comment table model."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    post_id: str = Field(foreign_key="post.id", index=True)
    username: str = Field(min_length=1, max_length=50, index=True)
    content: str = Field(min_length=1, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Like(SQLModel, table=True):
    """Like table model."""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    post_id: str = Field(foreign_key="post.id", index=True)
    username: str = Field(min_length=1, max_length=50, index=True)
    liked_at: datetime = Field(default_factory=datetime.utcnow)


# Request Models
class NewPostRequest(SQLModel):
    """Request model for creating a new post."""
    username: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=2000)


class UpdatePostRequest(SQLModel):
    """Request model for updating a post."""
    username: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=2000)


class NewCommentRequest(SQLModel):
    """Request model for creating a new comment."""
    username: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=1000)


class UpdateCommentRequest(SQLModel):
    """Request model for updating a comment."""
    username: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=1000)


class LikeRequest(SQLModel):
    """Request model for liking a post."""
    username: str = Field(min_length=1, max_length=50)


# Response Models
class LikeResponse(SQLModel):
    """Response model for like operations."""
    post_id: str
    username: str
    liked_at: datetime


class Error(SQLModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[list[str]] = None
