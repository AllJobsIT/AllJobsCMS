from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable

from core.models.snippets.worker import TechnologiesStreamBlock


class WorkExperience(Orderable):
    worker = ParentalKey("core.Worker", on_delete=models.CASCADE, related_name='work_experiences')
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
