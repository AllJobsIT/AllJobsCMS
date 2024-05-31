# Generated by Django 5.0.6 on 2024-05-31 15:09

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Грейд английского языка',
                'verbose_name_plural': 'Грейды английского языка',
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Грейд',
                'verbose_name_plural': 'Грейды',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название ранга заявки')),
                ('color', models.CharField(default='#FF0000',
                                           help_text='В Канбане у заявок с этим рангом фон будет указанного цвета',
                                           verbose_name='Цвет фона заявки')),
                ('is_default', models.BooleanField(blank=True, default=False,
                                                   help_text='Новым заявкам будет проставляться данный ранг (если не указан какой-либо другой)',
                                                   verbose_name='Является рангом по-умолчанию')),
            ],
            options={
                'verbose_name': 'Ранг заявки',
                'verbose_name_plural': 'Ранги заявок',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Специализация',
                'verbose_name_plural': 'Специализации',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Тип отношений',
                'verbose_name_plural': 'Типы отношений',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, verbose_name='Код клиента')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=255, verbose_name='Отчество')),
                ('status_date', models.DateField(blank=True, null=True, verbose_name='Дата изменения статуса')),
                ('employer', models.CharField(blank=True, max_length=255, verbose_name='Работодатель сотрудника')),
                ('sales_rate', models.IntegerField(blank=True, null=True, verbose_name='Рейт продажи')),
                ('purchase_rate', models.IntegerField(blank=True, null=True, verbose_name='Рейт покупки')),
                ('stack', models.CharField(blank=True, max_length=255, verbose_name='Стек')),
                ('skills_text', models.CharField(blank=True, max_length=1000, verbose_name='Навыки')),
                ('programming_languages_text',
                 models.CharField(blank=True, max_length=1000, verbose_name='Опыт работы с языками')),
                ('technologies_text', models.CharField(blank=True, max_length=1000, verbose_name='Технологии')),
                ('databases_text', models.CharField(blank=True, max_length=1000, verbose_name='Базы данных')),
                ('software_development_text',
                 models.CharField(blank=True, max_length=1000, verbose_name='Средства разработки ПО')),
                ('other_technologies_text',
                 models.CharField(blank=True, max_length=1000, verbose_name='Другие технологии')),
                ('about_worker', models.CharField(blank=True, max_length=1000, verbose_name='О себе')),
                ('experience', models.IntegerField(blank=True, null=True, verbose_name='Стаж')),
                ('city', models.CharField(blank=True, max_length=255, verbose_name='Город проживания')),
                ('citizenship', models.CharField(blank=True, max_length=255, verbose_name='Гражданство')),
                ('education', models.CharField(blank=True, max_length=1000, verbose_name='Образование')),
                ('certificates', models.CharField(blank=True, max_length=1000, verbose_name='Сертификаты')),
                ('employer_contact', models.CharField(blank=True, max_length=255, verbose_name='Контакт работодателя')),
                ('worker_contact', models.CharField(blank=True, max_length=255, verbose_name='Контакт сотрудника')),
                ('example_of_work', models.CharField(blank=True, max_length=1000, verbose_name='Пример работ')),
                ('comment', models.CharField(blank=True, max_length=1000, verbose_name='Комментарий')),
                ('is_published', models.BooleanField(blank=True, default=True, verbose_name='Публиковать')),
                ('english_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                    to='core.englishgrade', verbose_name='Английский язык')),
                ('grade',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.grade',
                                   verbose_name='Грейд')),
                ('specialization',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                   to='core.specialization', verbose_name='Специализация')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                             to='core.status', verbose_name='Статус')),
                ('type',
                 models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.type',
                                   verbose_name='Тип отношений')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование проекта')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='Начало работы')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='Конец работы')),
                ('role', models.CharField(blank=True, max_length=255, verbose_name='Роль в проекте')),
                ('responsibilities', wagtail.fields.RichTextField(blank=True, verbose_name='Обязанности на проекте')),
                ('description',
                 wagtail.fields.RichTextField(blank=True, max_length=255, verbose_name='Описание проекта')),
                ('technologies', models.CharField(blank=True, max_length=255, verbose_name='Технологии проекта')),
                ('team', models.CharField(blank=True, max_length=255, verbose_name='Состав команды')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects',
                                             to='core.worker')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
    ]
