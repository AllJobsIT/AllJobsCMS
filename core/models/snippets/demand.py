from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable


class Demand(Orderable, ClusterableModel):
    vacancy = ParentalKey("core.Vacancy", on_delete=models.SET_NULL, related_name="demands", null=True, blank=False)
    partner = models.CharField(
        max_length=255,
        verbose_name=_("Partner"),
        blank=True,
        null=True
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='managers',
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Manager"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
        blank=True
    )

    panels = [
        InlinePanel("projects", label=_("Worker")),
        FieldPanel('partner'),
        FieldPanel('manager', read_only=True),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return _(f"Worker {self.id}")

