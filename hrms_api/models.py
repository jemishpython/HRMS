from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from hrms_api.choices import GenderTypeChoice, MaritalStatusChoice, ProjectPriorityChoice, TaskStatusChoice, \
    ProjectStatusChoice, LeaveTypeChoice, LeaveStatusChoice, ProjectAssigneeTypeChoice


class Department(models.Model):
    department_name = models.CharField(verbose_name='Department Name', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.department_name


class Designation(models.Model):
    designation_name = models.CharField(verbose_name='Designation Name', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.designation_name


class Technology(models.Model):
    technology_name = models.CharField(verbose_name='Technology Name', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.technology_name


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):

        if "phone" in kwargs and 'password' in kwargs:
            phone = kwargs.pop("phone")
            password = kwargs.pop("password")
            user = self.model(
                phone=phone,
                **kwargs)
            user.set_password(password)
        elif "phone" in kwargs:
            phone = kwargs.pop("phone")
            user = self.model(
                phone=phone,
                **kwargs)
        else:
            raise ValueError('Users must have an phone and password')

        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **kwargs):
        user = self.create_user(
            phone=phone,
            **kwargs
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(verbose_name='User Name', max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="phone number entered in format +910987654321 .")
    country_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    dob = models.DateField(verbose_name='Birth Date', null=True, blank=True)
    address = models.CharField(verbose_name='Address', max_length=400, blank=True, null=True)
    nationality = models.CharField(verbose_name='Nationality', max_length=255, blank=True)
    email = models.EmailField(verbose_name='Email Address', max_length=255, blank=False)
    gender = models.CharField(verbose_name='Gender', choices=GenderTypeChoice.choices, default=GenderTypeChoice.MALE, max_length=255, null=True)
    report_to = models.CharField(verbose_name='Report to', blank=True, null=True, max_length=255)
    is_admin = models.BooleanField(verbose_name='is admin', default=False, blank=True)
    is_staff = models.BooleanField(verbose_name='is staff', default=False, blank=True)
    avatar = models.ImageField(verbose_name='Profile Image', upload_to='avatars', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField(verbose_name='Date of Joining', null=True, blank=True)
    birthdate = models.DateField(verbose_name='Birth Date', null=True)
    marital_status = models.CharField(verbose_name='Marital Status', choices=MaritalStatusChoice.choices, default=MaritalStatusChoice.SINGLE, null=True, max_length=255)
    religion = models.CharField(verbose_name='Religion', max_length=20, null=True)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username


class Education_Info(models.Model):
    institution = models.CharField(verbose_name='Institution Name', max_length=50, null=True, blank=True)
    start_year = models.DateField(verbose_name='Starting Year', max_length=10, null=True, blank=True)
    complete_year = models.DateField(verbose_name='Complete Year', max_length=10, null=True, blank=True)
    degree = models.CharField(verbose_name='Degree Name', max_length=60, null=True, blank=True)
    grade = models.CharField(verbose_name='Grade', max_length=20, null=True, blank=True)


class Holiday(models.Model):
    holiday_title = models.CharField(verbose_name='Holiday Title', max_length=50, null=True, blank=True)
    holiday_date = models.DateField(verbose_name="Holiday Date", null=True, blank=True)

    def __str__(self):
        return self.holiday_title


class Project(models.Model):
    project_name = models.CharField(verbose_name='Project Name', max_length=100, null=True, blank=True)
    project_client_name = models.CharField(verbose_name='Project Client Name', max_length=100, null=True, blank=True)
    project_start_date = models.DateField(verbose_name='Project Start Date', null=True, blank=True)
    project_end_date = models.DateField(verbose_name='Project End Date', null=True, blank=True)
    project_cost = models.CharField(verbose_name='Project Cost', max_length=50, null=True, blank=True)
    project_priority = models.CharField(verbose_name='Project Priority', choices=ProjectPriorityChoice.choices, default=ProjectPriorityChoice.HIGH, max_length=255, null=True, blank=True)
    project_summary = models.TextField(verbose_name='Project Summary', max_length=1000, null=True, blank=True)
    project_image = models.ImageField(verbose_name='Project Image', max_length=255, null=True, blank=True)
    project_file = models.FileField(verbose_name='Project File', max_length=255, null=True, blank=True)
    project_status = models.CharField(verbose_name='Project Status', choices=ProjectStatusChoice.choices, default=ProjectStatusChoice.NOT_STARTED, max_length=255, null=True, blank=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_title = models.CharField(verbose_name='Task Title', max_length=100, null=True)
    task_status = models.CharField(verbose_name='Task Status', choices=TaskStatusChoice.choices, default=TaskStatusChoice.WORKING, max_length=255, null=True, blank=True)
    task_project = models.ForeignKey(Project, verbose_name='Project Name', on_delete=models.DO_NOTHING, null=True)
    task_assign = models.ManyToManyField(User, verbose_name='Task Assign')

    def __str__(self):
        return self.task_title


class Leave(models.Model):
    leave_type = models.CharField(verbose_name='Leave Type', max_length=50, choices=LeaveTypeChoice.choices, default=LeaveTypeChoice.CASUAL, null=True, blank=True)
    leave_from = models.DateField(verbose_name='Leave From', null=True, blank=True)
    leave_to = models.DateField(verbose_name='Leave To', null=True, blank=True)
    leave_days = models.IntegerField(verbose_name='Leave Days', null=True, blank=True)
    leave_reason = models.CharField(verbose_name='Leave Reason', max_length=255, null=True, blank=True)
    leave_status = models.CharField(verbose_name='Leave Status', max_length=100, choices=LeaveStatusChoice.choices, default=LeaveStatusChoice.NEW, null=True, blank=True)
    leave_user = models.ForeignKey(User, verbose_name='User Name', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.leave_type


class ProjectAssign(models.Model):
    project_name = models.ForeignKey(Project, verbose_name='Project Name', on_delete=models.DO_NOTHING, null=True)
    assignee_type = models.CharField(verbose_name='Assignee Type', max_length=50, blank=True, null=True, choices=ProjectAssigneeTypeChoice.choices, default=ProjectAssigneeTypeChoice.TEAM_MEMBER)
    employee_name = models.ManyToManyField(User, verbose_name='Employee Name', through='Projectassign_Employee_Name')

    def __str__(self):
        return self.project_name.project_name


class Projectassign_Employee_Name(models.Model):
    projectassign = models.ForeignKey(ProjectAssign, on_delete=models.DO_NOTHING, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.projectassign.project_name.project_name} - {self.user.username}"