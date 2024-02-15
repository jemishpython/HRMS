from django import forms

from hrms_api.models import *


class AddLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type','leave_from','leave_to','leave_days','leave_reason']
        widgets = {
            'leave_from': forms.DateInput(attrs={'type': 'date'}),
            'leave_to': forms.DateInput(attrs={'type': 'date'}),
        }

class EditLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type','leave_from','leave_to','leave_days','leave_reason']
        widgets = {
            'leave_from': forms.DateInput(attrs={'type': 'date'}),
            'leave_to': forms.DateInput(attrs={'type': 'date'}),
        }
