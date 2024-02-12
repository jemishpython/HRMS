from django.contrib.auth import login, logout
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect


# Create your views here.
from hrms_api.models import User, Holiday, Designation, Department, Leave, Task, Project, ProjectAssign


def landing(request):
    return render(request, 'landing.html')


def EmployeeLogin(request):
    if request.method == "POST":
        employeephone = request.POST.get('employeephone')
        employeepassword = request.POST.get('employeepassword')
        try:
            user = User.objects.get(phone=employeephone)
        except:
            messages.error(request, "Invalid credentials")
            return redirect('EmployeeLogin')
        if user.is_active:
            if user.check_password(employeepassword):
                login(request, user)
                return redirect('EmployeeIndex')
            messages.error(request, "Invalid credentials")
            return redirect('EmployeeLogin')
        messages.error(request, "Please wait for admin is approve your request")
        return redirect('EmployeeLogin')
    return render(request, "employee/login.html")


# @login_required(login_url="EmployeeLogin")
def EmployeeIndex(request):
    user = request.user
    task_list = Task.objects.filter(task_assign=user.id)
    project_list = ProjectAssign.objects.filter(employee_name=user.id)

    context = {
        'user': user,
        'task_list': task_list,
        'project_list':project_list,
    }

    return render(request, "employee/employee-dashboard.html", context)


def EmployeeLogout(request):
    logout(request)
    return render(request, "employee/login.html")


def Holidays(request):
    holidaylist = Holiday.objects.all().order_by('holiday_date')
    context = {
        'holidaylist': holidaylist,
    }
    return render(request, "employee/holidays_list.html", context)


def DepartmentView(request):
    departmentlist = Department.objects.all()
    context = {
        'departmentlist': departmentlist,
    }
    return render(request, "employee/departments.html", context)


def DesignationView(request):
    designationlist = Designation.objects.all()
    context = {
        'designationlist': designationlist,
    }
    return render(request, "employee/designations.html", context)


def Leaves(request, id):
    leave_list = Leave.objects.filter(leave_user=id)
    context = {
        'leave_list': leave_list
    }
    return render(request, "employee/leaves-employee.html", context)


def AddLeave(request, id):
    user_id = User.objects.get(id=id)
    if request.method == "POST":
        add_leave_type = request.POST.get("leave_type")
        add_leave_from = request.POST.get("leave_from")
        add_leave_to = request.POST.get("leave_to")
        add_leave_days = request.POST.get("leave_days")
        add_leave_reason = request.POST.get("leave_reason")
        if add_leave_from < add_leave_to:
            leave_add = Leave(leave_type=add_leave_type, leave_from=add_leave_from, leave_to=add_leave_to, leave_days=add_leave_days, leave_reason=add_leave_reason, leave_user_id=user_id.id)
            leave_add.save()
        else:
            raise forms.ValidationError("Leave-from date must be not grater than leave-to date")
        return redirect('EmpLeaves', id=id)
    return render(request, "employee/leaves-employee.html")
