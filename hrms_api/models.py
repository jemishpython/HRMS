from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

# Create your models here.
from hrms_api.choices import GenderTypeChoice, MaritalStatusChoice, ProjectPriorityChoice, TaskStatusChoice, \
    ProjectStatusChoice, LeaveTypeChoice, LeaveStatusChoice, ProjectAssigneeTypeChoice, TicketPriorityChoice, \
    TicketStatusChoice, AttendanceStatusChoice, GroupMembertypeChoice, GroupMemberStatusChoice


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
    avatar = models.ImageField(verbose_name='Profile Image', upload_to='avatars/', default='avatars/306473.png')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField(verbose_name='Date of Joining', null=True, blank=True)
    marital_status = models.CharField(verbose_name='Marital Status', choices=MaritalStatusChoice.choices, default=MaritalStatusChoice.SINGLE, null=True, max_length=255)
    religion = models.CharField(verbose_name='Religion', max_length=20, null=True)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, null=True, blank=True)
    salary = models.IntegerField(verbose_name="Employee Salary", null=True, blank=True)
    chat_status = models.BooleanField(verbose_name="Chat Status", default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.username


class Education_Info(models.Model):
    institution = models.CharField(verbose_name='Institution Name', max_length=50, null=True, blank=True)
    location = models.CharField(verbose_name='Location Name', max_length=50, null=True, blank=True)
    start_year = models.DateField(verbose_name='Starting Year', max_length=10, null=True, blank=True)
    complete_year = models.DateField(verbose_name='Complete Year', max_length=10, null=True, blank=True)
    degree = models.CharField(verbose_name='Degree Name', max_length=60, null=True, blank=True)
    grade = models.CharField(verbose_name='Grade', max_length=20, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.institution


class Experience_Info(models.Model):
    company_name = models.CharField(verbose_name='Company Name', max_length=50, null=True, blank=True)
    location = models.CharField(verbose_name='Location Name', max_length=50, null=True, blank=True)
    start_date = models.DateField(verbose_name='Starting Date', max_length=10, null=True, blank=True)
    end_date = models.DateField(verbose_name='End Date', max_length=10, null=True, blank=True)
    role = models.CharField(verbose_name='Role Name', max_length=60, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.company_name


class Emergency_Contact(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="phone number entered in format +910987654321 .")
    primary_name = models.CharField(verbose_name='Name', max_length=50, null=True, blank=True)
    primary_con_relationship = models.CharField(verbose_name='relationship', max_length=50, null=True, blank=True)
    primary_phone1 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True)
    primary_phone2 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True)
    secondary_name = models.CharField(verbose_name='Name', max_length=50, null=True, blank=True)
    secondary_con_relationship = models.CharField(verbose_name='relationship', max_length=50, null=True, blank=True)
    secondary_phone1 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True)
    secondary_phone2 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.primary_name


