from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkerProcessStatusChoice(models.IntegerChoices):
    PROCESS_ERROR = -1, _("AI processing failed")
    PROCESS = 0, _("AI Processing")
    MODERATION = 1, _("Moderation")
    LOADED = 2, _("Waiting for vacancies")
    SUBMIT = 3, _("Submitted to request")
    REFUSE_AFTER_INTERVIEW = 4, _("Refusal after social security")
    REFUSE_ON_RESUME = 5, _("Resume refusal")
    CALL_IN_INTERVIEW = 6, _("Called for an interview")
    WAITING_FEEDBACK = 7, _("Waiting for feedback")
    AGREED_TO_WORK = 8, _("Output agreed")
    NOT_ACTIVE = 9, _("Not active")
    WORK_IN_PROJECT = 10, _("Working on the project")
    IN_ARCHIVE = 11, _("Archived")


class WorkerProjectFeedback(models.IntegerChoices):
    NEGATIVE = 0, _("Negative")
    NORMAL = 1, _("Normal")
    POSITIVE = 2, _("Positive")


class WorkerInputMethod(models.IntegerChoices):
    HABR = 0, _("Habr")
    HEAD_HUNTER = 1, _("Head Hunter")
    MANUAL = 2, _("Manual")
