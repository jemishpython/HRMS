from django.urls import path

from . import views


urlpatterns = [

    # path("admin_register", views.AdminRegister, name="AdminRegister"),
    path("admin_index", views.AdminIndex, name="AdminIndex"),
    path("admin_logout", views.AdminLogout, name="AdminLogout"),
    path('admin-password-reset-mail/', views.forget_password_mail, name='forget_password_mail'),
    path('admin-password-reset/<int:pk>/', views.reset_page, name='forgot_password'),
    path('admin-password-reset-successfully/<int:pk>/', views.update_password, name='update_password'),

    path("employee", views.EmployeeView, name="AdminEmployeeView"),
    path("employee_list", views.EmployeeListView, name="AdminEmployeeListView"),
    path("employee/add", views.AddEmployee, name="AdminAddEmployee"),
    path("employee/delete/<int:id>", views.DeleteEmployee, name="AdminDeleteEmployee"),
    path("employee_list/delete/<int:id>", views.DeleteEmployeeList, name="AdminDeleteEmployeeList"),


    path("employee/profile/<int:id>", views.ProfileView, name="AdminProfileView"),
    path("employee/profile-info-edit/<int:id>", views.EditProfileInfo, name="AdminEditProfileInfo"),
    path("employee/personal-info-edit/<int:id>", views.EditPersonalInfo, name="AdminEditPersonalInfo"),
    path("employee/bank-info-add/<int:id>", views.AddBankInfo, name="AdminAddBankInfo"),
    path("employee/<int:id>/bank-info-edit/<int:bank_id>", views.EditBankInfo, name="AdminEditBankInfo"),
    path("employee/education-info-add/<int:id>", views.AddEducationInfo, name="AdminAddEducationInfo"),
    path("employee/<int:id>/education-info-edit/<int:edu_id>", views.EditEducationInfo, name="AdminEditEducationInfo"),
    path("employee/<int:id>/education-info-delete/<int:edu_id>", views.DeleteEducation, name="AdminDeleteEducationInfo"),
    path("employee/experience-info-add/<int:id>", views.AddExperienceInfo, name="AdminAddExperienceInfo"),
    path("employee/<int:id>/experience-info-edit/<int:exp_id>", views.EditExperienceInfo, name="AdminEditExperienceInfo"),
    path("employee/<int:id>/experience-info-delete/<int:exp_id>", views.DeleteExperience, name="AdminDeleteExperienceInfo"),
    path("employee/emergency-contact-add/<int:id>", views.AddEmergencyInfo, name="AdminAddEmergencyInfo"),
    path("employee/<int:id>/emergency-contact-edit/<int:emg_id>", views.EditEmergencyInfo, name="AdminEditEmergencyInfo"),
    path("employee/<int:id>/emergency-contact-delete/<int:emg_id>", views.DeleteEmergency, name="AdminDeleteEmergencyInfo"),


    path("holidays", views.Holidays, name="AdminHolidays"),
    path("holidays/add/", views.AddHolidays, name="AdminAddHolidays"),
    path("holidays/update/<int:id>", views.UpdateHolidays, name="AdminUpdateHoliday"),
    path("holidays/delete/<int:id>", views.DeleteHolidays, name="AdminDeleteHolidays"),

    path("department", views.DepartmentView, name="AdminDepartmentView"),
    path("department/add", views.AddDepartment, name="AdminAddDepartment"),
    path("department/update/<int:id>", views.UpdateDepartment, name="AdminUpdateDepartment"),
    path("department/delete/<int:id>", views.DeleteDepartment, name="AdminDeleteDepartment"),

    path("technology", views.TechnologyView, name="AdminTechnologyView"),
    path("technology/add", views.AddTechnology, name="AdminAddTechnology"),
    path("technology/update/<int:id>", views.UpdateTechnology, name="AdminUpdateTechnology"),
    path("technology/delete/<int:id>", views.DeleteTechnology, name="AdminDeleteTechnology"),

    path("designation", views.DesignationView, name="AdminDesignationView"),
    path("designation/add", views.AddDesignation, name="AdminAddDesignation"),
    path("designation/update/<int:id>", views.UpdateDesignation, name="AdminUpdateDesignation"),
    path("designation/delete/<int:id>", views.DeleteDesignation, name="AdminDeleteDesignation"),

    path("clients", views.ClientsView, name="AdminClientsView"),

    path("projects", views.ProjectsView, name="AdminProjectsView"),
    path("projects/add", views.AddProject, name="AdminAddProjects"),
    path("projects/details-view/<int:id>", views.ProjectDetailsView, name="AdminProjectDetailsView"),
    path("projects/update/<int:id>", views.UpdateProject, name="AdminUpdateProject"),
    path("projects/delete/<int:id>", views.DeleteProject, name="AdminDeleteProject"),
    path("project/<int:projectid>/task-delete/<int:id>", views.DeleteProjectTask, name="AdminDeleteProjectTask"),

    path("project-assignee/<int:id>", views.AddProjectAssignee, name='AdminAddProjectAssignee'),

    path("projects/tasks", views.ProjectTask, name="AdminProjectTask"),
    path("project/<int:id>/tasks", views.ProjectTaskList, name="AdminProjectTaskList"),
    path("project/<int:id>/task-add", views.AddProjectTask, name="AdminAddProjectTask"),
    path("project/<int:projectid>/task-edit/<int:id>", views.EditProjectTask, name="AdminEditProjectTask"),

    path("project-task-assign/<int:id>", views.AddTaskAssign, name='AdminAddTaskAssign'),

    path("leaves", views.LeaveList, name='AdminLeaveList'),
    path("leaves/status-update/<int:id>", views.UpdateLeaveStatus, name='AdminLeaveStatusUpdate'),

    path("tickets", views.TicketList, name='AdminTicketList'),
    path("tickets/status-update/<int:id>", views.UpdateTicketstatus, name='AdminTicketStatusUpdate'),

    path("chat/<int:id>", views.ChatView, name='AdminChatView'),

    path("attendance/", views.AttendanceView, name='AdminAttendanceView'),
]
