# API Reference

## Base URL
```
https://api.cloudsync.com/v1
```

## Authentication Header
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

## Endpoints

### Create Sync Job
**POST** `/syncs`

Request:
```json
{
  "name": "My First Sync",
  "source": {
    "type": "s3",
    "bucket": "my-bucket",
    "region": "us-east-1"
  },
  "destination": {
    "type": "gcs",
    "bucket": "my-gcs-bucket",
    "project_id": "my-project"
  },
  "schedule": "hourly",
  "enabled": true
}
```

Response (201 Created):
```json
{
  "id": "sync_abc123",
  "name": "My First Sync",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "last_run": null
}
```

### List Syncs
**GET** `/syncs`

Query Parameters:
- `limit`: Max results (default: 10, max: 100)
- `offset`: Pagination offset (default: 0)
- `status`: Filter by status (active, paused, completed, failed)

Response:
```json
{
  "data": [
    {
      "id": "sync_abc123",
      "name": "My First Sync",
      "status": "active",
      "progress": 45.5
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

### Get Sync Details
**GET** `/syncs/{sync_id}`

Response:
```json
{
  "id": "sync_abc123",
  "name": "My First Sync",
  "status": "running",
  "progress": 45.5,
  "bytes_transferred": 5242880,
  "total_bytes": 11534336,
  "files_transferred": 128,
  "total_files": 256,
  "start_time": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T12:30:00Z"
}
```

### Pause Sync
**POST** `/syncs/{sync_id}/pause`

Response: 200 OK
```json
{
  "id": "sync_abc123",
  "status": "paused"
}
```

### Resume Sync
**POST** `/syncs/{sync_id}/resume`

Response: 200 OK
```json
{
  "id": "sync_abc123",
  "status": "active"
}
```

### Delete Sync
**DELETE** `/syncs/{sync_id}`

Response: 204 No Content

### Get Sync History
**GET** `/syncs/{sync_id}/history`

Response:
```json
{
  "data": [
    {
      "timestamp": "2024-01-15T10:30:00Z",
      "status": "completed",
      "files_transferred": 256,
      "bytes_transferred": 11534336,
      "duration_seconds": 3600
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request",
  "details": "Source bucket must be specified"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "details": "Invalid API key"
}
```

### 404 Not Found
```json
{
  "error": "Not found",
  "details": "Sync with ID sync_abc123 not found"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "request_id": "req_xyz789"
}
```

## Response Status Codes
- **200**: Success
- **201**: Created
- **204**: No Content (successful delete)
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Rate Limited
- **500**: Internal Server Error
- **503**: Service Unavailable
