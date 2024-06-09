import uuid

from django.db import models
from django.utils.functional import cached_property
from django_countries.fields import CountryField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.documents.models import Document
from wagtail.fields import RichTextField

from core.models.snippets.base import Specialization, Grade, EnglishGrade, Status, Type


class Worker(ClusterableModel):
    code = models.UUIDField(
        verbose_name='Код работника',
        blank=True,
        default=uuid.uuid4,
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия'
    )
    surname = models.CharField(
        max_length=255,
        verbose_name='Отчество',
        blank=True
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
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        verbose_name='Специализация',
        blank=True,
        null=True
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        verbose_name='Грейд',
        blank=True,
        null=True
    )
    stack = RichTextField(blank=True, verbose_name="Стек")
    skills = RichTextField(blank=True, verbose_name="Навыки")
    programming_languages = RichTextField(
        verbose_name='Опыт работы с языками',
        blank=True
    )
    technologies = RichTextField(
        verbose_name='Технологии',
        blank=True
    )
    databases = RichTextField(
        verbose_name='Базы данных',
        blank=True
    )
    software_development = RichTextField(
        verbose_name='Средства разработки ПО',
        blank=True
    )
    other_technologies = RichTextField(
        verbose_name='Другие технологии',
        blank=True,
    )
    about_worker = RichTextField(
        verbose_name='О себе',
        blank=True
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
        blank=True
    )
    citizenship = CountryField(
        verbose_name='Гражданство',
        blank=True
    )
    english_grade = models.ForeignKey(
        EnglishGrade,
        on_delete=models.SET_NULL,
        verbose_name='Английский язык',
        blank=True,
        null=True,
    )
    education = RichTextField(
        verbose_name='Образование',
        blank=True
    )
    certificates = RichTextField(
        verbose_name='Сертификаты',
        blank=True
    )
    employer_contact = models.CharField(
        max_length=255,
        verbose_name='Контакт работодателя',
        blank=True
    )
    worker_contact = models.CharField(
        max_length=255,
        verbose_name='Контакт сотрудника',
        blank=True
    )
    example_of_work = RichTextField(
        verbose_name='Пример работ',
        blank=True
    )
    comment = RichTextField(
        verbose_name='Комментарий',
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Публиковать',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("code", read_only=True),
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
        FieldPanel("comment"),
        FieldPanel("is_published"),
        InlinePanel(
            'projects', label="Projects"
        )
    ]

    def __str__(self):
        return f'{self.name} {self.last_name}'

    @cached_property
    def full_name(self):
        return f'{self.last_name} {self.name} {self.surname}'