class Client(models.Model):
    username = models.CharField(verbose_name='User Name', max_length=255, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="phone number entered in format +910987654321 .")
    country_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    dob = models.DateField(verbose_name='Birth Date', null=True, blank=True)
    active_status = models.BooleanField(verbose_name='Active Status', default=True, blank=True)
    address = models.CharField(verbose_name='Address', max_length=400, blank=True, null=True)
    nationality = models.CharField(verbose_name='Nationality', max_length=255, blank=True)
    email = models.EmailField(verbose_name='Email Address', max_length=255, blank=False)
    gender = models.CharField(verbose_name='Gender', choices=GenderTypeChoice.choices, default=GenderTypeChoice.MALE, max_length=255)
    client_avatar = models.ImageField(verbose_name='Profile Image', upload_to='client_avatar/')
    company_name = models.CharField(verbose_name='Company Name', max_length=255, blank=True, null=True)
    position = models.CharField(verbose_name='Position in company', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Holiday(models.Model):
    holiday_title = models.CharField(verbose_name='Holiday Title', max_length=50, null=True, blank=True)
    holiday_date = models.DateField(verbose_name="Holiday Date", null=True, blank=True)

    def __str__(self):
        return self.holiday_title


class Project(models.Model):
    project_name = models.CharField(verbose_name='Project Name', max_length=100, null=True, blank=True)
    project_client_name = models.ForeignKey(Client, verbose_name='Project Client Name', on_delete=models.CASCADE, null=True)
    project_start_date = models.DateField(verbose_name='Project Start Date', null=True, blank=True)
    project_end_date = models.DateField(verbose_name='Project End Date', null=True, blank=True)
    project_cost = models.CharField(verbose_name='Project Cost', max_length=50, null=True, blank=True)
    project_priority = models.CharField(verbose_name='Project Priority', choices=ProjectPriorityChoice.choices, default=ProjectPriorityChoice.LOW, max_length=255, null=True, blank=True)
    project_summary = models.TextField(verbose_name='Project Summary', max_length=1000, null=True, blank=True)
    project_status = models.CharField(verbose_name='Project Status', choices=ProjectStatusChoice.choices, default=ProjectStatusChoice.NOT_STARTED, max_length=255, null=True, blank=True)

    def __str__(self):
        return self.project_name


class ProjectAssign(models.Model):
    project_name = models.ForeignKey(Project, verbose_name='Project Name', on_delete=models.CASCADE, null=True)
    assignee_type = models.CharField(verbose_name='Assignee Type', max_length=50, blank=True, null=True, choices=ProjectAssigneeTypeChoice.choices, default=ProjectAssigneeTypeChoice.TEAM_MEMBER)
    employees = models.ManyToManyField(User, verbose_name='Employee Name')

    def __str__(self):
        return self.project_name.project_name


class ProjectImages(models.Model):
    project_image = models.FileField(verbose_name='Project Image', upload_to='project_images/')
    project_name = models.ForeignKey(Project, verbose_name='Project Id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.project_name


class ProjectFile(models.Model):
    project_file = models.FileField(verbose_name='Project File', upload_to='project_files/')
    project_name = models.ForeignKey(Project, verbose_name='Project Id', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.project_name


class Task(models.Model):
    task_title = models.CharField(verbose_name='Task Title', max_length=100, null=True, blank=True)
    task_status = models.CharField(verbose_name='Task Status', choices=TaskStatusChoice.choices, default=TaskStatusChoice.NEW, max_length=255, null=True, blank=True)
    task_time = models.DurationField(verbose_name="Task Time", null=True, blank=True)
    task_start_time = models.TimeField(verbose_name='Task Start Time', null=True, blank=True)
    task_complete_time = models.TimeField(verbose_name='Task Complete Time', null=True, blank=True)
    task_project = models.ForeignKey(Project, verbose_name='Project Name', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.task_title


class TaskAssign(models.Model):
    task_name = models.ForeignKey(Task, verbose_name='Task Name', on_delete=models.CASCADE, null=True)
    task_project_name = models.ForeignKey(Project, verbose_name='Project Name', on_delete=models.DO_NOTHING, null=True)
    employees = models.ManyToManyField(User, verbose_name='Employee Name', related_name='TaskName')

    def __str__(self):
        return self.task_name.task_title


class Leave(models.Model):
    leave_type = models.CharField(verbose_name='Leave Type', max_length=50, choices=LeaveTypeChoice.choices, default=LeaveTypeChoice.CASUAL, null=True, blank=True)
    leave_from = models.DateField(verbose_name='Leave From', null=True, blank=True)
    leave_to = models.DateField(verbose_name='Leave To', null=True, blank=True)
    leave_days = models.IntegerField(verbose_name='Leave Days', null=True, blank=True)
    leave_reason = models.CharField(verbose_name='Leave Reason', max_length=255, null=True, blank=True)
    leave_status = models.CharField(verbose_name='Leave Status', max_length=100, choices=LeaveStatusChoice.choices, default=LeaveStatusChoice.NEW, null=True, blank=True)
    leave_user = models.ForeignKey(User, verbose_name='User Name', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.leave_type or "Leave"


class Ticket(models.Model):
    ticket_title = models.CharField(verbose_name='Ticket Title', max_length=50, null=True, blank=True)
    ticket_user = models.ForeignKey(User, verbose_name='Ticket User Name', on_delete=models.CASCADE, null=True, blank=True)
    ticket_create_date = models.DateField(verbose_name='Ticket Date', null=True, blank=True)
    ticket_description = models.CharField(verbose_name='Ticket Description', max_length=500, null=True, blank=True)
    ticket_priority = models.CharField(verbose_name='Ticket Priority', max_length=50, choices=TicketPriorityChoice.choices, default=TicketPriorityChoice.LOW, null=True, blank=True)
    ticket_status = models.CharField(verbose_name='Ticket Status', max_length=50, choices=TicketStatusChoice.choices, default=TicketStatusChoice.NEW, null=True, blank=True)
    ticket_status_update_date = models.DateField(verbose_name='Ticket Status Update Date', null=True)

    def __str__(self):
        return self.ticket_title or "Tickets"


class Bank(models.Model):
    employee = models.ForeignKey(User, verbose_name='Bank User Name', on_delete=models.CASCADE, null=True, blank=True, unique=True)
    bank_name = models.CharField(verbose_name="Bank Name", max_length=50, null=True, blank=True)
    bank_account_number = models.BigIntegerField(verbose_name="Bank Account Number", null=True, blank=True)
    bank_ifsc_code = models.CharField(verbose_name="Bank IFSC Code", max_length=20, null=True, blank=True)
    user_pan_card_number = models.CharField(verbose_name="Pan Card Number", max_length=20, null=True, blank=True)
    user_aadhar_card_number = models.BigIntegerField(verbose_name="Aadhar Card", null=True, blank=True)

    def __str__(self):
        return self.employee or "Bank Information"


class Policies(models.Model):
    policy_name = models.CharField(verbose_name="Policy Name", max_length=100, null=True, blank=True)
    policy_department = models.CharField(verbose_name="Policy Department Name", max_length=100, null=True, blank=True)
    policy_create_date = models.DateField(verbose_name="Policy Create Date", null=True, blank=True)
    policy_file = models.FileField(verbose_name="Policy File", upload_to='policies/')

    def __str__(self):
        return self.policy_name


class Interviewers(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="phone number entered in format +910987654321 .")
    country_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True)
    dob = models.DateField(verbose_name='Birth Date', null=True)
    address = models.CharField(verbose_name='Address', max_length=400, null=True)
    email = models.EmailField(verbose_name='Email', max_length=255, null=True)
    gender = models.CharField(verbose_name='Gender', choices=GenderTypeChoice.choices, default=GenderTypeChoice.MALE, max_length=255, null=True)
    city = models.CharField(verbose_name='City', max_length=50, null=True)
    state = models.CharField(verbose_name='State', max_length=50, null=True)
    experience = models.CharField(verbose_name='Experience', max_length=50, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, null=True)
    resume = models.FileField(verbose_name='Upload Resume', upload_to='interviewer_resume/', null=True)
    result = models.CharField(verbose_name="Aptitude Test Result", max_length=50, null=True, blank=True)
    current_ctc = models.CharField(verbose_name="Current CTC", max_length=100, blank=True, null=True)
    current_salary = models.IntegerField(verbose_name="Current Salary", blank=True, null=True)
    expected_salary = models.CharField(verbose_name="Expected  Salary", max_length=50, blank=True, null=True)
    last_company_name = models.CharField(verbose_name="Last Company Name", max_length=100, blank=True, null=True)
    aptitude_test_token = models.CharField(max_length=100, null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class InterviewQuestions(models.Model):
    question = models.TextField(verbose_name="Question", null=True, blank=True)
    option_a = models.CharField(verbose_name="Option A", max_length=100, null=True, blank=True)
    option_b = models.CharField(verbose_name="Option B", max_length=100, null=True, blank=True)
    option_c = models.CharField(verbose_name="Option C", max_length=100, null=True, blank=True)
    option_d = models.CharField(verbose_name="Option D", max_length=100, null=True, blank=True)
    answer = models.CharField(verbose_name="Answer", max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question


class InterviewerResult(models.Model):
    interviewer = models.ForeignKey(Interviewers, verbose_name="Interviewer Name", on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(InterviewQuestions, verbose_name="Interviewer Question", on_delete=models.CASCADE, blank=True, null=True)
    user_answer = models.CharField(verbose_name="Answer", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.interviewer


class Conditions(models.Model):
    condition_title = models.CharField(verbose_name="Condition Title", max_length=250, blank=True, null=True)
    conditional_amount = models.IntegerField(verbose_name="Conditional Amount", blank=True, null=True)
    conditional_object = models.CharField(verbose_name="Conditional Object", max_length=10, blank=True, null=True)
    condition_create_date = models.DateField(verbose_name="Create Date", null=True, blank=True)

    def __str__(self):
        return self.condition_title


class Attendance(models.Model):
    attendee_user = models.ForeignKey(User, verbose_name="Attendee User", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(verbose_name="Date", blank=True, null=True)
    check_in_time = models.TimeField(verbose_name="Check in time", blank=True, null=True)
    check_out_time = models.TimeField(verbose_name="Check in time", blank=True, null=True)
    break_time = models.ForeignKey(Conditions, verbose_name='Break Time', on_delete=models.CASCADE, blank=True, null=True)
    production_hour = models.TimeField(verbose_name="Production Time", blank=True, null=True, max_length=20)
    attendance_status = models.CharField(verbose_name="Attendance status", max_length=50, choices=AttendanceStatusChoice.choices, default=AttendanceStatusChoice.ABSENT, blank=True, null=True)

    def __str__(self):
        return str(self.attendee_user)


class SalarySlip(models.Model):
    user_name = models.ForeignKey(User, verbose_name="User Name", on_delete=models.CASCADE, blank=True, null=True)
    final_salary_amount = models.CharField(verbose_name="Final Salary Amount", max_length=10, null=True, blank=True)
    generate_date = models.DateField(verbose_name="Generate Date", null=True, blank=True)

    def __str__(self):
        return str(self.user_name)


class PersonalConversation(models.Model):
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, blank=True, null=True, related_name="sender")
    receiver = models.ForeignKey(User,verbose_name="Receiver", on_delete=models.CASCADE,blank=True, null=True, related_name="receiver")

    class Meta:
        unique_together = ("sender", "receiver")
        verbose_name = 'Chat Message'

    def __str__(self):
        return str(f"{self.sender} to {self.receiver}")

    @property
    def room_name(self):
        return f'chat_{self.id}'

    @staticmethod
    def chat_conversation_exists(sender, receiver):
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        return PersonalConversation.objects.filter(Q(sender=sender_user, receiver=receiver_user) | Q(sender=receiver_user, receiver=sender_user)).first()

    @staticmethod
    def create_if_not_exists(sender, receiver):
        res = PersonalConversation.chat_conversation_exists(sender, receiver)
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        return False if res else PersonalConversation.objects.create(sender=sender_user, receiver=receiver_user)


class PersonalConversationMessage(models.Model):
    conversation = models.ForeignKey(PersonalConversation, verbose_name="Conversation", on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, verbose_name="Message Sender", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(verbose_name="Message", blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name="Message DateTime", blank=True, null=True)

    def __str__(self):
        return self.conversation


class GroupConversation(models.Model):
    name = models.CharField(verbose_name="Group Name", max_length=50, null=True, blank=True)
    group_avatar = models.ImageField(verbose_name="Group Avatar", upload_to='group_avatars/')

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    group = models.ForeignKey(GroupConversation, verbose_name="Group Conversation", on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Member")
    member_type = models.CharField(verbose_name="Member Type", max_length=20, choices=GroupMembertypeChoice.choices, default=GroupMembertypeChoice.MEMBER, null=True, blank=True)

    def __str__(self):
        return str(self.member)


class GroupConversationMessage(models.Model):
    conversation = models.ForeignKey(GroupMember, verbose_name="Conversation", on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, verbose_name="Message Sender", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(verbose_name="Message", blank=True, null=True)
    timestamp = models.DateTimeField(verbose_name="Message DateTime", blank=True, null=True)

    def __str__(self):
        return self.conversation

