import uuid

from botmanager.models import Task
from django import forms
from django.db import models
from django.forms.formsets import DELETION_FIELD_NAME, ORDERING_FIELD_NAME
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, TabbedInterface, ObjectList, Panel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

from core.choices.vacancy import VacancyProcessStatusChoices, VacancyTypeChoices
from core.models.snippets.blocks import CostStreamBlock
from core.panels.vacancy_panels import EligibleWorkersPanel
from core.tasks.vacancy_task import SendVacancy, ProcessVacancy

class MyInlinePanel(InlinePanel):
    class BoundPanel(Panel.BoundPanel):
        template_name = "wagtailadmin/panels/inline_panel.html"

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.label = self.panel.label

            if self.form is None:
                return

            self.formset = self.form.formsets.get(self.panel.relation_name, None)
            self.child_edit_handler = self.panel.child_edit_handler

            self.children = []
            for index, subform in enumerate(self.formset.forms):
                # override the DELETE field to have a hidden input
                subform.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()

                # ditto for the ORDER field, if present
                if self.formset.can_order:
                    subform.fields[ORDERING_FIELD_NAME].widget = forms.HiddenInput()

                self.children.append(
                    self.child_edit_handler.get_bound_panel(
                        instance=subform.instance,
                        request=self.request,
                        form=subform,
                        prefix=("%s-%d" % (self.prefix, index)),
                    )
                )

            # if this formset is valid, it may have been re-ordered; respect that
            # in case the parent form errored and we need to re-render
            if self.formset.can_order and self.formset.is_valid():
                self.children.sort(
                    key=lambda child: child.form.cleaned_data[ORDERING_FIELD_NAME] or 1
                )

            empty_form = self.formset.empty_form
            empty_form.fields[DELETION_FIELD_NAME].widget = forms.HiddenInput()
            if self.formset.can_order:
                empty_form.fields[ORDERING_FIELD_NAME].widget = forms.HiddenInput()

            self.empty_child = self.child_edit_handler.get_bound_panel(
                instance=empty_form.instance,
                request=self.request,
                form=empty_form,
                prefix=("%s-__prefix__" % self.prefix),
            )


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
                                    default=VacancyTypeChoices.A)

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
        MyInlinePanel("vacancy_demands", label=_("Demand"), max_num=1),
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
