from django import forms
from .models import *


class DateForm(forms.ModelForm):
    gaga = forms.CharField(label='')

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['gaga'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose', 'autocomplete': 'off'})
