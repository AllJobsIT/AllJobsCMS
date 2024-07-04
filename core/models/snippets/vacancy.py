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
    stack_item = blocks.CharBlock(label="Элемент стэка")


class RequirementsStreamField(StreamBlock):
    requirements_item = blocks.CharBlock(label="Элемент требования")


class ResponsibilitiesStreamField(StreamBlock):
    responsibilities_item = blocks.CharBlock(label="Элемент обязанности")


class Vacancy(ClusterableModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        verbose_name='UUID Вакансии',
    )
    title = models.CharField(max_length=255, verbose_name="Название вакансии", blank=True, null=True)
    specialization = StreamField(
        SpecializationStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Специализация"
    )
    stack = StreamField(
        StackStreamField(), blank=True, null=True, use_json_field=True, verbose_name="Стэк"
    )
    requirements = StreamField(
        RequirementsStreamField(), blank=True, null=True, use_json_field=True, verbose_name="Требования к кандидату"
    )
    responsibilities = StreamField(
        ResponsibilitiesStreamField(), blank=True, null=True, use_json_field=True, verbose_name="Обязанности кандидата"
    )
    cost = models.IntegerField(verbose_name="Рейт вакансии", blank=True, null=True)
    location = CountryField(verbose_name="Локация вакансии", blank=True, null=True)
    load = models.CharField(verbose_name="Загрузка вакансии", max_length=255, blank=True, null=True)

    tags = TaggableManager(through='VacancyTags', blank=True, related_name='vacancy_tags')
    grades = StreamField(
        GradeStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Грейды"
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
                                                      verbose_name="Полный текст скопированной из тг вакансии")

    main_panels = [
        FieldPanel("title"),
        FieldPanel("status"),
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
        FieldPanel("created_at", read_only=True),
        FieldPanel("updated_at", read_only=True),
        FieldPanel("channel", read_only=True),
        FieldPanel("full_vacancy_text_from_tg_chat"),
    ]

    demand_panels = [
        InlinePanel("demands", max_num=1, label=_("Request")),
    ]

    edit_handler = TabbedInterface([
        ObjectList(main_panels, heading='Главная'),
        ObjectList(demand_panels, heading='Запросы'),
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

    get_stack_display.admin_order_field = "Стэк"
    get_stack_display.short_description = "Стэк"

    get_status.admin_order_field = "Статус"
    get_status.short_description = "Статус"
