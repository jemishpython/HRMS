from django.db import models
from django.utils.translation import gettext_lazy as _


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
    WORKING = ("Working", _("WORKING"))
    COMPLETE = ("Complate", _("COMPLETE"))
    PENDING = ("Pending", _("PENDING"))


class LeaveTypeChoice(models.TextChoices):
    CASUAL = ("Casual Leave", _("Casual Leave"))
    MEDICAL = ("Medical Leave", _("Medical Leave"))


class LeaveStatusChoice(models.TextChoices):
    NEW = ("New", _("New"))
    APPROVED = ("Approved", _("Approved"))
    DECLINED = ("Declined", _("Declined"))



