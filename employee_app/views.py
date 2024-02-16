from django.contrib.auth import login, logout
from django.contrib import messages
from django import forms
from django.shortcuts import render, redirect

from employee_app.forms import AddLeaveForm, EditLeaveForm
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

def EmployeeListView(request):
    emp_list = User.objects.all()
    return render(request, "employee/employees_list.html",{'emp_list':emp_list})


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
    userid = User.objects.get(id=id)
    if request.method == 'POST':
        form = AddLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.leave_user = User.objects.get(id=id)
            leave.save()
            messages.success(request, 'Leave added successfully')
            return redirect('EmpLeaves', id=userid.id)
    else:
        form = AddLeaveForm()
    context = {'form': form}
    return render(request, "employee/add_leave.html", context)


def EditLeave(request, id, userid):
    userid = User.objects.get(id=userid)
    edit_leave = Leave.objects.get(id=id)
    form = EditLeaveForm(request.POST or None, instance=edit_leave)
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Leave Update successfully')
                return redirect('EmpLeaves', id=userid.id)
        except Exception as e:
            form = EditLeaveForm(instance=edit_leave)
    context = {'form': form, 'edit_leave': edit_leave}
    return render(request, "employee/edit_leave.html", context)


def DeleteLeave(request, id):
    userid = request.user.id
    delete_leave = Leave.objects.get(id=id)
    delete_leave.delete()
    return redirect('EmpLeaves', id=userid)
