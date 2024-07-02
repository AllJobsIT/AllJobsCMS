from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable

from core.models.snippets.worker import Worker, TechnologiesStreamBlock


class WorkExperience(Orderable):
    worker = ParentalKey(Worker, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Название компании'
    )
    start_year = models.DateField(
        verbose_name='Начало работы',
        blank=True,
        null=True,
    )
    end_year = models.DateField(
        verbose_name='Конец работы',
        blank=True,
        null=True,
    )
    duration = models.FloatField(
        verbose_name="Срок работы",
        blank=True,
        null=True,
    )
    position = models.CharField(
        max_length=255,
        verbose_name='Позиция',
        blank=True,
        null=True,
    )
    description = RichTextField(
        verbose_name='Описание проекта',
        blank=True,
        null=True,
    )
    technologies = StreamField(
        TechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Технологии"
    )

    panels = [
        FieldPanel("company_name"),
        FieldPanel("start_year"),
        FieldPanel("end_year"),
        FieldPanel("duration"),
        FieldPanel("position"),
        FieldPanel("description"),
        FieldPanel("technologies"),
    ]

    def __str__(self):
        return self.company_name


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
