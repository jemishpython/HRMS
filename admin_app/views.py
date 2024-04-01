import datetime
import calendar
import uuid

import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.http import JsonResponse
from django.template import loader
from datetime import date

from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from admin_app.forms import AddHolidaysForm, EditHolidaysForm, AddEmployeeForm, AddDepartmentForm, EditDepartmentForm, \
    AddDesignationForm, EditDesignationForm, EditProjectForm, AddProjectForm, ProjectAssignForm, AddTaskForm, \
    EditTaskForm, EditTechnologyForm, AddTechnologyForm, AddExperienceInfoForm, EditProfileInfoForm, \
    EditPersonalInfoForm, AddEducationInfoForm, EditEducationInfoForm, EditExperienceInfoForm, AddEmergencyContactForm, \
    EditEmergencyContactForm, AddBankForm, EditBankForm, TaskAssignForm, LeaveStatusUpdateForm, TicketStatusUpdateForm, \
    AddClientForm, EditClientForm, AddProjectImages, AddProjectFiles, AddPoliciesForm, InterviewerForm, \
    AddInterviewQuestionForm, EditInterviewQuestionForm, EditAttendanceForm, AddConditionForm, EditConditionForm
from hrms_api.choices import LeaveStatusChoice, TicketPriorityChoice, TicketStatusChoice, AttendanceStatusChoice
from hrms_api.models import User, Department, Designation, Holiday, Project, Task, Leave, ProjectAssign, Technology, \
    Education_Info, Experience_Info, Emergency_Contact, Ticket, Bank, Client, ProjectImages, ProjectFile, Policies, \
    Interviewers, InterviewQuestions, InterviewerResult, Attendance, Conditions


def AdminRegister(request):
    if request.method == "POST":
        adminname = request.POST.get('adminname')
        adminphone = request.POST.get('adminphone')
        adminpassword = request.POST.get('adminpassword')
        admin_details = User(admin_name=adminname, phone=adminphone, password=adminpassword)
        admin_details.save()
        return redirect('/admin_login')
    return render(request, "admin/register.html")


def Login(request):
    if request.method == "POST":
        adminphone = request.POST.get('adminphone')
        adminpassword = request.POST.get('adminpassword')
        try:
            user = User.objects.get(phone=adminphone, is_admin=True)
        except Exception as e:
            messages.error(request, "Login user is not Admin.")
            return redirect('Login')
        if user.is_active:
            if user.check_password(adminpassword):
                login(request, user)
                return redirect('AdminIndex')
            messages.error(request, "Invalid credentials")
            return redirect('Login')
        messages.warning(request, "Please wait for admin is approve your request")
        return redirect('Login')
    return render(request, "admin/login.html")


def forget_password_mail(request):
    forget_password_phone = request.POST.get('adminphone')
    user = User.objects.filter(phone=forget_password_phone, is_admin=True, is_active=True).first()

    forget_password_email = user.email

    context = {
        'username': user.username,
        'user_id': user.id,
        'request_url': request.get_host(), #For Liveproject
    }

    from_email = settings.EMAIL_HOST_USER
    mail_subject = f"HRMS Forget Password : {user.username}"

    email = loader.render_to_string('admin/forgot_password_email_template.html', context)
    send_mail(
        subject=mail_subject,
        message=email,
        from_email=from_email,
        recipient_list=[forget_password_email],
        html_message=email,
    )
    return redirect('Login')


def reset_page(request, pk):
    user = User.objects.get(id=pk)
    context = {
        'pk': pk,
        'user_id': user.id,
    }
    return render(request, 'admin/forgot_password.html', context)


def update_password(request, pk):
    user_pass = User.objects.get(id=pk)
    id = user_pass.id
    if request.method == 'POST':
        password = request.POST.get('admin_password')
        conf_password = request.POST.get('admin_confirm_password')
        if password == conf_password:
            user = User.objects.get(id=pk)
            user.password = make_password(password)
            user.save()
            return redirect('Login')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('forgot_password', pk=id)
    else:
        return redirect('Login')


@login_required(login_url="Login")
def AdminIndex(request):
    users = User.objects.all()
    project_list = Project.objects.all()[:5]
    task_list = Task.objects.all()
    client_list = Client.objects.all()[:5]
    new_ticket_list = Ticket.objects.filter(ticket_status=TicketStatusChoice.NEW)[:5]
    new_leaves_list = Leave.objects.filter(leave_status=LeaveStatusChoice.NEW)[:5]
    interviewer_list = Interviewers.objects.all()

    context = {
        'project_list': project_list,
        'task_list': task_list,
        'users': users,
        'client_list': client_list,
        'new_ticket_list': new_ticket_list,
        'new_leaves_list': new_leaves_list,
        'interviewer_list': interviewer_list,
    }
    return render(request, "admin/index.html", context)


