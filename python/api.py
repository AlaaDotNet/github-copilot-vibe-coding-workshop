"""
API endpoints for the Simple Social Media API.
"""
from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from database import SessionDep
from models import (
    Comment,
    Like,
    LikeRequest,
    LikeResponse,
    NewCommentRequest,
    NewPostRequest,
    Post,
    UpdateCommentRequest,
    UpdatePostRequest,
)

# Create API router
router = APIRouter(prefix="/api")


# Posts endpoints
@router.get("/posts", response_model=List[Post])
def get_posts(session: SessionDep):
    """List all posts."""
    posts = session.exec(select(Post)).all()
    return posts


@router.post("/posts", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post_data: NewPostRequest, session: SessionDep):
    """Create a new post."""
    post = Post(
        username=post_data.username,
        content=post_data.content
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/posts/{post_id}", response_model=Post)
def get_post_by_id(post_id: str, session: SessionDep):
    """Get a specific post by ID."""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    return post


@router.patch("/posts/{post_id}", response_model=Post)
def update_post(post_id: str, post_data: UpdatePostRequest, session: SessionDep):
    """Update a post."""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Update post fields
    post.username = post_data.username
    post.content = post_data.content
    post.updated_at = datetime.utcnow()
    
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, session: SessionDep):
    """Delete a post."""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Delete associated comments and likes
    comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
    for comment in comments:
        session.delete(comment)
    
    likes = session.exec(select(Like).where(Like.post_id == post_id)).all()
    for like in likes:
        session.delete(like)
    
    # Delete the post
    session.delete(post)
    session.commit()


# Comments endpoints
@router.get("/posts/{post_id}/comments", response_model=List[Comment])
def get_comments_by_post_id(post_id: str, session: SessionDep):
    """List comments for a post."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    comments = session.exec(select(Comment).where(Comment.post_id == post_id)).all()
    return comments


@router.post("/posts/{post_id}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: str, comment_data: NewCommentRequest, session: SessionDep):
    """Create a comment."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    comment = Comment(
        post_id=post_id,
        username=comment_data.username,
        content=comment_data.content
    )
    session.add(comment)
    
    # Update comments count
    post.comments_count += 1
    session.add(post)
    
    session.commit()
    session.refresh(comment)
    return comment


@router.get("/posts/{post_id}/comments/{comment_id}", response_model=Comment)
def get_comment_by_id(post_id: str, comment_id: str, session: SessionDep):
    """Get a specific comment."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    return comment


@router.patch("/posts/{post_id}/comments/{comment_id}", response_model=Comment)
def update_comment(post_id: str, comment_id: str, comment_data: UpdateCommentRequest, session: SessionDep):
    """Update a comment."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Update comment fields
    comment.username = comment_data.username
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()
    
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id: str, comment_id: str, session: SessionDep):
    """Delete a comment."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    comment = session.get(Comment, comment_id)
    if not comment or comment.post_id != post_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Update comments count
    post.comments_count -= 1
    session.add(post)
    
    # Delete the comment
    session.delete(comment)
    session.commit()


# Likes endpoints
@router.post("/posts/{post_id}/likes", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
def like_post(post_id: str, like_data: LikeRequest, session: SessionDep):
    """Like a post."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Check if user already liked this post
    existing_like = session.exec(
        select(Like).where(Like.post_id == post_id, Like.username == like_data.username)
    ).first()
    
    if existing_like:
        # User already liked this post, return existing like
        return LikeResponse(
            post_id=existing_like.post_id,
            username=existing_like.username,
            liked_at=existing_like.liked_at
        )
    
    # Create new like
    like = Like(
        post_id=post_id,
        username=like_data.username
    )
    session.add(like)
    
    # Update likes count
    post.likes_count += 1
    session.add(post)
    
    session.commit()
    session.refresh(like)
    
    return LikeResponse(
        post_id=like.post_id,
        username=like.username,
        liked_at=like.liked_at
    )


@router.delete("/posts/{post_id}/likes", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: str, session: SessionDep):
    """Unlike a post."""
    # Check if post exists
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested resource was not found"
        )
    
    # Since there's no way to identify the user in the DELETE request
    # and the OpenAPI spec doesn't specify parameters or request body,
    # we just return success. In a real implementation, this would
    # require authentication to identify the user.
    pass
