from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User
from accounts.utils import generate_key


@receiver(pre_save, sender=User)
def create_key(sender, instance, **kwargs):
    # GENERATING THE KEY FOR OTP.
    if not instance.key:
        instance.key = generate_key()
    if not instance.mob_number:
        instance.username = instance.first_name

