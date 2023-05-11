from django.contrib import admin
from django.contrib.auth.admin import *
from .models import User
# Register your models here.

class User_admin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("mob_number", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mob_number", "password1", "password2"),
            },
        ),
    )
    list_display = ("mob_number", "email", "first_name", "last_name", "is_staff")
    ordering = ("mob_number",)

admin.site.register(User, User_admin)
