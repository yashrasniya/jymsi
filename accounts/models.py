from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_superuser(self, mob_number, email='', password=None, **extra_fields):

        if not mob_number:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            mob_number=mob_number
        )
        user.set_password(password)

        user.email = email

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    mob_number = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'mob_number'
    username = ''
    objects = UserManager()
