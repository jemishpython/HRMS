from django import forms

from hrms_api.models import *


class AddLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type',  'leave_from', 'leave_to', 'leave_days', 'leave_reason']
        widgets = {
            'leave_from': forms.DateInput(attrs={'type': 'date'}),
            'leave_to': forms.DateInput(attrs={'type': 'date'}),
        }


class EditLeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'leave_from', 'leave_to', 'leave_days', 'leave_reason']
        widgets = {
            'leave_from': forms.DateInput(attrs={'type': 'date'}),
            'leave_to': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProfileInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone', 'dob', 'email', 'address', 'gender', 'date_joined', 'department', 'designation', 'technology', 'avatar']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }


class EditPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nationality', 'religion', 'marital_status']


class AddEducationInfoForm(forms.ModelForm):
    class Meta:
        model = Education_Info
        fields = ['institution', 'location', 'start_year', 'complete_year', 'degree', 'grade']
        widgets = {
            'start_year': forms.DateInput(attrs={'type': 'date'}),
            'complete_year': forms.DateInput(attrs={'type': 'date'}),
        }


class EditEducationInfoForm(forms.ModelForm):
    class Meta:
        model = Education_Info
        fields = ['institution', 'location', 'start_year', 'complete_year', 'degree', 'grade']
        widgets = {
            'start_year': forms.DateInput(attrs={'type': 'date'}),
            'complete_year': forms.DateInput(attrs={'type': 'date'}),
        }


class AddExperienceInfoForm(forms.ModelForm):
    class Meta:
        model = Experience_Info
        fields = ['company_name', 'location', 'start_date', 'end_date', 'role']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditExperienceInfoForm(forms.ModelForm):
    class Meta:
        model = Experience_Info
        fields = ['company_name', 'location', 'start_date', 'end_date', 'role']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddEmergencyContactForm(forms.ModelForm):
    primary_phone2 = forms.CharField(required=False)
    secondary_phone2 = forms.CharField(required=False)
    class Meta:
        model = Emergency_Contact
        fields = ['primary_name', 'primary_con_relationship', 'primary_phone1', 'primary_phone2', 'secondary_name', 'secondary_con_relationship', 'secondary_phone1', 'secondary_phone2']


class EditEmergencyContactForm(forms.ModelForm):
    primary_phone2 = forms.CharField(required=False)
    secondary_phone2 = forms.CharField(required=False)
    class Meta:
        model = Emergency_Contact
        fields = ['primary_name', 'primary_con_relationship', 'primary_phone1', 'primary_phone2', 'secondary_name', 'secondary_con_relationship', 'secondary_phone1', 'secondary_phone2']
