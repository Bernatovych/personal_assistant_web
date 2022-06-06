import django_filters
from note_book.models import Note


class NoteFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(lookup_expr='icontains')
    tag = django_filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:
        model = Note
        fields = ['text', 'tag']


