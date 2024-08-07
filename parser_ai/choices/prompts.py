from django.db import models
from django.utils.translation import gettext_lazy as _


class MethodChoice(models.TextChoices):
    REPLACE = "REPLACE", _("Replace")
    APPEND = "APPEND", _("Append")
