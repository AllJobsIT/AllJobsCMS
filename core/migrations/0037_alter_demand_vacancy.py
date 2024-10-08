# Generated by Django 5.0.6 on 2024-09-05 17:11

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_demand_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='vacancy',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demands', to='core.vacancy'),
        ),
    ]
