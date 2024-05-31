from django.db import models
from wagtail.fields import RichTextField

from core.models.snippets import Worker


class Project(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Наименование проекта'
    )
    worker = models.ForeignKey(
        Worker,
        related_name='projects',
        on_delete=models.CASCADE
    )
    date_start = models.DateField(
        verbose_name='Начало работы',
        blank=True,
        null=True,
    )
    date_end = models.DateField(
        verbose_name='Конец работы',
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=255,
        verbose_name='Роль в проекте',
        blank=True
    )
    responsibilities = RichTextField(
        verbose_name='Обязанности на проекте',
        blank=True,
    )
    description = RichTextField(
        max_length=255,
        verbose_name='Описание проекта',
        blank=True
    )
    technologies = models.CharField(
        max_length=255,
        verbose_name='Технологии проекта',
        blank=True
    )
    team = models.CharField(
        max_length=255,
        verbose_name='Состав команды',
        blank=True
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title
