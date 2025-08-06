from sqlalchemy import Column, Integer, String, Boolean, Date
from app.extensions import db


class User(db.Model):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    role = Column(String(20))
    first_name = Column(String(255))
    last_name = Column(String(255))
    birth_date = Column(Date)
    is_active = Column(Boolean)
    is_staff = Column(Boolean)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
