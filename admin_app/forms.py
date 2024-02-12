from django import forms

from hrms_api.models import *


class AddHolidaysForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'


class EditHolidaysForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
