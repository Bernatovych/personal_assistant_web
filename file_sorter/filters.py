import django_filters
from .models import File


class FileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = File
        fields = ['name']


