from django import forms
from .models import Affairs


class AffairsForm(forms.ModelForm):
    class Meta:
        model = Affairs
        exclude = ['prisealready', 'priseperformeralready']


class AffairsAddForm(forms.ModelForm):
    class Meta:
        model = Affairs
        fields = ['name', 'deal', 'date_in', 'date_out', 'customers', 'performer', 'jobcategories', 'prise',
                  'priseperformer', 'deal_status']

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
        self.fields['priseperformer'].widget.attrs.update({'class': 'form-control'})
        # self.fields['prisealready'].widget.attrs.update({'class': 'form-control'})
        # self.fields['priseperformeralready'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_in'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['date_out'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso2', 'autocomplete': 'off'})


class AffairsFiltersForm(forms.ModelForm):
    class Meta:
        model = Affairs
        fields = ['customers']

    def __init__(self, *args, **kwargs):
        super(AffairsFiltersForm, self).__init__(*args, **kwargs)
        self.fields['customers'].widget.attrs.update({'class': 'form-control select2_1'})
