from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import Document

from core.models.snippets.demand import Demand


class Candidate(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
    )
    telegram_nickname = models.CharField(
        max_length=255,
        verbose_name='Telegram',
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name='Название компании',
        blank=True
    )
    demand = models.ForeignKey(
        Demand,
        related_name='candidates',
        on_delete=models.CASCADE
    )
    file = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('telegram_nickname'),
        FieldPanel('company_name'),
        FieldPanel('demand'),
        FieldPanel('file'),
        FieldPanel('is_active'),
        FieldPanel('created_at', read_only=True),
        FieldPanel('updated_at', read_only=True),
    ]

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __str__(self):
        return self.name
