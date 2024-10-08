# Generated by Django 5.1.1 on 2024-09-07 12:42

from django.db import migrations

from core.choices.vacancy import VacancyTypeChoices


def set_type_b_in_vacancy(apps, schema):
    Vacancy = apps.get_model('core', "Vacancy")
    for item in Vacancy.objects.all():
        item.type = VacancyTypeChoices.B
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_alter_vacancy_type'),
    ]

    operations = [
        migrations.RunPython(set_type_b_in_vacancy)
    ]
