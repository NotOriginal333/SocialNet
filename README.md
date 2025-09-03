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
│   │   │   ├── feed/                         # Personalized feed & recommendations system 
│   │   │   ├── follows/                      # Follow system (subscriptions)
│   │   │   ├── images/                       # Image storage and processing
│   │   │   ├── interactions/                 # Tracking and managing user interactions (likes, views, etc.)
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

```bash
docker-compose up --build
```

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
* **Flask API Gateway**:    http://localhost:5000

### 4. Testing examples

#### User Registration and Authentication

**Step 1: Create a Public OAuth2 Client**

**URL (Django Admin):** `http://localhost:8000/admin/oauth2_provider/application/`

- **Steps:**
    1. Log in to Django admin.
    2. Navigate to **Applications → Add Application**.
    3. Fill the form:
        - **Name:** `Postman Public Client` (or any descriptive name)
        - **Client type:** `Public`
        - **Authorization grant type:** `Authorization code`
        - **Redirect URIs:** `<your_redirect_uri>` (e.g., `https://oauth.pstmn.io/v1/callback`)
        - **Skip authorization (optional):** unchecked
    4. Save.

**Documentation**: [Django OAuth Toolkit - Applications](https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_01.html#applications)

---

**Step 2: Register a New User** \
**URL**: `POST http://localhost:5000/users/create/` \
**Headers**: \
`Content-Type: application/json`\
**Body**:

```json
  {
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword123",
  "first_name": "John",
  "last_name": "Doe"
}
  ```

**Example (curl)**:

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

**Step 2: Obtain Authorization Code (PKCE Flow)**

**Endpoint**: `GET /o/authorize/`

**Parameters:**

- `client_id`: ID of your public client
- `response_type`: `code`
- `redirect_uri`: must match your client
- `scope`: optional scopes
- `code_challenge`: generated from `code_verifier`
- `code_challenge_method`: `S256`

**Documentation**: [Django OAuth Toolkit – Authorization Code Flow](https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_04.html)

> **Note:** Use your frontend or Postman to initiate this GET request. The response will redirect
> with `code=<auth_code>`.

**Step 3: Exchange Authorization Code for Tokens**

**Endpoint**: `POST /o/token/`  
**Headers**: `Content-Type: application/json`  
**Body Example**:

```json
{
  "grant_type": "authorization_code",
  "client_id": "<your-public-client-id>",
  "code": "<authorization-code-from-step-2>",
  "redirect_uri": "<your-redirect-uri>",
  "code_verifier": "<original-code-verifier>"
} 
```

**Response Example**:

```json
{
  "access_token": "<access-token>",
  "expires_in": 3600,
  "refresh_token": "<refresh-token>",
  "scope": "read write",
  "token_type": "Bearer"
}
```

**Step 4: Use Access Token to Authenticate Requests**

**Add header**: `Authorization: Bearer <access-token>`

**Example GET Request (Postman or Curl)**: 
```bash
curl -X GET http://localhost:5000/posts/ \
  -H "Authorization: Bearer <access-token>"
```

**Notes**

* Auth is powered by **django-oauth-toolkit**.
* All endpoints can go through the Flask API Gateway (localhost:5000), which forwards requests to Django (localhost:8000).

### 5. Media and Image Handling

* In development, media files (e.g. user avatars, post images, thumbnails) are stored locally in **./api/socialnet/media/**.

* For production, it is recommended to use an external storage service (e.g. S3, MinIO).

* Thumbnails are generated asynchronously using Celery.

--- 

### Notes

Django admin panel is available at [/admin/]() (superuser setup required).

You can run management commands with:

``` bash
docker-compose exec api python manage.py createsuperuser
```