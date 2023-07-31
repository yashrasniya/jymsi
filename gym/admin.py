from django.contrib import admin
from .models import (Gym, Facilities,
                     Trainer, Reviews,
                     Timing,Image,Deals,ZYM_read_only_model)
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.admin.utils import flatten_fieldsets
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
    # readonly_fields=['gym_ID']
    # inlines = [Trainer_admin,Facilities_admin,Reviews_admin]
    search_fields = ('gym_ID','gym_name',
                    'gym_city','gym_address','gym_state',
                    'gym_city','gym_PinCode','gym_mobile_number',
                    'gym_landLine_number','gym_description')

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

    def get_form(self, request, obj=None, **kwargs):
        fields = []
        if obj:
            for i in obj._meta.local_fields:
                fields.append(i.__str__().split('.')[2])
            for i in obj._meta.local_many_to_many:
                fields.append(i.__str__().split('.')[2])
            if request.user.has_perm('gym.Visible') and not (request.user.is_superuser):
                fields.remove('visible')
                self.readonly_fields = fields
            print(self.readonly_fields, request.user.has_perm('gym.Visible'))

        return super(gym, self).get_form(request, obj, **kwargs)

    # def get_changelist(self, request, **kwargs):
    #     fields = []  # Default fields for everyone
    #     if request.user.has_perm('gym.Visible'):  # Check if User IS in group
    #         fields += ['visible','gym_name']  # Add field that is associated with group to list
    #         self.list_editable = fields
    #     print(self.list_editable,request.user.has_perm('gym.Visible'),request.user)
    #     return super(gym, self).get_changelist(request, **kwargs)

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



