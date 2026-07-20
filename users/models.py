import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The field email is required')
        
        extra_fields.setdefault('is_active', True)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The field is_staff most be True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The field is_superuser most be True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('The field is_active most be True')
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
        
