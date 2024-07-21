from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable

from core.choices.worker import WorkerProjectFeedback
from core.models.snippets.blocks import CostStreamBlock
from core.models.snippets.worker import TechnologiesStreamBlock


class FeedbackStructBlock(StructBlock):
    type = blocks.ChoiceBlock(WorkerProjectFeedback.choices, label=_("Type feedback"))
    value = blocks.RichTextBlock(label=_("Feedback text"))


class FeedbackStreamField(StreamBlock):
    feedback_item = FeedbackStructBlock(label=_("Feedback item"))


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
        FieldPanel("duration"),
        FieldPanel("position"),
        FieldPanel("description"),
        FieldPanel("technologies"),
    ]

    def __str__(self):
        return self.company_name


class Project(Orderable):
    demand = ParentalKey(
        "core.Demand", on_delete=models.CASCADE, related_name='projects', null=True, blank=True
    )
    worker = models.ForeignKey(
        "core.Worker",
        on_delete=models.CASCADE, verbose_name=_("Worker for project"), null=True, default=None
    )
    date_start = models.DateField(
        verbose_name=_('Start work'),
        blank=True,
        null=True,
        default=now
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

    feedback = StreamField(
        FeedbackStreamField(max_num=1), use_json_field=True, null=True, blank=True, verbose_name=_("Feedback")
    )

    panels = [
        FieldPanel("worker"),
        FieldPanel("date_start"),
        FieldPanel("sales_rate"),
        FieldPanel("role"),
        FieldPanel("team"),
        FieldPanel("feedback"),
    ]

    def __str__(self):
        return self.worker.full_name()
