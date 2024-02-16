from django.urls import path

from . import views


urlpatterns = [
    path("", views.EmployeeLogin, name="EmployeeLogin"),
    path("employee_index", views.EmployeeIndex, name="EmployeeIndex"),
    path("employee_logout", views.EmployeeLogout, name="EmployeeLogout"),

    path("employee-list", views.EmployeeListView, name="EmployeeListView"),

    path("holidays", views.Holidays, name="EmpHolidays"),

    path("department", views.DepartmentView, name="EmpDepartmentView"),

    path("designation", views.DesignationView, name="EmpDesignationView"),

    path("leaves/<int:id>", views.Leaves, name="EmpLeaves"),
    path("<int:id>/leaves/add", views.AddLeave, name="EmpAddLeaves"),
    path("<int:userid>/leaves/update/<int:id>", views.EditLeave, name="EmpEditLeave"),
    path("<int:id>/leaves/delete", views.DeleteLeave, name="EmpDeleteLeave"),

]
