from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect

from admin_app.forms import AddHolidaysForm, EditHolidaysForm, AddEmployeeForm, AddDepartmentForm, EditDepartmentForm, \
    AddDesignationForm, EditDesignationForm, EditProjectForm, AddProjectForm, ProjectAssignForm, AddTaskForm, \
    EditTaskForm, EditTechnologyForm, AddTechnologyForm, AddExperienceInfoForm, EditProfileInfoForm, \
    EditPersonalInfoForm, AddEducationInfoForm, EditEducationInfoForm, EditExperienceInfoForm, AddEmergencyContactForm, \
    EditEmergencyContactForm
# Create your views here.
from hrms_api.models import User, Department, Designation, Holiday, Project, Task, Leave, ProjectAssign, Technology, \
    Education_Info, Experience_Info, Emergency_Contact


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
            user = User.objects.get(phone=adminphone)
        except:
            messages.error(request, "Invalid credentials")
            return redirect('AdminLogin')
        if user.is_active:
            if user.check_password(adminpassword):
                login(request, user)
                return redirect('AdminIndex')
            messages.error(request, "Invalid credentials")
            return redirect('AdminLogin')
        messages.error(request, "Please wait for admin is approve your request")
        return redirect('AdminLogin')
    return render(request, "admin/login.html")


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


def AdminLogout(request):
    logout(request)
    return render(request, "admin/login.html")


def EmployeeView(request):
    employeedetails = User.objects.all()
    return render(request, "admin/employees.html", {'employeedetails': employeedetails})


def EmployeeListView(request):
    employeedetails = User.objects.all()
    return render(request, "admin/employees_list.html", {'employeedetails': employeedetails})


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
            form = AddEmployeeForm()
    context = {'form': form}
    return render(request, "admin/add_employee.html", context)


