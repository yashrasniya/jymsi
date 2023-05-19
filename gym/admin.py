from django.contrib import admin
from .models import Gym
# Register your models here.
@admin.register(Gym)
class gym(admin.ModelAdmin):
    pass

