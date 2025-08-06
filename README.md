# SocialNet

This is a scalable backend project built with Django, Django REST Framework, Celery, PostgreSQL, Redis, and a
Flask-based API gateway server.

It is designed to support image processing, user roles, and premium content access — suitable for real-world B2C social
network platforms.

---

## ️ Tech Stack

- **Backend:** Django 5, DRF, Celery, Pillow
- **Proxy / OAuth2:** Flask + Authlib (WIP)
- **Queue:** Redis
- **Database:** PostgreSQL
- **Containerization:** Docker + Docker Compose
- **Images:** Local storage (S3-ready architecture)

## Project Structure
```
├── api/                                      # Main Django backend (SocialNet)
│   ├── Dockerfile                            # Docker image for Django API
│   ├── requirements.txt                      # Python dependencies
│   ├── socialnet/                            # Django project root
│   │   ├── apps/                             # Django apps
│   │   │   ├── comments/                     # Comments module
│   │   │   ├── common/                       # Shared utilities and base classes
│   │   │   ├── follows/                      # Follow system (subscriptions)
│   │   │   ├── images/                       # Image storage and processing
│   │   │   ├── posts/                        # Posts module
│   │   │   ├── users/                        # User management and authentication
│   │   │   └── __init__.py
│   │   ├── config/                           # Project configuration
│   │   ├── fixtures/                         # Data fixtures for testing/dev
│   │   ├── media/                            # User-uploaded media files
│   │   ├── static/                           # Static files
│   │   ├── manage.py                         # Django CLI
│   │   └── __init__.py
│   ├── .dockerignore
│   ├── .gitignore
│   └── __init__.py
│
├── api_gateway/                              # Flask API Gateway + OAuth2 server
│   ├── Dockerfile                            # Docker image for API Gateway
│   ├── requirements.txt                      # Python dependencies
│   ├── wsgi.py                               # WSGI entrypoint for the server
│   ├── app/                                  # Flask application code
│   │   ├── core/                             # Shared utilities, config, DI
│   │   ├── routes/                           # API routes
│   │   │   ├── api_gateway.py                # Gateway logic to Django API
│   │   │   └── __init__.py
│   │   ├── config.py                         # Flask app configuration
│   │   ├── extensions.py                     # Flask extensions initialization
│   │   └── __init__.py
│
├── docker-compose.yml                        # Docker orchestration for local development
├── .env.dev                                  # Local environment variables
├── .env.example                              # Example template for env file
├── .dockerignore
├── .gitignore
├── README.md
```

## Getting Started

---
### 1. Clone the Repository

```bash
git clone https://github.com/NotOriginal333/SocialNet.git
cd SocialNet
cp .env.example .env.dev
```

### 2. Build and Run

```docker-compose up --build```

#### This will start the following containers:

* **socialnet_backend**: Django backend on port **8000**
* **auth_proxy**: Flask proxy on port **5000**
* **postgres_db**: PostgreSQL database on port **5432**
* **redis**: Redis broker on port **6379**
* **celery_default**: Celery worker for default queue
* **celery_follows**: Celery worker for follows queue
* **celery_media**: Celery worker for media queue

### 3. Accessing the Services

* **Django API**:    http://localhost:8000
* **Flask Proxy**:    http://localhost:5000

### 4. Testing examples

#### User Registration and JWT Authentication

* **Step 1: Register a New User** \
  URL: `POST http://localhost:5000/users/create/` \
  Headers: \
  `Content-Type: application/json`\
  Body:
```json
  {
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword123",
  "first_name": "John",
  "last_name": "Doe"
  }
  ```
  Example (curl): 
```bash
  curl -X POST http://localhost:5000/users/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "strongpassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
  ```


* **Step 2: Obtain JWT Token** \
  URL: `POST http://localhost:5000/users/token/` \
  Headers: \
  `Content-Type: application/json` \
  Body: 
```json
  {
  "email": "john@example.com",
  "password": "strongpassword123"
  }
```
  Example (curl): 
```bash
  curl -X POST http://localhost:5000/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
  "email": "john@example.com",
  "password": "strongpassword123"
  }'
   ```
  Expected Response: 
```json
  { 
  "access": "eyJ0eXAiOiJKV1QiLCJh...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJi..."
  }
```
* **Step 3: Access Protected User Info** \
  URL: `GET http://localhost:5000/users/me/` \
  Headers: \
  `Authorization: Bearer <your_access_token>` \
  Example (curl): 
```bash
  curl -X GET http://localhost:5000/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJh..."
  ``` 
  Expected Response: 
```json
  {
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "first_name": "John",
  "last_name": "Doe",
  "birth_date": null
  }
```

* **Step 4: Refresh Access Token** \
  URL: `POST http://localhost:5000/users/token/refresh/` \
  Headers: \
  `Content-Type: application/json` \
  Body: 
```json
  {
   "refresh": "<your_refresh_token>"
  }
```
  Example (curl): 
```bash
  `curl -X POST http://localhost:5000/users/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
  "refresh": "eyJ0eXAiOiJKV1QiLCJi..."
  }'
  ```
  Expected Response: 
```json
  {
  "access": "eyJ0eXAiOiJKV1QiLCJh..."
  }
  ```

* **Postman Quick Guide**
    * Create a new user at **POST /users/create/**
    * Authenticate via **POST /users/token/** to receive access and refresh tokens.
    * Use the access token in headers as: `Authorization: Bearer <access_token>`
    * Refresh tokens via **POST /users/token/refresh/** when the access token expires.

**Notes**

* Auth is powered by **djangorestframework-simplejwt**.
* All endpoints go through the Flask proxy (localhost:5000), which forwards requests to Django (localhost:8000).

### 5. Media and Image Handling

* In development, media files (e.g. user avatars, post images, thumbnails) are stored locally in *
  *./api/socialnet/media/**.

* For production, it is recommended to use an external storage service (e.g. S3, MinIO).

* Thumbnails are generated asynchronously using Celery.

--- 

### Notes

Django admin panel is available at [/admin/]() (superuser setup required).

You can run management commands with:
`docker-compose exec api python manage.py createsuperuser`