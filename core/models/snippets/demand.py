import uuid
from datetime import datetime, timedelta

from django.db import models
from wagtail.fields import RichTextField

from core.models.snippets import Rank, Specialization, Worker


class Demand(models.Model):
    display_name = models.CharField(
        max_length=255,
        verbose_name='Название запроса',
        help_text='Пример: "Kokoc.tech | Java/Middle/2400"',
        blank=True,
    )
    uuid = models.CharField(
        max_length=50,
        default=uuid.uuid4,
        verbose_name='UUID запроса',
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name='Заказчик'
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        verbose_name='Специализация',
        blank=True,
        null=True
    )
    stack = models.CharField(
        max_length=2000,
        verbose_name='Стек',
    )
    rate = models.IntegerField(
        verbose_name='Рейт покупки',
        blank=True,
        null=True,
    )
    project_name = models.CharField(
        max_length=255,
        verbose_name='Название проекта',
        blank=True,
    )
    project_description = RichTextField(
        max_length=3000,
        verbose_name='Описание проекта',
        blank=True
    )
    project_term = models.CharField(
        max_length=255,
        verbose_name='Срок проекта',
        blank=True
    )
    # status = models.ForeignKey(
    #     Board,
    #     related_name='demands',
    #     on_delete=models.CASCADE,
    #     default=Board.get_default_board,
    #     verbose_name='Статус',
    # )
    workers = models.ManyToManyField(
        Worker,
        related_name="demands"
    )
    manager = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='demands',
        null=True,
        blank=True,
        verbose_name='Менеджер',
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.SET_NULL,
        related_name='demands',
        null=True,
        blank=True,
        default=Rank.get_default_rank if Rank.get_default_rank else None,
        verbose_name='Ранг заявки',
    )
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

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

        permissions = [
            ("allow_kanban", "Доступ к канбан"),
        ]

    def __str__(self):
        return 'Запрос ' + str(self.id)


class DemandTimeLog(models.Model):
    demand = models.ForeignKey(
        Demand,
        related_name='timelogs',
        on_delete=models.CASCADE,
        verbose_name='Запрос',
    )
    # status = models.ForeignKey(
    #     Board,
    #     related_name='timelogs',
    #     on_delete=models.CASCADE,
    #     verbose_name='Статус',
    # )
    status_start = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Начало',
    )
    status_end = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Конец',
    )
    total_seconds = models.BigIntegerField(
        default=0,
        blank=True,
        verbose_name='Суммарная длительность',
    )

    # возвращает цвет для лога времени в Канбане в зависимости от количества дней
    def get_timer_color(self):
        time = self.total_time_clean()
        days = time // (3600 * 24)

        if days >= 5:
            return 'red'
        if days >= 2:
            return 'orange'

        return 'green'

    # возвращает время в секундах
    def total_time_clean(self):
        output = ""
        # если статус неактивный - залогировано время и есть дата конца
        if self.total_seconds and self.status_end is not None:
            output = self.total_seconds
        # иначе показываем разницу между датой начала и датой конца + сохранённые ранее секунды (если есть)
        else:
            output = int(datetime.now().timestamp() - self.status_start.timestamp() + self.total_seconds)

        return output

    # время, формат (# дней, ЧЧ:ММ:СС)
    def total_time_hms(self):
        return timedelta(seconds=self.total_time_clean())

    # время, формат (#д #ч #м)
    def total_time_dhm(self):
        time = self.total_time_clean()
        days = time // (3600 * 24)
        hours = (time // 3600) % 24
        minutes = time % 3600 // 60

        output = ''
        if days:
            output += '{}д'.format(days) + ' '

        if hours:
            output += '{}ч'.format(hours) + ' '

        output += '{}м'.format(minutes)

        return output

    # время, формат (#ч, #м)
    def total_time_hm(self):
        time = self.total_time_clean()
        hours = time // 3600
        minutes = time % 3600 // 60

        output = ''
        if hours:
            output = '{}ч'.format(hours) + ' '

        output += '{}м'.format(minutes)
        return output

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'

    def __str__(self):
        return str(self.id)
