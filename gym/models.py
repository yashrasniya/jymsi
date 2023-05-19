from django.db import models
from accounts.models import User
import datetime
# Create your models here.

class Gym(models.Model):
    gym_name=models.TextField(max_length=100)
    gym_address=models.TextField(max_length=100)
    gym_description=models.TextField(max_length=1000)
    gym_link=models.URLField()
    gym_facilities=models.ManyToManyField('Facilities')
    gym_trainer=models.ManyToManyField('Trainer')
    gym_reviews=models.ManyToManyField('Reviews')

class Facilities(models.Model):
    Facilities_name=models.CharField(max_length=50)
    icon=models.ImageField(upload_to='facilities/icon',blank=False)

class Trainer(models.Model):
    trainer_name=models.CharField(max_length=60)
    trainer_image=models.ImageField(upload_to='Trainer/image')
    trainer_description=models.TextField(max_length=600)

class Reviews(models.Model):
    reviews_text=models.TextField(max_length=1000)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    dateTime=models.DateTimeField(default=datetime.datetime.today())
    rating=(
        ('-----','-----'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
            )
    rating=models.TextField(choices=rating,default='-----')

