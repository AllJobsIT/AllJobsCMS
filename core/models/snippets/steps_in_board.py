from django.db import models
from wagtail.admin.panels import FieldPanel

from core.models.snippets.base import BaseSnippet


class StepsInBoard(BaseSnippet):
    name = models.CharField(max_length=500)
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Сортировка',
        db_index=True,
        blank=False,
        null=False,
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Является шагом по-умолчанию',
        help_text='Новым заявкам будет проставляться данный шаг (если не указан какой-либо другой)',
        blank=True
    )
    is_hidden = models.BooleanField(
        default=False,
        verbose_name='Скрыть шаг (статус) на доске',
        help_text='Данный шаг (статус) не будет отображаться на доске. Заявкам можно проставить его чтобы скрыть их с доски',
        blank=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('sort_order'),
        FieldPanel('is_default'),
        FieldPanel('is_hidden'),
    ]

    @classmethod
    def get_default_board(cls):
        return cls.objects.get(is_default=True)
