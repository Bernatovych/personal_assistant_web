import os
from django.contrib.auth.models import User
from django.db import models


CATEGORIES = {
        'images': ('jpeg', 'png', 'jpg', 'svg'),
        'documents': ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'),
        'audio': ('mp3', 'ogg', 'wav', 'amr'),
        'video': ('avi', 'mp4', 'mov', 'mkv'),
        'archives': ('zip', 'gz', 'tar')
    }


def user_directory_path(instance, filename):
    upload_dir = os.path.join('uploads', 'users', str(instance.user.username), filename)
    return upload_dir


def category(filename):
    name, ext = os.path.splitext(filename)
    etx = ext.lstrip('.')
    category = ''
    for key, value in CATEGORIES.items():
        if etx in value:
            category = key
    if not category:
        category = 'other'
    return category


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=200, verbose_name='File name')
    file = models.FileField(upload_to=user_directory_path, verbose_name='File path')
    category = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.name = self.file.name
        self.category = category(self.file.name)
        super().save(*args, **kwargs)
