# Generated by Django 5.0.6 on 2024-07-21 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_vacancy_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demand',
            old_name='duration',
            new_name='deadline',
        ),
    ]
