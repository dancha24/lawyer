from django import forms
from performers.models import Performers


class FormForReportGlavLaw(forms.Form):
    date_in = forms.DateField(label='Дата (Начало)')
    date_in_max = forms.DateField(label='Дата (Конец)')
    performer_id = forms.ModelChoiceField(queryset=Performers.objects.all(), to_field_name='pk', label='Исполнитель',
                                          empty_label=None, initial=8)

    def __init__(self, *args, **kwargs):
        super(FormForReportGlavLaw, self).__init__(*args, **kwargs)
        self.fields['date_in'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso', 'autocomplete': 'off'})
        self.fields['date_in_max'].widget.attrs.update(
            {'class': 'form-control', 'id': 'datepicker-autoclose-iso2', 'autocomplete': 'off'})
        self.fields['performer_id'].widget.attrs.update({'class': 'form-control select2_1'})


class FormForReportIspolnitel(forms.Form):
    performer_id = forms.ModelChoiceField(queryset=Performers.objects.all(), to_field_name='pk', label='Исполнитель',
                                          empty_label=None, initial=8)

    def __init__(self, *args, **kwargs):
        super(FormForReportIspolnitel, self).__init__(*args, **kwargs)
        self.fields['performer_id'].widget.attrs.update({'class': 'form-control select2_1'})
