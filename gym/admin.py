from django.contrib import admin
from .models import (Gym, Facilities,
                     Trainer, Reviews,
                     Timing,Image,Deals,ZYM_read_only_model)
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html




# Register your models here.
class Trainer_admin(admin.TabularInline):
    model = Gym.gym_trainer.through
class Facilities_admin(admin.TabularInline):
    model = Gym.gym_facilities.through
class Reviews_admin(admin.TabularInline):
    model = Gym.gym_reviews.through



@admin.register(Gym)
class gym(admin.ModelAdmin):
    list_display=('gym_ID','partner','gym_name','gym_city','visible')
    list_display_links=('gym_ID',)
    # inlines = [Trainer_admin,Facilities_admin,Reviews_admin]
    search_fields = ('gym_ID','gym_name',
                    'gym_city','gym_address','gym_state',
                    'gym_city','gym_PinCode','gym_mobile_number',
                    'gym_landLine_number','gym_description')
    fields = (

    )
    filter_horizontal=('gym_images','gym_trainer',
                       'gym_reviews','gym_timing',
                       'gym_deals','gym_facilities'
                       )

    def partner(self,obj):
        user=obj.user
        url=''
        mob_number=''
        if user:
            print(dir(obj.user),'sdf')
            url=f"/admin/accounts/all_user/{obj.user.pk}/change/"
            mob_number=user.mob_number
        return format_html('<a href="{}">{}</a>', url, mob_number)

@admin.register(Facilities)
class Facilities_admin(admin.ModelAdmin):
    list_display = ('Facilities_name','icon')
    search_fields = ('Facilities_name',)

@admin.register(Trainer)
class Trainer_admin(admin.ModelAdmin):
    list_display = ('gym_id','trainer_name')
    search_fields = ('gym__gym_ID','trainer_name')


@admin.register(Reviews)
class Reviews(admin.ModelAdmin):
    list_display = ('user','reviews_text','rating','gym_id')
    search_fields = ('gym__gym_ID','reviews_text','user__mob_number')



@admin.register(Image)
class image_admin(admin.ModelAdmin):
    list_display = ('gym_id','image')
    search_fields = ('gym__gym_ID',)

@admin.register(Timing)
class timing_admin(admin.ModelAdmin):
    list_display = ('gym_id','type','opening','closing')
    search_fields = ('gym__gym_ID',)

@admin.register(Deals)
class Deals_admin(admin.ModelAdmin):
    list_display = ('gym_id','months','price','discounted_price','discount')
    search_fields = ('gym__gym_ID','months','price','discounted_price','discount')

@admin.register(ZYM_read_only_model)
class ZYM_read_only(gym):
    def has_change_permission(self,request,obj=None):
        return False
    def has_delete_permission(self,request,obj=None):
        return False



