from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable

from core.models.snippets.worker import Worker


class Project(Orderable):
    worker = ParentalKey(Worker, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование проекта'
    )
    date_start = models.DateField(
        verbose_name='Начало работы',
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name='Конец работы',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=255,
        verbose_name='Роль в проекте',
        blank=True
    )
    responsibilities = RichTextField(
        verbose_name='Обязанности на проекте',
        blank=True,
    )
    description = RichTextField(
        verbose_name='Описание проекта',
        blank=True
    )
    technologies = RichTextField(
        verbose_name='Технологии проекта',
        blank=True
    )
    team = RichTextField(
        verbose_name='Состав команды',
        blank=True
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("date_start"),
        FieldPanel("date_end"),
        FieldPanel("role"),
        FieldPanel("responsibilities"),
        FieldPanel("description"),
        FieldPanel("technologies"),
        FieldPanel("team"),
    ]

    def __str__(self):
        return self.title
