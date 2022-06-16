from django import forms
from note_book.models import Note


class NoteAddForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']


class TagAddForm(forms.Form):
    tag = forms.CharField(label='Tag', required=False)


