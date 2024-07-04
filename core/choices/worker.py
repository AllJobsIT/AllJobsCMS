from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkerProcessStatusChoice(models.IntegerChoices):
    PROCESS_ERROR = -1, _("Обработка с помощью ИИ не удалась")
    PROCESS = 0, _("Обработка с помощью ИИ")
    MODERATION = 1, _("Модерация")
    LOADED = 2, _("Ожидает вакансии")
    SUBMIT = 3, _("Подали на запрос")
    REFUSE_AFTER_INTERVIEW = 4, _("Отказ после собеса")
    REFUSE_ON_RESUME = 5, _("Отказ по резюме")
    CALL_IN_INTERVIEW = 6, _("Позвали на собес")
    WAITING_FEEDBACK = 7, _("Ожидаем ОС")
    AGREED_TO_WORK = 8, _("Согласован выход")
    NOT_ACTIVE = 9, _("Не активен")
    WORK_IN_PROJECT = 10, _("Работает на проекте")
    IN_ARCHIVE = 11, _("В архиве")
