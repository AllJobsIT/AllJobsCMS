import uuid

from django.db import models
from django_countries.fields import CountryField
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.documents.models import Document
from wagtail.fields import RichTextField, StreamField
from wagtail.snippets.blocks import SnippetChooserBlock

from core.models.snippets.base import Status, Type


class EnglishGradeStructBlock(StructBlock):
    language = blocks.CharBlock(label="Язык")
    grade = blocks.CharBlock(label="Знание языка")


class EnglishGradeStreamBlock(StreamBlock):
    language = EnglishGradeStructBlock(label="Элемент языка")


class StackStreamBlock(StreamBlock):
    stack_item = blocks.CharBlock(label="Элемент стэка")


class SkillStreamBlock(StreamBlock):
    skill_item = blocks.CharBlock(label="Элемент навыка")


class ProgrammingLanguageStreamBlock(StreamBlock):
    language_item = blocks.CharBlock(label="Язык программирования")


class TechnologiesStreamBlock(StreamBlock):
    technology_item = blocks.CharBlock(label="Элемент технологии")


class DatabasesStreamBlock(StreamBlock):
    database_item = blocks.CharBlock(label="Элемент базы данных")


class SoftwareDevelopmentStreamBlock(StreamBlock):
    software_development_item = blocks.CharBlock(label="Элемент средства разработки")


class OtherTechnologiesStreamBlock(StreamBlock):
    other_technology_item = blocks.CharBlock(label="Элемент другой технологии")


class CertificatesStreamBlock(StreamBlock):
    certificate_item = blocks.CharBlock(label="Элемент сертификата")


class ExampleOfWorkStreamBlock(StreamBlock):
    example_of_work_item = blocks.URLBlock(label="Элемент примера работы")


class ContactsStructBlock(StructBlock):
    name = blocks.CharBlock(label="Тип контакта")
    value = blocks.CharBlock(label="Значение")


class ContactsStreamBlock(StreamBlock):
    contact = ContactsStructBlock(label="Элемент контакта")


class LinksStructBlock(StructBlock):
    type = blocks.CharBlock(label="Тип ссылки")
    link = blocks.URLBlock(label="Ссылка")


class LinksStreamBlock(StreamBlock):
    link = LinksStructBlock(label="Элемент ссылки")


class SpecializationStreamBlock(StreamBlock):
    specialization = SnippetChooserBlock("core.Specialization")


class GradeStreamBlock(StreamBlock):
    grade = SnippetChooserBlock("core.Grade")


class Worker(ClusterableModel):
    STATUSES = (
        (-1, "Обработка с помощью ИИ не удалась"),
        (0, "Обработка с помощью ИИ"),
        (1, "Модерация"),
        (2, "Загружен"),
        (3, "В архиве"),
    )
    code = models.UUIDField(
        verbose_name='Код работника',
        blank=True,
        default=uuid.uuid4,
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя',
        null=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия',
        null=True
    )
    surname = models.CharField(
        max_length=255,
        verbose_name='Отчество',
        blank=True,
        null=True
    )
    file = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Резюме"
    )
    telegram_nickname = models.CharField(
        max_length=255,
        verbose_name='Telegram nickname',
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        verbose_name='Статус',
        blank=True,
        null=True
    )
    status_date = models.DateField(
        verbose_name='Дата изменения статуса',
        blank=True,
        null=True,
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        verbose_name='Тип отношений',
        blank=True,
        null=True
    )
    employer = models.CharField(
        max_length=255,
        verbose_name='Работодатель сотрудника',
        blank=True,
        null=True
    )
    sales_rate = models.IntegerField(
        verbose_name='Рейт продажи',
        blank=True,
        null=True,
    )
    purchase_rate = models.IntegerField(
        verbose_name='Рейт покупки',
        blank=True,
        null=True,
    )
    specialization = StreamField(
        SpecializationStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Специализация"
    )
    grade = StreamField(
        GradeStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Грейд"
    )
    stack = StreamField(
        StackStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Стэк"
    )
    skills = StreamField(
        SkillStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name="Навыки"
    )
    programming_languages = StreamField(
        ProgrammingLanguageStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Опыт работы с языками"
    )
    technologies = StreamField(
        TechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Технологии"
    )
    databases = StreamField(
        DatabasesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Базы данных"
    )
    software_development = StreamField(
        SoftwareDevelopmentStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Средства разработки ПО"
    )
    other_technologies = StreamField(
        OtherTechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Другие технологии"
    )
    about_worker = RichTextField(
        verbose_name='О себе',
        blank=True,
        null=True
    )
    experience = models.FloatField(
        verbose_name='Стаж',
        blank=True,
        null=True,
        default=0.0
    )
    city = models.CharField(
        max_length=255,
        verbose_name='Город проживания',
        blank=True,
        null=True
    )
    citizenship = CountryField(
        verbose_name='Гражданство',
        blank=True,
        null=True
    )
    english_grade = StreamField(
        EnglishGradeStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Языки"
    )
    education = RichTextField(
        verbose_name='Образование',
        blank=True,
        null=True
    )
    certificates = StreamField(
        CertificatesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Сертификаты"
    )
    employer_contact = models.CharField(
        max_length=255,
        verbose_name='Контакт работодателя',
        blank=True,
        null=True
    )
    worker_contact = StreamField(
        ContactsStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Контакты сотрудника"
    )
    example_of_work = StreamField(
        ExampleOfWorkStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Пример работ"
    )
    links = StreamField(
        LinksStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name="Ссылки"
    )
    comment = RichTextField(
        verbose_name='Комментарий',
        blank=True,
        null=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Публиковать',
        blank=True
    )
    process_status = models.IntegerField(choices=STATUSES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("code", read_only=True),
        FieldPanel("process_status"),
        FieldPanel("last_name"),
        FieldPanel("name"),
        FieldPanel("surname"),
        FieldPanel("file"),
        FieldPanel("telegram_nickname"),
        FieldPanel("status"),
        FieldPanel("status_date"),
        FieldPanel("type"),
        FieldPanel("employer"),
        FieldPanel("sales_rate"),
        FieldPanel("purchase_rate"),
        FieldPanel("specialization"),
        FieldPanel("grade"),
        FieldPanel("stack"),
        FieldPanel("skills"),
        FieldPanel("programming_languages"),
        FieldPanel("technologies"),
        FieldPanel("databases"),
        FieldPanel("software_development"),
        FieldPanel("other_technologies"),
        FieldPanel("about_worker"),
        FieldPanel("experience"),
        FieldPanel("city"),
        FieldPanel("citizenship"),
        FieldPanel("english_grade"),
        FieldPanel("education"),
        FieldPanel("certificates"),
        FieldPanel("employer_contact"),
        FieldPanel("worker_contact"),
        FieldPanel("example_of_work"),
        InlinePanel(
            'work_experiences', label="Work Experience"
        ),
        FieldPanel("comment"),
        FieldPanel("is_published"),
        InlinePanel(
            'projects', label="Projects"
        )
    ]

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def full_name(self):
        return f'{self.last_name} {self.name} {self.surname if self.surname else ""}'

    def get_status(self):
        return self.get_process_status_display()

    full_name.admin_order_field = "Полное имя"
    full_name.short_description = "Полное имя"

    get_status.admin_order_field = "Статус"
    get_status.short_description = "Статус"
