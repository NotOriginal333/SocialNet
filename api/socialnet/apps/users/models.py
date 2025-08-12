import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = str(uuid.uuid4())[:30]

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'

        user.save(using=self._db)

        return user


# class AdditionalFields(models.Model):
#     """Additional fields for users accounts."""
#     education = models.CharField(max_length=255, blank=True)
#     workplace = models.CharField(max_length=255, blank=True)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
        ('premium', 'Premium')
    ]
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    # additional = models.ManyToManyField(AdditionalFields)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
