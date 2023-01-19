from django import forms
from .models import Customers, WhereInfo


class CustomersForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ['dr', 'pasdate']


class InfoAddForm(forms.ModelForm):
    class Meta:
        model = WhereInfo
        exclude = '__all__'

    def __init__(self, *args, **kwargs):
        super(InfoAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})


class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['type', 'pol', 'surname', 'name', 'patronymic', 'dr', 'pasno', 'paskod', 'pasby', 'pasdate',
                  'address', 'tel']

    def __init__(self, *args, **kwargs):
        super(CustomerAddForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['pol'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['surname'].widget.attrs.update({'class': 'form-control'})
        self.fields['patronymic'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasno'].widget.attrs.update({'class': 'form-control'})
        self.fields['pasby'].widget.attrs.update({'class': 'form-control'})
        self.fields['paskod'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['tel'].widget.attrs.update({'class': 'form-control'})
        # self.fields['priseperformeralready'].widget.attrs.update({'class': 'form-control'})
        self.fields['dr'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['pasdate'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        # self.fields['date_out'].widget.attrs.update(
        # {'class': 'form-control', 'id': 'datepicker-autoclose-iso2', 'autocomplete': 'off'})


class CustomerDopPoleForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['adresfiktiv', 'cityfiktiv']

    def __init__(self, *args, **kwargs):
        super(CustomerDopPoleForm, self).__init__(*args, **kwargs)
        self.fields['adresfiktiv'].widget.attrs.update({'class': 'form-control'})
        self.fields['cityfiktiv'].widget.attrs.update({'class': 'form-control'})
