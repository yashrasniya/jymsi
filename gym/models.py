from django.db import models
from accounts.models import User
import datetime
from django.utils import timezone

# Create your models here.

class Gym(models.Model):
    gym_name = models.CharField(max_length=100)
    gym_ID = models.CharField(max_length=100)
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True)
    gym_address = models.TextField(max_length=100)
    gym_state=models.CharField(max_length=50)
    gym_city=models.CharField(max_length=50)
    gym_PinCode=models.CharField(max_length=6)
    gym_mobile_number=models.CharField(max_length=15)
    gym_landLine_number=models.CharField(max_length=15)
    gym_description = models.TextField(max_length=1000)
    gym_images = models.ManyToManyField('Image',blank=True)
    gym_link = models.URLField(max_length=30000)
    gym_facilities = models.ManyToManyField('Facilities',blank=True)
    gym_trainer = models.ManyToManyField('Trainer',blank=True)
    gym_reviews = models.ManyToManyField('Reviews',blank=True)
    gym_timing = models.ManyToManyField('Timing',blank=True)
    gym_holiday = models.CharField(max_length=50)
    gym_deals = models.ManyToManyField('Deals')
    visible=models.BooleanField(default=False)
    def __str__(self):
        return str(self.gym_ID)


class Facilities(models.Model):
    Facilities_name = models.CharField(max_length=50)
    icon = models.FileField(upload_to='facilities/icon', blank=False)
    def __str__(self):
        return self.Facilities_name

class Trainer(models.Model):
    trainer_name = models.CharField(max_length=60)
    trainer_image = models.ImageField(upload_to='Trainer/image')
    trainer_description = models.TextField(max_length=600)

    def gym_id(self):
        gym_obj=Gym.objects.filter(gym_trainer=self)
        if gym_obj:
            return str(gym_obj[0].gym_ID)
        return '---------'
    def __str__(self):
        return self.trainer_name

class Reviews(models.Model):
    reviews_text = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(default=timezone.now())
    rating = (
        ('-----', '-----'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = models.TextField(choices=rating, default='-----')

    # def dateTime(self):
    #     return self.dateTime
    def gym_id(self):
        gym_obj=Gym.objects.filter(gym_reviews=self)
        if gym_obj:
            return str(gym_obj[0].gym_ID)
        return '---------'

class Timing(models.Model):
    type = models.CharField(choices=(
        ('1', 'Morning'),
        ('2', 'Evening'),
    ), max_length=40)
    opening = models.TimeField(blank=True)
    closing = models.TimeField(blank=True)
    def gym_id(self):
        gym_obj=Gym.objects.filter(gym_timing=self)
        if gym_obj:
            return str(gym_obj[0].gym_ID)
        return '---------'

class Deals(models.Model):
    months = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    discounted_price = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)
    def gym_id(self):
        gym_obj=Gym.objects.filter(gym_deals=self)
        if gym_obj:
            return str(gym_obj[0].gym_ID)
        return '---------'

class Image(models.Model):
    image = models.ImageField(upload_to='gym_images')
    def gym_id(self):
        gym_obj=Gym.objects.filter(gym_images=self)
        if gym_obj:
            return str(gym_obj[0].gym_ID)
        return '---------'

class ZYM_read_only_model(Gym):
    class Meta:
        verbose_name = 'gym_read_only'
        verbose_name_plural = 'All_gym_read_only'
        proxy = True