def DeleteEmployee(request, id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    return redirect('AdminEmployeeView')


def DeleteEmployeeList(id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    return redirect('AdminEmployeeListView')


def ProfileView(request, id):
    profile = User.objects.get(id=id)
    view_education_info = Education_Info.objects.filter(employee=id).order_by('start_year')
    view_experience_info = Experience_Info.objects.filter(employee=id).order_by('start_date')
    view_emergency_contact = Emergency_Contact.objects.get(employee=id)

    context = {
        'profile': profile,
        'view_education_info': view_education_info,
        'view_experience_info': view_experience_info,
        'view_emergency_contact': view_emergency_contact
    }
    return render(request, "admin/profile.html", context)


def EditProfileInfo(request, id):
    edit_profile_info = User.objects.get(id=id)
    form = EditProfileInfoForm(request.POST or None, instance=edit_profile_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Info Update successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = EditProfileInfoForm(instance=edit_profile_info)
    context = {'form': form, 'edit_profile_info': edit_profile_info}
    return render(request, "admin/edit_profile_info.html", context)


def EditPersonalInfo(request, id):
    edit_personal_info = User.objects.get(id=id)
    form = EditPersonalInfoForm(request.POST or None, instance=edit_personal_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Personal Info Update successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = EditPersonalInfoForm(instance=edit_personal_info)
    context = {'form': form, 'edit_personal_info': edit_personal_info}
    return render(request, "admin/edit_personal_info.html", context)


def AddEducationInfo(request, id):
    form = AddEducationInfoForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                education = form.save(commit=False)
                education.employee = User.objects.get(id=id)
                education.save()
                messages.success(request, 'Education Info Add successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = AddEducationInfoForm()
    context = {'form': form}
    return render(request, "admin/add_education_info.html", context)


def EditEducationInfo(request, id, edu_id):
    edit_education_info = Education_Info.objects.filter(id=edu_id).first()
    form = EditEducationInfoForm(request.POST or None, instance=edit_education_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                education = form.save(commit=False)
                education.employee = User.objects.get(id=id)
                education.save()
                messages.success(request, 'Education Info Update successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = EditEducationInfoForm(instance=edit_education_info)
    context = {'form': form, 'edit_education_info': edit_education_info}
    return render(request, "admin/edit_education_info.html", context)


def AddExperienceInfo(request, id):
    form = AddExperienceInfoForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                experience = form.save(commit=False)
                experience.employee = User.objects.get(id=id)
                experience.save()
                messages.success(request, 'Experience Info Add successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = AddExperienceInfoForm()
    context = {'form': form}
    return render(request, "admin/add_experience_info.html", context)


def EditExperienceInfo(request, id, exp_id):
    edit_experience_info = Experience_Info.objects.filter(id=exp_id).first()
    form = EditExperienceInfoForm(request.POST or None, instance=edit_experience_info)
    if request.method == 'POST':
        try:
            if form.is_valid():
                experience = form.save(commit=False)
                experience.employee = User.objects.get(id=id)
                experience.save()
                messages.success(request, 'Experience Info Update successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = EditExperienceInfoForm(instance=edit_experience_info)
    context = {'form': form, 'edit_experience_info': edit_experience_info}
    return render(request, "admin/edit_experience_info.html", context)


def AddEmergencyInfo(request, id):
    form = AddEmergencyContactForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                emergency_contact = form.save(commit=False)
                emergency_contact.employee = User.objects.get(id=id)
                emergency_contact.save()
                messages.success(request, 'Experience Info Add successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = AddEmergencyContactForm()
    context = {'form': form}
    return render(request, "employee/add_emergency_contact.html", context)


def EditEmergencyInfo(request, id, emg_id):
    edit_emergency_contact = Emergency_Contact.objects.get(id=emg_id)
    form = EditEmergencyContactForm(request.POST or None, instance=edit_emergency_contact)
    if request.method == 'POST':
        try:
            if form.is_valid():
                emergency_contact = form.save(commit=False)
                emergency_contact.employee = User.objects.get(id=id)
                emergency_contact.save()
                messages.success(request, 'Experience Info Update successfully')
                return redirect('AdminProfileView', id=id)
        except Exception as e:
            form = EditEmergencyContactForm(instance=edit_emergency_contact)
    context = {'form': form, 'edit_emergency_contact': edit_emergency_contact}
    return render(request, "admin/edit_emergency_contact.html", context)


def Holidays(request):
    holidaylist = Holiday.objects.all().order_by('holiday_date')
    context = {
        'holidaylist': holidaylist,
    }
    return render(request, "admin/holidays_list.html", context)


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


def UpdateHolidays(request, id):
    edit_holiday = Holiday.objects.get(id=id)
    form = EditHolidaysForm(request.POST or None, instance=edit_holiday)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Holiday Update successfully')
                return redirect('AdminHolidays')
        except Exception as e:
            form = EditHolidaysForm(instance=edit_holiday)
    context = {'form': form, 'edit_holiday': edit_holiday}
    return render(request, "admin/edit_holidays.html", context)


def DeleteHolidays(request, id):
    delete_holiday = Holiday.objects.get(id=id)
    delete_holiday.delete()
    return redirect('AdminHolidays')


def DepartmentView(request):
    departmentlist = Department.objects.all()
    context = {
        'departmentlist': departmentlist,
    }
    return render(request, "admin/departments.html", context)


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


def UpdateDepartment(request, id):
    edit_department = Department.objects.get(id=id)
    form = EditDepartmentForm(request.POST or None, instance=edit_department)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Department Update successfully')
                return redirect('AdminDepartmentView')
        except Exception as e:
            form = EditDepartmentForm(instance=edit_department)
    context = {'form': form, 'edit_department': edit_department}
    return render(request, "admin/edit_department.html", context)


def DeleteDepartment(request, id):
    delete_department = Department.objects.get(id=id)
    delete_department.delete()
    return redirect('AdminDepartmentView')


def DesignationView(request):
    designationlist = Designation.objects.all()
    context = {
        'designationlist': designationlist,
    }
    return render(request, "admin/designations.html", context)


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


def UpdateDesignation(request, id):
    edit_designation = Designation.objects.get(id=id)
    form = EditDesignationForm(request.POST or None, instance=edit_designation)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Designation Update successfully')
                return redirect('AdminDesignationView')
        except Exception as e:
            form = EditDesignationForm(instance=edit_designation)
    context = {'form': form, 'edit_designation': edit_designation}
    return render(request, "admin/edit_designation.html", context)


def DeleteDesignation(request,id):
    delete_designation = Designation.objects.get(id=id)
    delete_designation.delete()
    return redirect('AdminDesignationView')


def TechnologyView(request):
    technologylist = Technology.objects.all()
    context = {
        'technologylist': technologylist,
    }
    return render(request, "admin/technology.html", context)


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


def UpdateTechnology(request, id):
    edit_technology = Technology.objects.get(id=id)
    form = EditTechnologyForm(request.POST or None, instance=edit_technology)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Designation Update successfully')
                return redirect('AdminTechnologyView')
        except Exception as e:
            form = EditTechnologyForm(instance=edit_technology)
    context = {'form': form, 'edit_technology': edit_technology}
    return render(request, "admin/edit_technology.html", context)


def DeleteTechnology(request,id):
    delete_technology = Technology.objects.get(id=id)
    delete_technology.delete()
    return redirect('AdminTechnologyView')


def ClientsView(request):
    return render(request, "admin/clients.html")


def ProjectsView(request):
    projectlist = Project.objects.all()
    return render(request, "admin/projects.html", {'projectlist': projectlist})


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


def UpdateProject(request, id):
    edit_project = Project.objects.get(id=id)
    form = EditProjectForm(request.POST or None, instance=edit_project)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Project Update successfully')
                return redirect('AdminProjectDetailsView', id=id)
        except Exception as e:
            messages.error(request, "Invalid credentials")
    context = {'form': form, 'edit_project': edit_project}
    return render(request, "admin/edit_project.html", context)


def DeleteProject(request,id):
    delete_project = Project.objects.get(id=id)
    delete_project.delete()
    return redirect('AdminProjectsView')


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


def ProjectTask(request):
    projectlist = Project.objects.all()
    return render(request, "admin/task-nav.html", {'projectlist': projectlist})


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
    context = {'form': form, 'add_project_id':add_project_id}
    return render(request, "admin/add_task.html", context)


def EditProjectTask(request, id, projectid):
    projectid = Project.objects.get(id=projectid)
    edit_task = Task.objects.get(id=id)
    form = EditTaskForm(request.POST or None, instance=edit_task)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Task Update successfully')
                return redirect('AdminProjectTaskList', id=projectid.id)
        except Exception as e:
            form = EditTaskForm(instance=edit_task)
    context = {'form': form, 'edit_task': edit_task, 'projectid':projectid}
    return render(request, "admin/edit_task.html", context)


def DeleteProjectTask(request, id, projectid):
    project_id = Project.objects.get(id=projectid)
    delete_leave = Task.objects.get(id=id)
    delete_leave.delete()
    return redirect('AdminProjectTaskList', id=project_id.id)


def AddTaskAssign(request, id):
    task_id = Task.objects.get(id=id)
    if request.method == "POST":
        task_assign_add = Task(task_id=task_id.id)
        task_assign_add.save()
        return redirect('AdminProjectTaskList', id=id)
    return render(request, "admin/tasks.html")


def LeaveList(request):
    leave_list = Leave.objects.all()
    context = {
        'leave_list': leave_list
    }
    return render(request, "admin/leaves.html", context)


def UpdateLeaveStatus(request, id):
    if request.method == 'POST':
        update_leave_status = request.POST.get('leave_status')
        leave_status_update = Leave.objects.get(id=id)
        leave_status_update.leave_status = update_leave_status
        leave_status_update.save()
        return redirect('AdminLeaveList')
    return render(request, "admin/leaves.html")


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
