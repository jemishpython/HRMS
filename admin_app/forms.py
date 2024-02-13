from django import forms

from hrms_api.models import *


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model= User
        fields = '__all__'


class AddHolidaysForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ('holiday_title', 'holiday_date')
        widgets = {
            'holiday_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditHolidaysForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'holiday_date': forms.DateInput(attrs={'type': 'date'}),
        }
