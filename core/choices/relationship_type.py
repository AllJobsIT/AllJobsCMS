from django.db import models
from django.utils.translation import gettext_lazy as _


class RelationshipTypeChoice(models.IntegerChoices):
    UNSPECIFIED = -1, "--"
    EMPLOYEE = 0, _("Наемный")
    STAFF = 1, _("Штатный")
    AFFILIATE = 2, _("От партнера")
