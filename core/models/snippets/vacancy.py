import uuid

from botmanager.models import Task
from django.db import models
from django_countries.fields import CountryField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

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
    STATUSES = (
        (-1, "Обработка с помощью ИИ не удалась"),
        (0, "Обработка с помощью ИИ"),
        (1, "Модерация"),
        (2, "Готов к отправке"),
        (3, "Отправлен"),
        (4, "Найден исполнитель"),
        (5, "В исполнении"),
        (6, "В архиве"),
    )
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
    status = models.IntegerField(choices=STATUSES, default=0)
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

    panels = [
        FieldPanel("title"),
        FieldPanel("specialization"),
        FieldPanel("stack"),
        FieldPanel("status"),
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
        InlinePanel("demands", max_num=1),
    ]

    def __str__(self):
        return f"{self.title} from {self.channel if self.channel else 'Manager'}"

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.status == 0 and self.full_vacancy_text_from_tg_chat is not None:
            for task in Task.objects.filter(name="process_vacancy"):
                if task.input.get('id') == self.id:
                    return
            ProcessVacancy.create(input={'id': self.id})
        if self.status == 2:
            SendVacancy.create(input={'id': self.id})
            self.status += 1
        if self.status == 4:
            request = get_current_request()
            demand = Demand.objects.create(
                vacancy=self,
                manager=request.user
            )
            demand.save()

    def get_status(self):
        return self.get_status_display()

    get_status.admin_order_field = "Статус"
    get_status.short_description = "Статус"
