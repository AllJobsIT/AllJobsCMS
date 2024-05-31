# Generated by Django 5.0.6 on 2024-05-31 16:25

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_remove_worker_skills_text_remove_worker_stack_and_more'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='skills_text',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.',
                                                  through='core.SkillsTags', to='taggit.Tag', verbose_name='Навыки'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='stack',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.',
                                                  through='core.StackTags', to='taggit.Tag', verbose_name='Стек'),
        ),
    ]
