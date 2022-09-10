from django import forms
from .models import Promocodes


class PromokodAddForm(forms.ModelForm):
    class Meta:
        model = Promocodes
        fields = ['name', 'sale', 'linkpay']

    def __init__(self, *args, **kwargs):
        super(PromokodAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sale'].widget.attrs.update({'class': 'form-control'})
        self.fields['linkpay'].widget.attrs.update({'class': 'form-control'})


class PromokodEditForm(forms.ModelForm):
    class Meta:
        model = Promocodes
        fields = ['name', 'sale', 'linkpay', 'aktive']

    def __init__(self, *args, **kwargs):
        super(PromokodEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sale'].widget.attrs.update({'class': 'form-control'})
        self.fields['linkpay'].widget.attrs.update({'class': 'form-control'})
        self.fields['aktive'].widget.attrs.update({'class': 'form-control'})
