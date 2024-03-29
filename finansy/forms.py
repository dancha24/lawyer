from django import forms
from .models import *


class DateForm(forms.Form):
    gaga = forms.CharField(label='')

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['gaga'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose', 'autocomplete': 'off'})


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        exclude = ['date_in']

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs.update({'class': 'form-control', 'id': 'num'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['category'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_categ'})
        self.fields['deal'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_deal'})
        self.fields['extra_deal'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_extra'})
        self.fields['com'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})


class ReceiptAddOnAffairForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
        exclude = ['date_in', 'deal']

    def __init__(self, af_id=None, *args, **kwargs):
        super(ReceiptAddOnAffairForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs.update({'class': 'form-control', 'id': 'num'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['category'].widget.attrs.update({'class': 'select2_1', 'id': 'id_categ'})
        self.fields['com'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['extra_deal'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_extra'})
        if af_id is not None:
            self.fields['extra_deal'].queryset = ExtraAffairs.objects.filter(affairs_id=af_id)


class ReceiptEditForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['sum', 'type', 'category', 'com', 'date', 'deal', 'extra_deal']

    def __init__(self, *args, **kwargs):
        super(ReceiptEditForm, self).__init__(*args, **kwargs)
        self.fields['sum'].widget.attrs.update({'class': 'form-control', 'id': 'num'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1 margin-bottom-20'})
        self.fields['category'].widget.attrs.update({'class': 'form-control select2_1 margin-bottom-20'})
        self.fields['extra_deal'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_extra'})


class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['sum', 'type', 'category',  'com', 'user_do', 'date', 'deal', 'performers']

    def __init__(self, *args, **kwargs):
        super(SpendingForm, self).__init__(*args, **kwargs)
        self.fields['user_do'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['sum'].widget.attrs.update({'class': 'form-control', 'id': 'num'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['category'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_categ'})
        self.fields['deal'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_deal'})
        self.fields['performers'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_performer'})
        self.fields['com'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})


class SpendingAddOnAffairForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = '__all__'
        exclude = ['deal']

    def __init__(self, af_id=None,  *args, **kwargs):
        super(SpendingAddOnAffairForm, self).__init__(*args, **kwargs)
        self.fields['user_do'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['sum'].widget.attrs.update({'class': 'form-control', 'id': 'num'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['category'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_categ'})
        self.fields['performers'].widget.attrs.update({'class': 'form-control select2_1', 'id': 'id_performer'})
        if af_id is not None:
            self.fields['performers'].queryset = Affairs.objects.get(pk=af_id).performer
        self.fields['com'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})


class SpendingEditForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['date', 'sum', 'type', 'category', 'com']

    def __init__(self, *args, **kwargs):
        super(SpendingEditForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control select2_1 margin-bottom-20'})
        self.fields['category'].widget.attrs.update({'class': 'form-control select2_1 margin-bottom-20'})


class CategorySpe(forms.ModelForm):
    class Meta:
        model = CategoriesOfSpending
        fields = '__all__'


class CategoryRec(forms.ModelForm):
    class Meta:
        model = CategoriesOfReceipt
        fields = '__all__'
