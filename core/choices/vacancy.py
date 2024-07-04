from django.db import models
from django.utils.translation import gettext_lazy as _


class VacancyStatusChoices(models.IntegerChoices):
    PROCESS_ERROR = -1, _("Обработка с помощью ИИ не удалась")
    AWAITING_APPROVE = 0, _("Ожидает одобрения")
    PROCESS = 1, _("Обработка с помощью ИИ")
    MODERATION = 2, _("Модерация")
    READY_TO_PUBLIC = 3, _("Готов к публикации")
    PUBLIC = 4, _("Опубликован")
    WORKER_FOUND = 5, _("Найден исполнитель")
    IN_PROGRESS = 6, _("В работе")
    IN_ARCHIVE = 7, _("В архиве")
