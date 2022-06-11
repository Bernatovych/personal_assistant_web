
from dataclasses import field, fields
from django import forms
from .models import UploadFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['loaded_file']
        widgets = {
            'loaded_file': forms.ClearableFileInput(attrs={'multiple': True}),
        }
