from django import forms
from .models import Promocodes, Botset


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


class SetEditForm(forms.ModelForm):
    class Meta:
        model = Botset
        fields = ['name', 'set']

    def __init__(self, *args, **kwargs):
        super(SetEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['set'].widget.attrs.update({'class': 'form-control'})


class GendocDorm(forms.Form):
    city = forms.CharField(label='Город')
    surnameadt = forms.CharField(label='Фамилия арендатора')
    nameadt = forms.CharField(label='Имя арендатора')
    patronymicadt = forms.CharField(label='Отчество арендатора')
    datadradt = forms.CharField(label='Дата рождения арендатора')
    passeradt = forms.CharField(label='Паспорт серия арендатора')
    pasnoadt = forms.CharField(label='Паспорт номер арендатора')
    pasvidanadt = forms.CharField(label='Кем выдан паспорт арендатора')
    pascodpadt = forms.CharField(label='Код подразделения')
    pasdataadt = forms.CharField(label='Дата выдачи')
    propiskaadt = forms.CharField(label='Прописка арендатора')
    adress = forms.CharField(label='Адрес')

    def __init__(self, *args, **kwargs):
        super(GendocDorm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['surnameadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['nameadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['patronymicadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['datadradt'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['passeradt'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasnoadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasvidanadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['pascodpadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasdataadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['propiskaadt'].widget.attrs.update({'class': 'form-control'})
        self.fields['adress'].widget.attrs.update({'class': 'form-control'})
