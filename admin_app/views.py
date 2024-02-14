from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib import messages
from django.shortcuts import render, redirect

from admin_app.forms import AddHolidaysForm, EditHolidaysForm, AddEmployeeForm, AddDepartmentForm, EditDepartmentForm, \
    AddDesignationForm, EditDesignationForm
# Create your views here.
from hrms_api.models import User, Department, Designation, Holiday, Project, Task, Leave, ProjectAssign


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
    return render(request, "admin/index.html")


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
                form.save()
                messages.success(request, 'Employee add successfully')
                return redirect('AdminEmployeeView')
        except Exception as e:
            form = AddEmployeeForm()
    context = {'form': form}
    return render(request, "admin/add_employee.html", context)


def DeleteEmployee(request,id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    return redirect('AdminEmployeeView')


def DeleteEmployeeList(id):
    delete_employee = User.objects.get(id=id)
    delete_employee.delete()
    return redirect('AdminEmployeeListView')


def ProfileView(request, id):
    profile = User.objects.get(id=id)
    return render(request, "admin/profile.html", {'profile': profile})


def FillProfileDetails(request):
    return render(request, "admin/profile.html")


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


def ClientsView(request):
    return render(request, "admin/clients.html")


def ProjectsView(request):
    projectlist = Project.objects.all()
    return render(request, "admin/projects.html", {'projectlist': projectlist})


def AddProjects(request):
    if request.method == 'POST':
        add_project_name = request.POST.get('project_name')
        add_project_client_name = request.POST.get('project_client_name')
        add_project_start_date = request.POST.get('project_start_date')
        add_project_end_date = request.POST.get('project_end_date')
        add_project_cost = request.POST.get('project_cost')
        add_project_priority = request.POST.get('project_priority')
        add_project_summary = request.POST.get('project_summary')
        add_project_images = request.POST.get('project_images')
        add_project_file = request.POST.get('project_file')
        project_add = Project(project_name=add_project_name, project_client_name=add_project_client_name, project_start_date=add_project_start_date, project_end_date=add_project_end_date, project_cost=add_project_cost, project_priority=add_project_priority, project_summary=add_project_summary, project_image=add_project_images, project_file=add_project_file)
        project_add.save()
        return redirect('AdminProjectsView')
    return render(request, "admin/projects.html")


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
    task_project_id = Project.objects.get(id=id)
    if request.method == 'POST':
        add_project_task = request.POST.get('task_title')
        project_task_add = Task(task_title=add_project_task, task_project_id=task_project_id.id)
        project_task_add.save()
        return redirect('AdminProjectTaskList', id=id)
    return render(request, "admin/tasks.html")


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


def AddProjectLeaderAssign(request, id):
    project_name_id = Project.objects.get(id=id)
    assignee_type_leader = 'Leader'
    if request.method == "POST":
        add_project_assign = request.POST.get('assign_leader_name')
        project_assign_add = ProjectAssign(project_name_id=project_name_id.id, assignee_type=assignee_type_leader, employee_name_id=add_project_assign)
        project_assign_add.save()
        return redirect('AdminProjectDetailsView', id=id)
    return render(request, "admin/project-view.html")


def AddProjectEmployeeAssign(request, id):
    project_name_id = Project.objects.get(id=id)
    assignee_type_teammember = 'Team Member'
    if request.method == "POST":
        add_project_assign = request.POST.get('assign_employee_name')
        project_assign_add = ProjectAssign(project_name_id=project_name_id.id, assignee_type=assignee_type_teammember, employee_name_id=add_project_assign)
        project_assign_add.save()
        return redirect('AdminProjectDetailsView', id=id)
    return render(request, "admin/project-view.html")
