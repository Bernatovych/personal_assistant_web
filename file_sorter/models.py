from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from pathlib import Path

def upload_to(instance, filename):
    CATEGORIES = {
        'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
        'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
        'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
        'video': ('AVI', 'MP4', 'MOV', 'MKV'),
        'archives': ('ZIP', 'GZ', 'TAR')
    }
    user_subdir = instance.user.username
    p = Path(settings.MEDIA_ROOT, user_subdir)
    ext = Path(filename).suffix[1:]
    for key, value in CATEGORIES.items():
        if ext.upper() in value:
            p = p.joinpath(key)
            break
    return p.joinpath(filename)

class UploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    # f_name = models.CharField(max_length=255)
    loaded_file = models.FileField(upload_to=upload_to)

    def __str__(self):
        return self.loaded_file
