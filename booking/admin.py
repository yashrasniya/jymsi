from django.contrib import admin
from .models import Free_trial
# Register your models here.

@admin.register(Free_trial)
class Free_trial_admin(admin.ModelAdmin):

    list_display = ('booking_ID','gym','user',"date",'type','valid','cancel')