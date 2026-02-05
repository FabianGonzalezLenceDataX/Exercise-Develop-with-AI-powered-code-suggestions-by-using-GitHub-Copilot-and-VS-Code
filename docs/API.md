# API Documentation

Complete API reference for the Mergington High School Activities Management System.

## Base URL

```
http://localhost:8000
```

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Root](#root)
  - [Get Activities](#get-activities)
  - [Sign Up for Activity](#sign-up-for-activity)
  - [Unregister from Activity](#unregister-from-activity)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Overview

The API is built using FastAPI and provides a RESTful interface for managing extracurricular activities. All responses are in JSON format unless otherwise specified.

### Interactive Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, the API does not require authentication. Students are identified by their email addresses provided in the request parameters.

## Endpoints

### Root

Redirects to the main application page.

#### Request

```http
GET /
```

#### Response

- **Status Code**: `307 Temporary Redirect`
- **Location**: `/static/index.html`

#### Example

```bash
curl -I http://localhost:8000/
```

```http
HTTP/1.1 307 Temporary Redirect
location: /static/index.html
```

---

### Get Activities

Retrieves all available extracurricular activities with their details.

#### Request

```http
GET /activities
```

#### Response

- **Status Code**: `200 OK`
- **Content-Type**: `application/json`

#### Response Body

```json
{
  "Activity Name": {
    "description": "string",
    "schedule": "string",
    "max_participants": integer,
    "participants": ["string"]
  }
}
```

#### Example

**Request:**
```bash
curl http://localhost:8000/activities
```

**Response:**
```json
{
  "Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": [
      "michael@mergington.edu",
      "daniel@mergington.edu"
    ]
  },
  "Programming Class": {
    "description": "Learn programming fundamentals and build software projects",
    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
    "max_participants": 20,
    "participants": [
      "emma@mergington.edu",
      "sophia@mergington.edu"
    ]
  }
}
```

---

### Sign Up for Activity

Registers a student for an extracurricular activity.

#### Request

```http
POST /activities/{activity_name}/signup?email={student_email}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `activity_name` | string | Yes | The name of the activity (URL encoded) |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | Student's email address |

#### Response

**Success (200 OK):**
```json
{
  "message": "Signed up {email} for {activity_name}"
}
```

**Activity Not Found (404):**
```json
{
  "detail": "Activity not found"
}
```

**Already Signed Up (400):**
```json
{
  "detail": "Student already signed up for this activity"
}
```

#### Example

**Request:**
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=john@mergington.edu"
```

**Response (Success):**
```json
{
  "message": "Signed up john@mergington.edu for Chess Club"
}
```

**Response (Already Registered):**
```json
{
  "detail": "Student already signed up for this activity"
}
```

#### Validation Rules

- Activity name must exist in the system
- Email must be a valid email format
- Student cannot be registered more than once for the same activity
- No limit checking is currently implemented (participants can exceed max_participants)

---

### Unregister from Activity

Removes a student's registration from an activity.

#### Request

```http
DELETE /activities/{activity_name}/unregister?email={student_email}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `activity_name` | string | Yes | The name of the activity (URL encoded) |

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | string | Yes | Student's email address |

#### Response

**Success (200 OK):**
```json
{
  "message": "Unregistered {email} from {activity_name}"
}
```

**Activity Not Found (404):**
```json
{
  "detail": "Activity not found"
}
```

**Not Registered (400):**
```json
{
  "detail": "Student is not registered for this activity"
}
```

#### Example

**Request:**
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=john@mergington.edu"
```

**Response (Success):**
```json
{
  "message": "Unregistered john@mergington.edu from Chess Club"
}
```

**Response (Not Registered):**
```json
{
  "detail": "Student is not registered for this activity"
}
```

---

## Data Models

### Activity

Represents an extracurricular activity.

```typescript
{
  description: string;        // Description of the activity
  schedule: string;          // When the activity takes place
  max_participants: number;  // Maximum allowed participants
  participants: string[];    // Array of student email addresses
}
```

### Activities Database

The application maintains an in-memory dictionary of activities:

```python
activities = {
    "Chess Club": {...},
    "Programming Class": {...},
    "Gym Class": {...},
    "Basketball Team": {...},
    "Soccer Club": {...},
    "Drama Club": {...},
    "Art Workshop": {...},
    "Math Olympiad": {...},
    "Science Club": {...}
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 307 | Temporary Redirect | Root endpoint redirect |
| 400 | Bad Request | Invalid request (duplicate signup, not registered) |
| 404 | Not Found | Activity does not exist |
| 422 | Unprocessable Entity | Validation error (missing parameters) |

### Error Response Format

All errors follow FastAPI's standard error format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Missing Query Parameter:**
```json
{
  "detail": [
    {
      "loc": ["query", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Invalid Activity Name:**
```json
{
  "detail": "Activity not found"
}
```

---

## Examples

### Complete Workflow

**1. Get all activities:**
```bash
curl http://localhost:8000/activities
```

**2. Sign up for an activity:**
```bash
curl -X POST "http://localhost:8000/activities/Basketball%20Team/signup?email=student@mergington.edu"
```

**3. Verify signup by getting activities again:**
```bash
curl http://localhost:8000/activities | jq '.["Basketball Team"].participants'
```

**4. Unregister from activity:**
```bash
curl -X DELETE "http://localhost:8000/activities/Basketball%20Team/unregister?email=student@mergington.edu"
```

### Using with JavaScript

```javascript
// Fetch all activities
const response = await fetch('/activities');
const activities = await response.json();

// Sign up for an activity
const signupResponse = await fetch(
  `/activities/${encodeURIComponent('Chess Club')}/signup?email=${encodeURIComponent('student@mergington.edu')}`,
  { method: 'POST' }
);
const result = await signupResponse.json();

// Unregister from an activity
const unregisterResponse = await fetch(
  `/activities/${encodeURIComponent('Chess Club')}/unregister?email=${encodeURIComponent('student@mergington.edu')}`,
  { method: 'DELETE' }
);
```

### Using with Python

```python
import requests

# Get all activities
response = requests.get('http://localhost:8000/activities')
activities = response.json()

# Sign up for an activity
response = requests.post(
    'http://localhost:8000/activities/Chess Club/signup',
    params={'email': 'student@mergington.edu'}
)
result = response.json()

# Unregister from an activity
response = requests.delete(
    'http://localhost:8000/activities/Chess Club/unregister',
    params={'email': 'student@mergington.edu'}
)
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. However, it's recommended to implement rate limiting in a production environment.

## CORS

CORS (Cross-Origin Resource Sharing) is not currently configured. If accessing the API from a different domain, you'll need to add CORS middleware to the FastAPI application.

## Future Enhancements

Potential API improvements:
- Authentication and authorization
- Pagination for large activity lists
- Filtering and search capabilities
- Participant limit enforcement
- Activity creation and modification endpoints
- Student profile management
- Email validation
- Webhook notifications for signups/unregistrations

---

**Last Updated:** February 5, 2026  
**API Version:** 1.0  
**Maintained by:** Fabián González Lence
