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
        fields = ['project_name', 'project_client_name', 'project_start_date', 'project_end_date', 'project_cost',
                  'project_priority', 'project_status', 'project_summary']
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_client_name', 'project_start_date', 'project_end_date', 'project_cost',
                  'project_priority', 'project_status', 'project_summary']
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ProjectAssignForm(forms.ModelForm):
    class Meta:
        model = ProjectAssign
        fields = ['assignee_type', 'employees']

        employees = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )


class LeaveStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_status']


class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_status']


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title']


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title']


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = TaskAssign
        fields = ['employees']

        employees = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )


class EditProfileInfoForm(forms.ModelForm):
    avatar = forms.ImageField(label='')

    class Meta:
        model = User
        fields = ['username', 'phone', 'dob', 'email', 'address', 'gender', 'date_joined', 'department', 'designation',
                  'technology', 'avatar']
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
        fields = ['primary_name', 'primary_con_relationship', 'primary_phone1', 'primary_phone2', 'secondary_name',
                  'secondary_con_relationship', 'secondary_phone1', 'secondary_phone2']


class EditEmergencyContactForm(forms.ModelForm):
    primary_phone2 = forms.CharField(required=False)
    secondary_phone2 = forms.CharField(required=False)

    class Meta:
        model = Emergency_Contact
        fields = ['primary_name', 'primary_con_relationship', 'primary_phone1', 'primary_phone2', 'secondary_name',
                  'secondary_con_relationship', 'secondary_phone1', 'secondary_phone2']


class AddBankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'bank_account_number', 'bank_ifsc_code', 'user_pan_card_number', 'user_aadhar_card_number']


class EditBankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['bank_name', 'bank_account_number', 'bank_ifsc_code', 'user_pan_card_number', 'user_aadhar_card_number']
