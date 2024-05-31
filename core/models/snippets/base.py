from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


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


class Status(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    class Meta:
        verbose_name = 'Тип отношений'
        verbose_name_plural = 'Типы отношений'

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


class EnglishGrade(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Грейд английского языка'
        verbose_name_plural = 'Грейды английского языка'

    def __str__(self):
        return self.title
