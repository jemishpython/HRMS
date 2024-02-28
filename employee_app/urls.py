from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.EmployeeLogin, name="EmployeeLogin"),
    path("employee_index", views.EmployeeIndex, name="EmployeeIndex"),
    path("employee_logout", views.EmployeeLogout, name="EmployeeLogout"),

    path("employee-list", views.EmployeeListView, name="EmployeeListView"),

    path("emp-profile/<int:id>", views.ProfileView, name="EmpProfileView"),
    path("emp-profile/profile-info-edit/<int:id>", views.EditProfileInfo, name="EmpEditProfileInfo"),
    path("emp-profile/personal-info-edit/<int:id>", views.EditPersonalInfo, name="EmpEditPersonalInfo"),
    path("emp-profile/education-info-add/<int:id>", views.AddEducationInfo, name="EmpAddEducationInfo"),
    path("emp-profile/education-info-edit/<int:user_id>/<int:edu_id>", views.EmpEditEducationInfo, name="EmpEditEducationInfo"),
    path("emp-profile/experience-info-add/<int:id>", views.AddExperienceInfo, name="EmpAddExperienceInfo"),
    path("emp-profile/experience-info-edit/<int:id>/<int:exp_id>", views.EditExperienceInfo, name="EmpEditExperienceInfo"),
    path("emp-profile/emergency-contact-add/<int:id>", views.AddEmergencyInfo, name="EmpAddEmergencyInfo"),
    path("emp-profile/emergency-contact-edit/<int:id>/<int:emg_id>", views.EditEmergencyInfo, name="EmpEditEmergencyInfo"),

    path("holidays", views.Holidays, name="EmpHolidays"),

    path("department", views.DepartmentView, name="EmpDepartmentView"),

    path("designation", views.DesignationView, name="EmpDesignationView"),

    path("technology", views.TechnologyView, name="EmpTechnologyView"),

    path("leaves/<int:id>", views.Leaves, name="EmpLeaves"),
    path("<int:id>/leaves/add", views.AddLeave, name="EmpAddLeaves"),
    path("<int:userid>/leaves/update/<int:id>", views.EditLeave, name="EmpEditLeave"),
    path("<int:id>/leaves/delete", views.DeleteLeave, name="EmpDeleteLeave"),
]
