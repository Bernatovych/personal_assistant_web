from django.db import models


class ParseResult(models.Model):
    CHOICES = (
        ('news', 'News'),
        ('weather', 'Weather'),
        ('football', 'Football'),
    )
    url = models.URLField(max_length=300, verbose_name='Url')
    title = models.TextField(verbose_name='Title')
    category = models.CharField(max_length=20, choices=CHOICES)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

