import django_filters
from contact_book.models import Contact


class ContactFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='emails__email', lookup_expr='icontains')
    address = django_filters.CharFilter(field_name='addresses__address', lookup_expr='icontains')

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'address']



