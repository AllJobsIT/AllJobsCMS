from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkerStatusChoice(models.IntegerChoices):
    PROCESS_ERROR = -1, _("Обработка с помощью ИИ не удалась")
    PROCESS = 0, _("Обработка с помощью ИИ")
    MODERATION = 1, _("Модерация")
    LOADED = 2, _("Загружен")
    IN_ARCHIVE = 3, _("В архиве")
