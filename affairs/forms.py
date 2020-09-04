from django import forms
from .models import Affairs


class AffairsForm(forms.ModelForm):

    class Meta:
        model = Affairs
        exclude = ['prisealready', 'priseperformeralready']
