import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = True
    DJANGO_BACKEND_URL = os.getenv("DJANGO_BACKEND_URL", "http://localhost:8000")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
