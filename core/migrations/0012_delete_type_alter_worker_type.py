# Generated by Django 5.0.6 on 2024-07-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_worker_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AlterField(
            model_name='worker',
            name='type',
            field=models.IntegerField(choices=[(-1, '--------------------------'), (0, 'Наемный'), (1, 'Штатный'), (2, 'От партнера')], default=-1, verbose_name='Тип отношений'),
        ),
    ]
