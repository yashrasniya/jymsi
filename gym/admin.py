from django.contrib import admin
from .models import (Gym, Facilities,
                     Trainer, Reviews,
                     Timing,Image,Deals)


# Register your models here.
class Trainer_admin(admin.TabularInline):
    model = Gym.gym_trainer.through
class Facilities_admin(admin.TabularInline):
    model = Gym.gym_facilities.through
class Reviews_admin(admin.TabularInline):
    model = Gym.gym_reviews.through



@admin.register(Gym)
class gym(admin.ModelAdmin):
    inlines = [Trainer_admin,Facilities_admin,Reviews_admin]
    list_display = ('gym_ID','user','gym_name','visible','gym_city')


@admin.register(Facilities)
class Facilities_admin(admin.ModelAdmin):
    list_display = ('Facilities_name','icon')


@admin.register(Trainer)
class Trainer_admin(admin.ModelAdmin):
    list_display = ('gym_id','trainer_name')


@admin.register(Reviews)
class gym(admin.ModelAdmin):
    list_display = ('user','reviews_text','rating','gym_id')


@admin.register(Image)
class image_admin(admin.ModelAdmin):
    list_display = ('gym_id','image')
@admin.register(Timing)
class timing_admin(admin.ModelAdmin):
    list_display = ('gym_id','type','opening','closing')
@admin.register(Deals)
class Deals_admin(admin.ModelAdmin):
    list_display = ('gym_id','months','price','discounted_price','discount')

