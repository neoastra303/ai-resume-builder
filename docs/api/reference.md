# API Documentation

## Authentication

All API endpoints require authentication unless otherwise specified.

### Token Authentication

Obtain an authentication token by sending a POST request to `/api/auth/login/`:

```bash
curl -X POST \
  http://localhost:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

Include the token in subsequent requests:

```bash
curl -H "Authorization: Token your_token_here" \
  http://localhost:8000/api/resumes/
```

## API Endpoints

### Users

#### Get Current User
```
GET /api/users/me/
```

Response:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2025-01-01T00:00:00Z"
}
```

#### Update User Profile
```
PUT /api/users/me/
```

Request:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

### Resumes

#### List Resumes
```
GET /api/resumes/
```

Response:
```json
[
  {
    "id": 1,
    "title": "Software Engineer Resume",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "is_public": false
  }
]
```

#### Create Resume
```
POST /api/resumes/
```

Request:
```json
{
  "title": "My New Resume",
  "template": "tech",
  "is_public": false
}
```

#### Get Resume
```
GET /api/resumes/{id}/
```

#### Update Resume
```
PUT /api/resumes/{id}/
```

#### Delete Resume
```
DELETE /api/resumes/{id}/
```

### Templates

#### List Templates
```
GET /api/templates/
```

Response:
```json
[
  {
    "id": "tech",
    "name": "Tech Professional",
    "description": "Template for technology professionals",
    "preview_url": "/media/templates/tech_preview.png"
  }
]
```

### AI Enhancements

#### Get Content Suggestions
```
POST /api/ai/suggestions/
```

Request:
```json
{
  "text": "Experienced software developer with 5 years of experience",
  "context": "professional_summary"
}
```

Response:
```json
{
  "suggestions": [
    "Results-driven software developer with 5 years of experience in full-stack development",
    "Experienced software engineer specializing in Python and JavaScript technologies"
  ]
}
```

#### Generate Professional Summary
```
POST /api/ai/summary/
```

Request:
```json
{
  "experience": [
    {
      "title": "Senior Developer",
      "company": "Tech Corp",
      "duration": "2 years"
    }
  ],
  "skills": ["Python", "Django", "React"]
}
```

Response:
```json
{
  "summary": "Senior Developer with 2 years of experience at Tech Corp, specializing in Python, Django, and React technologies. Proven track record of delivering scalable web applications."
}
```

## Rate Limiting

API requests are rate-limited to prevent abuse:
- 100 requests per hour for authenticated users
- 10 requests per hour for unauthenticated users

Exceeding these limits will result in a 429 (Too Many Requests) response.

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Webhooks

The API supports webhooks for real-time notifications. Configure webhooks in your user settings.

### Supported Events

- `resume.created`: Fired when a new resume is created
- `resume.updated`: Fired when a resume is updated
- `resume.deleted`: Fired when a resume is deleted

### Webhook Payload

```json
{
  "event": "resume.created",
  "timestamp": "2025-01-01T00:00:00Z",
  "data": {
    "resume_id": 1,
    "title": "New Resume"
  }
}
```

## Versioning

The API is versioned to ensure backward compatibility. The current version is v1.

All API endpoints are prefixed with `/api/v1/`.

## CORS

Cross-Origin Resource Sharing is enabled for the following origins:
- `https://yourdomain.com`
- `https://www.yourdomain.com`

For local development, `http://localhost:3000` is also allowed.

## Pagination

List endpoints support pagination:

```
GET /api/resumes/?page=2&page_size=10
```

Response includes pagination metadata:
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/resumes/?page=3",
  "previous": "http://localhost:8000/api/resumes/?page=1",
  "results": [...]
}
```

## Filtering and Search

List endpoints support filtering and search:

```
GET /api/resumes/?search=developer&ordering=-created_at
```

Supported filters vary by endpoint. See individual endpoint documentation for details.