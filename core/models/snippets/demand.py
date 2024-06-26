from datetime import datetime, timedelta

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable
from wagtail.snippets.blocks import SnippetChooserBlock

from core.models.snippets.steps_in_board import StepsInBoard


class WorkersStreamBlock(StreamBlock):
    worker = SnippetChooserBlock("core.Worker")


class Demand(Orderable):
    vacancy = ParentalKey("core.Vacancy", on_delete=models.SET_NULL, related_name="demands", null=True, blank=True)
    workers = StreamField(
        WorkersStreamBlock(), null=True, blank=True, use_json_field=True, verbose_name="Работник"
    )
    duration = models.DateField(verbose_name="Дедлайн проекта", blank=True, null=True)
    company_name = models.CharField(
        max_length=255,
        verbose_name='Заказчик',
        blank=True,
        null=True,
    )
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='demands',
        null=True,
        blank=True,
        verbose_name='Менеджер',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
        blank=True
    )

    panels = [
        FieldPanel('workers'),
        FieldPanel('company_name'),
        FieldPanel('manager'),
        FieldPanel('duration'),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return f"Запрос {self.id}"
