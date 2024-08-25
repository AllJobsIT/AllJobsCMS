# Generated by Django 5.0.6 on 2024-08-17 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_worker_created_at_alter_worker_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demand',
            name='customer',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='customer',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Customer'),
        ),
    ]