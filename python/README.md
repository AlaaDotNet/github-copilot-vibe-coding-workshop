# Simple Social Media API

A FastAPI-based social media backend API built according to the Product Requirements Document. This API allows users to create, retrieve, update, and delete posts; add comments; and like/unlike posts.

## Features

- **Posts Management**: Create, read, update, and delete posts
- **Comments System**: Add, read, update, and delete comments on posts  
- **Likes System**: Like and unlike posts
- **SQLite Database**: Persistent storage with automatic initialization
- **OpenAPI Documentation**: Auto-generated Swagger UI and ReDoc
- **CORS Support**: Enabled for all origins for development

## Project Structure

```
python/
├── main.py           # FastAPI application entry point
├── models.py         # SQLModel data models and schemas
├── database.py       # Database configuration and session management
├── api.py           # API route handlers and business logic
├── sns_api.db       # SQLite database file (created automatically)
├── test_api.sh      # Comprehensive API test script
├── .venv/           # Python virtual environment
└── README.md        # This file
```

## Setup and Installation

1. **Virtual Environment**: Already set up with `uv`
   ```bash
   source .venv/bin/activate
   ```

2. **Dependencies**: Installed via `uv`
   - FastAPI
   - SQLModel (includes SQLAlchemy and Pydantic)
   - Uvicorn (ASGI server)

## Running the Application

### Start the Server

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# Or with auto-reload for development
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc  
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Posts
- `GET /api/posts` - List all posts
- `POST /api/posts` - Create a new post
- `GET /api/posts/{post_id}` - Get a specific post
- `PATCH /api/posts/{post_id}` - Update a post
- `DELETE /api/posts/{post_id}` - Delete a post

### Comments
- `GET /api/posts/{post_id}/comments` - List comments for a post
- `POST /api/posts/{post_id}/comments` - Create a comment
- `GET /api/posts/{post_id}/comments/{comment_id}` - Get a specific comment
- `PATCH /api/posts/{post_id}/comments/{comment_id}` - Update a comment
- `DELETE /api/posts/{post_id}/comments/{comment_id}` - Delete a comment

### Likes
- `POST /api/posts/{post_id}/likes` - Like a post
- `DELETE /api/posts/{post_id}/likes` - Unlike a post

## Example Usage

### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "content": "Just had an amazing hike in the mountains! #outdoorlife"
  }'
```

### Add a Comment
```bash
curl -X POST http://localhost:8000/api/posts/{post_id}/comments \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_smith", 
    "content": "Great photo! Where was this taken?"
  }'
```

### Like a Post
```bash
curl -X POST http://localhost:8000/api/posts/{post_id}/likes \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mike_wilson"
  }'
```

## Testing

Run the comprehensive test script:
```bash
./test_api.sh
```

This script tests all major API functionality including creating posts, comments, and likes.

## Database

- **Type**: SQLite
- **File**: `sns_api.db` 
- **Initialization**: Automatic on application startup
- **Schema**: Defined using SQLModel with proper relationships and constraints

## Architecture

- **Framework**: FastAPI with SQLModel
- **Database ORM**: SQLAlchemy (via SQLModel)
- **Validation**: Pydantic (via SQLModel)
- **ASGI Server**: Uvicorn
- **CORS**: Enabled for all origins
- **Documentation**: Auto-generated OpenAPI 3.1.0 spec

## Compliance

This implementation strictly follows the provided OpenAPI specification and Product Requirements Document:

- ✅ All endpoints implemented as specified
- ✅ Proper HTTP status codes (200, 201, 204, 400, 404, 500)
- ✅ JSON request/response format
- ✅ Data validation and error handling
- ✅ SQLite database with automatic initialization
- ✅ CORS enabled for all origins
- ✅ Port 8000 as specified
- ✅ Swagger UI and OpenAPI documentation
- ✅ No authentication (as specified in requirements)
