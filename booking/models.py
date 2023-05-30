from django.db import models


# Create your models here.

class Free_trial(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    gym = models.ForeignKey('gym.Gym', on_delete=models.CASCADE)
    type = models.CharField(choices=(
        ('1', 'Morning'),
        ('2', 'Evening'),
    ), max_length=40)
    date = models.DateField()
    token = models.CharField(max_length=30, null=True)
    valid=models.BooleanField(default=True)