from django.db import models
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel

from core.models.snippets.base import Specialization, Grade, EnglishGrade, Status, Type


class StackTags(TaggedItemBase):
    content_object = models.ForeignKey('core.Worker', on_delete=models.CASCADE, related_name='tagged_items_stack')


class SkillsTags(TaggedItemBase):
    content_object = models.ForeignKey('core.Worker', on_delete=models.CASCADE, related_name='tagged_items_skills')


class SkillsTags(TaggedItemBase):
    content_object = models.ForeignKey('core.Worker', on_delete=models.CASCADE, related_name='tagged_items_skills')


class SkillsTags(TaggedItemBase):
    content_object = models.ForeignKey('core.Worker', on_delete=models.CASCADE, related_name='tagged_items_skills')


class Worker(models.Model):
    code = models.CharField(
        max_length=255,
        verbose_name='Код клиента',
        blank=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Фамилия'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=255,
        verbose_name='Отчество',
        blank=True
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
    stack = TaggableManager(through="core.StackTags", blank=True, verbose_name="Стек", related_name='worker_stack')
    skills_text = TaggableManager(through="core.SkillsTags", blank=True, verbose_name="Навыки",
                                  related_name='worker_skills')
    programming_languages = models.TextField(
        max_length=1000,
        verbose_name='Опыт работы с языками',
        blank=True
    )
    technologies = models.TextField(
        max_length=1000,
        verbose_name='Технологии',
        blank=True
    )
    databases_text = models.TextField(
        max_length=1000,
        verbose_name='Базы данных',
        blank=True
    )
    software_development_text = models.TextField(
        max_length=1000,
        verbose_name='Средства разработки ПО',
        blank=True
    )
    other_technologies_text = models.TextField(
        max_length=1000,
        verbose_name='Другие технологии',
        blank=True,
    )
    about_worker = models.TextField(
        max_length=1000,
        verbose_name='О себе',
        blank=True
    )
    experience = models.IntegerField(
        verbose_name='Стаж',
        blank=True,
        null=True
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
    education = models.TextField(
        max_length=1000,
        verbose_name='Образование',
        blank=True
    )
    certificates = models.TextField(
        max_length=1000,
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
    example_of_work = models.TextField(
        max_length=1000,
        verbose_name='Пример работ',
        blank=True
    )
    comment = models.TextField(
        max_length=1000,
        verbose_name='Комментарий',
        blank=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Публиковать',
        blank=True
    )

    panels = [
        FieldPanel("code"),
        FieldPanel("last_name"),
        FieldPanel("name"),
        FieldPanel("surname"),
        FieldPanel("status"),
        FieldPanel("status_date"),
        FieldPanel("type"),
        FieldPanel("employer"),
        FieldPanel("sales_rate"),
        FieldPanel("purchase_rate"),
        FieldPanel("specialization"),
        FieldPanel("grade"),
        FieldPanel("stack"),
        FieldPanel("skills_text"),
        FieldPanel("programming_languages_text"),
        FieldPanel("technologies_text"),
        FieldPanel("databases_text"),
        FieldPanel("software_development_text"),
        FieldPanel("other_technologies_text"),
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
    ]

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def full_name(self):
        return f'{self.last_name} {self.name} {self.surname}'
