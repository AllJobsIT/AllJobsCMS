# Generated by Django 5.0.6 on 2024-07-21 12:42

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0018_remove_worker_sales_rate_project_sales_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='responsibilities',
        ),
        migrations.RemoveField(
            model_name='project',
            name='technologies',
        ),
        migrations.RemoveField(
            model_name='project',
            name='title',
        ),
        migrations.AddField(
            model_name='project',
            name='vacancy',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='core.vacancy', verbose_name='Vacancy for project'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='sales_rate',
        ),
        migrations.AddField(
            model_name='project',
            name='sales_rate',
            field=wagtail.fields.StreamField([('cost_item', wagtail.blocks.StructBlock(
                [('size', wagtail.blocks.IntegerBlock(label='Cost size')), ('currency',
                                                                            wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                'core.CurrencySnippet',
                                                                                label='Cost currency'))],
                label='Cost item'))], blank=True, null=True, verbose_name='Sales rate'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='salary',
            field=wagtail.fields.StreamField([('cost_item', wagtail.blocks.StructBlock(
                [('size', wagtail.blocks.IntegerBlock(label='Cost size')), ('currency',
                                                                            wagtail.snippets.blocks.SnippetChooserBlock(
                                                                                'core.CurrencySnippet',
                                                                                label='Cost currency'))],
                label='Cost item'))], blank=True, null=True, verbose_name='Worker salary'),
        ),
    ]
