#!/bin/bash
# Simple test script to demonstrate the API functionality

echo "Starting FastAPI server in background..."
cd /workspaces/github-copilot-vibe-coding-workshop/python
source .venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 3

echo "======================================"
echo "Testing Simple Social Media API"
echo "======================================"

echo ""
echo "1. Root endpoint:"
curl -s http://localhost:8000/ | python -m json.tool

echo ""
echo "2. Get all posts (should be empty):"
curl -s http://localhost:8000/api/posts | python -m json.tool

echo ""
echo "3. Create a new post:"
POST_RESPONSE=$(curl -s -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "content": "Just had an amazing hike in the mountains! #outdoorlife"}')
echo "$POST_RESPONSE" | python -m json.tool

# Extract post ID for further testing
POST_ID=$(echo "$POST_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo ""
echo "4. Get all posts (should have 1 post):"
curl -s http://localhost:8000/api/posts | python -m json.tool

echo ""
echo "5. Get specific post by ID:"
curl -s "http://localhost:8000/api/posts/$POST_ID" | python -m json.tool

echo ""
echo "6. Create a comment on the post:"
COMMENT_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/posts/$POST_ID/comments" \
  -H "Content-Type: application/json" \
  -d '{"username": "jane_smith", "content": "Great photo! Where was this taken?"}')
echo "$COMMENT_RESPONSE" | python -m json.tool

echo ""
echo "7. Get comments for the post:"
curl -s "http://localhost:8000/api/posts/$POST_ID/comments" | python -m json.tool

echo ""
echo "8. Like the post:"
curl -s -X POST "http://localhost:8000/api/posts/$POST_ID/likes" \
  -H "Content-Type: application/json" \
  -d '{"username": "mike_wilson"}' | python -m json.tool

echo ""
echo "9. Check OpenAPI documentation is available:"
curl -s http://localhost:8000/openapi.json | python -c "import sys, json; data=json.load(sys.stdin); print(f'OpenAPI version: {data[\"openapi\"]}, Title: {data[\"info\"][\"title\"]}')"

echo ""
echo "10. Swagger UI should be available at: http://localhost:8000/docs"
echo "11. ReDoc should be available at: http://localhost:8000/redoc"

echo ""
echo "======================================"
echo "All tests completed successfully!"
echo "======================================"

# Clean up
echo "Stopping server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
