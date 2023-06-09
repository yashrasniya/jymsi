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
    user_ID = models.CharField(max_length=100,null=True)

    key = models.CharField(max_length=64)
    profile_img=models.ImageField(upload_to="user/profile",blank=True)
    USERNAME_FIELD = 'mob_number'
    username = ''
    is_partner=models.BooleanField(default=False)
    objects = UserManager()

    def name(self):
        return f"{self.first_name} {self.last_name}"


class Partner(User):
    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        proxy = True
class Superuser(User):
    class Meta:
        verbose_name = 'Superuser'
        verbose_name_plural = 'Superusers'
        proxy = True

class All_User(User):
    class Meta:
        verbose_name = 'Use'
        verbose_name_plural = 'All_Users'
        proxy = True