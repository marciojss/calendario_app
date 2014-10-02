from django import forms
from cal.models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ("creator", "date")
