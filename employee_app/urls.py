from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.EmployeeLogin, name="EmployeeLogin"),
    path("employee_index", views.EmployeeIndex, name="EmployeeIndex"),
    path("employee_logout", views.EmployeeLogout, name="EmployeeLogout"),

    # Forget Password
    path('emp-password-reset-mail/', views.forget_password_mail, name='emp_forget_password_mail'),
    path('emp-password-reset/<int:pk>/', views.reset_page, name='emp_forgot_password'),
    path('emp-password-reset-successfully/<int:pk>/', views.update_password, name='emp_update_password'),

    path("employee-list", views.EmployeeListView, name="EmployeeListView"),

    path("emp-profile/<int:id>", views.ProfileView, name="EmpProfileView"),
    path("emp-profile/profile-info-edit/<int:id>", views.EditProfileInfo, name="EmpEditProfileInfo"),
    path("emp-profile/personal-info-edit/<int:id>", views.EditPersonalInfo, name="EmpEditPersonalInfo"),
    path("emp-profile/education-info-add/<int:id>", views.AddEducationInfo, name="EmpAddEducationInfo"),
    path("emp-profile/<int:user_id>/education-info-edit/<int:edu_id>", views.EmpEditEducationInfo, name="EmpEditEducationInfo"),
    path("emp-profile/experience-info-add/<int:id>", views.AddExperienceInfo, name="EmpAddExperienceInfo"),
    path("emp-profile/<int:id>/experience-info-edit/<int:exp_id>", views.EditExperienceInfo, name="EmpEditExperienceInfo"),
    path("emp-profile/emergency-contact-add/<int:id>", views.AddEmergencyInfo, name="EmpAddEmergencyInfo"),
    path("emp-profile/<int:id>/emergency-contact-edit/<int:emg_id>", views.EditEmergencyInfo, name="EmpEditEmergencyInfo"),

    path("holidays", views.Holidays, name="EmpHolidays"),

    path("department", views.DepartmentView, name="EmpDepartmentView"),

    path("designation", views.DesignationView, name="EmpDesignationView"),

    path("technology", views.TechnologyView, name="EmpTechnologyView"),

    path("leaves/<int:id>", views.Leaves, name="EmpLeaves"),
    path("<int:id>/leaves/add", views.AddLeave, name="EmpAddLeaves"),
    path("<int:userid>/leaves/update/<int:id>", views.EditLeave, name="EmpEditLeave"),
    path("<int:id>/leaves/delete", views.DeleteLeave, name="EmpDeleteLeave"),

    path("tickets/<int:id>", views.Tickets, name="EmpTickets"),
    path("<int:id>/tickets/add", views.AddTicket, name="EmpAddTicket"),
    path("<int:userid>/tickets-update/<int:id>", views.EditTicket, name="EmpEditTicket"),
    path("<int:id>/tickets/delete", views.DeleteTicket, name="EmpDeleteTicket"),

]
