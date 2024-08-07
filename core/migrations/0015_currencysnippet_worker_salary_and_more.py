# Generated by Django 5.0.6 on 2024-07-20 12:06

import core.models.snippets.currency
import django.db.models.deletion
import django_countries.fields
import uuid
import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_worker_birthday_alter_worker_type'),
        ('wagtaildocs', '0013_delete_uploadeddocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencySnippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_code', models.CharField(max_length=3, unique=True, verbose_name='Currency code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('symbol', models.CharField(max_length=4, verbose_name='Currency symbol')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.AddField(
            model_name='worker',
            name='salary',
            field=wagtail.fields.StreamField([('salary_item', wagtail.blocks.StructBlock([('salary_size', wagtail.blocks.IntegerBlock()), ('salary_currency', wagtail.snippets.blocks.SnippetChooserBlock(core.models.snippets.currency.CurrencySnippet))], label='Salary item'))], blank=True, null=True, verbose_name='Worker salary'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='about_worker',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='About worker'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Worker birthday'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='certificates',
            field=wagtail.fields.StreamField([('certificate_item', wagtail.blocks.CharBlock(label='Certificate item'))], blank=True, null=True, verbose_name='Worker certificates'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='citizenship',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Worker citizenship'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Worker city'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='code',
            field=models.UUIDField(blank=True, default=uuid.uuid4, verbose_name='Worker unique code'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='comment',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Manager comment about worker'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='databases',
            field=wagtail.fields.StreamField([('database_item', wagtail.blocks.CharBlock(label='Database item'))], blank=True, null=True, verbose_name='Worker databases'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='education',
            field=wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Worker education'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='employer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Worker employer'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='employer_contact',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Worker employer contacts'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='english_grade',
            field=wagtail.fields.StreamField([('language', wagtail.blocks.StructBlock([('language', wagtail.blocks.CharBlock(label='Language item')), ('grade', wagtail.blocks.CharBlock(label='Language grade'))], label='Language'))], blank=True, null=True, verbose_name='Worker languages'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='example_of_work',
            field=wagtail.fields.StreamField([('example_of_work_item', wagtail.blocks.URLBlock(label='Work example item'))], blank=True, null=True, verbose_name='Worker example of work'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='experience',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Worker years of experience'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='File CV'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='grade',
            field=wagtail.fields.StreamField([('grade', wagtail.snippets.blocks.SnippetChooserBlock('core.Grade', label='Grade'))], blank=True, null=True, verbose_name='Worker grade'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='is_published',
            field=models.BooleanField(blank=True, default=True, verbose_name='Is published'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='links',
            field=wagtail.fields.StreamField([('link', wagtail.blocks.StructBlock([('type', wagtail.blocks.CharBlock(label='Link type')), ('link', wagtail.blocks.URLBlock(label='Link value'))], label='Link item'))], blank=True, null=True, verbose_name='Worker links'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='other_technologies',
            field=wagtail.fields.StreamField([('other_technology_item', wagtail.blocks.CharBlock(label='Other technology item'))], blank=True, null=True, verbose_name='Worker other technologies'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='programming_languages',
            field=wagtail.fields.StreamField([('language_item', wagtail.blocks.CharBlock(label='Programming language'))], blank=True, null=True, verbose_name='Worker programming languages'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='purchase_rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='Purchase rate'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='sales_rate',
            field=models.IntegerField(blank=True, null=True, verbose_name='Sales rate'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='skills',
            field=wagtail.fields.StreamField([('skill_item', wagtail.blocks.CharBlock(label='Skill item'))], blank=True, null=True, verbose_name='Worker skills'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='software_development',
            field=wagtail.fields.StreamField([('software_development_item', wagtail.blocks.CharBlock(label='Software development item'))], blank=True, null=True, verbose_name='Worker software developments'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='specialization',
            field=wagtail.fields.StreamField([('specialization', wagtail.snippets.blocks.SnippetChooserBlock('core.Specialization', label='Specialization'))], blank=True, null=True, verbose_name='Worker specialization'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='stack',
            field=wagtail.fields.StreamField([('stack_item', wagtail.blocks.CharBlock(label='Stack item'))], blank=True, null=True, verbose_name='Worker stacks'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status', verbose_name='Worker status'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status_date',
            field=models.DateField(blank=True, null=True, verbose_name='Changed date status'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='surname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Surname'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='technologies',
            field=wagtail.fields.StreamField([('technology_item', wagtail.blocks.CharBlock(label='Technology item'))], blank=True, null=True, verbose_name='Worker technologies'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='telegram_nickname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telegram nickname'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='type',
            field=models.IntegerField(choices=[(-1, '--'), (0, 'Наемный'), (1, 'Штатный'), (2, 'От партнера')], default=-1, verbose_name='Relationship type'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='worker_contact',
            field=wagtail.fields.StreamField([('contact', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock(label='Contact type')), ('value', wagtail.blocks.CharBlock(label='Contact value'))], label='Contact item'))], blank=True, null=True, verbose_name='Worker contacts'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='technologies',
            field=wagtail.fields.StreamField([('technology_item', wagtail.blocks.CharBlock(label='Technology item'))], blank=True, null=True, verbose_name='Технологии'),
        ),
    ]
