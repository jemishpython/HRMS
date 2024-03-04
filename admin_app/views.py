from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
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
    EditEmergencyContactForm
from hrms_api.models import User, Department, Designation, Holiday, Project, Task, Leave, ProjectAssign, Technology, \
    Education_Info, Experience_Info, Emergency_Contact, Ticket


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
            messages.error(request, "Login user is not Admin.", extra_tags='danger')
            return redirect('Login')
        if user.is_active:
            if user.check_password(adminpassword):
                login(request, user)
                return redirect('AdminIndex')
            messages.error(request, "Invalid credentials", extra_tags='danger')
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
        # 'request_url': request.get_host(), #For Liveproject
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
    projects = Project.objects.all()
    tasks = Task.objects.all()

    context = {
        'projects': projects,
        'tasks': tasks,
        'users': users,
    }
    return render(request, "admin/index.html", context)


@login_required(login_url="Login")
def AdminLogout(request):
    logout(request)
    return render(request, "admin/login.html")


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
        except Exception as e:
            print(e, "-----ERROR-----")
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
def ProfileView(request, id):
    profile = User.objects.get(id=id)
    view_education_info = Education_Info.objects.filter(employee=id).order_by('start_year')
    view_experience_info = Experience_Info.objects.filter(employee=id).order_by('start_date')
    view_emergency_contact = Emergency_Contact.objects.filter(employee=id).first()

    context = {
        'profile': profile,
        'view_education_info': view_education_info,
        'view_experience_info': view_experience_info,
        'view_emergency_contact': view_emergency_contact
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
        except Exception as e:
            form = EditProfileInfoForm(instance=edit_profile_info)
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
        except Exception as e:
            form = EditPersonalInfoForm(instance=edit_personal_info)
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
        except Exception as e:
            form = AddEducationInfoForm()
    context = {'form': form, 'user_id':user_id}
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
        except Exception as e:
            form = EditEducationInfoForm(instance=edit_education_info)
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
        except Exception as e:
            form = AddExperienceInfoForm()
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
        except Exception as e:
            form = EditExperienceInfoForm(instance=edit_experience_info)
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
        except Exception as e:
            form = AddEmergencyContactForm()
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
        except Exception as e:
            form = EditEmergencyContactForm(instance=edit_emergency_contact)
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
def Holidays(request):
    holidaylist = Holiday.objects.all().order_by('holiday_date')
    context = {
        'holidaylist': holidaylist,
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
        except Exception as e:
            form = AddHolidaysForm()
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
        except Exception as e:
            form = EditHolidaysForm(instance=edit_holiday)
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
        except Exception as e:
            form = AddDepartmentForm()
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
        except Exception as e:
            form = EditDepartmentForm(instance=edit_department)
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
        except Exception as e:
            form = AddDesignationForm()
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
        except Exception as e:
            form = EditDesignationForm(instance=edit_designation)
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
        except Exception as e:
            form = AddTechnologyForm()
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
        except Exception as e:
            form = EditTechnologyForm(instance=edit_technology)
    context = {'form': form, 'edit_technology': edit_technology}
    return render(request, "admin/edit_technology.html", context)


@login_required(login_url="Login")
def DeleteTechnology(request, id):
    delete_technology = Technology.objects.get(id=id)
    delete_technology.delete()
    messages.error(request, 'Technology Delete successfully')
    return redirect('AdminTechnologyView')


@login_required(login_url="Login")
def ClientsView(request):
    return render(request, "admin/clients.html")


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
        except Exception as e:
            form = AddProjectForm()
    context = {'form': form}
    return render(request, "admin/add_project.html", context)


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
        except Exception as e:
            messages.error(request, "Invalid credentials")
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

    context = {
        'projectdetailview': projectdetailview,
        'task_list': task_list,
        'user_list': user_list,
        'project_leader_list': project_leader_list,
        'project_team_member_list': project_team_member_list,
    }
    return render(request, "admin/project-view.html", context)


@login_required(login_url="Login")
def ProjectTask(request):
    projectlist = Project.objects.all()
    return render(request, "admin/task-nav.html", {'projectlist': projectlist})


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
        except Exception as e:
            form = EditTaskForm(instance=edit_task)
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
    task_id = Task.objects.get(id=id)
    if request.method == "POST":
        task_assign_add = Task(task_id=task_id.id)
        task_assign_add.save()
        return redirect('AdminProjectTaskList', id=id)
    return render(request, "admin/tasks.html")


@login_required(login_url="Login")
def LeaveList(request):
    leave_list = Leave.objects.all()
    context = {
        'leave_list': leave_list
    }
    return render(request, "admin/leaves.html", context)


@login_required(login_url="Login")
def UpdateLeaveStatus(request, id):
    if request.method == 'POST':
        update_leave_status = request.POST.get('leave_status')
        leave_status_update = Leave.objects.get(id=id)
        leave_status_update.leave_status = update_leave_status
        leave_status_update.save()

        leave_status_update_email = leave_status_update.leave_user.email

        context = {
            'username': leave_status_update.leave_user.username,
            'user_id': leave_status_update.leave_user.id,
            'leave_status': leave_status_update.leave_status,
            'leave_type': leave_status_update.leave_type,
            'leave_from': leave_status_update.leave_from,
            'leave_to': leave_status_update.leave_to,
            'leave_days': leave_status_update.leave_days,
            'current_date': date.today()
            # 'request_url': request.get_host(), #For Liveproject
        }

        from_email = settings.EMAIL_HOST_USER
        mail_subject = f"Leave : {leave_status_update.leave_type}"

        email = loader.render_to_string('admin/leave_status_email_template.html', context)
        send_mail(
            subject=mail_subject,
            message=email,
            from_email=from_email,
            recipient_list=[leave_status_update_email],
            html_message=email,
        )
        messages.info(request, 'Leave status update successfully')
        return redirect('AdminLeaveList')
    return render(request, "admin/leaves.html")


@login_required(login_url="Login")
def AddProjectAssignee(request, id):
    users_list = User.objects.all()
    project_id = Project.objects.get(id=id)
    form = ProjectAssignForm(request.POST or None, instance=project_id)
    if request.method == 'POST':
        try:
            if form.is_valid():
                project_assign = form.save(commit=False)
                selected_users_ids = request.POST.getlist('employee_name')
                for user_id in selected_users_ids:
                    user = User.objects.get(id=user_id)
                    project_assign.employee_name.add(user)
                project_assign.save()
                messages.success(request, 'Project Assign successfully')
                return redirect('AdminProjectDetailsView', id=id)
        except Exception as e:
            form = ProjectAssignForm(instance=project_id)
    context = {'form': form, 'users_list': users_list, 'project_id': project_id}
    return render(request, "admin/add_project_assignee.html", context)


@login_required(login_url="Login")
def TicketList(request):
    ticket_list = Ticket.objects.all()
    context = {
        'ticket_list': ticket_list
    }
    return render(request, 'admin/tickets.html',context)


@login_required(login_url="Login")
def UpdateTicketstatus(request, id):
    if request.method == 'POST':
        update_ticket_status = request.POST.get('ticket_status')
        ticket_status_update = Ticket.objects.get(id=id)
        ticket_status_update.ticket_status = update_ticket_status
        ticket_status_update.ticket_status_update_date = date.today()
        ticket_status_update.save()
        messages.info(request, 'Ticket status update successfully')
        return redirect('AdminTicketList')
    return render(request, "admin/tickets.html")
