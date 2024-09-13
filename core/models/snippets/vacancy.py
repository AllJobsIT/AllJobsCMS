from botmanager.models import Task
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

from core.choices.vacancy import VacancyProcessStatusChoices, VacancyTypeChoices
from core.choices.worker import WorkerProjectFeedback
from core.models.snippets.blocks import CostStreamBlock
from core.panels.vacancy_panels import EligibleWorkersPanel
from core.tasks.vacancy_task import SendVacancy, ProcessVacancy


class VacancyTags(TaggedItemBase):
    content_object = ParentalKey(
        to='Vacancy', on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class GradeStreamBlock(StreamBlock):
    grade = SnippetChooserBlock("core.Grade")


class SpecializationStreamBlock(StreamBlock):
    specialization = SnippetChooserBlock("core.Specialization")


class StackStreamField(StreamBlock):
    stack_item = blocks.CharBlock(label=_("Stack item"))


class RequirementsStreamField(StreamBlock):
    requirements_item = blocks.CharBlock(label=_("Requirements item"))


class ResponsibilitiesStreamField(StreamBlock):
    responsibilities_item = blocks.CharBlock(label=_("Responsibilities item"))


class FeedbackStructBlock(StructBlock):
    type = blocks.ChoiceBlock(WorkerProjectFeedback.choices, label=_("Type feedback"))
    value = blocks.RichTextBlock(label=_("Feedback text"))


class FeedbackStreamField(StreamBlock):
    feedback_item = FeedbackStructBlock(label=_("Feedback item"))


class ProjectStructBlock(StructBlock):
    worker = SnippetChooserBlock(
        "core.Worker", label=_("Worker for project")
    )
    date_start = blocks.DateBlock(
        label=_('Project submission date'),
        blank=True,
        null=True,
    )
    sales_rate = CostStreamBlock(label=_("Cost item"))

    feedback = FeedbackStreamField(label=_("Feedback item"))


class ProjectStreamBlock(StreamBlock):
    project = ProjectStructBlock()


class DemandStructBlock(StructBlock):
    projects = ProjectStreamBlock()
    partner = blocks.CharBlock(
        max_length=255,
        label=_("Partner"),
        blank=True,
        null=True
    )
    is_active = blocks.BooleanBlock(
        default=True,
        label=_("Is active"),
        blank=True
    )


class DemandStreamBlock(StreamBlock):
    demand = DemandStructBlock()


class Vacancy(ClusterableModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True, null=True)
    specialization = StreamField(
        SpecializationStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Specializations")
    )
    stack = StreamField(
        StackStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Stack")
    )
    requirements = StreamField(
        RequirementsStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Requirements")
    )
    responsibilities = StreamField(
        ResponsibilitiesStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Responsibilities")
    )
    cost = models.IntegerField(verbose_name=_("Cost"), blank=True, null=True)
    salary = StreamField(
        CostStreamBlock(max_num=1), blank=False, null=True, use_json_field=True, verbose_name=_("Salary")
    )
    location = CountryField(verbose_name=_("Location"), blank=True, null=True)
    load = models.CharField(verbose_name=_("Load"), max_length=255, blank=True, null=True)

    tags = TaggableManager(through='VacancyTags', blank=True, related_name='vacancy_tags')
    grades = StreamField(
        GradeStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Grades")
    )
    status = models.IntegerField(choices=VacancyProcessStatusChoices,
                                 default=VacancyProcessStatusChoices.AWAITING_APPROVE)
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is active"),
        blank=True
    )
    customer = models.CharField(
        max_length=255,
        verbose_name=_("Customer"),
        blank=True,
        null=True,
    )
    deadline = models.DateField(verbose_name=_("Project deadline"), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    is_send = models.BooleanField(default=False)
    channel = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    full_vacancy_text_from_tg_chat = models.TextField(blank=True,
                                                      verbose_name=_("Full vacancy text"))
    type = models.SmallIntegerField(verbose_name=_("Type vacancy"), choices=VacancyTypeChoices.choices,
                                    default=VacancyTypeChoices.B)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='managers',
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Manager"),
    )
    demands = StreamField(
        DemandStreamBlock(max_num=1), verbose_name=_("Demand"), use_json_field=True, blank=True
    )

    main_panels = [
        FieldPanel("full_vacancy_text_from_tg_chat"),
        FieldPanel("title"),
        FieldPanel("status"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        FieldPanel("channel"),
        FieldPanel("source"),
    ]

    about_vacancy_panels = [
        FieldPanel("customer"),
        FieldPanel("deadline"),
        FieldPanel("type"),
        FieldPanel("specialization"),
        FieldPanel("stack"),
        FieldPanel("requirements"),
        FieldPanel("responsibilities"),
        FieldPanel("cost"),
        FieldPanel("salary"),
        FieldPanel("location"),
        FieldPanel("load"),
        FieldPanel("tags"),
        FieldPanel("grades"),
        FieldPanel("is_active"),
    ]

    demand_panels = [
        FieldPanel("demands"),
        FieldPanel("manager", read_only=True),
    ]

    eligible_workers_panels = [
        EligibleWorkersPanel()
    ]

    edit_handler = TabbedInterface([
        ObjectList(main_panels, heading=_("Main")),
        ObjectList(about_vacancy_panels, heading=_("About vacancy")),
        ObjectList(demand_panels, heading=_("Submitted workers")),
        ObjectList(eligible_workers_panels, heading=_("Eligible workers")),
    ])

    def __str__(self):
        return f"{self.title} from {self.channel if self.channel else 'Manager'}"

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.status == VacancyProcessStatusChoices.PROCESS and self.full_vacancy_text_from_tg_chat:
            for task in Task.objects.filter(name="process_vacancy"):
                if task.input.get("id", None) == self.id:
                    return
            ProcessVacancy.create(input={'id': self.id})
            return
        if self.status == VacancyProcessStatusChoices.READY_TO_PUBLIC:
            for task in Task.objects.filter(name="send_vacancy"):
                if task.input.get("id", None) == self.id:
                    return
            SendVacancy.create(input={'id': self.id})

    def get_status(self):
        return self.get_status_display()

    def get_stack_display(self):
        # Возвращает строковое представление грейда
        return ", ".join([str(item.value) for item in self.stack])[:80] + '...'

    def get_type(self):
        return self.get_type_display()

    get_stack_display.admin_order_field = "stack"
    get_stack_display.short_description = _("Stack")

    get_type.admin_order_field = "type"
    get_type.short_description = _("Type vacancy")

    get_status.admin_order_field = "status"
    get_status.short_description = _("Status")
