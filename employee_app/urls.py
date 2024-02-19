from django.urls import path

from . import views


urlpatterns = [
    path("", views.EmployeeLogin, name="EmployeeLogin"),
    path("employee_index", views.EmployeeIndex, name="EmployeeIndex"),
    path("employee_logout", views.EmployeeLogout, name="EmployeeLogout"),

    path("employee-list", views.EmployeeListView, name="EmployeeListView"),

    path("profile/<int:id>", views.ProfileView, name="EmpProfileView"),
    path("profile/profile-info-edit/<int:id>", views.EditProfileInfo, name="EmpEditProfileInfo"),
    path("profile/personal-info-edit/<int:id>", views.EditPersonalInfo, name="EmpEditPersonalInfo"),
    path("profile/education-info-edit/<int:id>", views.EditEducationInfo, name="EmpEditEducationInfo"),
    path("profile/experience-info-edit/<int:id>", views.EditExperienceInfo, name="EmpEditExperienceInfo"),

    path("holidays", views.Holidays, name="EmpHolidays"),

    path("department", views.DepartmentView, name="EmpDepartmentView"),

    path("designation", views.DesignationView, name="EmpDesignationView"),

    path("technology", views.TechnologyView, name="EmpTechnologyView"),

    path("leaves/<int:id>", views.Leaves, name="EmpLeaves"),
    path("<int:id>/leaves/add", views.AddLeave, name="EmpAddLeaves"),
    path("<int:userid>/leaves/update/<int:id>", views.EditLeave, name="EmpEditLeave"),
    path("<int:id>/leaves/delete", views.DeleteLeave, name="EmpDeleteLeave"),
]
