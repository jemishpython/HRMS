from django.db import models
from django.utils.translation import gettext_lazy as _

from hrms_api.models import *


class GenderTypeChoice(models.TextChoices):
    FEMALE = ("Female", _("FEMALE"))
    MALE = ("Male", _("MALE"))


class MaritalStatusChoice(models.TextChoices):
    MARRIED = ("Marride", _("MARRIDE"))
    SINGLE = ("Single", _("SINGLE"))


class ProjectAssigneeTypeChoice(models.TextChoices):
    LEADER = ("Leader", _("LEADER"))
    TEAM_MEMBER = ("Team Member", _("TEAM MEMBER"))


class ProjectPriorityChoice(models.TextChoices):
    LOW = ("Low", _("LOW"))
    MEDIUM = ("Medium", _("MEDIUM"))
    HIGH = ("High", _("HIGH"))


class ProjectStatusChoice(models.TextChoices):
    ON_TRACK = ("On Track", _("ON_TRACK"))
    POSTPONED = ("Postponed", _("POSTPONED"))
    FINISHED = ("Finished", _("FINISHED"))
    NOT_STARTED = ("Not Started", _("NOT_STARTED"))


class TaskStatusChoice(models.TextChoices):
    NEW = ("New", _("NEW"))
    WORKING = ("Working", _("WORKING"))
    PENDING = ("Pending", _("PENDING"))
    COMPLETE = ("Complete", _("COMPLETE"))


class LeaveTypeChoice(models.TextChoices):
    CASUAL = ("Casual Leave", _("Casual Leave"))
    MEDICAL = ("Medical Leave", _("Medical Leave"))


class LeaveStatusChoice(models.TextChoices):
    NEW = ("New", _("New"))
    APPROVED = ("Approved", _("Approved"))
    DECLINED = ("Declined", _("Declined"))


class TicketPriorityChoice(models.TextChoices):
    LOW = ("Low", _("LOW"))
    MEDIUM = ("Medium", _("MEDIUM"))
    HIGH = ("High", _("HIGH"))


class TicketStatusChoice(models.TextChoices):
    NEW = ("New", _("New"))
    APPROVED = ("Approved", _("Approved"))
    DECLINED = ("Declined", _("Declined"))


class AttendanceStatusChoice(models.TextChoices):
    PRESENT = ("Present", _("PRESENT"))
    ABSENT = ("Absent", _("ABSENT"))
    HALF_DAY = ("Half Day", _("HALF_DAY"))


class GroupMembertypeChoice(models.TextChoices):
    ADMIN = ("Admin", _("ADMIN"))
    MEMBER = ("Member", _("MEMBER"))


class GroupMemberStatusChoice(models.TextChoices):
    ONLINE = ("Online", _("ONLINE"))
    OFFLINE = ("Offline", _("OFFLINE"))
