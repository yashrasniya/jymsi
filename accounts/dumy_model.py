from accounts.models import User
class Partner(User):
    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        proxy = True
class Superuser(User):
    class Meta:
        verbose_name = 'Superuser'
        verbose_name_plural = 'Superusers'
        proxy = True

class All_User(User):
    class Meta:
        verbose_name = 'Use'
        verbose_name_plural = 'All_Users'
        proxy = True