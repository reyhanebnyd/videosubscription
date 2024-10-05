from django.db import models
from User.models import CustomUser


class Video(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    upload_date = models.DateTimeField(null=False, blank=False)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
