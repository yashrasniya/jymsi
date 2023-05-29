from django.db import models
from accounts.models import User
import datetime


# Create your models here.

class Gym(models.Model):
    gym_name = models.CharField(max_length=100)
    user = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True)
    gym_address = models.TextField(max_length=100)
    gym_state=models.CharField(max_length=50)
    gym_city=models.CharField(max_length=50)
    gym_PinCode=models.CharField(max_length=6)
    gym_mobile_number=models.CharField(max_length=15)
    gym_landLine_number=models.CharField(max_length=15)
    gym_description = models.TextField(max_length=1000)
    gym_images = models.ManyToManyField('Image')
    gym_link = models.URLField()
    gym_facilities = models.ManyToManyField('Facilities')
    gym_trainer = models.ManyToManyField('Trainer')
    gym_reviews = models.ManyToManyField('Reviews')
    gym_timing = models.ForeignKey('Timing', on_delete=models.CASCADE,null=True)
    gym_holiday = models.CharField(max_length=50)
    gym_deals = models.ManyToManyField('Deals')


class Facilities(models.Model):
    Facilities_name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='facilities/icon', blank=False)


class Trainer(models.Model):
    trainer_name = models.CharField(max_length=60)
    trainer_image = models.ImageField(upload_to='Trainer/image')
    trainer_description = models.TextField(max_length=600)


class Reviews(models.Model):
    reviews_text = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(default=datetime.datetime.today())
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


class Timing(models.Model):
    type = models.CharField(choices=(
        ('1', 'Morning'),
        ('2', 'Evening'),
    ), max_length=40)
    opening = models.TimeField(blank=True)
    closing = models.TimeField(blank=True)


class Deals(models.Model):
    months = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    discounted_price = models.CharField(max_length=200)
    discount = models.CharField(max_length=200)


class Image(models.Model):
    image = models.ImageField(upload_to='gym_images')
