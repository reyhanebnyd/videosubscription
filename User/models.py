from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re
from django.dispatch import receiver
from django.db.models.signals import post_save

def validate_phone_number(value):
    reg = re.compile(r'^(09\d{9}|\+989\d{9}|00989\d{9})$')
    if not reg.match(value) :
        raise ValidationError('Your Phone Number is incorrect')


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number], unique=True, null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.FileField(upload_to='user/profile', max_length=600, blank=True, null=True)  


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()      





