from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable
from wagtail.snippets.blocks import SnippetChooserBlock

from core.choices.worker import WorkerProcessStatusChoice
from core.models.snippets.project import Project
from core.models.snippets.blocks import CostStreamBlock


class WorkersStructBlock(StructBlock):
    worker = SnippetChooserBlock("core.Worker")
    role = blocks.CharBlock(label=_("Role in project"))
    sales_rate = CostStreamBlock(max_num=1, label=_("Sales rate"))


class WorkersStreamBlock(StreamBlock):
    worker = WorkersStructBlock(label=_("Worker info"))


class Demand(Orderable, ClusterableModel):
    vacancy = ParentalKey("core.Vacancy", on_delete=models.SET_NULL, related_name="demands", null=True, blank=True)
    deadline = models.DateField(verbose_name=_("Project deadline"), blank=True, null=True)
    customer = models.CharField(
        max_length=255,
        verbose_name=_("Customer"),
        blank=True,
        null=True,
    )
    partner = models.CharField(
        max_length=255,
        verbose_name=_("Partner"),
        blank=True,
        null=True
    )
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='demands',
        null=True,
        blank=True,
        verbose_name=_("Manager"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
        blank=True
    )

    panels = [
        InlinePanel("projects", label=_("Worker")),
        FieldPanel('customer'),
        FieldPanel('partner'),
        FieldPanel('manager'),
        FieldPanel('deadline'),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return _(f"Запрос {self.id}")
