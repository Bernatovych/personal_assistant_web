from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=50, verbose_name='First name')
    last_name = models.CharField(max_length=50, verbose_name='Last name')
    birthday = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Phone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phones')
    phone_regex = RegexValidator(regex=r'^\+\d{12}$',
                                 message="Phone number must be entered in the format: '+380935671234'."
                                         "12 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13)

    def __str__(self):
        return self.phone_number


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=100, verbose_name='Address')

    def __str__(self):
        return self.address


class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(max_length=50, verbose_name='Email')

    def __str__(self):
        return self.email


