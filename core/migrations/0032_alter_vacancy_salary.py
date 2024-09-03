# Generated by Django 5.0.6 on 2024-09-03 10:07

import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_vacancy_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=wagtail.fields.StreamField([('cost_item', wagtail.blocks.StructBlock([('size', wagtail.blocks.IntegerBlock(label='Cost size')), ('currency', wagtail.snippets.blocks.SnippetChooserBlock('core.CurrencySnippet', label='Cost currency'))], label='Cost item'))], null=True, verbose_name='Salary'),
        ),
    ]
