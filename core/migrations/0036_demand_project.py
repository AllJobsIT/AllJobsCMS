# Generated by Django 5.0.6 on 2024-09-05 15:34

import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_remove_project_demand_remove_project_worker_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Demand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('partner', models.CharField(blank=True, max_length=255, null=True, verbose_name='Partner')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Is active')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managers', to=settings.AUTH_USER_MODEL, verbose_name='Manager')),
                ('vacancy', modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='demands', to='core.vacancy')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('date_start', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Project submission date')),
                ('sales_rate', wagtail.fields.StreamField([('cost_item', wagtail.blocks.StructBlock([('size', wagtail.blocks.IntegerBlock(label='Cost size')), ('currency', wagtail.snippets.blocks.SnippetChooserBlock('core.CurrencySnippet', label='Cost currency'))], label='Cost item'))], blank=True, null=True, verbose_name='Sales rate')),
                ('feedback', wagtail.fields.StreamField([('feedback_item', wagtail.blocks.StructBlock([('type', wagtail.blocks.ChoiceBlock(choices=[(0, 'Negative'), (1, 'Normal'), (2, 'Positive')], label='Type feedback')), ('value', wagtail.blocks.RichTextBlock(label='Feedback text'))], label='Feedback item'))], blank=True, null=True, verbose_name='Feedback')),
                ('demand', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='core.demand')),
                ('worker', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.worker', verbose_name='Worker for project')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]