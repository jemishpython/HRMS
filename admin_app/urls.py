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
    path("client/add", views.AddClient, name="AdminAddClient"),
    path("client/delete/<int:id>", views.DeleteClient, name="AdminDeleteClient"),
    path("clients-details/<int:id>", views.ClientDetailView, name="AdminClientDetailView"),
    path("clients/profile-info-edit/<int:id>", views.EditClientInfo, name="AdminEditClientInfo"),
    path("clients/<int:user_id>/project-delete/<int:id>", views.ClientDeleteProject, name="AdminClientDeleteProject"),


    path("projects", views.ProjectsView, name="AdminProjectsView"),
    path("projects/add", views.AddProject, name="AdminAddProjects"),
    path("projects/details-view/<int:id>", views.ProjectDetailsView, name="AdminProjectDetailsView"),
    path("projects/images-add/<int:id>", views.AddProjectImage, name="AdminAddProjectImage"),
    path("projects/<int:project_id>/image-delete/<int:id>", views.AdminDeleteProjectImage, name="AdminDeleteProjectImage"),
    path("projects/files-add/<int:id>", views.AddProjectFile, name="AdminAddProjectFile"),
    path("projects/<int:project_id>/file-delete/<int:id>", views.AdminDeleteProjectFile, name="AdminDeleteProjectFile"),
    path("projects/update/<int:id>", views.UpdateProject, name="AdminUpdateProject"),
    path("projects/delete/<int:id>", views.DeleteProject, name="AdminDeleteProject"),
    path("project/<int:projectid>/task-delete/<int:id>", views.DeleteProjectTask, name="AdminDeleteProjectTask"),

    path("project-assignee/<int:id>", views.AddProjectAssignee, name='AdminAddProjectAssignee'),
    path("<int:project_id>/project-assignee-delete/<int:id>", views.DeleteAssignEmployee, name='AdminDeleteAssignEmployee'),

    path("project/tasks", views.ProjectTask, name="AdminProjectTask"),
    path("project/<int:id>/tasks", views.ProjectTaskList, name="AdminProjectTaskList"),
    path("project/<int:id>/task-add", views.AddProjectTask, name="AdminAddProjectTask"),
    path("project/<int:projectid>/task-edit/<int:id>", views.EditProjectTask, name="AdminEditProjectTask"),

    path("project-task-assign/<int:id>", views.AddTaskAssign, name='AdminAddTaskAssign'),
    path("project-task-assign/<int:task_id>/remove/<int:id>", views.DeleteTaskAssignee, name='AdminDeleteTaskAssignee'),

    path("leaves", views.LeaveList, name='AdminLeaveList'),
    path("leaves/status-update/<int:id>", views.UpdateLeaveStatus, name='AdminLeaveStatusUpdate'),

    path("tickets", views.TicketList, name='AdminTicketList'),
    path("tickets/status-update/<int:id>", views.UpdateTicketstatus, name='AdminTicketStatusUpdate'),

    path("attendance/", views.AttendanceView, name='AdminAttendanceView'),
    path("attendance/edit/<int:id>/", views.AttendanceEdit, name='AdminAttendanceEdit'),

    path("employee-salary-slip/", views.SalarySlipDashboard, name='AdminSalarySlipDashboard'),
    path("employee-salary-slip/edit/<int:id>", views.EditEmployeeSalarySlip, name='AdminEditEmployeeSalarySlip'),
    path("employee-salary-slip/generate/<int:id>", views.GenerateEmployeeSalarySlip, name='AdminGenerateEmployeeSalarySlip'),
    path("employee-salary-slip/list/", views.EmployeeSalarySlipList, name='AdminEmployeeSalarySlipList'),
    path("employee-salary-slip/pdf/<int:id>", views.SalarySlipPDFCreate, name='AdminEmployeeSalarySlipPDF'),
    path("employee-salary-slip/view/<int:id>", views.EmployeeSalarySlipView, name='AdminEmployeeSalarySlipView'),
    path("employee-salary-slip/delete/<int:id>", views.DeleteSalarySlip, name='AdminDeleteSalarySlip'),

    path("interviewer-list/", views.InterviewerDash, name='AdminInterviewerDash'),
    path("interviewer-detail/", views.InterviewerDetails, name='AdminInterviewerDetails'),
    path("interviewer-form/", views.InterviewerApply, name='AdminInterviewerForm'),
    path("interviewer-delete/<int:id>/", views.DeleteInterviewer, name='AdminDeleteInterviewer'),
    path("interview-questions/", views.InterviewQuestion, name='AdminInterviewQuestion'),
    path("interview-questions/add/", views.AddInterviewQuestion, name='AdminAddInterviewQuestion'),
    path("interview-questions/edit/<int:id>", views.EditInterviewQuestion, name='AdminEditInterviewQuestion'),
    path("interview-questions/delete/<int:id>", views.DeleteInterviewQuestion, name='AdminDeleteInterviewQuestion'),

    path("interviewer/aptitude-test-mail-send/<int:id>", views.SendAptitudeTestMail, name='AdminSendAptitudeTestMail'),
    path("interviewer/aptitude-test-result/<int:id>", views.AptitudeTestResult, name='AdminAptitudeTestResult'),

    path("condition-and-rules/", views.ConditionsView, name='AdminConditionsView'),
    path("condition-and-rules/add/", views.AddConditon, name="AdminAddCondition"),
    path("condition-and-rules/edit/<int:id>/", views.EditCondition, name="AdminEditCondition"),
    path("condition-and-rules/delete/<int:id>/", views.DeleteCondition, name="AdminDeleteCondition"),

    path("policies/", views.PoliciesView, name='AdminPoliciesView'),
    path("policies/add/", views.AddPolicies, name="AdminAddPolicies"),
    path("policies/delete/<int:id>", views.DeletePolicies, name="AdminDeletePolicies"),
]
