from distutils.command.upload import upload
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from pathlib import Path


class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    # f_name = models.CharField(max_length=255)
    loaded_file = models.FileField(blank=False, max_length=500) # upload_to=upload_to,

    def __str__(self):
        return self.loaded_file
