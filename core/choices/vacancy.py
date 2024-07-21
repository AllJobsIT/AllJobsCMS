from django.db import models
from django.utils.translation import gettext_lazy as _


class VacancyProcessStatusChoices(models.IntegerChoices):
    PROCESS_ERROR = -1, _("AI processing failed")
    AWAITING_APPROVE = 0, _("Awaiting approval")
    PROCESS = 1, _("AI Processing")
    MODERATION = 2, _("Moderation")
    READY_TO_PUBLIC = 3, _("Ready to publish")
    PUBLIC = 4, _("Published")
    WORKER_FOUND = 5, _("Worker found")
    IN_PROGRESS = 6, _("In progress")
    IN_ARCHIVE = 7, _("In archive")
