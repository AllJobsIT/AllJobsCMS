from django.db import models
from django.utils.translation import gettext_lazy as _


class RelationshipTypeChoice(models.IntegerChoices):
    UNSPECIFIED = -1, "--"
    EMPLOYEE = 0, _("Employee")
    STAFF = 1, _("Standard")
    AFFILIATE = 2, _("From Affiliate")
