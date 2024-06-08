from string import Template

import requests
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_countries.fields import CountryField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel

from core.models.snippets.message_settings import MessageSettings
from libs.rich_text import richtext_to_md2


class VacancyTags(TaggedItemBase):
    content_object = ParentalKey(
        to='Vacancy', on_delete=models.CASCADE,
        related_name='tagged_items'
    )


class Vacancy(ClusterableModel):
    STATUSES = (
        (0, "Модерация"),
        (1, "Отправлен"),
    )
    title = models.CharField(max_length=255, verbose_name="Название вакансии", blank=True, null=True)
    requirements = models.TextField(max_length=2056, verbose_name="Требования к кандидату", blank=True, null=True)
    responsibilities = models.TextField(max_length=2056, verbose_name="Обязанности кандидата", blank=True, null=True)
    cost = models.IntegerField(verbose_name="Рейт вакансии", blank=True, null=True)
    location = CountryField(verbose_name="Локация вакансии", blank=True, null=True)
    load = models.CharField(verbose_name="Загрузка вакансии", max_length=255, blank=True, null=True)
    tags = TaggableManager(through='VacancyTags', blank=True, related_name='vacancy_tags')
    grade = models.ForeignKey(
        'core.Grade',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Грейд',
    )
    status = models.IntegerField(choices=STATUSES, default=0)

    full_vacancy_text_from_tg_chat = models.TextField(blank=True,
                                                      verbose_name="Полный текст скопированной из тг вакансии")

    panels = [
        FieldPanel("title"),
        FieldPanel("status"),
        FieldPanel("requirements"),
        FieldPanel("responsibilities"),
        FieldPanel("cost"),
        FieldPanel("location"),
        FieldPanel("load"),
        FieldPanel("tags"),
        FieldPanel("grade"),
        FieldPanel("full_vacancy_text_from_tg_chat"),
    ]

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.status == 1:
            template_message = Template(MessageSettings.objects.all().first().text)
            data = {
                "title": self.title,
                "requirements": self.requirements,
                "responsibilities": self.responsibilities,
                "cost": self.cost,
                "location": self.location,
                "load": self.load,
                "tags": " ".join([f"#{tag.name}" for tag in self.tags.all()]),
                "grade": self.grade,
            }
            requests.post("http://127.0.0.1:8000/vacancy/", json={"vacancy_text": richtext_to_md2(template_message.substitute(data))})
