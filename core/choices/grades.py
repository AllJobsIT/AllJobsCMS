from django.db import models
from django.utils.translation import gettext_lazy as _


class GradeChoice(models.IntegerChoices):
    INTERN = 0, _("Intern")
    JUNIOR = 1, _("Junior")
    MIDDLE = 2, _("Middle")
    SENIOR = 3, _("Senior")
    LEAD = 4, _("Lead")
