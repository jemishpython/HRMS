from django.urls import path

from . import views


urlpatterns = [

    # path("admin_register", views.AdminRegister, name="AdminRegister"),
    path("", views.Login, name="Login"),
    path("admin_index", views.AdminIndex, name="AdminIndex"),
    path("admin_logout", views.AdminLogout, name="AdminLogout"),


    path("employee", views.EmployeeView, name="AdminEmployeeView"),
    path("employee_list", views.EmployeeListView, name="AdminEmployeeListView"),
    path("employee/add", views.AddEmployee, name="AdminAddEmployee"),
    path("employee/delete/<int:id>", views.DeleteEmployee, name="AdminDeleteEmployee"),
    path("employee_list/delete/<int:id>", views.DeleteEmployeeList, name="AdminDeleteEmployeeList"),


    path("employee/profile/<int:id>", views.ProfileView, name="AdminProfileView"),
    path("employee/profile-info-edit/<int:id>", views.EditProfileInfo, name="AdminEditProfileInfo"),
    path("employee/personal-info-edit/<int:id>", views.EditPersonalInfo, name="AdminEditPersonalInfo"),
    path("employee/education-info-add/<int:id>", views.AddEducationInfo, name="AdminAddEducationInfo"),
    path("employee/education-info-edit/<int:id>/<int:edu_id>", views.EditEducationInfo, name="AdminEditEducationInfo"),
    path("employee/experience-info-add/<int:id>", views.AddExperienceInfo, name="AdminAddExperienceInfo"),
    path("employee/experience-info-edit/<int:id>/<int:exp_id>", views.EditExperienceInfo, name="AdminEditExperienceInfo"),
    path("employee/emergency-contact-add/<int:id>", views.AddEmergencyInfo, name="AdminAddEmergencyInfo"),
    path("employee/emergency-contact-edit/<int:id>/<int:emg_id>", views.EditEmergencyInfo, name="AdminEditEmergencyInfo"),


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

    # path("clients", views.ClientsView, name="AdminClientsView"),

    path("projects", views.ProjectsView, name="AdminProjectsView"),
    path("projects/add", views.AddProject, name="AdminAddProjects"),
    path("projects/details-view/<int:id>", views.ProjectDetailsView, name="AdminProjectDetailsView"),
    path("projects/update/<int:id>", views.UpdateProject, name="AdminUpdateProject"),
    path("projects/delete/<int:id>", views.DeleteProject, name="AdminDeleteProject"),

    path("projects/tasks", views.ProjectTask, name="AdminProjectTask"),
    path("project/<int:id>/tasks", views.ProjectTaskList, name="AdminProjectTaskList"),
    path("project/<int:id>/task-add", views.AddProjectTask, name="AdminAddProjectTask"),
    path("project/<int:projectid>/task-edit/<int:id>", views.EditProjectTask, name="AdminEditProjectTask"),
    path("project/<int:projectid>/task-delete/<int:id>", views.DeleteProjectTask, name="AdminDeleteProjectTask"),

    path("project-task-assign/<int:id>", views.AddTaskAssign, name='AdminAddTaskAssign'),

    path("leaves", views.LeaveList, name='AdminLeaveList'),
    path("leaves/status-update/<int:id>", views.UpdateLeaveStatus, name='AdminLeaveStatusUpdate'),

    path("project-assignee/<int:id>", views.AddProjectAssignee, name='AdminAddProjectAssignee'),

]
