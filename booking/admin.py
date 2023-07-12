from django.contrib import admin
from .models import Free_trial
import datetime
from django.utils.html import format_html
# Register your models here.

@admin.register(Free_trial)
class Free_trial_admin(admin.ModelAdmin):

    list_display = ('booking_ID','gym_ID','user',"date",'status')
    
    def status(self,obj):
        if obj.cancel:
            return 'Cancel'
        if not obj.valid:
            return 'Used'
        is_valid = obj.date - datetime.date.today()
        if is_valid.days >= 0:
            return 'Valid'

        else:
            return 'Expired'

    def gym_ID(self,obj):
        user=obj.gym
        url=''
        mob_number=''
        if user:
            print(dir(obj.user),'sdf')
            url=f"/admin/gym/gym/{obj.gym.pk}/change/"
            mob_number=user.gym_ID
        return format_html('<a href="{}">{}</a>', url, mob_number)
        