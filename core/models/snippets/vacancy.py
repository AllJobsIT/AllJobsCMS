import uuid

from botmanager.models import Task
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

from core.choices.vacancy import VacancyProcessStatusChoices
from core.middleware import get_current_request
from core.models.snippets.demand import Demand
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


class Vacancy(ClusterableModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        verbose_name=_("UUID vacancy"),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=True, null=True)
    specialization = StreamField(
        SpecializationStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Specializations")
    )
    stack = StreamField(
        StackStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Stacks")
    )
    requirements = StreamField(
        RequirementsStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Requirements")
    )
    responsibilities = StreamField(
        ResponsibilitiesStreamField(), blank=True, null=True, use_json_field=True, verbose_name=_("Responsibilities")
    )
    cost = models.IntegerField(verbose_name=_("Cost"), blank=True, null=True)
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
        verbose_name='Активный',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )
    is_send = models.BooleanField(default=False)
    channel = models.CharField(max_length=255, blank=True, null=True)
    full_vacancy_text_from_tg_chat = models.TextField(blank=True,
                                                      verbose_name=_("Full vacancy text"))

    main_panels = [
        FieldPanel("title"),
        FieldPanel("status"),
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        FieldPanel("channel", read_only=True),
        FieldPanel("full_vacancy_text_from_tg_chat"),
    ]

    about_vacancy_panels = [
        FieldPanel("specialization"),
        FieldPanel("stack"),
        FieldPanel("requirements"),
        FieldPanel("responsibilities"),
        FieldPanel("cost"),
        FieldPanel("location"),
        FieldPanel("load"),
        FieldPanel("tags"),
        FieldPanel("grades"),
        FieldPanel("is_active"),
    ]

    demand_panels = [
        InlinePanel("demands", max_num=1, label=_("Submitted candidates")),
    ]

    edit_handler = TabbedInterface([
        ObjectList(main_panels, heading=_("Main")),
        ObjectList(about_vacancy_panels, heading=_("About vacancy")),
        ObjectList(demand_panels, heading=_("Demands")),
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
        if self.status == VacancyProcessStatusChoices.PUBLIC:
            request = get_current_request()
            demand = Demand.objects.create(
                vacancy=self,
                manager=request.user
            )
            demand.save()

    def get_status(self):
        return self.get_status_display()

    def get_stack_display(self):
        # Возвращает строковое представление грейда
        return ", ".join([str(item.value) for item in self.stack])[:80] + '...'

    get_stack_display.admin_order_field = _("Stack")
    get_stack_display.short_description = _("Stack")

    get_status.admin_order_field = _("Status")
    get_status.short_description = _("Status")
