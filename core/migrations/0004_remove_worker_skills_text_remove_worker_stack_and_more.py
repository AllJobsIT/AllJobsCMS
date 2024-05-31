# Generated by Django 5.0.6 on 2024-05-31 16:06

import django.db.models.deletion
import modelcluster.contrib.taggit
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_alter_worker_citizenship'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='skills_text',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='stack',
        ),
        migrations.CreateModel(
            name='SkillsTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items_skills',
                                   to='core.worker')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                          related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StackTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items_stack',
                                   to='core.worker')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                          related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='worker',
            name='skills_text',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True,
                                                                     help_text='A comma-separated list of tags.',
                                                                     through='core.SkillsTags', to='taggit.Tag',
                                                                     verbose_name='Навыки'),
        ),
        migrations.AddField(
            model_name='worker',
            name='stack',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True,
                                                                     help_text='A comma-separated list of tags.',
                                                                     through='core.StackTags', to='taggit.Tag',
                                                                     verbose_name='Стек'),
        ),
    ]
