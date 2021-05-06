from django import forms
from .models import Performers


class PerformersForm(forms.ModelForm):
    class Meta:
        model = Performers
        exclude = ['dr', 'pasdate']


class PerformersAddForm(forms.ModelForm):
    class Meta:
        model = Performers
        fields = ['surname', 'name', 'patronymic', 'birthday', 'pasno', 'paskod', 'pasby', 'pasdate', 'adres',
                  'tel', 'file']

    def __init__(self, *args, **kwargs):
        super(PerformersAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['surname'].widget.attrs.update({'class': 'form-control'})
        self.fields['patronymic'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasno'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasby'].widget.attrs.update({'class': 'form-control'})
        self.fields['paskod'].widget.attrs.update({'class': 'form-control'})
        self.fields['adres'].widget.attrs.update({'class': 'form-control'})
        self.fields['tel'].widget.attrs.update({'class': 'form-control'})
        # self.fields['priseperformeralready'].widget.attrs.update({'class': 'form-control'})
        self.fields['birthday'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['pasdate'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso2', 'autocomplete': 'off'})
        self.fields['file'].widget.attrs.update({'class': 'dropify', 'id': 'input-file-now-custom-1 margin-bottom-20'})
