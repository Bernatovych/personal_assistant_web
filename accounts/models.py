from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    period = models.IntegerField(validators=[MaxValueValidator(365), MinValueValidator(1)],
                                 verbose_name='Birthday in period', default=7)
    is_news = models.BooleanField(default=False, verbose_name='News')
    is_weather = models.BooleanField(default=False, verbose_name='Weather')
    is_exchange_rate = models.BooleanField(default=False, verbose_name='Exchange Rate')
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()