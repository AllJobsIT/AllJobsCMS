from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
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


class Demand(Orderable):
    vacancy = ParentalKey("core.Vacancy", on_delete=models.SET_NULL, related_name="demands", null=True, blank=True)
    workers = StreamField(
        WorkersStreamBlock(), null=True, blank=True, use_json_field=True, verbose_name="Работник"
    )
    deadline = models.DateField(verbose_name="Дедлайн проекта", blank=True, null=True)
    company_name = models.CharField(
        max_length=255,
        verbose_name='Заказчик',
        blank=True,
        null=True,
    )
    partner = models.CharField(
        max_length=255,
        verbose_name="Партнер",
        blank=True,
        null=True
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
        FieldPanel('partner'),
        FieldPanel('manager'),
        FieldPanel('deadline'),
        FieldPanel('is_active'),
    ]

    def __str__(self):
        return f"Запрос {self.id}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        for block in self.workers:
            worker = block.value
            worker['worker'].process_status = WorkerProcessStatusChoice.SUBMIT
            today = now().date()
            project = Project.objects.create(
                worker=worker['worker'],
                vacancy=self.vacancy,
                date_start=today,
                date_end=self.deadline,
                sales_rate=worker['sales_rate'],
                role=worker['role'],
                date_of_application=today
            )
            worker['worker'].projects.add(project)
            worker['worker'].save()
