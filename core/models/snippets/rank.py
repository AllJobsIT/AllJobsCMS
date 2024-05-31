from django.db import models


class Rank(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название ранга заявки'
    )
    color = models.CharField(
        default='#FF0000',
        verbose_name='Цвет фона заявки',
        help_text='В Канбане у заявок с этим рангом фон будет указанного цвета',
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Является рангом по-умолчанию',
        help_text='Новым заявкам будет проставляться данный ранг (если не указан какой-либо другой)',
        blank=True
    )

    class Meta:
        verbose_name = 'Ранг заявки'
        verbose_name_plural = 'Ранги заявок'

    def __str__(self):
        return self.name

    @classmethod
    def get_default_rank(cls):
        try:
            return cls.objects.get(is_default=True)
        except Rank.DoesNotExist:
            return None
