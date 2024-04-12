from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     search_fields =('username', 'pk')
#     filter_horizontal =()
#     fieldsets = ()
#     list_per_page = 20
#
#     def has_add_permission(self, request):
#         return True
#
#     def has_delete_permission(self, request, obj=None):
#         return True

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Technology)
admin.site.register(User)
admin.site.register(Education_Info)
admin.site.register(Experience_Info)
admin.site.register(Emergency_Contact)
admin.site.register(Client)
admin.site.register(Holiday)
admin.site.register(Project)
admin.site.register(ProjectAssign)
admin.site.register(ProjectImages)
admin.site.register(ProjectFile)
admin.site.register(Task)
admin.site.register(TaskAssign)
admin.site.register(Leave)
admin.site.register(Ticket)
admin.site.register(Bank)
admin.site.register(Policies)
admin.site.register(Interviewers)
admin.site.register(InterviewQuestions)
admin.site.register(InterviewerResult)
admin.site.register(Conditions)
admin.site.register(Attendance)
admin.site.register(SalarySlip)
