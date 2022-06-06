from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    text = models.TextField(verbose_name='Note')

    def __str__(self):
        return self.text


class Tag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=50, verbose_name='Tag')

    def __str__(self):
        return self.tag

