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


class EditProfileInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'dob', 'email', 'address', 'gender', 'date_joined', 'department', 'designation', 'technology']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }


class EditPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nationality', 'religion', 'marital_status']


class EditEducationInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nationality', 'religion', 'marital_status']
