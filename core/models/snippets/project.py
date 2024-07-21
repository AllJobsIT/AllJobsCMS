from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable

from core.models.snippets.blocks import CostStreamBlock
from core.models.snippets.worker import Worker, TechnologiesStreamBlock


class WorkExperience(Orderable):
    worker = ParentalKey(Worker, on_delete=models.CASCADE, related_name='work_experiences')
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Company name')
    )
    start_year = models.DateField(
        verbose_name=_('Start work'),
        blank=True,
        null=True,
    )
    end_year = models.DateField(
        verbose_name=_('End work'),
        blank=True,
        null=True,
    )
    duration = models.FloatField(
        verbose_name=_("Work duration"),
        blank=True,
        null=True,
    )
    position = models.CharField(
        max_length=255,
        verbose_name=_('Position'),
        blank=True,
        null=True,
    )
    description = RichTextField(
        verbose_name=_('Project description'),
        blank=True,
        null=True,
    )
    technologies = StreamField(
        TechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Project technologies")
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
    vacancy = models.ForeignKey(
        "core.Vacancy",
        on_delete=models.CASCADE, verbose_name=_("Vacancy for project"), null=True, default=None
    )
    date_start = models.DateField(
        verbose_name=_('Start work'),
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name=_('End work'),
        blank=True,
        null=True,
    )
    sales_rate = StreamField(
        CostStreamBlock(max_num=1), blank=True, null=True, use_json_field=True, verbose_name=_("Sales rate")
    )
    role = models.CharField(
        max_length=255,
        verbose_name=_('Role in project'),
        blank=True
    )
    team = RichTextField(
        verbose_name=_("Project team"),
        blank=True
    )
    date_of_application = models.DateField(
        verbose_name=_("Date of application"), default=now
    )

    panels = [
        FieldPanel("vacancy"),
        FieldPanel("date_start"),
        FieldPanel("date_end"),
        FieldPanel("sales_rate"),
        FieldPanel("role"),
        FieldPanel("team"),
        FieldPanel("date_of_application"),
    ]

    def __str__(self):
        return self.title
