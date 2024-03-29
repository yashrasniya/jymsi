from django.contrib import admin
from django.contrib.auth.admin import *
from .models import User
from .dumy_model import Superuser,Partner,All_User
from django.db.models import Q
# Register your models here.
@admin.register(User)
class User_admin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("mob_number", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email",'user_ID','profile_img')}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_partner",
                    "mobile_verify",
                    # "user_permissions",
                ),
            },
        ),
        # (("Important dates"), {"fields": ("last_login", "date_joined")}),
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
    list_display = ("mob_number", "name","is_active",'email')
    search_fields=('mob_number','user_ID', "first_name", "last_name", "email")
    ordering = ("mob_number",)
    def get_queryset(self, request):
        return self.model.objects.filter(is_superuser=False,is_partner=False,is_staff=False)

@admin.register(Partner)
class partner(User_admin):
    def get_queryset(self, request):
        return self.model.objects.filter(is_partner=True)
@admin.register(Superuser)
class admin_users(User_admin):
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
                    "is_partner",
                    "user_permissions",
                    "groups",
                ),
            },
        ),
        # (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display=("mob_number", "name","is_superuser","is_staff",'email')
    def get_queryset(self, request):
        return self.model.objects.filter(Q(is_superuser=True)| Q(is_staff=True))

class AllUserAdmin(User_admin):
    def get_queryset(self, request):
        return self.model.objects.all()
admin.site.register(All_User,AllUserAdmin)
