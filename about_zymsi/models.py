from django.db import models

# Create your models here.

class About(models.Model):
    User_mobile_number=models.CharField(max_length=30)
    User_Email=models.EmailField()
    Partner_mobile_number=models.CharField(max_length=30)
    Partner_Email=models.EmailField()
    default_img=models.ImageField(upload_to='about/default')


