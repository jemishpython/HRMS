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
    path("employee/edit/<int:id>", views.EditEmployee, name="AdminEditEmployee"),
    path("employee/delete/<int:id>", views.DeleteEmployee, name="AdminDeleteEmployee"),
    path("employee_list/delete/<int:id>", views.DeleteEmployeeList, name="AdminDeleteEmployeeList"),


    path("employee/profile/<int:id>", views.ProfileView, name="AdminProfileView"),
    path("profile/detailsform/<int:id>", views.FillProfileDetails, name="AdminFillProfileDetails"),


    path("holidays", views.Holidays, name="AdminHolidays"),
    path("holidays/add/", views.AddHolidays, name="AdminAddHolidays"),
    path("holidays/update/<int:id>", views.UpdateHolidays, name="AdminUpdateHoliday"),
    path("holidays/delete/<int:id>", views.DeleteHolidays, name="AdminDeleteHolidays"),

    path("department", views.DepartmentView, name="AdminDepartmentView"),
    path("department/add", views.AddDepartment, name="AdminAddDepartment"),
    # path("department/update/<int:id>", views.UpdateDepartment, name="AdminUpdateDepartment"),
    path("department/delete/<int:id>", views.DeleteDepartment, name="AdminDeleteDepartment"),

    path("designation", views.DesignationView, name="AdminDesignationView"),
    path("designation/add", views.AddDesignation, name="AdminAddDesignation"),
    # path("designation/update/<int:id>", views.UpdateDesignation, name="AdminUpdateDesignation"),
    path("designation/delete/<int:id>", views.DeleteDesignation, name="AdminDeleteDesignation"),

    # path("clients", views.ClientsView, name="AdminClientsView"),

    path("projects", views.ProjectsView, name="AdminProjectsView"),
    path("projects/add", views.AddProjects, name="AdminAddProjects"),
    path("projects/details-view/<int:id>", views.ProjectDetailsView, name="AdminProjectDetailsView"),

    path("projects/tasks", views.ProjectTask, name="AdminProjectTask"),
    path("project/<int:id>/tasks", views.ProjectTaskList, name="AdminProjectTaskList"),
    path("project/<int:id>/task-add", views.AddProjectTask, name="AdminAddProjectTask"),

    path("project-task-assign/<int:id>", views.AddTaskAssign, name='AdminAddTaskAssign'),

    path("leaves", views.LeaveList, name='AdminLeaveList'),
    path("leaves/status-update/<int:id>", views.UpdateLeaveStatus, name='AdminLeaveStatusUpdate'),

    path("project-leader-assign/<int:id>", views.AddProjectLeaderAssign, name='AdminAddProjectLeaderAssign'),
    path("project-team-member-assign/<int:id>", views.AddProjectEmployeeAssign, name='AdminAddProjectEmployeeAssign'),

]
