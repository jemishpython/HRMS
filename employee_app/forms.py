from django import forms

from hrms_api.models import *


class AddLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'


class EditLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
