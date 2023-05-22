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


@admin.register(Facilities)
class gym(admin.ModelAdmin):
    pass


@admin.register(Trainer)
class gym(admin.ModelAdmin):
    pass


@admin.register(Reviews)
class gym(admin.ModelAdmin):
    pass

admin.site.register(Image)
admin.site.register(Timing)
admin.site.register(Deals)