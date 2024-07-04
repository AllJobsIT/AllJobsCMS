from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.search import index


class BaseSnippet(models.Model):
    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        my_model = apps.get_model(self._meta.label)
        existing_count = my_model.objects.count()
        max_instances = 1
        if existing_count >= max_instances and self._state.adding:
            raise ValidationError(_(f"Может быть только {max_instances} экземпляр(ов) сниппета {self.__str__()}."))


class Status(index.Indexed, models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    search_fields = [
        index.SearchField('title'),
        index.AutocompleteField('title'),
    ]

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.title


class Specialization(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return self.title


class Grade(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    class Meta:
        verbose_name = 'Грейд'
        verbose_name_plural = 'Грейды'

    def __str__(self):
        return self.title
