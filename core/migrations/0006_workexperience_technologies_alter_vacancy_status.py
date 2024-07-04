# Generated by Django 5.0.6 on 2024-07-02 13:19

import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_worker_worker_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='workexperience',
            name='technologies',
            field=wagtail.fields.StreamField([('technology_item', wagtail.blocks.CharBlock(label='Элемент технологии'))], blank=True, null=True, verbose_name='Технологии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='status',
            field=models.IntegerField(choices=[(-1, 'Обработка с помощью ИИ не удалась'), (0, 'Ожидает одобрения'), (1, 'Обработка с помощью ИИ'), (2, 'Модерация'), (3, 'Готов к отправке'), (4, 'Отправлен'), (5, 'Найден исполнитель'), (6, 'В исполнении'), (7, 'В архиве')], default=0),
        ),
    ]