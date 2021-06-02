from django import forms
from .models import Affairs, ExtraAffairs


class AffairsForm(forms.ModelForm):
    class Meta:
        model = Affairs
        fields = "__all__"


class AffairsAddForm(forms.ModelForm):
    class Meta:
        model = Affairs
        fields = ['name', 'deal', 'date_in', 'date_out', 'customers', 'performer', 'jobcategories', 'prise',
                  'deal_status', 'com']

    def __init__(self, *args, **kwargs):
        super(AffairsAddForm, self).__init__(*args, **kwargs)
        self.fields['customers'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['jobcategories'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['performer'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['deal_status'].widget.attrs.update({'class': 'form-control select2_1'})
        # self.fields['prise_status'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['deal'].widget.attrs.update({'class': 'form-control'})
        self.fields['prise'].widget.attrs.update({'class': 'form-control'})
        # self.fields['priseperformer'].widget.attrs.update({'class': 'form-control'})
        # self.fields['prisealready'].widget.attrs.update({'class': 'form-control'})
        # self.fields['priseperformeralready'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_in'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['date_out'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso2', 'autocomplete': 'off'})
        self.fields['com'].widget.attrs.update({'class': 'form-control'})


class ExtraAffairsAddForm(forms.ModelForm):
    class Meta:
        model = ExtraAffairs
        fields = ['name', 'affairs', 'sum', 'comment', 'file', 'deal']

    def __init__(self, *args, **kwargs):
        super(ExtraAffairsAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['affairs'].widget.attrs.update({'class': 'form-control select2_1'})
        self.fields['sum'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['deal'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'dropify', 'id': 'input-file-now-custom-1 margin-bottom-20'})


class ExtraAffairsAddOnAffairsForm(forms.ModelForm):
    class Meta:
        model = ExtraAffairs
        fields = ['name', 'sum', 'comment', 'file', 'deal']

    def __init__(self, *args, **kwargs):
        super(ExtraAffairsAddOnAffairsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['sum'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['deal'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'dropify', 'id': 'input-file-now-custom-1 margin-bottom-20'})


class AffairsFiltersForm(forms.ModelForm):
    class Meta:
        model = Affairs
        fields = ['customers']

    def __init__(self, *args, **kwargs):
        super(AffairsFiltersForm, self).__init__(*args, **kwargs)
        self.fields['customers'].widget.attrs.update({'class': 'form-control select2_1'})
