# Generated by Django 5.1.1 on 2024-10-10 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20241010_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='input_method',
            field=models.IntegerField(choices=[(0, 'Habr'), (1, 'Manual')], default=1, verbose_name='Worker input method'),
        ),
    ]
