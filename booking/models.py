from django.db import models


# Create your models here.

class Free_trial(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    booking_ID = models.CharField(max_length=100,null=True)
    gym = models.ForeignKey('gym.Gym', on_delete=models.CASCADE)
    type = models.CharField(choices=(
        ('1', 'Morning'),
        ('2', 'Evening'),
    ), max_length=40)
    date = models.DateField()
    book_datetime = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=30, null=True)
    valid=models.BooleanField(default=True)
    cancel=models.BooleanField(default=False)
    def __str__(self):
        return self.booking_ID
    def date_time(self):
        print(dir(self.type),self.type.title())
        return str(self.date)+" "+str(self.type)