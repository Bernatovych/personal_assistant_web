from django.conf import settings
from django.db import models

# Create your models here.

def upload_to(instance, filename):
    return f"{settings.MEDIA_URL.append({instance.user.user.id}).append({filename})}"

class MyUploadFile(models.Model):
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to=upload_to)
