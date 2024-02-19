from django import forms

from hrms_api.models import *


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'date_joined', 'department', 'designation', 'technology']
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


class AddTechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'


class EditTechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_client_name', 'project_start_date', 'project_end_date', 'project_cost', 'project_priority', 'project_status', 'project_summary']
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_client_name', 'project_start_date', 'project_end_date', 'project_cost', 'project_priority', 'project_status', 'project_summary']
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ProjectAssignForm(forms.ModelForm):
    class Meta:
        model = ProjectAssign
        fields = '__all__'

        employee_name = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title']


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title']
