from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        db_index=True,
    )
    full_name = models.CharField(
        max_length=128,
        blank=True,
    )
    display_name = models.CharField(
        max_length=64,
        blank=True,
    )
    subscribe_email_updates = models.BooleanField(default=True)

    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_absolute_url(self):
        return f"/users/{self.id}"

    def get_full_name(self):
        return self.full_name

    def get_display_name(self):
        return self.display_name
    
    def getMostRecentComment(self):
        return self.comments.order_by('-created').first().created

    def __str__(self):
        return f"{self.email}"