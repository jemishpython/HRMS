from django import forms

from hrms_api.models import *


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'date_joined', 'department', 'designation', 'technology']
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'technology': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
        }


class AddClientForm(forms.ModelForm):
    client_avatar = forms.ImageField(label='')

    class Meta:
        model = Client
        fields = ['username', 'phone', 'dob', 'address', 'nationality', 'email', 'gender', 'client_avatar', 'company_name', 'position']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class EditClientForm(forms.ModelForm):
    client_avatar = forms.ImageField(label='')

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'active_status': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'client_avatar': forms.ClearableFileInput(attrs={'class': 'form-control', 'type': 'file'}),
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
            'project_client_name': forms.Select(attrs={'class': 'form-control'}),
            'project_priority': forms.Select(attrs={'class': 'form-control'}),
            'project_status': forms.Select(attrs={'class': 'form-control'}),
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_client_name', 'project_start_date', 'project_end_date', 'project_cost', 'project_priority', 'project_status', 'project_summary']
        widgets = {
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
            'project_client_name': forms.Select(attrs={'class': 'form-control'}),
            'project_priority': forms.Select(attrs={'class': 'form-control'}),
            'project_status': forms.Select(attrs={'class': 'form-control'}),
        }


class ProjectAssignForm(forms.ModelForm):
    class Meta:
        model = ProjectAssign
        fields = ['assignee_type', 'employees']
        widgets = {
            'assignee_type': forms.Select(attrs={'class': 'form-control'}),
            'employees': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        employees = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )


class AddProjectImages(forms.ModelForm):
    project_image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "name": "project_image",
        "type": "file",
        "class": "form-control",
        "multiple": True,
    }), label="")

    class Meta:
        model = ProjectImages
        fields = ['project_image']


class AddProjectFiles(forms.ModelForm):
    project_file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "name": "project_file",
        "type": "file",
        "class": "form-control",
        "multiple": True,
    }), label="")

    class Meta:
        model = ProjectFile
        fields = ['project_file']


class LeaveStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_status']
        widgets = {
            'leave_status': forms.Select(attrs={'class': 'form-control'}),
        }


class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_status']
        widgets = {
            'ticket_status': forms.Select(attrs={'class': 'form-control'}),
        }


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
        widgets = {
            'employees': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

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
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'technology': forms.Select(attrs={'class': 'form-control'}),
        }


class EditPersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nationality', 'religion', 'marital_status']
        widgets = {
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
        }


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


class AddPoliciesForm(forms.ModelForm):
    policy_file = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "name": "policy_file",
        "type": "file",
        "class": "form-control",
    }), label="Upload policy file")

    class Meta:
        model = Policies
        fields = ['policy_name', 'policy_department', 'policy_file']


class InterviewerForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "name": "policy_file",
        "type": "file",
        "class": "form-control",
    }), label="Upload Resume")

    class Meta:
        model = Interviewers
        fields = ['name', 'phone', 'dob', 'address', 'email', 'gender', 'city', 'state', 'experience', 'department', 'technology', 'resume', 'current_ctc', 'current_salary', 'expected_salary', 'last_company_name']


class AddInterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = InterviewQuestions
        fields = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer', 'technology', 'department']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'technology': forms.Select(attrs={'class': 'form-control'}),
        }


class EditInterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = InterviewQuestions
        fields = ['question', 'option_a', 'option_b', 'option_c', 'option_d', 'answer', 'technology', 'department']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'technology': forms.Select(attrs={'class': 'form-control'}),
        }


class EditAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'check_in_time', 'check_out_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time', 'step': 'any'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time', 'step': 'any'}),
        }


class AddConditionForm(forms.ModelForm):
    class Meta:
        model = Conditions
        fields = ['condition_title', 'conditional_amount', 'conditional_object']


class EditConditionForm(forms.ModelForm):
    class Meta:
        model = Conditions
        fields = ['condition_title', 'conditional_amount', 'conditional_object']
