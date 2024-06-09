from string import Template

import requests
from django.db import models
from django_countries.fields import CountryField
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
        (0, "Обработка с помощью ИИ"),
        (1, "Модерация"),
        (2, "Готов к отправке"),
        (3, "Отправлен"),
    )
    title = models.CharField(max_length=255, verbose_name="Название вакансии", blank=True, null=True)
    requirements = models.TextField(max_length=2056, verbose_name="Требования к кандидату", blank=True, null=True,
                                    help_text="; = новая строка")
    responsibilities = models.TextField(max_length=2056, verbose_name="Обязанности кандидата", blank=True, null=True,
                                        help_text="; = новая строка")
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
    channel = models.CharField(max_length=255, blank=True, null=True)

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
        FieldPanel("channel", read_only=True),
        FieldPanel("full_vacancy_text_from_tg_chat"),
    ]

    def __str__(self):
        return f"{self.title} from {self.channel}"

    def save(self, **kwargs):
        if self.status == 2:
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
            self.status = 3
            requests.post("http://127.0.0.1:8000/vacancy/",
                          json={"vacancy_text": richtext_to_md2(template_message.substitute(data))})
        super().save(**kwargs)
