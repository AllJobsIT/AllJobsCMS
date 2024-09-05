# Generated by Django 5.1.1 on 2024-09-05 19:22

import django.db.models.deletion
import wagtail.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_demand_vacancy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='demand',
        ),
        migrations.RemoveField(
            model_name='project',
            name='worker',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='demands',
            field=wagtail.fields.StreamField([('demand', 14)], blank=True, block_lookup={0: ('wagtail.snippets.blocks.SnippetChooserBlock', ('core.Worker',), {'label': 'Worker for project'}), 1: ('wagtail.blocks.DateBlock', (), {'blank': True, 'label': 'Project submission date', 'null': True}), 2: ('wagtail.blocks.IntegerBlock', (), {'label': 'Cost size'}), 3: ('wagtail.snippets.blocks.SnippetChooserBlock', ('core.CurrencySnippet',), {'label': 'Cost currency'}), 4: ('wagtail.blocks.StructBlock', [[('size', 2), ('currency', 3)]], {'label': 'Cost item'}), 5: ('wagtail.blocks.StreamBlock', [[('cost_item', 4)]], {'label': 'Cost item'}), 6: ('wagtail.blocks.ChoiceBlock', [], {'choices': [(0, 'Negative'), (1, 'Normal'), (2, 'Positive')], 'label': 'Type feedback'}), 7: ('wagtail.blocks.RichTextBlock', (), {'label': 'Feedback text'}), 8: ('wagtail.blocks.StructBlock', [[('type', 6), ('value', 7)]], {'label': 'Feedback item'}), 9: ('wagtail.blocks.StreamBlock', [[('feedback_item', 8)]], {'label': 'Feedback item'}), 10: ('wagtail.blocks.StructBlock', [[('worker', 0), ('date_start', 1), ('sales_rate', 5), ('feedback', 9)]], {}), 11: ('wagtail.blocks.StreamBlock', [[('project', 10)]], {}), 12: ('wagtail.blocks.CharBlock', (), {'blank': True, 'label': 'Partner', 'max_length': 255, 'null': True}), 13: ('wagtail.blocks.BooleanBlock', (), {'blank': True, 'default': True, 'label': 'Is active'}), 14: ('wagtail.blocks.StructBlock', [[('projects', 11), ('partner', 12), ('is_active', 13)]], {})}, verbose_name='Demand'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managers', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.DeleteModel(
            name='Demand',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]
