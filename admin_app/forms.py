from django import forms

from hrms_api.models import *


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model= User
        fields = ['username','email','password','phone','date_joined','department','designation']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }


class AddHolidaysForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['holiday_title', 'holiday_date']
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


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class EditDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class AddDesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'


class EditDesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ProjectAssignForm(forms.ModelForm):
    class Meta:
        model = ProjectAssign
        fields = '__all__'
