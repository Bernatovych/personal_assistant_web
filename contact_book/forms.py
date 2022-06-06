import datetime
from django import forms
from contact_book.models import Contact, Phone, Email


class ContactAddForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birthday']
        years = range(1900, datetime.datetime.now().year + 1)
        widgets = {
            'birthday': forms.SelectDateWidget(years=years)
        }


class PhoneAddForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['phone_number']


class EmailAddForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email']
