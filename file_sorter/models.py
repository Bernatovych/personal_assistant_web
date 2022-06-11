from django.contrib.auth.models import User
# from django.conf import settings
from django.db import models


def upload_to(instance, filename):
    print( '--- FILES:', '/'.join(['content', instance.user.id, filename]) )
    return '/'.join(['content', instance.user.id, filename])

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    f_name = models.CharField(max_length=255)
    myfiles = models.FileField(upload_to='upload_to/')

    def __str__(self):
        return self.myfiles