@login_required(login_url="Login")
def AdminLogout(request):
    logout(request)
    return redirect('Login')


@login_required(login_url="Login")
def EmployeeView(request):
    employeedetails = User.objects.all()
    return render(request, "admin/employees.html", {'employeedetails': employeedetails})


@login_required(login_url="Login")
def EmployeeListView(request):
    employeedetails = User.objects.all()
    return render(request, "admin/employees_list.html", {'employeedetails': employeedetails})


@login_required(login_url="Login")
def AddEmployee(request):
    form = AddEmployeeForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                add_emp = form.save(commit=False)
                add_emp.password = make_password(form.cleaned_data['password'])
                add_emp.save()
                messages.success(request, 'Employee add successfully')
                return redirect('AdminEmployeeView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_employee.html", context)


@login_required(login_url="Login")
def DeleteEmployee(request, id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    messages.error(request, 'Employee Delete successfully')
    return redirect('AdminEmployeeView')


@login_required(login_url="Login")
def DeleteEmployeeList(id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    messages.error('Employee Delete successfully')
    return redirect('AdminEmployeeListView')


@login_required(login_url="Login")
def ClientsView(request):
    client_list = Client.objects.all()
    context = {
        'client_list': client_list
    }
    return render(request, "admin/clients.html", context)


@login_required(login_url="Login")
def ClientDetailView(request, id):
    client = Client.objects.get(id=id)
    client_project_list = Project.objects.filter(project_client_name=id)
    context = {
        'client': client,
        'client_project_list': client_project_list,
    }
    return render(request, "admin/client-profile.html", context)


@login_required(login_url="Login")
def AddClient(request):
    form = AddClientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Client add successfully')
                return redirect('AdminClientsView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_client.html", context)


@login_required(login_url="Login")
def EditClientInfo(request, id):
    edit_client_info = Client.objects.get(id=id)
    form = EditClientForm(request.POST or None, request.FILES or None, instance=edit_client_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Profile Info Update successfully')
                return redirect('AdminClientDetailView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_client_info': edit_client_info}
    return render(request, "admin/edit_client_info.html", context)


@login_required(login_url="Login")
def ClientDeleteProject(request, id, user_id):
    delete_project = Project.objects.get(id=id)
    delete_project.delete()
    messages.error(request, 'Project Delete successfully')
    return redirect('AdminClientDetailView', id=user_id)


@login_required(login_url="Login")
def DeleteClient(request, id):
    delete_client = Client.objects.get(id=id)
    delete_client.delete()
    messages.error(request, 'Client Delete successfully')
    return redirect('AdminClientsView')


@login_required(login_url="Login")
def ProfileView(request, id):
    profile = User.objects.get(id=id)
    view_education_info = Education_Info.objects.filter(employee=id).order_by('start_year')
    view_experience_info = Experience_Info.objects.filter(employee=id).order_by('start_date')
    view_emergency_contact = Emergency_Contact.objects.filter(employee=id).first()
    view_bank_info = Bank.objects.filter(employee=id).first()

    context = {
        'profile': profile,
        'view_education_info': view_education_info,
        'view_experience_info': view_experience_info,
        'view_emergency_contact': view_emergency_contact,
        'view_bank_info': view_bank_info,
    }
    return render(request, "admin/profile.html", context)


@login_required(login_url="Login")
def EditProfileInfo(request, id):
    edit_profile_info = User.objects.get(id=id)
    form = EditProfileInfoForm(request.POST or None, request.FILES or None, instance=edit_profile_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Profile Info Update successfully')
                return redirect('AdminProfileView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_profile_info': edit_profile_info}
    return render(request, "admin/edit_profile_info.html", context)


@login_required(login_url="Login")
def EditPersonalInfo(request, id):
    edit_personal_info = User.objects.get(id=id)
    form = EditPersonalInfoForm(request.POST or None, instance=edit_personal_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Personal Info Update successfully')
                return redirect('AdminProfileView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_personal_info': edit_personal_info}
    return render(request, "admin/edit_personal_info.html", context)


@login_required(login_url="Login")
def AddEducationInfo(request, id):
    user = User.objects.get(id=id)
    user_id = user.id
    form = AddEducationInfoForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                education = form.save(commit=False)
                education.employee = User.objects.get(id=user_id)
                education.save()
                messages.success(request, 'Education Info Add successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'user_id': user_id}
    return render(request, "admin/add_education_info.html", context)


@login_required(login_url="Login")
def EditEducationInfo(request, id, edu_id):
    user = User.objects.get(id=id)
    user_id = user.id
    edit_education_info = Education_Info.objects.filter(id=edu_id).first()
    form = EditEducationInfoForm(request.POST or None, instance=edit_education_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Education Info Update successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_education_info': edit_education_info, 'user_id': user_id}
    return render(request, "admin/edit_education_info.html", context)


@login_required(login_url="Login")
def DeleteEducation(request, id, edu_id):
    user_id = User.objects.get(id=id)
    delete_edu = Education_Info.objects.get(id=edu_id)
    delete_edu.delete()
    messages.error(request, 'Education information Delete successfully')
    return redirect('AdminProfileView', id=user_id.id)


@login_required(login_url="Login")
def AddExperienceInfo(request, id):
    user = User.objects.get(id=id)
    user_id = user.id
    form = AddExperienceInfoForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                experience = form.save(commit=False)
                experience.employee = User.objects.get(id=user_id)
                experience.save()
                messages.success(request, 'Experience Info Add successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'user_id': user_id}
    return render(request, "admin/add_experience_info.html", context)


@login_required(login_url="Login")
def EditExperienceInfo(request, id, exp_id):
    user = User.objects.get(id=id)
    user_id = user.id
    edit_experience_info = Experience_Info.objects.filter(id=exp_id).first()
    form = EditExperienceInfoForm(request.POST or None, instance=edit_experience_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Experience Info Update successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_experience_info': edit_experience_info, 'user_id': user_id}
    return render(request, "admin/edit_experience_info.html", context)


@login_required(login_url="Login")
def DeleteExperience(request, id, exp_id):
    user_id = User.objects.get(id=id)
    delete_exp = Experience_Info.objects.get(id=exp_id)
    delete_exp.delete()
    messages.error(request, 'Experience information Delete successfully')
    return redirect('AdminProfileView', id=user_id.id)


@login_required(login_url="Login")
def AddEmergencyInfo(request, id):
    user = User.objects.get(id=id)
    user_id = user.id
    form = AddEmergencyContactForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                emergency_contact = form.save(commit=False)
                emergency_contact.employee = User.objects.get(id=user_id)
                emergency_contact.save()
                messages.success(request, 'Experience Info Add successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'user_id': user_id}
    return render(request, "admin/add_emergency_contact.html", context)


@login_required(login_url="Login")
def EditEmergencyInfo(request, id, emg_id):
    user = User.objects.get(id=id)
    user_id = user.id
    edit_emergency_contact = Emergency_Contact.objects.get(id=emg_id)
    form = EditEmergencyContactForm(request.POST or None, instance=edit_emergency_contact)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Experience Info Update successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_emergency_contact': edit_emergency_contact, 'user_id': user_id}
    return render(request, "admin/edit_emergency_contact.html", context)


@login_required(login_url="Login")
def DeleteEmergency(request, id, emg_id):
    user_id = User.objects.get(id=id)
    delete_emg = Emergency_Contact.objects.get(id=emg_id)
    delete_emg.delete()
    messages.error(request, 'Emergency information Delete successfully')
    return redirect('AdminProfileView', id=user_id.id)


@login_required(login_url="Login")
def AddBankInfo(request, id):
    user = User.objects.get(id=id)
    user_id = user.id
    form = AddBankForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                bank_info = form.save(commit=False)
                bank_info.employee = User.objects.get(id=user_id)
                bank_info.save()
                messages.success(request, 'Banke Info Add successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'user_id': user_id}
    return render(request, "admin/add_bank_info.html", context)


@login_required(login_url="Login")
def EditBankInfo(request, id, bank_id):
    user = User.objects.get(id=id)
    user_id = user.id
    edit_bank_info = Bank.objects.get(id=bank_id)
    form = EditBankForm(request.POST or None, instance=edit_bank_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Banke Info Update successfully')
                return redirect('AdminProfileView', id=user_id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_bank_info': edit_bank_info, 'user_id': user_id}
    return render(request, "admin/edit_bank_info.html", context)


@login_required(login_url="Login")
def DeleteBank(request, id, emg_id):
    user_id = User.objects.get(id=id)
    delete_bank = Bank.objects.get(id=emg_id)
    delete_bank.delete()
    messages.error(request, 'Bank information Delete successfully')
    return redirect('AdminProfileView', id=user_id.id)


@login_required(login_url="Login")
def Holidays(request):
    year = date.today()
    holidaylist = Holiday.objects.all().order_by('holiday_date')
    context = {
        'holidaylist': holidaylist,
        'year': year,
    }
    return render(request, "admin/holidays_list.html", context)


@login_required(login_url="Login")
def AddHolidays(request):
    form = AddHolidaysForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Holiday add successfully')
                return redirect('AdminHolidays')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_holidays.html", context)


@login_required(login_url="Login")
def UpdateHolidays(request, id):
    edit_holiday = Holiday.objects.get(id=id)
    form = EditHolidaysForm(request.POST or None, instance=edit_holiday)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Holiday Update successfully')
                return redirect('AdminHolidays')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_holiday': edit_holiday}
    return render(request, "admin/edit_holidays.html", context)


@login_required(login_url="Login")
def DeleteHolidays(request, id):
    delete_holiday = Holiday.objects.get(id=id)
    delete_holiday.delete()
    messages.error(request, 'Holiday Delete successfully')
    return redirect('AdminHolidays')


@login_required(login_url="Login")
def DepartmentView(request):
    departmentlist = Department.objects.all()
    context = {
        'departmentlist': departmentlist,
    }
    return render(request, "admin/departments.html", context)


@login_required(login_url="Login")
def AddDepartment(request):
    form = AddDepartmentForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Department add successfully')
                return redirect('AdminDepartmentView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_department.html", context)


@login_required(login_url="Login")
def UpdateDepartment(request, id):
    edit_department = Department.objects.get(id=id)
    form = EditDepartmentForm(request.POST or None, instance=edit_department)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Department Update successfully')
                return redirect('AdminDepartmentView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_department': edit_department}
    return render(request, "admin/edit_department.html", context)


@login_required(login_url="Login")
def DeleteDepartment(request, id):
    delete_department = Department.objects.get(id=id)
    delete_department.delete()
    messages.error(request, 'Department Delete successfully')
    return redirect('AdminDepartmentView')


@login_required(login_url="Login")
def DesignationView(request):
    designationlist = Designation.objects.all()
    context = {
        'designationlist': designationlist,
    }
    return render(request, "admin/designations.html", context)


@login_required(login_url="Login")
def AddDesignation(request):
    form = AddDesignationForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Designation add successfully')
                return redirect('AdminDesignationView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_designation.html", context)


@login_required(login_url="Login")
def UpdateDesignation(request, id):
    edit_designation = Designation.objects.get(id=id)
    form = EditDesignationForm(request.POST or None, instance=edit_designation)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Designation Update successfully')
                return redirect('AdminDesignationView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_designation': edit_designation}
    return render(request, "admin/edit_designation.html", context)


@login_required(login_url="Login")
def DeleteDesignation(request, id):
    delete_designation = Designation.objects.get(id=id)
    delete_designation.delete()
    messages.error(request, 'Designation Delete successfully')
    return redirect('AdminDesignationView')


@login_required(login_url="Login")
def TechnologyView(request):
    technologylist = Technology.objects.all()
    context = {
        'technologylist': technologylist,
    }
    return render(request, "admin/technology.html", context)


@login_required(login_url="Login")
def AddTechnology(request):
    form = AddTechnologyForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Technology add successfully')
                return redirect('AdminTechnologyView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_technology.html", context)


@login_required(login_url="Login")
def UpdateTechnology(request, id):
    edit_technology = Technology.objects.get(id=id)
    form = EditTechnologyForm(request.POST or None, instance=edit_technology)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Designation Update successfully')
                return redirect('AdminTechnologyView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_technology': edit_technology}
    return render(request, "admin/edit_technology.html", context)


@login_required(login_url="Login")
def DeleteTechnology(request, id):
    delete_technology = Technology.objects.get(id=id)
    delete_technology.delete()
    messages.error(request, 'Technology Delete successfully')
    return redirect('AdminTechnologyView')


@login_required(login_url="Login")
def ProjectsView(request):
    projectlist = Project.objects.all()
    return render(request, "admin/projects.html", {'projectlist': projectlist})


@login_required(login_url="Login")
def AddProject(request):
    form = AddProjectForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Project add successfully')
                return redirect('AdminProjectsView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_project.html", context)


@login_required(login_url="Login")
def AddProjectImage(request, id):
    project_id = Project.objects.get(id=id)
    form = AddProjectImages(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                images = request.FILES.getlist('project_image')
                for image in images:
                    projectimage = ProjectImages(project_name=project_id, project_image=image)
                    projectimage.save()
                messages.success(request, 'Project images add successfully')
                return redirect('AdminProjectDetailsView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'project_id': project_id}
    return render(request, "admin/add_project_images.html", context)


@login_required(login_url="Login")
def AdminDeleteProjectImage(request, id, project_id):
    delete_project_image = ProjectImages.objects.get(id=id)
    delete_project_image.delete()
    messages.error(request, 'Project Image Delete successfully')
    return redirect('AdminProjectDetailsView', id=project_id)


@login_required(login_url="Login")
def AddProjectFile(request, id):
    project_id = Project.objects.get(id=id)
    form = AddProjectFiles(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                files = request.FILES.getlist('project_file')
                for file in files:
                    projectfile = ProjectFile(project_name=project_id, project_file=file)
                    projectfile.save()
                messages.success(request, 'Project files add successfully')
                return redirect('AdminProjectDetailsView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'project_id': project_id}
    return render(request, "admin/add_project_files.html", context)


@login_required(login_url="Login")
def AdminDeleteProjectFile(request, id, project_id):
    delete_project_file = ProjectFile.objects.get(id=id)
    delete_project_file.delete()
    messages.error(request, 'Project file delete successfully')
    return redirect('AdminProjectDetailsView', id=project_id)


@login_required(login_url="Login")
def AddProjectAssignee(request, id):
    users_list = User.objects.all()
    project_id = Project.objects.get(id=id)
    form = ProjectAssignForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                project_assign = form.save(commit=False)
                project_assign.project_name = project_id
                project_assign.save()
                selected_users_ids = request.POST.getlist('employees')
                for user_id in selected_users_ids:
                    user = User.objects.get(id=user_id)
                    project_assign.employees.add(user)
                messages.success(request, 'Project Assign successfully')
                return redirect('AdminProjectDetailsView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'users_list': users_list, 'project_id': project_id}
    return render(request, "admin/add_project_assignee.html", context)


@login_required(login_url="Login")
def DeleteAssignEmployee(request, id, project_id):
    delete_assign_employee = ProjectAssign.objects.filter(employees=id)
    delete_assign_employee.delete()
    messages.error(request, 'Assign Employee Delete successfully')
    return redirect('AdminProjectDetailsView', id=project_id)


@login_required(login_url="Login")
def UpdateProject(request, id):
    edit_project = Project.objects.get(id=id)
    form = EditProjectForm(request.POST or None, instance=edit_project)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Project Update successfully')
                return redirect('AdminProjectDetailsView', id=id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_project': edit_project}
    return render(request, "admin/edit_project.html", context)


@login_required(login_url="Login")
def DeleteProject(request, id):
    delete_project = Project.objects.get(id=id)
    delete_project.delete()
    messages.error(request, 'Project Delete successfully')
    return redirect('AdminProjectsView')


@login_required(login_url="Login")
def ProjectDetailsView(request, id):
    projectdetailview = Project.objects.get(id=id)
    task_list = Task.objects.filter(task_project=id)
    user_list = User.objects.all()
    project_leader_list = ProjectAssign.objects.filter(project_name=id, assignee_type='Leader')
    project_team_member_list = ProjectAssign.objects.filter(project_name=id, assignee_type='Team Member')
    project_images = ProjectImages.objects.filter(project_name=id)
    project_files = ProjectFile.objects.filter(project_name=id)

    context = {
        'projectdetailview': projectdetailview,
        'task_list': task_list,
        'user_list': user_list,
        'project_leader_list': project_leader_list,
        'project_team_member_list': project_team_member_list,
        'project_images': project_images,
        'project_files': project_files,
    }
    return render(request, "admin/project-view.html", context)


@login_required(login_url="Login")
def ProjectTask(request):
    projectlist = Project.objects.all()
    project_id = id

    context = {
        'project_id': project_id,
        'projectlist': projectlist,
    }
    return render(request, "admin/tasks.html", context)


@login_required(login_url="Login")
def ProjectTaskList(request, id):
    projectlist = Project.objects.all()
    project_id = id
    tasklist = Task.objects.filter(task_project=id)
    user_list = User.objects.all()

    context = {
        'project_tasklist': tasklist,
        'project_id': project_id,
        'projectlist': projectlist,
        'user_list': user_list,

    }
    return render(request, "admin/tasks.html", context)


@login_required(login_url="Login")
def AddProjectTask(request, id):
    add_project_id = Project.objects.get(id=id)
    form = AddTaskForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            task.task_project = Project.objects.get(id=id)
            task.save()
            messages.success(request, 'Task added successfully')
            return redirect('AdminProjectTaskList', id=id)
        else:
            messages.error(request, f"Form Not Valid : {form.errors}")
    else:
        form = AddTaskForm()
    context = {'form': form, 'add_project_id': add_project_id}
    return render(request, "admin/add_task.html", context)


@login_required(login_url="Login")
def EditProjectTask(request, id, projectid):
    projectid = Project.objects.get(id=projectid)
    edit_task = Task.objects.get(id=id)
    form = EditTaskForm(request.POST or None, instance=edit_task)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Task Update successfully')
                return redirect('AdminProjectTaskList', id=projectid.id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_task': edit_task, 'projectid': projectid}
    return render(request, "admin/edit_task.html", context)


@login_required(login_url="Login")
def DeleteProjectTask(request, id, projectid):
    project_id = Project.objects.get(id=projectid)
    delete_leave = Task.objects.get(id=id)
    delete_leave.delete()
    messages.error(request, 'Project Task Delete successfully')
    return redirect('AdminProjectTaskList', id=project_id.id)


@login_required(login_url="Login")
def AddTaskAssign(request, id):
    users_list = User.objects.all()
    task_id = Task.objects.get(id=id)
    project_id = Project.objects.get(id=task_id.task_project.id)
    form = TaskAssignForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                task_assign = form.save(commit=False)
                task_assign.task_name = task_id
                task_assign.task_project_name = project_id
                task_assign.save()
                selected_users_ids = request.POST.getlist('employees')
                for user_id in selected_users_ids:
                    user = User.objects.get(id=user_id)
                    task_assign.employees.add(user)
                messages.success(request, 'Task Assign successfully')
                return redirect('AdminProjectTaskList', id=task_id.task_project.id)
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'users_list': users_list, 'task_id': task_id, 'project_id': project_id}
    return render(request, "admin/add_task_assignee.html", context)


@login_required(login_url="Login")
def LeaveList(request):
    leave_list = Leave.objects.all()
    leave_status = LeaveStatusChoice.choices
    context = {
        'leave_list': leave_list,
        'leave_status': leave_status
    }
    return render(request, "admin/leaves.html", context)


@login_required(login_url="Login")
def UpdateLeaveStatus(request, id):
    update_leave_status = Leave.objects.get(id=id)
    form = LeaveStatusUpdateForm(request.POST or None, instance=update_leave_status)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                leave_status_update_email = update_leave_status.leave_user.email

                context = {
                    'username': update_leave_status.leave_user.username,
                    'user_id': update_leave_status.leave_user.id,
                    'leave_status': update_leave_status.leave_status,
                    'leave_type': update_leave_status.leave_type,
                    'leave_from': update_leave_status.leave_from,
                    'leave_to': update_leave_status.leave_to,
                    'leave_days': update_leave_status.leave_days,
                    'current_date': date.today(),
                }

                from_email = settings.EMAIL_HOST_USER

                mail_subject = f"Leave : {update_leave_status.leave_type}"
                email = loader.render_to_string('admin/leave_status_email_template.html', context)
                send_mail(
                    subject=mail_subject,
                    message=email,
                    from_email=from_email,
                    recipient_list=[leave_status_update_email],
                    html_message=email,
                )
                messages.info(request, 'Leave Status Update successfully')
                return redirect('AdminLeaveList')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
                return redirect('AdminLeaveList')
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/update_leave_status.html", {'form': form, 'update_leave_status': update_leave_status})


@login_required(login_url="Login")
def TicketList(request):
    ticket_list = Ticket.objects.all()
    new_tickets_count = ticket_list.filter(ticket_status=TicketStatusChoice.NEW).count()
    approved_tickets_count = ticket_list.filter(ticket_status=TicketStatusChoice.APPROVED).count()
    decline_tickets_count = ticket_list.filter(ticket_status=TicketStatusChoice.DECLINED).count()
    ticket_priority = TicketPriorityChoice.choices
    ticket_status = TicketStatusChoice.choices
    context = {
        'ticket_list': ticket_list,
        'new_tickets_count': new_tickets_count,
        'approved_tickets_count': approved_tickets_count,
        'decline_tickets_count': decline_tickets_count,
        'ticket_priority': ticket_priority,
        'ticket_status': ticket_status,
    }
    return render(request, 'admin/tickets.html', context)


@login_required(login_url="Login")
def UpdateTicketstatus(request, id):
    update_ticket_status = Ticket.objects.get(id=id)
    form = TicketStatusUpdateForm(request.POST or None, instance=update_ticket_status)
    if request.method == 'POST':
        try:
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.ticket_status_update_date = date.today()
                ticket.save()
                ticket_status_update_email = update_ticket_status.ticket_user.email

                context = {
                    'username': update_ticket_status.ticket_user.username,
                    'user_id': update_ticket_status.ticket_user.id,
                    'ticket_status': update_ticket_status.ticket_status,
                    'ticket_create_date': update_ticket_status.ticket_create_date,
                    'ticket_description': update_ticket_status.ticket_description,
                    'ticket_title': update_ticket_status.ticket_title,
                    'current_date': date.today()
                }

                from_email = settings.EMAIL_HOST_USER

                mail_subject = f"Ticket Update : {update_ticket_status.ticket_title}"
                email = loader.render_to_string('admin/ticket_status_email_template.html', context)
                send_mail(
                    subject=mail_subject,
                    message=email,
                    from_email=from_email,
                    recipient_list=[ticket_status_update_email],
                    html_message=email,
                )
                messages.info(request, 'Ticket Status Update successfully')
                return redirect('AdminTicketList')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
                return redirect('AdminTicketList')
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/update_ticket_status.html",
                  {'form': form, 'update_ticket_status': update_ticket_status})


@login_required(login_url="Login")
def ChatView(request):
    user_list = User.objects.all()
    context = {
        'user_list':user_list,
    }
    return render(request, "admin/chat.html", context)


@login_required(login_url="Login")
def Chat(request, id):
    user_list = User.objects.all()
    chat_users = User.objects.get(id=id)
    context = {
        'chat_users': chat_users,
        'user_list': user_list,
    }
    return render(request, "admin/chat.html", context)


@login_required(login_url="Login")
def AttendanceView(request):
    attendances = Attendance.objects.all().order_by('-date')
    context = {
        'attendances': attendances,
        'day_range': range(1, 32),
        'year_range': range(2020, 2031),
    }
    return render(request, "admin/attendance.html", context)


@login_required(login_url="Login")
def AttendanceEdit(request, id):
    edit_attendance = Attendance.objects.get(id=id)
    form = EditAttendanceForm(request.POST or None, instance=edit_attendance)
    if request.method == 'POST':
        try:
            if form.is_valid():
                attendance_update = form.save(commit=False)
                production_time = datetime.datetime.combine(datetime.date.today(),attendance_update.check_out_time) - datetime.datetime.combine(datetime.date.today(), attendance_update.check_in_time)
                if production_time.total_seconds() / 3600 > 5:
                    production_time -= datetime.timedelta(hours=1)
                attendance_update.production_hour = str(production_time)

                half_day_morning_end = datetime.time(13, 0)  # 1 PM
                half_day_evening_start = datetime.time(13, 0)  # 1 PM
                half_day_evening_end = datetime.time(18, 30)  # 6:30 PM
                full_day_start = datetime.time(8, 0)  # 8 AM
                full_day_end = datetime.time(18, 30)  # 6:30 PM

                if attendance_update.check_in_time >= full_day_start and attendance_update.check_out_time <= half_day_morning_end:
                    attendance_update.attendance_status = AttendanceStatusChoice.HALF_DAY
                elif attendance_update.check_in_time >= half_day_evening_start and attendance_update.check_out_time <= half_day_evening_end:
                    attendance_update.attendance_status = AttendanceStatusChoice.HALF_DAY
                elif attendance_update.check_in_time >= full_day_start and attendance_update.check_out_time <= full_day_end:
                    attendance_update.attendance_status = AttendanceStatusChoice.PRESENT
                else:
                    attendance_update.attendance_status = AttendanceStatusChoice.ABSENT

                attendance_update.save()
                messages.info(request, 'Attendance Update successfully')
                return redirect('AdminAttendanceView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_attendance': edit_attendance}
    return render(request, "admin/edit_attendance.html", context)


@login_required(login_url="Login")
def ConditionsView(request):
    conditions = Conditions.objects.all()

    context = {
        'conditions': conditions,
    }
    return render(request, "admin/conditions.html", context)


@login_required(login_url="Login")
def AddConditon(request):
    form = AddConditionForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                conditions = form.save(commit=False)
                conditions.condition_create_date = date.today()
                conditions.save()
                messages.success(request, 'Condition & Rules add successfully')
                return redirect('AdminConditionsView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_condition.html", context)


@login_required(login_url="Login")
def EditCondition(request, id):
    edit_condition = Conditions.objects.get(id=id)
    form = EditConditionForm(request.POST or None, instance=edit_condition)
    if request.method == 'POST':
        try:
            if form.is_valid():
                conditions = form.save(commit=False)
                conditions.condition_create_date = date.today()
                conditions.save()
                messages.info(request, 'Condition & Rules update successfully')
                return redirect('AdminConditionsView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
                messages.error(request, f"ERROR : {e}")
    context = {'form': form, 'edit_condition': edit_condition}
    return render(request, "admin/edit_condition.html", context)


@login_required(login_url="Login")
def DeleteCondition(request, id):
    delete_condition = Conditions.objects.get(id=id)
    delete_condition.delete()
    messages.error(request, 'Condition Delete successfully')
    return redirect('AdminConditionsView')


@login_required(login_url="Login")
def PoliciesView(request):
    policies = Policies.objects.all()

    context = {
        'policies': policies,
    }
    return render(request, "admin/policies.html", context)


@login_required(login_url="Login")
def AddPolicies(request):
    form = AddPoliciesForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                polices = form.save(commit=False)
                polices.policy_create_date = date.today()
                polices.save()
                messages.success(request, 'Policy add successfully')
                return redirect('AdminPoliciesView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    context = {'form': form}
    return render(request, "admin/add_policy.html", context)


@login_required(login_url="Login")
def DeletePolicies(request, id):
    delete_policy = Policies.objects.get(id=id)
    delete_policy.delete()
    messages.error(request, 'Policy Delete successfully')
    return redirect('AdminPoliciesView')


@login_required(login_url="Login")
def InterviewerDash(request):
    interviewer_list = Interviewers.objects.all()

    context = {
        'interviewer_list':interviewer_list,
    }
    return render(request, "admin/interview-dashboard.html", context)


@login_required(login_url="Login")
def InterviewerDetails(request):
    interviewer_list = Interviewers.objects.all()
    data = serialize('json', interviewer_list)

    return JsonResponse(data, safe=False)


def InterviewerApply(request):
    form = InterviewerForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Interviewer data save successfully')
                return redirect('AdminInterviewerDash')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "interviewer_form.html", {'form': form})


@login_required(login_url="Login")
def SendAptitudeTestMail(request, id):
    interviewer_details = Interviewers.objects.get(id=id)
    interviewer_details.aptitude_test_token = str(uuid.uuid4())
    interviewer_details.token_created_at = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    interviewer_details.save()

    forget_password_email = interviewer_details.email

    context = {
        'username': interviewer_details.name,
        'user_id': interviewer_details.id,
        'technology': interviewer_details.technology.id,
        'request_url': request.get_host(), #For Liveproject
        'token': interviewer_details.aptitude_test_token,
    }

    from_email = settings.EMAIL_HOST_USER
    mail_subject = f"HRMS Aptitude Test Link : {interviewer_details.name}"

    email = loader.render_to_string('admin/aptitude_mail_template.html', context)
    send_mail(
        subject=mail_subject,
        message=email,
        from_email=from_email,
        recipient_list=[forget_password_email],
        html_message=email,
    )
    messages.success(request, "Mail Send Successfully")
    return redirect('AdminInterviewerDash')


@login_required(login_url="Login")
def DeleteInterviewer(request, id):
    delete_interviewer = Interviewers.objects.get(id=id)
    delete_interviewer.delete()
    messages.error(request, 'Interviewer Delete successfully')
    return redirect('AdminInterviewerDash')


@login_required(login_url="Login")
def InterviewQuestion(request):
    interview_question_list = InterviewQuestions.objects.all()
    context = {
        'interview_question_list': interview_question_list,
    }
    return render(request, "admin/interview_questions.html",context)


@login_required(login_url="Login")
def AptitudeTestResult(request, id):
    interviewer_results = InterviewerResult.objects.filter(interviewer=id)
    context = {
        'interviewer_results': interviewer_results,
    }
    return render(request, 'admin/interviewer_result.html', context)


@login_required(login_url="Login")
def AddInterviewQuestion(request):
    form = AddInterviewQuestionForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Question add successfully')
                return redirect('AdminInterviewQuestion')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/add_interview_question.html",{'form': form})


@login_required(login_url="Login")
def EditInterviewQuestion(request, id):
    edit_interview_question = InterviewQuestions.objects.get(id=id)
    form = EditInterviewQuestionForm(request.POST or None, instance=edit_interview_question)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.info(request, 'Question edit successfully')
                return redirect('AdminInterviewQuestion')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/edit_interview_question.html",{'form': form, 'edit_interview_question': edit_interview_question})


@login_required(login_url="Login")
def DeleteInterviewQuestion(request, id):
    delete_question = InterviewQuestions.objects.get(id=id)
    delete_question.delete()
    messages.error(request, 'Question Delete successfully')
    return redirect('AdminInterviewQuestion')


@login_required(login_url="Login")
def EmployeeSalarySlip(request):
    user_list = User.objects.all()
    context = {
        'user_list': user_list,
        'day_range': range(1, 32),
        'year_range': range(2020, 2031),
    }
    return render(request, "admin/employee_salary.html", context)