# Generated by Django 5.1.1 on 2024-10-10 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parser_ai', '0002_alter_prompt_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prompt',
            options={'verbose_name': 'Prompt', 'verbose_name_plural': 'Prompts'},
        ),
    ]
