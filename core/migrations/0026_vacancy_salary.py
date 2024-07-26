# Generated by Django 5.0.6 on 2024-07-26 09:23

import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_messagesettings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='salary',
            field=wagtail.fields.StreamField([('cost_item', wagtail.blocks.StructBlock([('size', wagtail.blocks.IntegerBlock(label='Cost size')), ('currency', wagtail.snippets.blocks.SnippetChooserBlock('core.CurrencySnippet', label='Cost currency'))], label='Cost item'))], blank=True, null=True, verbose_name='Salary'),
        ),
    ]
